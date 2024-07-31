"""A very simple script showing using pymodbus to read temperature from taidecent thermomenter
at its default device id, 1.
"""

import logging # noqa
import time

from pymodbus.client import ModbusSerialClient
from pymodbus.client import ModbusTcpClient

## MODIFY AS NEEDED #####
serial  = True
verbose = False
serial_port = "/dev/tty.usbserial-B001K2B8"
host = "192.168.1.210"
#########################

if __name__ == "__main__":

    if verbose:
        logging.basicConfig()
        log = logging.getLogger()
        log.setLevel(logging.DEBUG)

    if serial:
        client = ModbusSerialClient(serial_port, baudrate=9600)
    else:
        client = ModbusTcpClient(host)
    client.connect()

    time.sleep(.2)
    address = 0x0000
    device_id = 1
    resp = client.read_holding_registers(address=address, slave=device_id, count=1)

    s = f"Read device {device_id}, memory address 0x{address:02X}  (Temperature)  "
    if isinstance(resp, Exception):
        s += str(resp)
    else:
        s += f"Raw:{resp.registers[0]:4d}"
        C = resp.registers[0] / 100
        F = C * 9 / 5 + 32
        s += f"  {C}\u00B0C  {F:4.2f}\u00B0F"
    print(s)
