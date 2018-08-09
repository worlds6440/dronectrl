from time import sleep
from approxeng.input.selectbinder import ControllerResource
# from omxplayer.player import OMXPlayer

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
mPlayer = None
mAllowControl = True
mFoundController = False


def axis_to_drone(axis):
    if (axis == 0):
        return RC_VAL_MID

    # Interpolate new value and ensure its an INT
    drone_value = RC_VAL_MID
    if axis < 0.0:
        drone_value = int(RC_VAL_MID - (abs(axis) * (RC_VAL_MID - RC_VAL_MIN)))
    else:
        drone_value = int(RC_VAL_MID + (axis * (RC_VAL_MAX - RC_VAL_MID)))

    # Cap value to min/max range
    if drone_value < RC_VAL_MIN:
        drone_value = RC_VAL_MIN
    if drone_value > RC_VAL_MAX:
        drone_value = RC_VAL_MAX

    return drone_value

running = True
while running:
    print("Looking for controller")
    try:
        with ControllerResource(dead_zone=0.1, hot_zone=0.2) as joystick:
            while joystick.connected and running:
                mFoundController = True

                # tested each loop, if drone isnt here then create.
                if mDrone is None:
                    mDrone = tello.Tello()
                    # mPlayer = OMXPlayer(VIDEO_PATH)

                # Grab left and right stick axis positions.
                lx, ly, rx, ry = joystick['lx', 'ly', 'rx', 'ry']

                # Convert stick axis to drone Roll, pitch, thrust and yaw
                mRCVal[IDX_YAW] = axis_to_drone(lx)
                mRCVal[IDX_THR] = axis_to_drone(ly)

                mRCVal[IDX_ROLL] = axis_to_drone(rx)
                mRCVal[IDX_PITCH] = axis_to_drone(ry)

                # print(
                #     ("Y:{}  T:{}  R:{}  P:{}").format(
                #         mRCVal[IDX_YAW],
                #         mRCVal[IDX_THR],
                #         mRCVal[IDX_ROLL],
                #         mRCVal[IDX_PITCH])
                # )

                # Check whether any buttons have been pressed since before.
                joystick.check_presses()
                if joystick.has_presses:
                    print(joystick.presses)

                    # DPad buttons
                    if 'dup' in joystick.presses:
                        if mDrone is not None and mAllowControl:
                            mDrone.flipForward()
                    if 'ddown' in joystick.presses:
                        if mDrone is not None and mAllowControl:
                            mDrone.flipBackward()
                    if 'dleft' in joystick.presses:
                        if mDrone is not None and mAllowControl:
                            mDrone.flipLeft()
                    if 'dright' in joystick.presses:
                        if mDrone is not None and mAllowControl:
                            mDrone.flipRight()

                    # Middle Buttons
                    if 'start' in joystick.presses:
                        pass
                    if 'home' in joystick.presses:
                        running = False
                        if mDrone is not None and mAllowControl:
                            mDrone.land()

                    # Trigger buttons
                    if 'l1' in joystick.presses:
                        print("Landing")
                        if mDrone is not None and mAllowControl:
                            mDrone.land()
                    if 'l2' in joystick.presses:
                        pass

                    if 'r1' in joystick.presses:
                        print("Takeoff")
                        if mDrone is not None and mAllowControl:
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
                if mDrone is not None and mAllowControl:
                    mDrone.setStickData(
                        0,
                        mRCVal[IDX_ROLL],
                        mRCVal[IDX_PITCH],
                        mRCVal[IDX_THR],
                        mRCVal[IDX_YAW]
                    )
                # Timeout between controlled loop
                sleep(0.1)
            # Timeout between not connected to controller
            sleep(1.0)
    except IOError:
        # Controller not found, wait and re-try
        # Ensure drone is grounded if controller has gone out of range.
        if mFoundController:
            print("Error, controller out of range")
        if mDrone is not None:
            mDrone.land()
        sleep(1)

# Ensure drone is grounded when we stop playing
if mDrone is not None:
    print("Landing and Stopping")
    mDrone.land()
    mDrone.stop()
