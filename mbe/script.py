import logging # noqa
import time

from pymodbus.client import ModbusSerialClient # noqa
from pymodbus.client import ModbusTcpClient # noqa

from mbe.taidecent import Taidecent
from mbe.waveshare_relays import WaveShareRelayControl
from mbe.waveshare_relays import WaveshareRelays

client = ModbusTcpClient("192.168.1.210")
# client = ModbusSerialClient("/dev/tty.usbserial-B001K6G3", baudrate=9600)

def main():
    # logging.basicConfig()
    # log = logging.getLogger()
    # log.setLevel(logging.DEBUG)

    client.connect()

    taidecent = Taidecent(client)
    relays = WaveshareRelays(client)

    # taidecent.read_registers()
    # relays.read_all_relays()
    # for _ in range(1):
    #     relays.write_all_relays(WaveShareRelayControl.Open)
    #     relays.write_all_relays(WaveShareRelayControl.Close)
    #     relays.write_all_relays(WaveShareRelayControl.Open)
    #     relays.write_all_relays(WaveShareRelayControl.Close)

    mode = WaveShareRelayControl.Open
    i = 0
    while i < 3:
        time.sleep(2)
        taidecent.read_temperature(fahrenheit=True)
        relays.read_all_relays()
        if mode == WaveShareRelayControl.Open:
            mode = WaveShareRelayControl.Close
        else:
            mode = WaveShareRelayControl.Open
        relays.write_relay(relay_idx=0, mode=mode)
        i += 1

if __name__ == "__main__":
    main()
