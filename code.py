import board
import digitalio
import usb_hid
import time
import toml

from matrix import ButtonMatrix, Encoders

from hid_gamepad import Gamepad

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

gp = Gamepad(usb_hid.devices)

with open("modes.toml", "r") as f:
    config = toml.load(f)

#Define the Modificador button
MODE = int(config["mode"])

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


# Encoder Pins
enc = [(board.GP11, board.GP20), (board.GP12, board.GP19), (board.GP13, board.GP18), (board.GP14, board.GP17), (board.GP15, board.GP16)]
encoders = Encoders(enc)


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

def modeSelec(button):
    index = str(abs(button))

    if isinstance(config[str(mode)][index], list) and config[str(mode)][index][0] == "gamepad":
        gpButton = int(config[str(mode)][index][1])
        print("gamepad:", gpButton)
        if config[str(mode)][index][2] == "TOGGLE":
            gp.click_buttons(gpButton)

        elif config[str(mode)][index][2] == "SWITCH":
            if button > 0:
                gp.press_buttons(gpButton)
            else:
                gp.release_buttons(gpButton)


    elif isinstance(config[str(mode)][index], list) and config[str(mode)][index][0] == "key":
        # Extract keycodes from the list
        keycodes = [getattr(Keycode, code.upper()) for code in config[str(mode)][index][1:]]
        # Send the keycodes
        print(f"Sending: {keycodes}")  # Debugging output
        keyboard.send(keycodes)

    elif isinstance(config[str(mode)][index], list) and config[str(mode)][index][0] == "string":
        layout.write(config[str(mode)][index][1])
    

while True:
    switch = matrix.SwitchCheck()
    if switch is not None:
        modeSelec(button)
    
    button = matrix.check()
    if button is not None:
        if button == -1:
            ModePress()
        elif button == -2: 
            ModeLongPress()
        else:
            modeSelec(button)


    encoders.check()
