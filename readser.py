from serial import rs485
import rich

with rs485.RS485('/dev/tty.usbserial-B001K6G3') as ser:
    rich.print(ser)
    i = 1
    while True:
        data = ser.read(1)
        print(f"{data[0]:02X}", end="", flush=True)
        if i % 16 == 0:
            print()
        elif i % 4 == 0:
            print("  ", end="", flush=True)
        i += 1