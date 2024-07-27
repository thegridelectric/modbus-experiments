import logging # noqa
import time
from enum import IntEnum

from pymodbus.client import ModbusSerialClient # noqa
from pymodbus.client import ModbusTcpClient # noqa
import pymodbus.bit_read_message as pdu_bit_read
import pymodbus.register_read_message as pdu_reg_read


import rich

client = ModbusTcpClient("192.168.1.210")
# client = ModbusSerialClient("/dev/tty.usbserial-B001K6G3", baudrate=9600)

TaidacentRegisters = dict(
    Temperature        = 0x0000,
    Humidity           = 0x0001,
    ModelCode          = 0x0064,
    MeasuringPoints    = 0x0065,
    DeviceAddress      = 0x0066,
    BaudRate           = 0x0067,
    CommunicationMode  = 0x0068,
    ProtocolType       = 0x0069,
    TempCorrection     = 0x006B,
    HumidityCorrection = 0x006C,
)

taidacent_temp_correction = -178 & 0xFFFF
taidacent_read_address = 2
taidacent_write_address = 2

def taidacent_read_registers(device: int) -> None:
    print("Taidecent Thermometer")
    for name, address in TaidacentRegisters.items():
        time.sleep(.2)
        resp = client.read_holding_registers(address=address, slave=device, count=1)
        s = f"Read 0x{address:02X}   {name:20}: "
        if isinstance(resp, Exception):
            s += str(resp)
        else:
            s += f"{resp.registers[0]:6d}"
            if name == "Temperature":
                C = resp.registers[0]/100
                F = C * 9/5 + 32
                s += f"  {C}\u00B0C  {F:4.2f}\u00B0F"
        print(s)

def taidecent_read_temperature(device: int, fahrenheit = False, show: bool = True) -> float:
    name = "Temperature"
    address = TaidacentRegisters[name]
    time.sleep(.2)
    # resp = client.read_holding_registers(address=address, slave=device, count=1)
    req = pdu_reg_read.ReadHoldingRegistersRequest(address, count=1, slave=device)
    resp = client.execute(req)
    if isinstance(resp, Exception):
        raise resp
    C = resp.registers[0] / 100
    F = C * 9 / 5 + 32
    if show:
        print(f"Read 0x{address:02X}   {name:20}:   0x{resp.registers[0]:04X}  {resp.registers[0]:6d}  {C}\u00B0C  {F:4.2f}\u00B0F")
    if fahrenheit:
        return F
    return C


def taidacent_set_temp_correction(device: int, correction: int) -> None:
    name = "TempCorrection"
    address = TaidacentRegisters[name]
    time.sleep(.2)
    resp = client.read_holding_registers(address=address, slave=device, count=1)
    if isinstance(resp, Exception):
        raise resp
    correction &= 0xFFFF
    if correction != resp.registers[0]:
        print(f"Setting {name}")
        time.sleep(.2)
        resp = client.write_register(address=address, value=correction & 0xFFFF, slave=device)
        if isinstance(resp, Exception):
            raise resp
        rich.print(resp)
        time.sleep(.2)
        resp = client.read_holding_registers(address=address, slave=device, count=1)
        s = f"Read 0x{address:02X}   {name:20}: "
        if isinstance(resp, Exception):
            s += str(resp)
        else:
            s += f"{resp.registers[0]:6d}"
        print(s)

def set_address(address: int, read_device: int, write_device: int) -> None:
    name = "DeviceAddress"
    resp = client.read_holding_registers(address=address, slave=read_device, count=1)
    if isinstance(resp, Exception):
        raise resp
    if write_device != resp.registers[0]:
        print(f"Setting {name} to {resp.registers[0]} -> {write_device}")
        time.sleep(.2)
        resp = client.write_register(address=address, value=write_device & 0xFFFF, slave=read_device)
        if isinstance(resp, Exception):
            raise resp
        rich.print(resp)
        time.sleep(.2)
        resp = client.read_holding_registers(address=address, slave=write_device, count=1)
        s = f"Read 0x{address:02X}   {name:20}: "
        if isinstance(resp, Exception):
            s += str(resp)
        else:
            s += f"{resp.registers[0]:6d}"
        print(s)

def taidacent_set_address(read_device: int, write_device: int) -> None:
    set_address(TaidacentRegisters["DeviceAddress"], read_device, write_device)

def read_registers(device: int, registers: dict[str, int]):
    for name, address in registers.items():
        time.sleep(.2)
        resp = client.read_holding_registers(address=address, slave=device, count=1)
        s = f"Read 0x{address:02X}   {name:20}: "
        if isinstance(resp, Exception):
            s += str(resp)
        else:
            s += f"{resp.registers[0]:6d}"
        print(s)

def write_register(device: int, address: int, value: int, name: str = ""):
    time.sleep(.2)
    resp = client.write_register(address=address, value=value & 0xFFFF, slave=device)
    if isinstance(resp, Exception):
        print(resp)
    else:
        time.sleep(.2)
        resp = client.read_holding_registers(address=address, slave=device, count=1)
        s = f"Read 0x{address:02X}   {name:20}: "
        if isinstance(resp, Exception):
            s += str(resp)
        else:
            s += f"{resp.registers[0]:6d}"
        print(s)

