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
MODE = 27

#Define the current mode 
mode = 1

# Matrix pins 
col_pins = (board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5) 
row_pins = (board.GP8, board.GP9, board.GP10)
switch_col_pins = [0, 1, 2, 3, 4, 5]
switch_row_pins = (board.GP6,board.GP7)

matrix = ButtonMatrix(col_pins, row_pins, switch_col_pins, switch_row_pins, MODE)


    
def ModeLongPress():
    global mode
    print("chose mode")
    while True:
        button = matrix.check()
        if button is None: continue
        if button == -1:
            print("return "+ str(mode))
            return
        elif 11 <= button <= 13:
            mode = button - 10
            print(button, button - 10, mode)
            return

def ModePress():
    global mode
    mode += 1 
    
    if mode == 4:
        mode = 1
    
while True:

    matrix.SwitchCheck()
    button = matrix.check()

    if button is not None:
        if button == -1: ModePress()
        elif button == -2: ModeLongPress()
        
        print("mode:" + str(mode))
