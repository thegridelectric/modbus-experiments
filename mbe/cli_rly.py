import typer

from mbe import make_client
from mbe.cli_config import MbeConfig
from mbe.waveshare_relays import WAVESHARE_RELAY_DEVICE_ID
from mbe.waveshare_relays import WAVESHARE_RELAY_DEVICE_ID_FACTORY
from mbe.waveshare_relays import WaveshareRelays

app = typer.Typer(no_args_is_help=True)

@app.command("set")
def set_relay(idx: int, closed: bool) -> None:
    cfg = MbeConfig.load()
    client = make_client.make(cfg)
    client.connect()
    relays = WaveshareRelays(client, device=cfg.waveshare_relay_device_id)
    relays.write_relay(relay_idx=idx, mode=closed)

@app.command("set-all")
def set_all_relays(closed: bool) -> None:
    cfg = MbeConfig.load()
    client = make_client.make(cfg)
    client.connect()
    relays = WaveshareRelays(client, device=cfg.waveshare_relay_device_id)
    relays.write_all_relays(mode=closed)

@app.command("read")
def read_relays() -> None:
    cfg = MbeConfig.load()
    client = make_client.make(cfg)
    client.connect()
    relays = WaveshareRelays(client, device=cfg.waveshare_relay_device_id)
    relays.read_all_relays()

@app.command()
def set_device_id(from_id: int = WAVESHARE_RELAY_DEVICE_ID_FACTORY, to_id: int = WAVESHARE_RELAY_DEVICE_ID):
    cfg = MbeConfig.load()
    client = make_client.make(cfg)
    client.connect()
    relays = WaveshareRelays(client, device=from_id)
    relays.set_device_id(to_id)
    if to_id != cfg.waveshare_relay_device_id:
        cfg.waveshare_relay_device_id = to_id
        cfg.save()
