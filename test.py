import pigpio
from time import sleep

class lego_remote:
    """ Implements the protocol documented in LEGO Power Functions RC 1.20. """
    # https://github.com/iConor/lego-lirc/blob/master/docs/LEGO_Power_Functions_RC_v120.pdf

    def _init_waves(self, pi, gpio_pin):
        pi.wave_clear()

        def _gen_pulses(total_length_us):
            # Length of a 38 kHz cycle ~= 26.316 us.
            # Round the mark pulse lengths to 13 us and pad with accurate pause length in the end. Hope it works.
            for i in range(6):
                yield pigpio.pulse(1 << gpio_pin, 0, 13)
                yield pigpio.pulse(0, 1 << gpio_pin, 13 if i < 5 else total_length_us - (13 * 11))

        pi.wave_add_generic(list(_gen_pulses(421)))
        self._low_bit = pi.wave_create()

        pi.wave_add_generic(list(_gen_pulses(711)))
        self._high_bit = pi.wave_create()

        pi.wave_add_generic(list(_gen_pulses(1184)))
        self._start_bit = pi.wave_create()

        self._stop_bit = self._start_bit  # also 1184 us

    def __init__(self, pi, gpio_pin):
        self._pi = pi
        self._gpio_pin = gpio_pin
        self._init_waves(self._pi, self._gpio_pin)

    def _send(self, nibble1, nibble2, nibble3):
        self._pi.set_mode(self._gpio_pin, pigpio.OUTPUT)

        def _gen_waves(nibble):
            for i in range(3, -1, -1):
                yield self._high_bit if nibble & (1 << i) else self._low_bit

        lrc = 0xF ^ nibble1 ^ nibble2 ^ nibble3

        chain = ([self._start_bit] +
            list(_gen_waves(nibble1)) +
            list(_gen_waves(nibble2)) +
            list(_gen_waves(nibble3)) +
            list(_gen_waves(lrc)) +
            [self._stop_bit])
        print('wave_chain(' + repr(chain) + '):', repr(self._pi.wave_chain(chain)))

        print('Sending', end='...')
        while self._pi.wave_tx_busy():
            sleep(.1)
        print(' done')

    def drive(self, channel, speed):
        """ Combo PWM mode """
        self._send(0b0100 | channel, speed, speed)


pi = pigpio.pi()

if not pi.connected:
   exit(0)

##r = lego_remote(pi, 3)
##r.drive(0, 5)  # forward
##sleep(2)
##r.drive(0, 8)  # brake then float
##sleep(2)
##r.drive(0, 8 | 5)  # backward
##sleep(2)
##r.drive(0, 8)  # brake then float

##IR_GPIO = 12
##r = lego_remote(pi, IR_GPIO)
##while True:
##    r.drive(3, 4)  # forward
##    sleep(1)
##    r.drive(3, 8)  # brake then float
##    sleep(1)

pi.set_pull_up_down(23, pigpio.PUD_UP)
pi.set_mode(23, pigpio.INPUT)

pi.set_pull_up_down(25, pigpio.PUD_UP)
pi.set_mode(25, pigpio.INPUT)

bits_23 = ''
bits_25 = ''
while True:
   bits_23 += str(pi.read(23))
   bits_25 += str(pi.read(25))
   if len(bits_23) == 10:
       print(bits_23 + '  ' + bits_25, flush=True)
       bits_23 = ''
       bits_25 = ''
   sleep(.1)

# for i in range(2):
#     # pi.set_servo_pulsewidth(16, 2500) # clockwise
#     # sleep(.5)
#     # pi.set_servo_pulsewidth(16, 0)
#     # sleep(.5)
#
#     # pi.set_servo_pulsewidth(16, 1500) # center
#     # sleep(.5)
#     # pi.set_servo_pulsewidth(16, 0)
#     # sleep(.5)
#
#     # pi.set_servo_pulsewidth(16, 800) # safe anti-clockwise
#     # sleep(.5)
#     # pi.set_servo_pulsewidth(16, 0)
#     # sleep(.5)
#
#     pi.set_servo_pulsewidth(16, 2000)
#     sleep(.3)
#     pi.set_servo_pulsewidth(16, 0)
#     sleep(1)
#
#     pi.set_servo_pulsewidth(16, 1000)
#     sleep(.3)  # this side is harder due to axis misalignment
#     pi.set_servo_pulsewidth(16, 0)
#     sleep(1)
