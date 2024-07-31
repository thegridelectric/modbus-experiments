from enum import Enum
from pathlib import Path
from typing import Annotated
from typing import Optional

import rich
import xdg
from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator

from mbe.taidecent import TAIDECENT_DEVICE_ID
from mbe.waveshare_relays import WAVESHARE_RELAY_DEVICE_ID

NO_SERIAL_PORT_FOUND = "NO-SERIAL-PORT-SPECIFIED-OR-FOUND"


class SerialConfig(BaseModel):
    port: Annotated[Optional[str], Field(validate_default=True)] = None
    baud: int = 9600

    # noinspection PyNestedDecorators
    @field_validator("port")
    @classmethod
    def find_usb_serial_port(cls, v: Optional[str]) -> str:
        """If port unspecified, look in /dev for first entry containing "tty.usbserial"."""
        if v is None or v == NO_SERIAL_PORT_FOUND:
            v = NO_SERIAL_PORT_FOUND
            try:
                dev = Path("/dev")
                if dev.exists():
                    for entry in dev.iterdir():
                        str_entry = str(entry)
                        if "tty.usbserial" in str_entry:
                            v = str_entry
                            break
            except:  # noqa
                pass
        return v


class TCPConfig(BaseModel):
    host: str = "192.168.1.210"


CONFIG_FILE = Path(xdg.xdg_config_home() / "gridworks" / "mbe" / "config.json")


class Modes(str, Enum):
    serial = "serial"
    tcp = "tcp"


class MbeConfig(BaseModel):
    taidecent_device_id: int = TAIDECENT_DEVICE_ID
    waveshare_relay_device_id: int = WAVESHARE_RELAY_DEVICE_ID
    mode: Modes = Modes.serial
    serial: SerialConfig = SerialConfig()
    tcp: TCPConfig = TCPConfig()

    @property
    def path(self) -> Path:
        return CONFIG_FILE

    @classmethod
    def _ensure_dir(cls):
        if not CONFIG_FILE.parent.exists():
            CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

    @classmethod
    def load(cls) -> "MbeConfig":
        cls._ensure_dir()
        if not CONFIG_FILE.exists():
            rich.print("Creating default config")
            MbeConfig().save()
        with CONFIG_FILE.open() as f:
            return cls.model_validate_json(f.read())

    def save(self) -> "MbeConfig":
        self._ensure_dir()
        with CONFIG_FILE.open("w") as f:
            f.write(self.model_dump_json(indent=2))
        return self
