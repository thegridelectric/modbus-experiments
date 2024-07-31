import time

import rich

from pymodbus.client.base import ModbusBaseSyncClient

from mbe.io import set_device_id

TaidacentRegisters = dict(
    Temperature=0x0000,
    Humidity=0x0001,
    ModelCode=0x0064,
    MeasuringPoints=0x0065,
    DeviceAddress=0x0066,
    BaudRate=0x0067,
    CommunicationMode=0x0068,
    ProtocolType=0x0069,
    TempCorrection=0x006B,
    HumidityCorrection=0x006C,
)

TAIDECENT_TEMP_CORRECTION = -178 & 0xFFFF
TAIDECENT_DEVICE_ID_FACTORY = 1
TAIDECENT_DEVICE_ID = 2


class Taidecent:
    client: ModbusBaseSyncClient
    device: int

    def __init__(self, client: ModbusBaseSyncClient, device: int = TAIDECENT_DEVICE_ID):
        self.client = client
        self.device = device

    def read_registers(self) -> None:
        print("Taidecent Thermometer")
        for name, address in TaidacentRegisters.items():
            time.sleep(0.2)
            resp = self.client.read_holding_registers(
                address=address, slave=self.device, count=1
            )
            s = f"Read 0x{address:02X}   {name:20}: "
            if isinstance(resp, Exception):
                s += str(resp)
            else:
                s += f"{resp.registers[0]:6d}"
                if name == "Temperature":
                    C = resp.registers[0] / 100
                    F = C * 9 / 5 + 32
                    s += f"  {C}\u00b0C  {F:4.2f}\u00b0F"
            print(s)

    def read_temperature(self, fahrenheit: bool = False, show: bool = True) -> float:
        name = "Temperature"
        address = TaidacentRegisters[name]
        time.sleep(0.2)
        resp = self.client.read_holding_registers(
            address=address, slave=self.device, count=1
        )
        if isinstance(resp, Exception):
            raise resp
        C = resp.registers[0] / 100
        F = C * 9 / 5 + 32
        if show:
            print(
                f"Read 0x{address:02X}   {name:20}:   0x{resp.registers[0]:04X}  {resp.registers[0]:6d}  {C}\u00b0C  {F:4.2f}\u00b0F"
            )
        if fahrenheit:
            return F
        return C

    def set_device_id(self, new_device_id) -> None:
        set_device_id(
            self.client, TaidacentRegisters["DeviceAddress"], self.device, new_device_id
        )
        self.device = new_device_id

    def set_temp_correction(self, correction: int) -> None:
        """Set temperature correction register"""
        name = "TempCorrection"
        address = TaidacentRegisters[name]
        time.sleep(0.2)
        resp = self.client.read_holding_registers(
            address=address, slave=self.device, count=1
        )
        if isinstance(resp, Exception):
            raise resp
        correction &= 0xFFFF
        if correction != resp.registers[0]:
            print(f"Setting {name}")
            time.sleep(0.2)
            resp = self.client.write_register(
                address=address, value=correction & 0xFFFF, slave=self.device
            )
            if isinstance(resp, Exception):
                raise resp
            rich.print(resp)
            time.sleep(0.2)
            resp = self.client.read_holding_registers(
                address=address, slave=self.device, count=1
            )
            s = f"Read 0x{address:02X}   {name:20}: "
            if isinstance(resp, Exception):
                s += str(resp)
            else:
                s += f"{resp.registers[0]:6d}"
            print(s)
