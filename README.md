# Modbus Experiments

[Modbus][Modbus Spec] is a de facto standard serial request/response protocol
used in industrial control since the 1980s. This document investigates the use
of Modbus over half duplex [RS485](https://en.wikipedia.org/wiki/RS-485). Half
duplex 485 uses 3 wires (A+, A- and Common), but acts like only a single wire,
since A+ and A- are a differential pair and Common is ground. This means there
are no control signals and only one device may drive signals on the bus at a
time. As consequences, only one client may be present on the bus, only the
client may initiate conversation, servers must only respond to messages with
their device ID and the client must wait for a response from each request. 

Serial Modbus ("Modbus RTU") has an extension to IP networks via [Modbus TCP].
This essentially wraps the serial protocol into messages exchanged over a TCP
stream. This allows an entire Modbus serial bus to be available at an IP address
via a [Modbus gateway](https://www.google.com/search?client=firefox-b-1-d&q=modbus+tcp+gateway),
and conveniently allows Modbus protocol to be sniffed by, for example, [Wireshark].

This document summarizes various Modbus experiments, in particular:

* Setting up a Modbus [mini lab](#mini-lab)
* A Modbus [sniffing kit](#sniffing-kit)
* Connecting Modbus devices to automatable hubs such as Hubitat

# Shopping lists


## Bus Hardware

These are useful for setting up a Modbus bus:

* A [24 VDC power supply with sufficient amperage][Alitove].
* 5 colors of 22 AWG stranded [wire][AdaFruit-Wires] (2 for power, 3 for data).
* [Wago connectors] (check wire gauge).

## <a name="connectivity-hardware">Client connectivity hardware</a>

Experiments described here used both MacOS and Raspberry Pi clients, both
connected over serial and IP. Both serial and IP connectivity might be used in
different contexts. Connectivity equipment includes: 

* Waveshare ModbusTCP gateway: [purchase][Waveshare Eth/RS485 on Amazon], 
  [web page][Waveshare Eth/RS485] and [manual][Waveshare Eth/RS485 User Manual]. 
* Waveshare USB to RS485 dongle: [purchase][Waveshare USB/RS485 on Amazon] and
  [manual][Waveshare USB/RS485]. Two might be useful to both speak on and sniff
  a serial-only bus.
* [USB-C/USB-A] cable for connecting Macintosh to USB dongle.
* [USB-A extension cable] for connecting Pi to USB dongle when a different
  dongle, such as the [Zooz Z-Wave dongle] blocks access. 

## Sniffing hardware and software
In a diagnostic situation either IP or serial sniffing might be required. For IP
sniffing an ethernet hub that supports [Port Mirroring] is necessary if the
sniffing is not done from the client machine. 

For serial sniffing, display of raw hex bytes is easy via [pyserial], but useful
parsing of messages is non-trivial since there is not obvious packet framing - a
parser must check find a frame boundary by parsing each byte as the potential
start of a request or a response. Instead, I recommend existing Modbus parsing
software. I like [IONinja], but it is not free after a 14 day eval. There are
other tools available. I found [Serial Port Monitor] unsatisfactory. The 
[SerialTool] free version might be worth a try. 

In addition to the [client connectivity](#client-connectivity-hardware) listed above,
* IP sniffing needs:
  * NetGear Port Mirroring switch: [purchase][Port mirroring switch on amazon] and
    [manual][GS108ev3 manual].
  * A [USB-C to Ethernet connector][Mokin USB-C/Eth] for the Macintosh.
  * 4 Ethernet cables.
  * [Wireshark] software (awesome and free).
* Serial sniffing needs:
  * [IONinja] software. Sign up for the 14 day eval.
    
  
## Test devices
It is useful to have cheap and simple Modbus devices to experiment with.
Experients described here were carried out with. I did experiments with: 

* [Taidecent thermometer]. Arrives with very nice one page paper manual in the
  package.
* Waveshare Modbus relays: [purchase][Waveshare relays on Amazon] and
  [manual][Waveshare relays].

# Instructions

## <a name="minilab">Mini lab</a>

### A simple read

Start with a [really simple script][simple script] in which the use of pymodbus to interact with
a device is very directly visible. In this case, we will read the temperature
from the Taidecent thermometer.

1. Wire the Taidecent thermometer to power and to the RS485 data bus. The 
   Taidecent thermomenter does not use the RS485 Common wire.
2. Wire one [USB serial dongle][Waveshare USB/RS485] to the RS485 data bus. 
   The dongle gets power from the USB connection. 
3. Connect the USB serial dongle to the [USB-C/USB-A] cable, and connect the 
   USB-C/USB-A cable to your macintosh. 
4. Clone this repo, Create virtual environment, activate it, and install the
   prequisites.
   
    ```shell
    git clone https://github.com/thegridelectric/modbus-experiments.git
    cd modbus-experiments
    poetry install
    poetry shell
    pre-commit install 
    ```
    This will install [pymodbus], [pyserial], a [simple script], a cli for
    more involved experiments (`mbe`) and development tools. To just run the 
    simple script all you would need to do is: 
   
    ```shell
    git clone https://github.com/thegridelectric/modbus-experiments.git
    cd modbus-experiments
    python -m venv .venv
    source .venv/bin/activate
    pip install pyserial pymodbus rich
    ```
5. Find your serial port: 
    ```shell
    ls /dev | grep tty.usbserial
    ```
    You should see an entry such as:
    ```
    tty.usbserial-B001K2B8
    ```
    in which case your serial port will be:
    ```
    /dev/tty.usbserial-B001K2B8
    ```
6. Modify `mbe/script.py` to contain your actual serial port. 
7. Run `mbe/script.py`:
   ```shell
   python mbe/script.py
   ```
   You should see output such as: 
   ```
   Read device 1, memory address 0x00  (Temperature)  Raw:2757  27.57°C  81.63°F
   ```
   This code boils down to:
   ```python
   import time
   from pymodbus.client import ModbusSerialClient
   client = ModbusSerialClient("/dev/tty.usbserial-B001K2B8", baudrate=9600)
   client.connect()
   time.sleep(.2)
   resp = client.read_holding_registers(address=0, slave=1, count=1)
   print(resp.registers[0])
   ```
    If you have errors, the most likely sources are: 
    * Serial port name is wrong.
    * Device id ('slave') is not configured to 1 on the Taidecent (it should be
      by default).
    * Faulty wiring or bus power. 
   
    If that does not resolve questions, see next section.

### Simple sniffing

Even if you don't have errors it is instructive to watch the raw bytes on the
bus. You can do that with a second [USB serial dongle][Waveshare USB/RS485]: 

1. Wire the second USB serial dongle to the RS485 data bus.
2. Connect the second USB serial dongle to the other USB-A connector on the
   [USB-C/USB-A] cable.
3. Find the name of the second serial port: 
    ```shell
    ls /dev | grep tty.usbserial
    ```
    You should see something like: 
    ```
    tty.usbserial-B001K2B8
    tty.usbserial-B001K6G3
    ```

    Note which is the old one and which is the new one. 
4. Open a new terminal (correct this command for the actual second port): 
   ```shell
   cd modbus-experiments
   poetry shell
   mbe sniff --port /dev/tty.usbserial-B001K6G3
   ```
   You should see something like: 
    ```
    Sniffing on: RS485<id=0x100ca3400, open=True>(port='/dev/tty.usbserial-B001K6G3', 
    baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=False, 
    rtscts=False, dsrdtr=False)
    ```
   If you do not, check your config with: 
   ```shell
   mbe config
   ```
   and also consider error sources listed above.
5. Now in the first terminal, run the simple script again:
   ```shell
   python mbe/script.py
   ```
   In the first terminal you should see something like:
   ```
   Read device 1, memory address 0x00  (Temperature)  Raw:2758  27.58°C  81.64°F
   ```
   and in the second terminal you should see something like: 
   ```
   01030000  0001840A  0103020A  C63EB6
   ```
   What does this mean? Since we saw the temperature printed, we know there was
   a request and a response, but because there is no framing we don't know
   where the request ends and the response begins. We could parse it from the
   spec but it's much faster to use a parser. A quick compromise is to make a 
   guess and then use this awesome [online Modbus parser] from Rapid SCADA.
   If we paste all those bytes into the parser we get an error. But without
   carefully parsing the request and response we can note that non-exotic 
   requests starts with one byte of device id and one byte of function code and 
   the response mirrors that. Both have a two byte CRC at the end which is 
   likely to look like "some random hex number". With that in mind we can glance
   at the bytes and guess that: 
   ```
   request:  01030000  0001840A  
   response: 0103020A  C63EB6
   ```
   We can now paste each of those into the [online Modbus parser] and get a
   sensible explanation of data exchange. **This is too cumbersome** for 
   interesting conversations. For those we need a real parser like [Wireshark]
   or [IONinja]. Wireshark is free, so we will start with that. To watch Modbus
   with Wireshark, we need to set up the
   [Waveshare ModbusTCP gateway][Waveshare Eth/RS485 User manual].


### <a name="waveshare-gateway">Waveshare gateway</a>

The [Waveshare ModbusTCP gateway][Waveshare Eth/RS485] allows us to
communicate to a Modbus serial bus over TCP. To use the Waveshare gateway we
need choose static IP or DHCP or DHCP with a network name reservation. I will
describe the latter since it is practical and robust. As [Rod McBain] notes, 
the Waveshare gateway needs to be configured with Waveshare's [vircom] windows
program. In order to use Wireshark to sniff communication to the gateway, the
machine running Wireshark must see the traffic going to the gateway. Here we
assume the only traffic going to the gateway is coming from the machine running
wireshark, so we do not need a [special network switch][Port mirroring switch]
or to configure port mirroring.

1. Attach the gateway to RS485 data, to power, and to Ethernet.
2. Download and install [Vircom] on a Windows machine. 
3. Start Vircom. 
4. Press "Device"
5. The factory setting gateway will be at 192.168.1.254. Press "Auto Search" if
   the gateway isn't present. 
6. Double click on the row for the gateway. 
7. Note the "Dev Name" field. This is the gateway's network name. Confirm that with:
   ```shell
   # replace "DEV_NAME_SHOWN" with value of Dev Name field.
   ping DEV_NAME_SHOWN.local
   ```
8. Log into your home router. In the section that configures the LAN, add an
   address reservation for that network name. Save your changes. 
9. Make these changes in vircom:
   * Change "IP Mode" to DHCP.
   * Set the baud rate to 9600.
   * Set the "Transfer Protocol" to "Modbus_TCP Protocol"
   * Press "Modify Setting" 
10. Wait a moment. If the IP address does not change to the value of your
    reservation, stop stop all Vircom windows, cycle power on the gateway and
    restart Vircom. Vircom should now show the expected IP address. You cross 
    check by pinging the network name and by logging into your home router and
    looking at devices attached to the LAN. 
11. Once the gateway has the desired IP, stop all Vircom windows. You can now
    put away your Windows machine.
12. Test that Modbus is working via the gateway by modifying `mbe/script.py` so
    that `serial = False` and `host` has the correct IP address. 
13. Run
    ```shell
    python mbe/script.py
    ```
    You should see the temperature printed as before. If you have errors, check
    that the IP address is correct. Another likey source of errors is the
    gateway wiring. You can get also information about your gateway connection
    by setting `serial = True` and noting what behavior changes. If that does
    not resolve questions, see next section.

### Wireshark sniffing

Even if you don't have errors it is instructive to watch communication using 
[Wireshark]. 

Note that Wireshark uses two kinds of filters, with two different
filter languages: 
* [Capture filters] control which packets are actually captured. You select
  capture filters when you start capturing. They can reduce the size of captured
  data. 
* [Display filters] control which packets are displayed during capture. They can
  be changed during capture.

If you don't expect IP connection issues, a capture filter will reduce clutter.
On the other hand, if you are having trouble connecting, it might be better to
use no capture filter and use display filters to try to better understand what 
is happening. A comparison of simple filters: 
```
capture: host 192.168.1.210
display: ip.addr==192.168.1.210
```

Setup and usage:
1. [Install][Wireshark download] Wireshark. 
2. Start Wireshark.
3. Choose which network interface to capture on (e.g. "Wi-Fi en0").
4. If you think your script execution found the right IP address, use a capture
   filter with the IP address of the gateway such as
   ```
   host 192.168.1.210
   ```
   If you are having IP connectivity issues, use no capture filter. 
5. Start the capture.
6. In a terminal, run the script: 
   ```shell
   python mbe/script.py
   ```
   You should see a bunch of rows in Wireshark containint at least the entire
   TCP connection used by the script. If you can successfully reach the
   gateway you should see two rows with Protocol of Modbus/TCP. If you select
   the "Query" row, you should see a break down of the protocol stack used by 
   that packet in the lower left hand corner. You would be able to click on 
   "Modbus" in that breakdown and see a breakdown of the fields that will be
   put on the serial bus. Note there is no CRC; that is computed before putting
   the data on the bus; to see that you need to sniff on the actual serial port.

If you are having connectivity issues you might want to start with no capture
filter and instead use display filters to remove unrelated packets from view, at
least until you've concluded that you and the gateway agree about its IP address.
You can also filter by MAC address since you should be able to figure out the 
MAC address of the gateway. You might want to try pinging the device while the
capture is running. 

### Configuring multiple devices
If multiple servers are present on a Modbus bus, they must have different device
IDs. Generally devices ship with a the same default ID (1), so you have to
change their device IDs. How to change their device ID must be documented by the
device. It is typically done by writing a register. We will use the `mbe` cli
to change device address, which just calls `write_register()` on the pymodbus
client.

Check out the `mbe` cli:
```shell
mbe --help
mbe config --help
mbe tai --help
mbe rly --help
```

Check out the current config: 
```shell
mbe config
```

Config can also be changed by editing config.json file or with the config
command. For example, this command sets the IP address of the gateway to 
192.168.1.210 and specifies ModbusTCP, not serial, should be used.
```shell
mbe config --host 192.168.1.210 --no-serial
```

Now we change the device IDs of the Taidecent and Waveshare Relays so they can
co-exist on the bus:
1. Using `mbe config` or the config.json file, verify serial or TCP mode is
   specified and host IP and serial port are set up as expected.
2. Change the device ID of the Taidecent: 
   ```shell
   mbe tai set-device-id --from-id 1 --to-id 2
   ```
3. Wire the [Waveshare relay board][Waveshare relays] to  to power and to the 
   RS485 data bus.
4. Configure Waveshare relay device ID to default value:
   ```shell
   mbe config --waveshare-relay-device-id 1
   ```
5. Verify you hear at least one click when you run:
   ```shell
   mbe rly set-all 0
   mbe rly read
   mbe rly set-all 1
   mbe rly read
   ```
6. Change the device ID of the relay board: 
   ```shell
   mbe rly set-device-id --from-id 1 --to-id 3
   ```
7. Verify you can interact with both devices at their new addresses:
   ```shell
   mbe run
   ```

### IONinja sniffing

There are time when it is preferable to sniff the RS495 bus directly, for
example because the client does not or cannot communicate ModbusTCP. A
[trivial serial program] such as `mbe sniff` can do this, but it does not 
provide useful parsing. [IONinja] is program that parses Modbus serial
communication and provides a nice visual display [similar to Wireshark].
IONinja is not free but it has a free eval and a [reasonable subscription price]
(note there is also one time $35 cost for the serial plugin when upgrading the
eval).

To set up IONinja: 

1. [Download][IONinja] and install IONinja.
2. Create a free account on IONinja.
3. Sign up for the eval. 
4. When you start IONinja, choose "Sign in online". 
5. You might need to follow instructions to enter the key for the eval.

Sniffing:

1. Start IONinja
2. File / New Session / Serial
3. File / Layer Pipeline / Add / Modbus Analyzer
4. Choose a serial port
5. Set:
   * Baud rate: 9600
   * DTR: off
   * Protocol: ModbusRTU
   * Streams: Half duplex RX
6. Session / Open (*you must do this each time*)

To generate experimental traffic:

1. Verify `mbe` is configured to communicat using a different mechanism:
   ```shell
   mbe config
   # Check that "mode" and "serial" or "tcp" are as you desire.
   ```
2. If necessary configure `mbe` to communicate on a *different* serial port or on 
    a ModbusTCP gateway. For example: 
   ```shell
   # To enable serial on port /dev/tty.usbserial-B001K2B8:
   mbe config --serial --port /dev/tty.usbserial-B001K2B8
   # Or, to enable tcp on host 192.168.1.210:
   mbe config --no-serial --host 192.168.1.210
   ```
3. Generate a simple request / response with: 
   ```shell
   mbe tai read 
   ```

You should be able to click on the '+' icon in each row to get a detailed
parsing of that packet.

### Port mirroring
[Wireshark], but it can only show packets that your computer sees. If you trying
to watch TCP communication between a ModbusTCP client and ModbusTCP gateway, 
and the client is an actual other device, not software running on your computer,
there is a good chance that the LAN hardware the client, the gateway and your
computer will not present packets between the client and the gateway to your
computer. This is primarily for efficiency reasons, but also for security. 

This problem is solvable using a network switch that supports [Port Mirroring],
assuming you can reconnect the Ethernet cable of at least one monitored device
to the new swich, and connect the new switch to the existing LAN. We verified
this set up with a [GS108ev3][Port mirroring switch on amazon] from NetGear.

To set up this sniffing Ethernet link 
1. Connect the GS108ev3 to your LAN.
2. Enable port mirroring on the switch per the [GS108ev3 manual]. Basically: 
   * Determine the IP address of the switch by logging into your router or using
     the [NetGear discovery tool]
   * Log onto the switch using a browser.
   * Change the switch password.
   * Follow instruction in the manual to enable port mirroring to one of the
     ports of the switch (I chose port 8). For efficiency and security only one
     port receives the packets mirrored from other ports.
3. Connect either or both of the client and the gateway to the GS1018ev3.
4. Connect your sniffing computer to the port on the swich you configured to
   receive mirrored packets.

## <a name="sniffing-kit">Sniffing kit</a>

* [Power supply][Alitove]
* [5 colors of 22 AWG stranded wire][AdaFruit-Wires]
* Wire stripper
* Screw drivers
* [Wago connectors]
* [Waveshare ModbusTCP gateway][Waveshare Eth/RS485 on Amazon] 
* Two [Waveshare USB/RS485 dongles][Waveshare USB/RS485 on Amazon]
* [USB-C/USB-A]
* [USB-A extension cable]
* [Port mirroring switch][Port mirroring switch on amazon]
* [USB-C to Ethernet connector][Mokin USB-C/Eth]
* 4 Ethernet cables
* [Wireshark] software
* [IONinja] software with eval license or subscription.
* Test devices: 
  * [Taidecent Thermometer]
  * [Waveshare Relays]

[links]: .

[bus hardware]: .
[Wago connectors]: https://www.wago.com/us/c/wire-splicing-connectors?f=%3Afacet_product_Produkthauptfunktion_5200%3ASplicing%20Connector%20with%20Levers%3Afacet_product_Betaetigungsart_01_3901%3ALever&sort=relevance&pageSize=20
[Alitove]: https://www.amazon.com/ALITOVE-Transformer-Universal-Regulated-Switching/dp/B078RYWZMH/ref=sr_1_4?dib=eyJ2IjoiMSJ9.5igMaIazfkV-vmQFfpuzk11z5IOilxi7GusTD5PPRHU97Ow1K2fDhFemWyDKqGkbd5bRq7Zp2hHP1ej0IYU_gIXq98NCERmrkIpdWQVGP_T618vqhYMWJzWeu5trVSgaawG8Y0jdFhOdPzoz5idF2yP_nYkubNheqavr1mAMXFQKL97HCSeVs5C-Xo2gSeCt9nC1inwiIbDOF_KWTRhSaB8kbwaA-yIL6bT4_3LEqHk.dwGPrZ7_eyJxw7FFeStd7dL74WlOCCBm2ignLUM5E1c&dib_tag=se&keywords=power%2Bsupply%2B24v%2B10a&qid=1722015511&sr=8-4&th=1
[AdaFruit-Wires]: https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/2184/3111_Web.pdf

[modbus]: .
[Modbus Spec]: https://www.modbus.org/docs/Modbus_Application_Protocol_V1_1b3.pdf
[Modbus TCP]: https://www.modbus.org/docs/Modbus_Messaging_Implementation_Guide_V1_0b.pdf

[pymodbus]: .
[pymodbus]: https://pymodbus.readthedocs.io/en/latest/source/simulator.html
[pymodbus parser example]: https://github.com/pymodbus-dev/pymodbus/blob/master/examples/message_parser.py
[pymodbus generator example]: https://github.com/pymodbus-dev/pymodbus/blob/master/examples/message_generator.py

[waveshare gateway]: .
[Waveshare Eth/RS485]: https://www.waveshare.com/wiki/RS485_TO_ETH_(B)
[Waveshare Eth/RS485 POE]: https://www.waveshare.com/wiki/RS485_TO_POE_ETH_(B)
[Rod McBain]: https://www.youtube.com/watch?v=Xuj2YFZ5zME&t=413s
[Waveshare Eth/RS485 on Amazon]: https://www.amazon.com/gp/aw/d/B0BGBQJH21/?_encoding=UTF8&pd_rd_plhdr=t&aaxitk=775308fcdd401f801a872fdc2dbde0aa&hsa_cr_id=0&qid=1717868677&sr=1-2-9e67e56a-6f64-441f-a281-df67fc737124&ref_=sbx_be_s_sparkle_sccd_asin_1_img&pd_rd_w=opBhC&content-id=amzn1.sym.417820b0-80f2-4084-adb3-fb612550f30b%3Aamzn1.sym.417820b0-80f2-4084-adb3-fb612550f30b&pf_rd_p=417820b0-80f2-4084-adb3-fb612550f30b&pf_rd_r=F4K0KKF6WDCTFDHQKFRG&pd_rd_wg=ncXV7&pd_rd_r=9c68359e-b279-41d1-b36b-340620ab8513
[Waveshare Eth/RS485 User manual]: https://files.waveshare.com/upload/4/4d/RS485-to-eth-b-user-manual-EN-v1.33.pdf
[Waveshare Eth/RS485 MQTT manual]: https://files.waveshare.com/upload/a/a6/EN-RS485-TO-ETH-B-MQTT-and-json-user-manual2.pdf
[Vircom]: https://www.waveshare.com/wiki/File:VirCom_en.rar

[test devies]: .
[Waveshare relays on Amazon]: https://www.amazon.com/dp/B0CLV4KNKX?psc=1&ref=ppx_yo2ov_dt_b_product_details
[Waveshare relays]: https://www.waveshare.com/wiki/Modbus_RTU_Relay
[Taidecent thermometer]: https://www.amazon.com/dp/B07ZYVZZKK?psc=1&ref=ppx_yo2ov_dt_b_product_details

[usb/rs485]: .
[Waveshare USB/RS485 on Amazon]: https://www.amazon.com/gp/aw/d/B081NBCJRS/?_encoding=UTF8&pd_rd_plhdr=t&aaxitk=3b189f989dddebde3c804d6a7e36be6e&hsa_cr_id=0&qid=1722013232&sr=1-2-9e67e56a-6f64-441f-a281-df67fc737124&ref_=sbx_be_s_sparkle_sccd_asin_1_img&pd_rd_w=tGxX7&content-id=amzn1.sym.8591358d-1345-4efd-9d50-5bd4e69cd942%3Aamzn1.sym.8591358d-1345-4efd-9d50-5bd4e69cd942&pf_rd_p=8591358d-1345-4efd-9d50-5bd4e69cd942&pf_rd_r=DFBYFKQQZNWPBGN8AYEK&pd_rd_wg=bdGhC&pd_rd_r=26852b6b-31ae-4eb5-8ddf-4be5cb91a90e
[Waveshare USB/RS485]: https://www.waveshare.com/wiki/USB_TO_RS485
[USB-C/USB-A]: https://www.amazon.com/dp/B07TPS44SL?psc=1&ref=ppx_yo2ov_dt_b_product_details
[USB-A extension cable]: https://www.amazon.com/Extension-AINOPE-Material-Transfer-Compatible/dp/B07ZV6FHWF/ref=sr_1_4?crid=1K4IZ13NTV8O5&dib=eyJ2IjoiMSJ9.D0CvjxSS7KAqyLV1bV1Vpnwv8HUOg95mrDFi8zBrA9mrHl6xZ8G4QZbswPhSm2HONCB3jcAvQ58bxNyfNroCbsnVaIxV6mmbiQHpZu-nuq807PBXfVBa3KawoYtHYXojpzSly6eg5Rv8tjLmnxFa8VvYADi98qIKLHGbLVoJPVAta1VUiemkusVvLdiDdv5prMliPjWsA32tjmv7pWiRXsBQUTetJAPff33Fj-aods8.0aozzyW_uv_25zmInNW6NzFD_JZ7wpclNcEGPBtXEgo&dib_tag=se&keywords=usb%2Ba%2Bextension%2Bcable&qid=1722119822&sprefix=usb%2Ba%2Bexte%2Caps%2C90&sr=8-4&th=1

[Port Mirroring stuff]: .
[Mokin USB-C/Eth]: https://www.amazon.com/Adapter-MacBook-MOKiN-Ethernet-Charging/dp/B07S8MKJ6Q/ref=sr_1_1?crid=BXDQ4XH33GL4&dib=eyJ2IjoiMSJ9.X1DLChZXvZ24YjkLM31TQwZ52LgwzHNTjbh-j4M5SA8tdY4jB4Vjx8q16Rt-PxjK1P-G2Y6bnz3gd7bQdlWN084Y8ERLYhomGBNq0sxIV5RXwotxMJ8lPHTFEHt76xJjYSUGXB4wz_faceFE0QGmwwu2ePKvMpmH4prMoTaion0LpczreikrVXhs3oibQ8FrYu5bHydO37GpU6NqiujT-PvcD0Y1RwfmgcAYL4ydTQShcbX0K-j90eFWYvoZ_V-rsqdu1pUqVh-_jZtVi7I-Dms2RPj6btHFn7FVGz89WNA.FWtg0dIeiggE2y_2TESxI30J_Z06pfCKGgsEYGV25mA&dib_tag=se&keywords=mokin+usb+c+ethernet&qid=1722014640&s=electronics&sprefix=mokin+usb+c+ethernet%2Celectronics%2C77&sr=1-1
[Port mirroring switch on amazon]: https://www.amazon.com/dp/B00M1C0186?psc=1&ref=ppx_yo2ov_dt_b_product_details
[Port mirroring switch]: https://www.netgear.com/support/product/gs108ev3/
[GS108ev3 manual]: https://www.downloads.netgear.com/files/GDC/GS105EV2/WebManagedSwitches_UM_EN.pdf
[Port Mirroring]: https://en.wikipedia.org/wiki/Port_mirroring
[NetGear discovery tool]: https://www.netgear.com/support/product/netgear-discovery-tool/

[wireshark stuff]: .
[Wireshark]: https://www.wireshark.org/
[Wireshark download]: https://www.wireshark.org/download.html
[capture filters]: https://www.tcpdump.org/manpages/pcap-filter.7.html
[display filters]: https://www.wireshark.org/docs/man-pages/wireshark-filter.html

[IONinja and friends]: .
[pyserial]: https://pyserial.readthedocs.io/en/latest/shortintro.html
[trivial serial program]: https://github.com/thegridelectric/modbus-experiments/blob/3804caaab36d0f452d0a36ccd7e2c9601ca01921/mbe/cli.py#L44
[IONinja]: https://ioninja.com/downloads.html
[similar to Wireshark]: https://www.youtube.com/watch?v=uwKJUWeOlnQ&t=82s
[reasonable subscription price]: https://ioninja.com/account/subscription.html?utm_source=google&utm_medium=cpc&utm_campaign=pmax-hardware&gad_source=1&gclid=CjwKCAjw5Ky1BhAgEiwA5jGujiS1wZ8J_QWuI0HTwCcXfvvJgY1MDRsejMiI8eBDOY9SuAbGG7BA2RoCcp8QAvD_BwE
[Serial Port Monitor]: https://www.com-port-monitoring.com/downloads.html
[SerialTool]: https://www.serialtool.com/_en/serial-port-license

[misc]: .
[simple script]: https://github.com/thegridelectric/modbus-experiments/blob/main/mbe/script.py
[Online Modbus parser]: https://rapidscada.net/modbus/
[Modbus Function Codes]: https://ozeki.hu/p_5873-modbus-function-codes.html
