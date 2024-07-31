import logging
import time
from typing import Annotated
from typing import Optional

import rich
import typer
from serial import rs485

from mbe import cli_rly
from mbe import cli_tai
from mbe import make_client
from mbe.cli_config import MbeConfig
from mbe.taidecent import Taidecent
from mbe.waveshare_relays import WaveShareRelayControl
from mbe.waveshare_relays import WaveshareRelays

app = typer.Typer(no_args_is_help=True)
app.add_typer(cli_tai.app, name="tai", help="Interact with taidecent thermometer")
app.add_typer(cli_rly.app, name="rly", help="Interact with waveshare relays")

@app.callback()
def main_app_callback(
    verbose: bool = False,
):
    if verbose:
        logging.basicConfig()
        log = logging.getLogger()
        log.setLevel(logging.DEBUG)


@app.command()
def sniff(port: str = "") -> None:
    """Sniff a serial port"""
    cfg = MbeConfig.load()
    if not port:
        port = cfg.serial.port
    elif port != cfg.serial.port:
        cfg.serial.port = port
        cfg.save()
    with rs485.RS485(port) as ser:
        rich.print()
        rich.print(f"Sniffing on: {ser}")
        i = 1
        while True:
            data = ser.read(1)
            print(f"{data[0]:02X}", end="", flush=True)
            if i % 16 == 0:
                print()
            elif i % 4 == 0:
                print("  ", end="", flush=True)
            i += 1

@app.command()
def config(
        taidecent_device_id: Optional[int] = None,
        waveshare_relay_device_id: Optional[int] = None,
        serial: Annotated[bool, typer.Option(show_default=False, help="Set serial or tcp mode")] = None,
        port: Optional[str] = None,
        host: Optional[str] = None,
        force: Annotated[bool, typer.Option(show_default=False, help="Force write of config.")] = False,
        reset: Annotated[bool, typer.Option(show_default=False, help="Overwrite config with defaults. Any specified parameters will be applied on top of defaults.")] = False,
) -> None:
    """Show config file and contents. Optionally update config file if any parameter specified.
    Always creates default config file if none is present. """
    if reset:
        MbeConfig().save()
    cfg = MbeConfig.load()
    update_config = force
    if taidecent_device_id is not None and taidecent_device_id != cfg.taidecent_device_id:
        cfg.taidecent_device_id = taidecent_device_id
        update_config = True
    if waveshare_relay_device_id is not None and waveshare_relay_device_id != cfg.waveshare_relay_device_id:
        cfg.waveshare_relay_device_id = waveshare_relay_device_id
        update_config = True
    if serial is not None:
        mode = "serial" if serial else "tcp"
        if mode != cfg.mode:
            cfg.mode = mode
            update_config = True
    if port and port != cfg.serial.port:
        cfg.serial.port = port
        update_config = True
    if host and host != cfg.tcp.host:
        cfg.tcp.host = host
        update_config = True
    if update_config:
        rich.print("Updating config file")
        cfg.save()
    cfg = MbeConfig.load()
    rich.print(f"Config file: {cfg.path}")
    rich.print(cfg)

@app.command()
def run(itr: int = 3) -> None:
    """Reads taidecent thermometer and sets waveshare relays."""
    cfg = MbeConfig.load()

    client = make_client.make(cfg)
    client.connect()

    taidecent = Taidecent(client, device=cfg.taidecent_device_id)
    relays = WaveshareRelays(client, device=cfg.waveshare_relay_device_id)

    mode = WaveShareRelayControl.Open
    i = 0
    while i < itr:
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
    app()