class Taidecent:
    device: int

    def __init__(
        self,
        device: int = taidacent_read_address
    ):
        self.device = device

    def read_registers(self) -> None:
        taidacent_read_registers(self.device)

    def read_temperature(self, fahrenheit=False, show: bool = True) -> float:
        return taidecent_read_temperature(self.device, fahrenheit, show)

WAVESHARE_RELAY_READ_ADDRESS = 0x03
WAVESHARE_RELAY_WRITE_ADDRESS = 0x03

class WaveShareRelayControl(IntEnum):
    Close  = 0xFF00
    Open   = 0x0000
    Flip   = 0x5500

WAVESHARE_READ_ALL_RELAYS_ADDRESS = 0x0000
WAVESHARE_READ_WRITE_ALL_RELAYS_COUNT = 0x0008
WAVESHARE_WRITE_ALL_RELAYS_IDX = 0xFF

WaveShareRelayReadRegisters = dict(
    DeviceAddress   = 0x4000,
    SoftwareVersion = 0x8000,
)
WaveShareRelayWriteRegisters = dict(
    DeviceAddress   = 0x4000,
    BaudRate        = 0x2000,
)


def write_relay(device: int, relay_idx: int, mode: WaveShareRelayControl | bool) -> None:
    time.sleep(.2)
    if isinstance(mode, bool):
        if mode is True:
            mode = WaveShareRelayControl.Close
        else:
            mode = WaveShareRelayControl.Open
    client.write_coil(
        address=relay_idx,
        value=mode.value, # noqa
        slave=device,
    )

def write_all_relays(device: int, mode: WaveShareRelayControl | bool) -> None:
    write_relay(device, WAVESHARE_WRITE_ALL_RELAYS_IDX, mode)

def read_all_relays(device: int) -> None:
    print("WaveShare Relays")
    req = pdu_bit_read.ReadCoilsRequest(
        address=WAVESHARE_READ_ALL_RELAYS_ADDRESS,
        count=WAVESHARE_READ_WRITE_ALL_RELAYS_COUNT,
        slave=device,
    )
    # rich.print(req)
    # rich.inspect(req, all=True)
    time.sleep(.2)
    resp = client.execute(req)
    if isinstance(resp, Exception):
        raise resp
    states = 0
    s1 = "Relay  "
    s2 = "State  "
    for bit_idx in range(len(resp.bits)):
        s1 += f" {bit_idx:1d}"
        s2 += f" {resp.bits[bit_idx]:1d}"
        if resp.bits[bit_idx]:
            states |= 1 << bit_idx
    print(f"Relay states: 0x{states:02X}")
    print(s1)
    print(s2)

class WaveshareRelays:
    device: int

    def __init__(self, device: int = WAVESHARE_RELAY_READ_ADDRESS) -> None:
        self.device = device

    def write_relay(self, relay_idx: int, mode: WaveShareRelayControl | bool) -> None:
        write_relay(self.device, relay_idx, mode)

    def write_all_relays(self, mode: WaveShareRelayControl | bool) -> None:
        write_all_relays(self.device, mode)

    def read_all_relays(self) -> None:
        read_all_relays(self.device)

    def write_register(self, address: int, value: int, name: str = ""):
        write_register(self.device, address, value, name)

    def read_registers(self):
        read_registers(self.device, WaveShareRelayReadRegisters)

def main():
    # logging.basicConfig()
    # log = logging.getLogger()
    # log.setLevel(logging.DEBUG)

    client.connect()

    # taidacent_read_registers(taidacent_read_address)
    # read_all_relays(device=WAVESHARE_RELAY_READ_ADDRESS)
    # for _ in range(1):
    #     write_all_relays(device=WAVESHARE_RELAY_READ_ADDRESS, mode=WaveShareRelayControl.Open)
    #     write_all_relays(device=WAVESHARE_RELAY_READ_ADDRESS, mode=WaveShareRelayControl.Close)
    #     write_all_relays(device=WAVESHARE_RELAY_READ_ADDRESS, mode=WaveShareRelayControl.Open)
    #     write_all_relays(device=WAVESHARE_RELAY_READ_ADDRESS, mode=WaveShareRelayControl.Close)

    mode = WaveShareRelayControl.Open
    i = 0
    while i < 2:
        time.sleep(2)
        taidecent_read_temperature(taidacent_read_address, fahrenheit=True)
        # break
        read_all_relays(device=WAVESHARE_RELAY_READ_ADDRESS)
        if mode == WaveShareRelayControl.Open:
            mode = WaveShareRelayControl.Close
        else:
            mode = WaveShareRelayControl.Open
        write_relay(device=WAVESHARE_RELAY_READ_ADDRESS, relay_idx=0, mode=mode)
        i += 1

if __name__ == "__main__":
    main()
