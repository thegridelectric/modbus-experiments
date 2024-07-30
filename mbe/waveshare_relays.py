import time
from enum import IntEnum

from pymodbus.client.base import ModbusBaseSyncClient

from mbe.io import set_address

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



class WaveshareRelays:
    client: ModbusBaseSyncClient
    device: int

    def __init__(self, client: ModbusBaseSyncClient, device: int = WAVESHARE_RELAY_READ_ADDRESS) -> None:
        self.client = client
        self.device = device

    def write_relay(self, relay_idx: int, mode: WaveShareRelayControl | bool) -> None:
        time.sleep(.2)
        if isinstance(mode, bool):
            if mode is True:
                mode = WaveShareRelayControl.Close
            else:
                mode = WaveShareRelayControl.Open
        self.client.write_coil(
            address=relay_idx,
            value=mode.value, # noqa
            slave=self.device,
        )

    def write_all_relays(self, mode: WaveShareRelayControl | bool) -> None:
        self.write_relay(WAVESHARE_WRITE_ALL_RELAYS_IDX, mode)

    def read_all_relays(self) -> None:
        print("WaveShare Relays")
        time.sleep(.2)
        resp = self.client.read_coils(
            address=WAVESHARE_READ_ALL_RELAYS_ADDRESS,
            count=WAVESHARE_READ_WRITE_ALL_RELAYS_COUNT,
            slave=self.device,
        )
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


    def set_address(self, new_device_id) -> None:
        set_address(self.client, WaveShareRelayReadRegisters["DeviceAddress"], self.device, new_device_id)
        self.device = new_device_id
