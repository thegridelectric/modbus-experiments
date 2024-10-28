import time

from pymodbus.client.base import ModbusBaseSyncClient
from pymodbus.pdu.register_read_message import ReadInputRegistersResponse

from mbe.io import set_device_id

SchneiderRegisters = dict(
    Name=(0x001D, 10),
    # These seems to cause read errors
    # Model=(0x0031, 10),
    # Manufacturer=(0x0045, 10),
    # SerialNumber=(0x0081, 1),
    Protocol=(0x1963, 1),
    Address=(0x1964, 1),
    BaudRate=(0x1965, 1),
    Parity=(0x1965, 1),
    I1_Phase1Current=(0x0BB7, 2),
    Voltage_LN_1=(0xBD3, 2),
    Frequency=(0x0C25, 2),
)

SCHNEIDER_DEVICE_ID_FACTORY = 1
SCHNEIDER_DEVICE_ID = 12


class Schneider:
    client: ModbusBaseSyncClient
    device: int

    def __init__(self, client: ModbusBaseSyncClient, device: int = SCHNEIDER_DEVICE_ID):
        self.client = client
        self.device = device

    def read_registers(self) -> None:
        print("Schneider Electric Meter")
        for name, (address, count) in SchneiderRegisters.items():
            time.sleep(1.0)
            resp = self.client.read_holding_registers(
                address=address, slave=self.device, count=count
            )
            s = f"Read 0x{address:04X}   {name:20}: "
            if not isinstance(resp, ReadInputRegistersResponse):
                s += str(resp)
            else:
                for c in resp.registers:  # noqa
                    s += f"{c:04X} "
            print(s)

    def set_device_id(self, new_device_id) -> None:
        set_device_id(
            self.client,
            SchneiderRegisters["DeviceAddress"][0],
            self.device,
            new_device_id,
        )
        self.device = new_device_id
