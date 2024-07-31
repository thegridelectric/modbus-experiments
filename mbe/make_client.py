from pymodbus.client import ModbusSerialClient
from pymodbus.client import ModbusTcpClient
from pymodbus.client.base import ModbusBaseSyncClient

from mbe.cli_config import MbeConfig


def make(cfg: MbeConfig) -> ModbusBaseSyncClient:
    if cfg.mode == "serial":
        if cfg.serial.port is None:
            raise ValueError("No serial port specified")
        return ModbusSerialClient(cfg.serial.port, baudrate=cfg.serial.baud)
    else:
        return ModbusTcpClient(cfg.tcp.host)
