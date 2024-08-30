import board
import digitalio
import usb_hid
from hid_gamepad import Gamepad
import time


gp = Gamepad(usb_hid.devices)

push_button = digitalio.DigitalInOut(board.GP16)
push_button.switch_to_input(pull=digitalio.Pull.UP)

encoder_A = digitalio.DigitalInOut(board.GP20)
encoder_A.switch_to_input(pull=digitalio.Pull.UP)

encoder_B = digitalio.DigitalInOut(board.GP21)
encoder_B.switch_to_input(pull=digitalio.Pull.UP)

counter = 0
last_press = 0
previous_state = encoder_A.value

while True:

    press = push_button.value
    if last_press != press:
        if not(press):
            last_press = press
        else:
            last_press = press
    print (press)
    time.sleep(0.2)