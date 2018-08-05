from time import sleep
from approxeng.input.selectbinder import ControllerResource

import sys
sys.path.append('../pytello/')
import tello


# Constants
RC_VAL_MIN = 364
RC_VAL_MID = 1024
RC_VAL_MAX = 1684

IDX_ROLL = 0
IDX_PITCH = 1
IDX_THR = 2
IDX_YAW = 3

# Global vars
mRCVal = [1024, 1024, 1024, 1024]
mDrone = None

def axis_to_drone(axis):
    if (axis == 0):
        return RC_VAL_MID

    drone_value = RC_VAL_MID
    if axis < 0.0:
        drone_value = RC_VAL_MID - (abs(axis) * (RC_VAL_MID - RC_VAL_MIN))
    else:
        drone_value = RC_VAL_MID + (axis * (RC_VAL_MAX - RC_VAL_MID))

    return drone_value


while True:
    print("Looking for controller")
    try:
        with ControllerResource(dead_zone=0.1, hot_zone=0.2) as joystick:
            while joystick.connected:

                # tested each loop, if drone isnt here then create.
                if mDrone is None:
                    mDrone = tello.Tello()

                if mDrone is not None:
                    # Grab left and right stick axis positions.
                    lx, ly, rx, ry = joystick['lx', 'ly', 'rx', 'ry']

                    # Convert stick axis to drone Roll, pitch, thrust and yaw
                    mRCVal[IDX_YAW] = axis_to_drone(lx)
                    mRCVal[IDX_THR] = axis_to_drone(ly)

                    mRCVal[IDX_ROLL] = axis_to_drone(rx)
                    mRCVal[IDX_PITCH] = axis_to_drone(ry)

                    # Check whether any buttons have been pressed since before.
                    joystick.check_presses()
                    if joystick.has_presses:
                        print(joystick.presses)

                        # DPad buttons
                        if 'dup' in joystick.presses:
                            pass
                        if 'ddown' in joystick.presses:
                            pass
                        if 'dleft' in joystick.presses:
                            pass
                        if 'dright' in joystick.presses:
                            pass

                        # Middle Buttons
                        if 'start' in joystick.presses:
                            pass
                        if 'home' in joystick.presses:
                            pass

                        # Trigger buttons
                        if 'l1' in joystick.presses:
                            mDrone.land()
                        if 'l2' in joystick.presses:
                            pass

                        if 'r1' in joystick.presses:
                            mDrone.takeOff()
                        if 'r2' in joystick.presses:
                            pass

                        # Shape Buttons
                        if 'triangle' in joystick.presses:
                            pass
                        if 'cross' in joystick.presses:
                            pass
                        if 'square' in joystick.presses:
                            pass
                        if 'circle' in joystick.presses:
                            pass

                    # Send stick positions to drone
                    mDrone.setStickData(
                        0,
                        mRCVal[IDX_ROLL],
                        mRCVal[IDX_PITCH],
                        mRCVal[IDX_THR],
                        mRCVal[IDX_YAW]
                    )
            sleep(0.05)
    except IOError:
        mDrone.stop()
        sleep(1)
