import board
import digitalio
import usb_hid
import time

from hid_gamepad import Gamepad

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.consumer_control import ConsumerControl

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

mediacontrol = ConsumerControl(usb_hid.devices)

# gp = Gamepad(usb_hid.devices)

#Define the Modificador button
MODE = 20

#Define the current mode 
global mode
mode = 0
# Matrix pins 
col_pins = (board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5) 
row_pins = (board.GP6, board.GP7, board.GP8, board.GP9, board.GP10)

# Initialize the buttons 
col_buttons = [digitalio.DigitalInOut(pin) for pin in col_pins]
row_buttons = [digitalio.DigitalInOut(pin) for pin in row_pins]

for col in col_buttons:
    col.direction = digitalio.Direction.OUTPUT

for row in row_buttons:
    row.direction = digitalio.Direction.INPUT
    row.pull = digitalio.Pull.DOWN

def PressButton(button):
    print(f"Press Button; {button}")
    
def ModeLongPress(): 
    print("Long Press")

def ModePress():
    if mode == 3:
        mode = 1
        return
    mode += 1 

    print("Press")

while True:
    #Check the button matrix
    for col_num, col in enumerate(col_buttons):
        col.value = 1
        # print(f"col: {col_num}")

        for row_num, row in enumerate(row_buttons):
            # print(f"    row: {row_num}")
            if row.value == 1:
                button_num = row_num * 5 + col_num + 1

                if button_num == MODE:
                    press_start = time.time()
                    while row.value == 1: nop = 0
                    press_end = time.time()
                    if press_end - press_start > 1:
                        ModeLongPress()
                        continue
                    ModePress()
                    continue

                PressButton(button_num)
                # print(f"        col: {col_num}, row: {row_num}, buttons: {row_num * 5 + col_num + 1}")
                time.sleep(0.5)
        col.value = 0