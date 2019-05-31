# pi-train-controller

Automated remote control of a LEGO model railway, based on Raspberry Pi Zero W.

Documentation of the protocol used by the LEGO Power Functions infrared remote control can be found [here](https://github.com/jurriaan/Arduino-PowerFunctions/blob/master/LEGO_Power_Functions_RC_v120.pdf).

Following the awesome advice in [Brian Schwind's blog](https://blog.bschwind.com/2016/05/29/sending-infrared-commands-from-a-raspberry-pi-without-lirc/), I disregarded lirc and went for the [pigpio](https://github.com/joan2937/pigpio) library, which worked like a charm. Install it and configure `pigpiod` to run on boot:

	pi@raspberrypi:~ $ sudo apt install python3-pigpio
	pi@raspberrypi:~ $ sudo systemctl enable pigpiod
	pi@raspberrypi:~ $ sudo systemctl start pigpiod

Hardware used:
- [Raspberry Pi Zero W](https://www.electrokit.com/produkt/raspberry-pi-zero-w-board/)
- Micro SD card 2 GB (running Raspbian Stretch Lite image)
- Micro USB charger (could try a small USB powerbank instead)
- [Infrared transmitter module](https://www.electrokit.com/produkt/ir-sandare-38khz/) (any 5mm IR LED should work)
- some wiggly wires
