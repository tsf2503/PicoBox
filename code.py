import board
import digitalio
import usb_hid
import time
from tomli._parser import load as toml_load

from matrix import ButtonMatrix, Encoders

from hid_gamepad import Gamepad

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

kb = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kb)

gp = Gamepad(usb_hid.devices)

with open("modes.toml", "rb") as f:
    config = toml_load(f)

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

# Turn on the BLUE light for mode 0 and off for all others
indicator_led[0].value = 1
indicator_led[1].value = 1
indicator_led[2].value = 0


# Matrix pins
col_pins = (board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5)
row_pins = (board.GP6,board.GP7, board.GP8, board.GP9, board.GP10)

matrix = ButtonMatrix(col_pins, row_pins, MODE)


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
        if button == -MODE:
            ModeColorSelect(mode)
            print("return "+ str(mode))
            return
        elif 11 <= button <= 13:
            mode = button - 11
            ModeColorSelect(mode)
            print("mode info:", button, button - 10, mode)
            return
        elif button == 16:
            kb.release_all()
            gp.release_all_buttons()
            print("release all")


# Short press on mode button switches to next mode
def ModePress():
    global mode
    mode += 1

    if mode == 3:
        mode = 0

    ModeColorSelect(mode)

def Selec(button):
    index = str(abs(button))

    if isinstance(config[str(mode)][index], list) and config[str(mode)][index][1] == "GAMEPAD":
        gpButton = int(config[str(mode)][index][2])
        
        # Click Button
        if config[str(mode)][index][0] == "TOGGLE":
            print("Click:", gpButton)
            gp.click_buttons(gpButton)

        # Press/Release Button   
        elif config[str(mode)][index][0] == "PUSH":
            if button > 0:
                print("Press:", gpButton)
                gp.press_buttons(gpButton)
            else:
                print("Release:", gpButton)
                gp.release_buttons(gpButton)


    elif isinstance(config[str(mode)][index], list) and config[str(mode)][index][1] == "KEY":
        # Extract keycodes from the list
        keycodes = [getattr(Keycode, code.upper()) for code in config[str(mode)][index][2:]]

        # Send the keycodes
        if config[str(mode)][index][0] == "TOGGLE":
            # Only sends on press
            if button > 0:
                print(f"Sending: {keycodes}")
                kb.send(*keycodes)
    
        elif config[str(mode)][index][0] == "PUSH":
            if button > 0:
                print("Press:", keycodes)
                kb.press(keycodes)
            else:
                print("Release:", gpButton)
                kb.release(keycodes)

    elif isinstance(config[str(mode)][index], list) and config[str(mode)][index][1] == "STRING":
        # Only writes on press regardless of mode
        if button > 0:
            print("wrote", config[str(mode)][index][2])
            layout.write(config[str(mode)][index][2])



while True:
    press = matrix.check()
    if press is not None:
        # Mode button was pressed
        if press == MODE:
            start = time.monotonic()
        # Mode button was released
        elif press == -MODE: 
            end = time.monotonic()
            #short press
            print(end-start)
            if (end - start) < 0.5:
                ModePress()
            else:
                ModeLongPress()
                start = 0
        else:
            Selec(press)


    # enc = encoders.check()
    # while enc is not None:
    #     print(enc)
    #     Selec(enc)
    #     enc = encoders.check()
