import board
import digitalio
import usb_hid
import time


class ButtonMatrix:
    
    def __init__(self, col_pins, row_pins):
        # Initialize the buttons 
        self.cols = [digitalio.DigitalInOut(pin) for pin in col_pins]
        self.rows = [digitalio.DigitalInOut(pin) for pin in row_pins]

        #Set columns as Output and rows as Input pull down
        for col in self.cols:
            col.direction = digitalio.Direction.OUTPUT
        for row in self.rows:
            row.direction = digitalio.Direction.INPUT
            row.pull = digitalio.Pull.DOWN

    def check(self):
            for col_num, col in enumerate(self.cols):
                col.value = 1
                for row_num, row in enumerate(self.rows):
                    if row.value != 1: continue

                    if col_num == 5:
                        button_num = 25 + row_num - 1
                    else:
                        button_num = row_num * 5 + col_num + 1

                    col.value = 0
                    return button_num
                col.value = 0

    def PressButton(self, button):
        print(f"Press Button; {button}")
