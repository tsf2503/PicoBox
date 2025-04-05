import toml

with open("modes.toml", "r") as f:
    config = toml.load(f)

mode = 0

def ClickButton(button):
    print(f"Click Button; {button}")
    
def PressButton(button):
    print(f"Press Button; {button}")

def ReleaseButton(button):
    print(f"Release Button; {button}")


def modeSelec(button):
    index = str(abs(button))

    if isinstance(config[str(mode)][index], list) and config[str(mode)][index][0] == "gamepad":
        gpButton = int(config[str(mode)][index][1])
        print("gamepad:", gpButton)
        if config[str(mode)][index][2] == "TOGGLE":
            ClickButton(gpButton)

        elif config[str(mode)][index][2] == "SWITCH":
            if button > 0:
                PressButton(gpButton)
            else:
                ReleaseButton(gpButton)


    elif isinstance(config[str(mode)][index], list) and config[str(mode)][index][0] == "key":
        for code in config[str(mode)][index][1:]:
            print(code) 
        # Extract keycodes from the list
        # keycodes = [getattr(Keycode, code.upper()) for code in config[str(mode)][index][1:]]
        # Send the keycodes
        # print(f"Sending: {keycodes}")  # Debugging output
        # keyboard.send(keycodes)

    elif isinstance(config[str(mode)][index], list) and config[str(mode)][index][0] == "string":
        # layout.write(config[str(mode)][index][1])
        print(config[str(mode)][index][1])

while True:
    button = input("Enter Button: ")
    if int(button) == 0:
        mode = int(input("Enter mode: "))
        continue
    modeSelec(int(button))