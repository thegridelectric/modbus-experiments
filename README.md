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
* Connecting Modbus devices to hubs such as Hubitat

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

* Waveshare ModbusTCP gateway: [purchase][Waveshare Eth/RS485 on Amazon] and
  [manual][Waveshare Eth/RS485]. 
* Waveshare USB to RS485 dongle: [purchase][Waveshare USB/RS485 on Amazon] and
  [manual][Waveshare USB/RS485].
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

In addition to the [client connectivity](#connectivity-hardware) listed above,
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

## Mini lab software

* [pymodbus]
* [pyserial]

## Hub hardware

* Hubitat
* Pi for Home Assistant

# Instructions

## Setting up a <a name="minilab">mini lab</a>


## Setting up <a name="sniffing-kit">sniffing</a>

# Useful links

* [Waveshare Eth/RS485]
  * [Rod McBain to the rescue]
* [Waveshare USB/RS485 on Amazon]
* [Online Modbus parser]
* [Function Codes][Modbus Function Codes]
* [Spec][Modbus Spec]
* [pymodbus]
* [IONinja]
* [Wireshark]

# Hub connectivity

## Bridges
  
### "Hand written" HTTP to Modbus

### Node-red

### Stride

### Home Assistant

[Wago connectors]: https://www.wago.com/us/c/wire-splicing-connectors?f=%3Afacet_product_Produkthauptfunktion_5200%3ASplicing%20Connector%20with%20Levers%3Afacet_product_Betaetigungsart_01_3901%3ALever&sort=relevance&pageSize=20
[Wireshark]: https://www.wireshark.org/
[Modbus Spec]: https://www.modbus.org/docs/Modbus_Application_Protocol_V1_1b3.pdf
[Modbus TCP]: https://www.modbus.org/docs/Modbus_Messaging_Implementation_Guide_V1_0b.pdf
[Modbus Function Codes]: https://ozeki.hu/p_5873-modbus-function-codes.html
[pymodbus]: https://pymodbus.readthedocs.io/en/latest/source/simulator.html
[pymodbus parser example]: https://github.com/pymodbus-dev/pymodbus/blob/master/examples/message_parser.py
[pymodbus generator example]: https://github.com/pymodbus-dev/pymodbus/blob/master/examples/message_generator.py
[Waveshare Eth/RS485]: www.waveshare.com/wiki/RS485_TO_ETH_(B)
[Waveshare Eth/RS485 POE]: www.waveshare.com/wiki/RS485_TO_POE_ETH_(B)
[Rod McBain to the rescue]: https://www.youtube.com/watch?v=Xuj2YFZ5zME&t=413s
[Waveshare Eth/RS485 on Amazon]: https://www.amazon.com/gp/aw/d/B0BGBQJH21/?_encoding=UTF8&pd_rd_plhdr=t&aaxitk=775308fcdd401f801a872fdc2dbde0aa&hsa_cr_id=0&qid=1717868677&sr=1-2-9e67e56a-6f64-441f-a281-df67fc737124&ref_=sbx_be_s_sparkle_sccd_asin_1_img&pd_rd_w=opBhC&content-id=amzn1.sym.417820b0-80f2-4084-adb3-fb612550f30b%3Aamzn1.sym.417820b0-80f2-4084-adb3-fb612550f30b&pf_rd_p=417820b0-80f2-4084-adb3-fb612550f30b&pf_rd_r=F4K0KKF6WDCTFDHQKFRG&pd_rd_wg=ncXV7&pd_rd_r=9c68359e-b279-41d1-b36b-340620ab8513
[Waveshare Eth/RS485 User manual]: https://files.waveshare.com/upload/4/4d/RS485-to-eth-b-user-manual-EN-v1.33.pdf
[Waveshare Eth/RS485 MQTT manual]: https://files.waveshare.com/upload/a/a6/EN-RS485-TO-ETH-B-MQTT-and-json-user-manual2.pdf
[IONinja]: https://ioninja.com/downloads.html
[Online Modbus parser]: https://rapidscada.net/modbus/
[Waveshare relays on Amazon]: https://www.amazon.com/dp/B0CLV4KNKX?psc=1&ref=ppx_yo2ov_dt_b_product_details
[Waveshare relays]: https://www.waveshare.com/wiki/Modbus_RTU_Relay
[Waveshare USB/RS485 on Amazon]: https://www.amazon.com/gp/aw/d/B081NBCJRS/?_encoding=UTF8&pd_rd_plhdr=t&aaxitk=3b189f989dddebde3c804d6a7e36be6e&hsa_cr_id=0&qid=1722013232&sr=1-2-9e67e56a-6f64-441f-a281-df67fc737124&ref_=sbx_be_s_sparkle_sccd_asin_1_img&pd_rd_w=tGxX7&content-id=amzn1.sym.8591358d-1345-4efd-9d50-5bd4e69cd942%3Aamzn1.sym.8591358d-1345-4efd-9d50-5bd4e69cd942&pf_rd_p=8591358d-1345-4efd-9d50-5bd4e69cd942&pf_rd_r=DFBYFKQQZNWPBGN8AYEK&pd_rd_wg=bdGhC&pd_rd_r=26852b6b-31ae-4eb5-8ddf-4be5cb91a90e
[Waveshare USB/RS485]: https://www.waveshare.com/wiki/USB_TO_RS485
[Taidecent thermometer]: https://www.amazon.com/dp/B07ZYVZZKK?psc=1&ref=ppx_yo2ov_dt_b_product_details
[Stride MQTT/Modbus gateway]: https://www.automationdirect.com/adc/overview/catalog/communications/industrial_iot_solutions/mqtt_gateways?gad_source=1&gclid=Cj0KCQjwv7O0BhDwARIsAC0sjWOFsqDI15TGkvbkFKIGhMCeQjELYF7IWXI_HFQ4OxPRbsqn6WhabsIaAhK4EALw_wcB#bodycontentppc
[Stride MQTT/Modbus gateway user manual]: https://cdn.automationdirect.com/static/manuals/mqttgateway/sgwmq1611userm.pdf
[USB-C/USB-A]: https://www.amazon.com/dp/B07TPS44SL?psc=1&ref=ppx_yo2ov_dt_b_product_details
[USB-A extension cable]: https://www.amazon.com/Extension-AINOPE-Material-Transfer-Compatible/dp/B07ZV6FHWF/ref=sr_1_4?crid=1K4IZ13NTV8O5&dib=eyJ2IjoiMSJ9.D0CvjxSS7KAqyLV1bV1Vpnwv8HUOg95mrDFi8zBrA9mrHl6xZ8G4QZbswPhSm2HONCB3jcAvQ58bxNyfNroCbsnVaIxV6mmbiQHpZu-nuq807PBXfVBa3KawoYtHYXojpzSly6eg5Rv8tjLmnxFa8VvYADi98qIKLHGbLVoJPVAta1VUiemkusVvLdiDdv5prMliPjWsA32tjmv7pWiRXsBQUTetJAPff33Fj-aods8.0aozzyW_uv_25zmInNW6NzFD_JZ7wpclNcEGPBtXEgo&dib_tag=se&keywords=usb%2Ba%2Bextension%2Bcable&qid=1722119822&sprefix=usb%2Ba%2Bexte%2Caps%2C90&sr=8-4&th=1
[Mokin USB-C/Eth]: https://www.amazon.com/Adapter-MacBook-MOKiN-Ethernet-Charging/dp/B07S8MKJ6Q/ref=sr_1_1?crid=BXDQ4XH33GL4&dib=eyJ2IjoiMSJ9.X1DLChZXvZ24YjkLM31TQwZ52LgwzHNTjbh-j4M5SA8tdY4jB4Vjx8q16Rt-PxjK1P-G2Y6bnz3gd7bQdlWN084Y8ERLYhomGBNq0sxIV5RXwotxMJ8lPHTFEHt76xJjYSUGXB4wz_faceFE0QGmwwu2ePKvMpmH4prMoTaion0LpczreikrVXhs3oibQ8FrYu5bHydO37GpU6NqiujT-PvcD0Y1RwfmgcAYL4ydTQShcbX0K-j90eFWYvoZ_V-rsqdu1pUqVh-_jZtVi7I-Dms2RPj6btHFn7FVGz89WNA.FWtg0dIeiggE2y_2TESxI30J_Z06pfCKGgsEYGV25mA&dib_tag=se&keywords=mokin+usb+c+ethernet&qid=1722014640&s=electronics&sprefix=mokin+usb+c+ethernet%2Celectronics%2C77&sr=1-1
[Port mirroring switch on amazon]: https://www.amazon.com/dp/B00M1C0186?psc=1&ref=ppx_yo2ov_dt_b_product_details
[Port mirroring switch]: https://www.netgear.com/support/product/gs108ev3/
[GS108ev3 manual]: https://www.downloads.netgear.com/files/GDC/GS105EV2/WebManagedSwitches_UM_EN.pdf
[Alitove]: https://www.amazon.com/ALITOVE-Transformer-Universal-Regulated-Switching/dp/B078RYWZMH/ref=sr_1_4?dib=eyJ2IjoiMSJ9.5igMaIazfkV-vmQFfpuzk11z5IOilxi7GusTD5PPRHU97Ow1K2fDhFemWyDKqGkbd5bRq7Zp2hHP1ej0IYU_gIXq98NCERmrkIpdWQVGP_T618vqhYMWJzWeu5trVSgaawG8Y0jdFhOdPzoz5idF2yP_nYkubNheqavr1mAMXFQKL97HCSeVs5C-Xo2gSeCt9nC1inwiIbDOF_KWTRhSaB8kbwaA-yIL6bT4_3LEqHk.dwGPrZ7_eyJxw7FFeStd7dL74WlOCCBm2ignLUM5E1c&dib_tag=se&keywords=power%2Bsupply%2B24v%2B10a&qid=1722015511&sr=8-4&th=1
[AdaFruit-Wires]: https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/2184/3111_Web.pdf
[Zooz Z-Wave dongle]: https://www.amazon.com/Z-Wave-ZST39-Assistant-HomeSeer-Software/dp/B0BW171KP3
[Port Mirroring]: https://en.wikipedia.org/wiki/Port_mirroring
[Serial Port Monitor]: https://www.com-port-monitoring.com/downloads.html
[SerialTool]: https://www.serialtool.com/_en/serial-port-license
[pyserial]: https://pyserial.readthedocs.io/en/latest/shortintro.html
