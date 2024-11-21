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
mode = 0

# Mode indicator leds 
indicator_led_pins = (board.GP26, board.GP22, board.GP21)

indicator_led = []
for pin in indicator_led_pins:
    led = digitalio.DigitalInOut(pin)
    led.direction = digitalio.Direction.OUTPUT
    indicator_led.append(led)

# Turn on the Red light for mode 0 and off for all others
indicator_led[0].value = 0
indicator_led[1].value = 1
indicator_led[2].value = 1


# Matrix pins 
col_pins = (board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5) 
row_pins = (board.GP8, board.GP9, board.GP10)
switch_col_pins = [0, 1, 2, 3, 4, 5]
switch_row_pins = (board.GP6,board.GP7)

matrix = ButtonMatrix(col_pins, row_pins, switch_col_pins, switch_row_pins, MODE)

# Switches the mode button color to input 
def ModeColorSelect(color):
    global indicator_led

    indicator_led[color - 2].value = 1
    indicator_led[color - 1].value = 1
    indicator_led[color].value = 0


# Long press on mode button enters selector mode checks the button pressed to select mode
def ModeLongPress():
    global mode
    
    print("chose mode")
    
    start = time.monotonic() 
    color = mode
    while True:
        print(start-time.monotonic())
        if time.monotonic() - start > 1.5:
            color += 1
            if color == 3: color = 0
            ModeColorSelect(color)
            start = time.monotonic()
        
        button = matrix.check()
        if button is None: continue
        if button == -1:
            ModeColorSelect(mode)
            print("return "+ str(mode))
            return
        elif 11 <= button <= 13:
            mode = button - 11
            ModeColorSelect(mode)
            print(button, button - 10, mode)
            return


# Short press on mode button switches to next mode 
def ModePress():
    global mode
    mode += 1 

    if mode == 3:
        mode = 0
    
    ModeColorSelect(mode)
    
    
while True:

    matrix.SwitchCheck()
    button = matrix.check()

    if button is not None:
        if button == -1: ModePress()
        elif button == -2: ModeLongPress()
        
        print("mode:" + str(mode))
