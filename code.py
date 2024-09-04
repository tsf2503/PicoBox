import board
import digitalio
import usb_hid
import time

from matrix import ButtonMatrix

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
mode = 1

# Matrix pins 
col_pins = (board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5) 
row_pins = (board.GP6, board.GP7, board.GP8, board.GP9, board.GP10)

matrix = ButtonMatrix(col_pins, row_pins)



    
def ModeLongPress():
    global mode
    print("chose mode")
    while True:
        button = matrix.check()
        if button is None: continue
        if button == MODE:
            return
        elif 11 <= button <= 13:
            mode = button - 10
            print(button, button - 10, mode)
            return

def ModePress():
    global mode
    
    if mode == 3:
        mode = 1
        return
    mode += 1 
    
while True:


    button = matrix.check()
    time.sleep(0.2)
    if button is not None:
        if button == MODE:
            press_start = time.monotonic()
            while button == MODE: 
                button = matrix.check()
            press_end = time.monotonic()
            if round(press_end - press_start) >= 1:
                ModeLongPress()
            else:
                ModePress()
            print(mode)
            time.sleep(0.2)
        else:
            matrix.PressButton(button)
            