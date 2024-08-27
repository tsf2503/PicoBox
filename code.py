import board
import digitalio
import usb_hid
from hid_gamepad import Gamepad


gp = Gamepad(usb_hid.devices)

class Matrix:
    def __init__(self, rows, cols):
        self.row = []
        self.col = []

        for row in rows:
            button = digitalio.DigitalInOut(row)
            button.direction = digitalio.Direction.OUTPUT
            self.row.append(button)
        for col in cols:
            button = digitalio.DigitalInOut(col)
            button.switch_to_input(pull=digitalio.Pull.DOWN)
            self.col.append(button)

    def check(self):
        last_state = 0
        for i, row in enumerate(self.row):
            row.value = True
            for j, col in enumerate(self.col):
                state = col.value 
                if state != last_state:
                    if state: gp.press_buttons(i * 4 + j + 1)
            row.value = False


row_pins = (board.GP0, board.GP1, board.GP10, board.GP11)
col_pins = (board.GP12, board.GP13, board.GP14, board.GP15)

matrix = Matrix(row_pins, col_pins)
matrix.check()