import board
import digitalio
import usb_hid
from hid_gamepad import Gamepad


gp = Gamepad(usb_hid.devices)

push_button = digitalio.DigitalInOut(board.GP11)
push_button.switch_to_input(pull=digitalio.Pull.UP)

encoder_A = digitalio.DigitalInOut(board.GP20)
encoder_A.switch_to_input(pull=digitalio.Pull.UP)

encoder_B = digitalio.DigitalInOut(board.GP21)
encoder_B.switch_to_input(pull=digitalio.Pull.UP)

counter = 0
last_press = 0
previous_state = encoder_A.value

while True:

    current_state = encoder_A.value
    if previous_state != current_state & current_state == 1:
        # moved
        if current_state != encoder_B.value:
            gp.click_buttons(2)
        else:
            gp.click_buttons(3)
        print(counter)
    previous_state = current_state

    press = push_button.value
    if press != last_press:
        if not(press):
            gp.press_buttons(1)
            last_press = press
        else:
            gp.release_buttons(1) 
            last_press = press