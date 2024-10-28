import time

import typer

from mbe import make_client
from mbe.cli_config import MbeConfig
from mbe.schneider import Schneider
from mbe.schneider import SCHNEIDER_DEVICE_ID
from mbe.schneider import SCHNEIDER_DEVICE_ID_FACTORY

app = typer.Typer(no_args_is_help=True)


@app.command()
def read_all() -> None:
    """Read all registers."""
    cfg = MbeConfig.load()
    client = make_client.make(cfg)
    client.connect()
    schneider = Schneider(client, device=cfg.schneider_device_id)
    time.sleep(2)
    schneider.read_registers()


@app.command()
def set_device_id(
    from_id: int = SCHNEIDER_DEVICE_ID_FACTORY, to_id: int = SCHNEIDER_DEVICE_ID
) -> None:
    """Change the device id of the Schneider Electric Meter."""
    cfg = MbeConfig.load()
    client = make_client.make(cfg)
    client.connect()
    schneider = Schneider(client, device=from_id)
    schneider.set_device_id(to_id)
    if to_id != cfg.taidecent_device_id:
        cfg.taidecent_device_id = to_id
        cfg.save()
