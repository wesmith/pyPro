from adafruit_servokit import ServoKit
import time
myKit = ServoKit(channels=16)
pan  = myKit.servo[0]  # WS mod
tilt = myKit.servo[1]  # WS mod

# WS note: when commanded to move from 0 to 180, the servos actually seem to go from 0 to 120 deg

delta = 0.01

#for k in [30, 60, 90, 120, 150, 180]:  # WS mod
k = 180
tilt.angle = 0

for j in range(5):

    # box the scene
    for i in range(0, k, 1):
        pan.angle  = i
        time.sleep(delta)
    for i in range(0, k, 1):
        tilt.angle = i
        time.sleep(delta)
    for i in range(k, 0, -1):
        pan.angle  = i
        time.sleep(delta)
    for i in range(k, 0, -1):
        tilt.angle = i
        time.sleep(delta)

# set back to center at 90 deg before leaving
pan.angle  = 90
tilt.angle = 90
        

