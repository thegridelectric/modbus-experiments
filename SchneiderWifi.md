# WaveShare RS45 to WiFi

WaveShare provides a WiFi to Modbus bridge. Here are links for:

* [Purchase](https://www.waveshare.com/rs485-to-wifi-eth.htm)
* [Wiki](https://www.waveshare.com/wiki/RS485_TO_WIFI/ETH)
* [Manual](https://files.waveshare.com/upload/6/61/RS485-TO-WIFI-ETH-User-Manual-EN.pdf)

I found the manual difficult to follow, but with Tech Support's help I was able
to communicate from my computer to the Schneider Electric Meter over WiFi and
RS485 Modbus: 

## Configuring the WaveShare WiFi/Modbus device

1. Connect the antenna to the WaveShare WiFi/Modbus device.
2. Connect power to the WaveShare WiFi/Modbus device.
3. On a Mac: Mac Menu Bar / WiFi icon / Other Networks. 
4. The WaveShare device should appear as something like WaveShare_XXX, where the
   XXXX is the last four digits of the MAC address printed on the device. 
5. Connect the Mac to that network. 
6. In a brower, go to 10.10.100.254. Log in as "admin" / "admin" 
7. In "Mode Selection":
   1. Choose "STA Mode"
   2. Choose "Data Transfer Mode" / "Modbus TCP<=>Modbus RTU"
   3. Click Apply
8. In "STA Interface Setting":
   1. Click the "Search" button. 
   2. Select your home WiFi network
   3. Press "Apply"
9. In "Application Setting" / "Network A Setting" change "Port" to 502. 
10. In "Device Management" click "Restart"
11. Wait for your device to restart and connect to your home network and
    determine it's IP address. 
12. You might want to give it an address reservation in your home router so that
    it can reliably be connected to.
13. Configure `mbe` to use its IP address with: 
    ```shell
    mbe config --host IP_OF_WAVESHARE_WIFI
    ```

# Schneider Electric Meter

The terminal command `mbe mtr` provides simple interaction with the Schneider
Electric Meter. 

Verify your mbe communication configuration with: 
```shell
mbe config
``` 

See "Configuring multiple devices" in the [README](./README.md) for information
on modifying mbe configuration.

To read a selection of registers from the Schneider Electric Meter run: 
```shell
mbe mtr read-all
```

The mbe configuration defaults to using the Schneider Electric Meter at address
twelve. That configuration can be changed, for example to one, with: 

```shell
mbe config --schneider-device-id 1
```

Alternately you *might* be able to change the deivce of the meter, for
example from one to two, with: 

```
mbe mtr set-device-id --from-id 1 --to-id 2
```

However this has not been tested.

