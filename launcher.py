from time import sleep
from approxeng.input.selectbinder import ControllerResource

import sys
sys.path.append('../pytello/')
import tello

while True:
    print("Looking for controller")
    drone = None
    try:
        with ControllerResource(dead_zone=0.1, hot_zone=0.2) as joystick:
            while joystick.connected:

                # tested each loop, if drone isnt here then create.
                if drone is None:
                    drone = tello.Tello()

                if drone is not None:
                    # Grab left and right stick axis positions.
                    lx, ly, rx, ry = joystick['lx', 'ly', 'rx', 'ry']

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
                            pass
                        if 'l2' in joystick.presses:
                            pass
                        if 'r1' in joystick.presses:
                            pass
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
            sleep(0.05)
    except IOError:
        sleep(1)
