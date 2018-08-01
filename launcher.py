from time import sleep
from approxeng.input.selectbinder import ControllerResource

while True:
    print("Looking for controller")
    try:
        with ControllerResource(dead_zone=0.1, hot_zone=0.2) as joystick:
            while joystick.connected:
                x_axis, y_axis = joystick['lx', 'ly']
                print("{} : {}".format(x_axis, y_axis))
                joystick.check_presses()
                if joystick.has_presses:
                    print(joystick.presses)
            sleep(0.05)
    except IOError:
        sleep(1)
