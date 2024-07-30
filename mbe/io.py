import time

import rich

from pymodbus.client.base import ModbusBaseSyncClient


def set_address(client: ModbusBaseSyncClient, address: int, curr_device_id: int, new_device_id: int) -> None:
    """Change the device id of a modbus server, if that device does not already report new_device_id.

    Uses pymodbus read_holding_registers() and write_register()
    """
    name = "DeviceAddress"
    resp = client.read_holding_registers(address=address, slave=curr_device_id, count=1)
    if isinstance(resp, Exception):
        raise resp
    if new_device_id != resp.registers[0]:
        print(f"Setting {name} to {resp.registers[0]} -> {new_device_id}")
        time.sleep(.2)
        resp = client.write_register(address=address, value=new_device_id & 0xFFFF, slave=curr_device_id)
        if isinstance(resp, Exception):
            raise resp
        rich.print(resp)
        time.sleep(.2)
        resp = client.read_holding_registers(address=address, slave=new_device_id, count=1)
        s = f"Read 0x{address:02X}   {name:20}: "
        if isinstance(resp, Exception):
            s += str(resp)
            raise ValueError(s)
        else:
            read_back_id = resp.registers[0]
            s += f"{read_back_id:6d}"
            print(s)
            if read_back_id != new_device_id:
                s += f"  ERROR. Read back device id {read_back_id} after setting address {new_device_id}"
                raise ValueError(s)

def print_registers(client: ModbusBaseSyncClient, device: int, registers: dict[str, int]) -> None:
    """Read and print registers of a device using pymodbus read_holding_registers()"""
    for name, address in registers.items():
        time.sleep(.2)
        resp = client.read_holding_registers(address=address, slave=device, count=1)
        s = f"Read 0x{address:02X}   {name:20}: "
        if isinstance(resp, Exception):
            s += str(resp)
        else:
            s += f"{resp.registers[0]:6d}"
        print(s)

def write_register(client: ModbusBaseSyncClient, device: int, address: int, value: int, name: str = ""):
    """Write a register, read it back, print result. Uses pymodbus write_register() and
    read_holding_registers()."""
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
