import pigpio
from lego_rc import LEGO_RC
import time

pi = pigpio.pi()

if not pi.connected:
   exit(0)

IR_EMITTER_PIN = 12
SENSOR_EAST_PIN = 23
SENSOR_WEST_PIN = 25
SERVO_PIN = 16
CARGO_TRAIN_CHANNEL = 0
EXPRESS_TRAIN_CHANNEL = 3

pi.set_pull_up_down(SENSOR_WEST_PIN, pigpio.PUD_UP)
pi.set_mode(SENSOR_WEST_PIN, pigpio.INPUT)

pi.set_pull_up_down(SENSOR_EAST_PIN, pigpio.PUD_UP)
pi.set_mode(SENSOR_EAST_PIN, pigpio.INPUT)

rc = LEGO_RC(pi, IR_EMITTER_PIN)

def run_trains():
   loop_started = time.time()
   print('loop_started:', loop_started)
   express_train_braked_westbound = None
   express_train_arrived_westbound = None
   express_train_departed_westbound = None
   express_train_braked_far_west = None
   express_train_arrived_far_west = None
   switched_for_eastbound = None
   express_train_departed_far_west = None
   express_train_braked_eastbound = None
   express_train_arrived_eastbound = None
   switched_for_cargo = None
   express_train_departed_eastbound = None
   express_train_braked_far_east = None
   express_train_arrived_far_east = None
   loop_ended = None

   # the express train starts before the east sensor, driving westbound fast
   rc.drive(EXPRESS_TRAIN_CHANNEL, 8 | 1)

   while True:
       # made a boo-boo and wired SENSOR_EAST_PIN to emit one when obscured?! Opposite SENSOR_WEST_PIN
       if True and pi.read(SENSOR_EAST_PIN) == 1 and not express_train_braked_westbound:
           # brake westbound
           rc.drive(EXPRESS_TRAIN_CHANNEL, 8 | 6)
           express_train_braked_westbound = time.time()
           print('express_train_braked_westbound:', express_train_braked_westbound)
       elif True and time.time() - loop_started > 5 and not express_train_braked_westbound:
           raise RuntimeException("Failed to detect the express train at SENSOR_EAST_PIN within the expected time")

       if express_train_braked_westbound and time.time() - express_train_braked_westbound > 6 and not express_train_arrived_westbound:
           # stop at city westbound
           rc.drive(EXPRESS_TRAIN_CHANNEL, 8)
           express_train_arrived_westbound = time.time()
           print('express_train_arrived_westbound:', express_train_arrived_westbound)

       if express_train_arrived_westbound and time.time() - express_train_arrived_westbound > 4 and not express_train_departed_westbound:
           # depart from city westbound
           rc.drive(EXPRESS_TRAIN_CHANNEL, 8 | 1)
           express_train_departed_westbound = time.time()
           print('express_train_departed_westbound:', express_train_departed_westbound)

       if express_train_departed_westbound and time.time() - express_train_departed_westbound > 3 and not express_train_braked_far_west:
           # brake far west
           rc.drive(EXPRESS_TRAIN_CHANNEL, 8 | 6)
           express_train_braked_far_west = time.time()
           print('express_train_braked_far_west:', express_train_braked_far_west)

       if express_train_braked_far_west and time.time() - express_train_braked_far_west > 1 and not express_train_arrived_far_west:
           # stop at platform far west
           rc.drive(EXPRESS_TRAIN_CHANNEL, 8)
           express_train_arrived_far_west = time.time()
           print('express_train_arrived_far_west:', express_train_arrived_far_west)

       if express_train_arrived_far_west and time.time() - express_train_arrived_far_west > 2 and not switched_for_eastbound:
           # switch the points for the express train to end up on the eastbound track
           pi.set_servo_pulsewidth(SERVO_PIN, 2000)
           time.sleep(.3)
           pi.set_servo_pulsewidth(SERVO_PIN, 0)
           switched_for_eastbound = time.time()
           print('switched_for_eastbound:', switched_for_eastbound)

       if switched_for_eastbound and time.time() - switched_for_eastbound > 2 and not express_train_departed_far_west:
           # depart from far west eastbound
           rc.drive(EXPRESS_TRAIN_CHANNEL, 7)
           express_train_departed_far_west = time.time()
           print('express_train_departed_far_west:', express_train_departed_far_west)

       if express_train_departed_far_west and pi.read(SENSOR_WEST_PIN) == 0 and not express_train_braked_eastbound:
           # brake eastbound
           # rc.drive(EXPRESS_TRAIN_CHANNEL, 1)
           rc.drive(EXPRESS_TRAIN_CHANNEL, 2)
           express_train_braked_eastbound = time.time()
           print('express_train_braked_eastbound:', express_train_braked_eastbound)
       elif express_train_departed_far_west and time.time() - express_train_departed_far_west > 5 and not express_train_braked_eastbound:
           raise RuntimeException("Failed to detect the express train at SENSOR_WEST_PIN within the expected time")

       if express_train_braked_eastbound and time.time() - express_train_braked_eastbound > 2.5 and not express_train_arrived_eastbound:
           # stop at city eastbound
           rc.drive(EXPRESS_TRAIN_CHANNEL, 8)
           express_train_arrived_eastbound = time.time()
           print('express_train_arrived_eastbound:', express_train_arrived_eastbound)

       if express_train_arrived_eastbound and time.time() - express_train_arrived_eastbound > 2 and not switched_for_cargo:
           # switch the points for the cargo train to end up on its own track
           pi.set_servo_pulsewidth(SERVO_PIN, 1000)
           time.sleep(.3)
           pi.set_servo_pulsewidth(SERVO_PIN, 0)
           switched_for_cargo = time.time()
           print('switched_for_cargo:', switched_for_cargo)

       if express_train_arrived_eastbound and time.time() - express_train_arrived_eastbound > 4 and not express_train_departed_eastbound:
           # depart from city eastbound
           rc.drive(EXPRESS_TRAIN_CHANNEL, 7)
           express_train_departed_eastbound = time.time()
           print('express_train_departed_eastbound:', express_train_departed_eastbound)

       if express_train_departed_eastbound and time.time() - express_train_departed_eastbound > 3 and not express_train_braked_far_east:
           # brake far east
           rc.drive(EXPRESS_TRAIN_CHANNEL, 2)
           express_train_braked_far_east = time.time()
           print('express_train_braked_far_east:', express_train_braked_far_east)

       if express_train_braked_far_east and time.time() - express_train_braked_far_east > 1 and not express_train_arrived_far_east:
           # stop at platform far east
           rc.drive(EXPRESS_TRAIN_CHANNEL, 8)
           express_train_arrived_far_east = time.time()
           print('express_train_arrived_far_east:', express_train_arrived_far_east)

       if express_train_arrived_far_east and time.time() - express_train_arrived_far_east > 4 and not loop_ended:
           loop_ended = time.time()
           print('loop_ended:', loop_ended)
           break

       time.sleep(.01)

try:
   while True:
       run_trains()
finally:
   # shut down all the things
   print('shutting down all the things', flush=True)
   pi.set_servo_pulsewidth(SERVO_PIN, 0)
   rc.drive(CARGO_TRAIN_CHANNEL, 8)
   rc.drive(EXPRESS_TRAIN_CHANNEL, 8)
