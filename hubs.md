# Hubs

Our desired Modbus client was [Hubitat] due to a significant amount of
automation IP was already configured as Hubitat Rules. However: 
* Hubitat does [not appear] to support Modbus directly. 
* You [cannot import] a ModbusTCP groovy library.
* They [don't really support] a raw socket interface.

Hubitat does support:
* HTTP via
  * [An explicit interface]
  * [Rule Machine]
  * [MakerAPI]
* [Websockets]
* [MQTT]

We therefore need a "bridge" to convert between one of Hubitat's well-supported
interfaces and Modbus. We selected [Home Assistant] as a bridge.

We were able to confirm that:
* Hubitat can communicate with Home Assistant
* Home Assistant can communicate with Modbus devices over serial and Modbus TCP.
* Home Assistant can communicate with Z-Wave devices using a USB dongle.
* Modbus and Z-Wave devices can interact with Hubitat Rules via the Home 
  Assistant.

We were also able to:
* Quickly write an HTTP/Modbus bridge prototype and control Modbus devices from 
  HTTP. 
* Quickly set up Node-Red as an MQTT/Modbus bridge and control Modbus devices
  from MQTT.

# Home Assistant

We use:
* a Raspberry Pi 4 
* 32MB SD card
* [Home Assistant operating system]

Clarity note - in Home Assistant:
* An "[add-on]" is a separate docker container that Home Assistant allows you to
  install. 
* An "[integration]" is a piece of code running, one way or another, *within*
  Home Assistant.


## Setup

* Follow the [Raspberry Pi installation instructions].   
* Follow the [onboarding page]
* Set up access to configuration.yaml: 
  * Install the [File Editor] add-on.
  * Follow [configuration.yaml] instructions and verify you can edit the main
    Home Assistant configuration.

See below for Modbus and Z-Wave instructions.

## Modbus
...
* [Modbus integration]
* [example configuration.yaml](./configuration.yaml)

## Z-Wave
...
[Z-Wave add-on]

Alternative: https://github.com/hassio-addons/addon-zwave-js-ui/tree/main

### Devices

* [Zooz Z-Wave dongle]

#### Test devices
It is useful to have a cheap and simple Z-Wave device to experiment with. Any
selection is fine as long as read and write functionality (e.g. read temperature
and set relay state) is supported. A Fibaro Smart Implant is probably
sufficient, though I did my testing with Zooz and Heltun devices. 

These are options:
* [Fibaro Smart Implant]
* [Zooz Thermometer]
* [Zooz Motion Sensor]
* [Zooz Smart Plug]
* [Zooz Relays]
* [Heltun Quinto relays]

## Hubitat connection

## Relevant known issues
* Security
* Non-trivial modbus interactions

# Rejected bridge options 

## Node-Red
[Node-Red] is a [NodeJs] server for connecting devices with a graphical
interface. We got it working such that it could receive commands on MQTT and
use to those to interact with Modbus devices. We rejected this because it would
require a separate Pi to run Node-Red. Home Assistant can run Node-Red as an 
"add-on" (in a separate container). 

Node-Red install, from [Node-Red getting started]:

* Update nvm:

      wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
    
* Update node: 

      nvm install node
      nvm use NODE-VERSION-YOU-INSTALLED
      nvm alias default node

* Install node-red:
    
      sudo npm install -g --unsafe-perm node-red

* Instal [node-red-contrib-modbus]:
     
      npm install node-red-contrib-modbus

* Run node-red
  
      node-red
     
* Access browser at http://127.0.0.1:1880/

We used flows found in [node-red-flows.json](./node-red-flows.json). The flow
used "mqtt in", "mqtt out", "modbus-flex-getter" and "modbus-flex-write" nodes.

## Hand-written HTTP/Modbus bridge
We could write an HTTP / Modbus bridge in python and run that on a Pi. This is
attractive because HTTP interaction is even more widely available than MQTT. We
rejected this because it would require maintenance time and a separate Pi
running in the system. Experiment at `$HOME/git/modbus-http` on Andy's machine.

##  Waveshare gateway MQTT

Don't do this.

The [Waveshare Modbus gateway] claims to [support MQTT], but after several hours
of work, I was only able to make it exchange a MQTT messages, the gateway
stopped working as a ModbusTCP gateway and it took more hours to reset. The
manual is hard to understand and tech support thought the problem was my MQTT
broker (it is not).

## Stride MQTT Gateway
Stride sells an [MQTT/Modbus gateway]. We rejected this because it would require
a Pi to run an MQTT broker.

[links]: .

[Home Assistant stuff]: .
[Home Assistant]: https://www.home-assistant.io/installation/ 
[Home Assistant Modbus]: https://www.home-assistant.io/integrations/modbus/
[Raspberry Pi installation instructions]: https://www.home-assistant.io/installation/raspberryp
[onboarding page]: https://www.home-assistant.io/getting-started/onboarding/
[Home Assistant operating system]: https://www.home-assistant.io/blog/2017/07/25/introducing-hassio/
[integration]: https://www.home-assistant.io/integrations/
[MQTT broker add-on]: https://www.home-assistant.io/integrations/mqtt/
[add-on]: https://www.home-assistant.io/addons/
[Modbus integration]: https://www.home-assistant.io/integrations/modbus/
[configuration.yaml]: https://www.home-assistant.io/docs/configuration/
[File Editor]: https://www.home-assistant.io/common-tasks/os/#installing-and-using-the-file-editor-add-on

[Z-Wave]: . 
[Z-Wave add-on]: https://www.home-assistant.io/integrations/zwave_js/
[Z-Wave UI add-on]: https://github.com/hassio-addons/addon-zwave-js-ui
[Zooz Z-Wave dongle]: https://www.amazon.com/Z-Wave-ZST39-Assistant-HomeSeer-Software/dp/B0BW171KP3
[Zooz Thermometer]: https://www.thesmartesthouse.com/products/zooz-z-wave-plus-700-series-xs-temperature-humidity-sensor-zse44
[Zooz Motion Sensor]: https://www.thesmartesthouse.com/products/zooz-z-wave-plus-motion-sensor-zse18-with-magnetic-base-battery-or-usb-power 
[Zooz Smart Plug]: https://www.thesmartesthouse.com/collections/zooz/products/zooz-700-series-z-wave-plus-smart-plug-zen04
[Zooz Relays]:vhttps://www.thesmartesthouse.com/products/zooz-z-wave-plus-700-series-universal-relay-zen17-with-2-no-nc-relays-20a-10a 
[Heltun Quinto relays]: https://smartsd.ch/relay-switch-quinto-5x5a-heltun-he-rs01/
[Fibaro Smart Implant]: https://www.amazon.com/FGBS-222-US-Implant-Universal-Required/dp/B07NDRCTJK/ref=sr_1_1?crid=545LHMSORHDL&dib=eyJ2IjoiMSJ9.o-_UOsPBQCx0NH75hDGl1DIfsRm7_PzmbsCDwzlZZYnIeGbFsnWOfZPoXQpUBFKzrPBFjIdwobWParZ86bzOxvvfKVm8e7cw9ygQbmRFnwOk3yOLWyqZqxg7UDhktPa-2FVtacwN_USo7whaHw21OuZ-rnaxjHGJBXQNY86MIHoFRJ8xUjq8iruDx3bt3vXv5ND5aZbDydGRpZlFqaLFTMSaW5aJnZYJYKarQrAOsWBBon5V-GT0rJQSvTECsKXDYywQLNqR97ZIjo8LhGsup6J5RUgzvq0_L4tvxC3Nav8.MICrIdSIatFOOi9Dko0POi3JgIcztlujunLW9OzZcR4&dib_tag=se&keywords=fibaro+smart+implant&qid=1722630324&sprefix=fibaro+smart%2Caps%2C96&sr=8-1


[Hubitat stuff]: .
[Hubitat]: https://hubitat.com/products?region=280262836267
[Hubitat documentation]: https://docs2.hubitat.com/en/home
[MakerAPI]: https://docs2.hubitat.com/en/apps/maker-api
[An explicit interface]: https://docs2.hubitat.com/en/developer/driver/building-a-lan-driver
[not appear]: https://community.hubitat.com/t/modbus-driver-for-hubitat/20126/3
[cannot import]: https://docs2.hubitat.com/en/developer/allowed-imports
[good support]: https://docs2.hubitat.com/en/developer/interfaces/raw-socket-interface
[Websockets]: https://docs2.hubitat.com/en/developer/interfaces/websocket-interface
[Rule Machine]: https://docs2.hubitat.com/en/apps/rule-machine/rule-5-1
[MQTT]: https://docs2.hubitat.com/en/developer/interfaces/mqtt-interface
[HADB]: https://community.hubitat.com/t/release-home-assistant-device-bridge-hadb/67109
[HADB App]: https://raw.githubusercontent.com/ymerj/HE-HA-control/main/haDeviceBridgeConfiguration.groovy
[HADB Driver]: https://raw.githubusercontent.com/ymerj/HE-HA-control/main/HA%20parent.groovy

[misc]: .
[pymodbus]: https://pymodbus.readthedocs.io/en/latest/source/simulator.html

[waveshare gateway]: .
[Waveshare Eth/RS485]: https://www.waveshare.com/wiki/RS485_TO_ETH_(B)
[Waveshare Modbus gateway]: https://www.waveshare.com/wiki/RS485_TO_ETH_(B)
[support MQTT]: https://files.waveshare.com/upload/a/a6/EN-RS485-TO-ETH-B-MQTT-and-json-user-manual2.pdf
[Waveshare Eth/RS485 POE]: https://www.waveshare.com/wiki/RS485_TO_POE_ETH_(B)
[Rod McBain]: https://www.youtube.com/watch?v=Xuj2YFZ5zME&t=413s
[Waveshare Eth/RS485 on Amazon]: https://www.amazon.com/gp/aw/d/B0BGBQJH21/?_encoding=UTF8&pd_rd_plhdr=t&aaxitk=775308fcdd401f801a872fdc2dbde0aa&hsa_cr_id=0&qid=1717868677&sr=1-2-9e67e56a-6f64-441f-a281-df67fc737124&ref_=sbx_be_s_sparkle_sccd_asin_1_img&pd_rd_w=opBhC&content-id=amzn1.sym.417820b0-80f2-4084-adb3-fb612550f30b%3Aamzn1.sym.417820b0-80f2-4084-adb3-fb612550f30b&pf_rd_p=417820b0-80f2-4084-adb3-fb612550f30b&pf_rd_r=F4K0KKF6WDCTFDHQKFRG&pd_rd_wg=ncXV7&pd_rd_r=9c68359e-b279-41d1-b36b-340620ab8513
[Waveshare Eth/RS485 User manual]: https://files.waveshare.com/upload/4/4d/RS485-to-eth-b-user-manual-EN-v1.33.pdf
[Waveshare Eth/RS485 MQTT]: https://files.waveshare.com/upload/a/a6/EN-RS485-TO-ETH-B-MQTT-and-json-user-manual2.pdf
[Vircom]: https://www.waveshare.com/wiki/File:VirCom_en.rar

[stride MQTT gateway]: .
[MQTT/Modbus gateway]: https://www.automationdirect.com/adc/overview/catalog/communications/industrial_iot_solutions/mqtt_gateways?gad_source=1&gclid=Cj0KCQjwv7O0BhDwARIsAC0sjWOFsqDI15TGkvbkFKIGhMCeQjELYF7IWXI_HFQ4OxPRbsqn6WhabsIaAhK4EALw_wcB#bodycontentppc
[Stride MQTT/Modbus gateway]: https://www.automationdirect.com/adc/overview/catalog/communications/industrial_iot_solutions/mqtt_gateways?gad_source=1&gclid=Cj0KCQjwv7O0BhDwARIsAC0sjWOFsqDI15TGkvbkFKIGhMCeQjELYF7IWXI_HFQ4OxPRbsqn6WhabsIaAhK4EALw_wcB#bodycontentppc
[Stride MQTT/Modbus gateway user manual]: https://cdn.automationdirect.com/static/manuals/mqttgateway/sgwmq1611userm.pdf

[Node-Red stuff]: . 
[Node-Red]: https://nodered.org/
[NodeJs]: https://nodejs.org/en
[Node-Red getting started]: https://nodered.org/docs/getting-started/local
[node-red-contrib-modbus]: https://flows.nodered.org/node/node-red-contrib-modbus

[gateways]: .
[Hubitat Trend]: https://trends.google.com/trends/explore?date=all&geo=US&q=hubitat&hl=en-US
[Home Assistant Trend]: https://trends.google.com/trends/explore?date=all&geo=US&q=%2Fg%2F11fzxlb_q4&hl=en-US

