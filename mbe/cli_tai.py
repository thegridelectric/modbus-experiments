import time

import typer

from mbe import make_client
from mbe.cli_config import MbeConfig
from mbe.taidecent import Taidecent
from mbe.taidecent import TAIDECENT_DEVICE_ID
from mbe.taidecent import TAIDECENT_DEVICE_ID_FACTORY

app = typer.Typer(no_args_is_help=True)


@app.command()
def read() -> None:
    """Read temperature."""
    cfg = MbeConfig.load()
    client = make_client.make(cfg)
    client.connect()
    taidecent = Taidecent(client, device=cfg.taidecent_device_id)
    time.sleep(2)
    taidecent.read_temperature(fahrenheit=True)


@app.command()
def read_all() -> None:
    """Read all registers."""
    cfg = MbeConfig.load()
    client = make_client.make(cfg)
    client.connect()
    taidecent = Taidecent(client, device=cfg.taidecent_device_id)
    time.sleep(2)
    taidecent.read_registers()


@app.command()
def set_device_id(
    from_id: int = TAIDECENT_DEVICE_ID_FACTORY, to_id: int = TAIDECENT_DEVICE_ID
) -> None:
    """Change the device id of the Taidecent thermometer."""
    cfg = MbeConfig.load()
    client = make_client.make(cfg)
    client.connect()
    taidecent = Taidecent(client, device=from_id)
    taidecent.set_device_id(to_id)
    if to_id != cfg.taidecent_device_id:
        cfg.taidecent_device_id = to_id
        cfg.save()


@app.command()
def set_temp_correction(correction: int) -> None:
    """Set the temperature correction factor on Taidecent thermometer."""
    cfg = MbeConfig.load()
    client = make_client.make(cfg)
    client.connect()
    taidecent = Taidecent(client, device=cfg.taidecent_device_id)
    time.sleep(2)
    taidecent.set_temp_correction(correction)
