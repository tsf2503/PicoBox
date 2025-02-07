import board
import digitalio
import usb_hid
import time

class ButtonMatrix:
    
    def __init__(self, col_pins, row_pins, switch_col_pins, switch_row_pins, MODE):
        #Initialize the buttons 
        self.cols = [digitalio.DigitalInOut(pin) for pin in col_pins]
        self.rows = [digitalio.DigitalInOut(pin) for pin in row_pins]

        #Initialize the rows
        self.switch_rows = [digitalio.DigitalInOut(pin) for pin in switch_row_pins]

        #List to hold switch columns (filled in column set loop) 
        self.switch_cols = []
        #List holds the status of each switch
        self.switch_status = [0] * len(switch_col_pins) * len(switch_row_pins)
        
        #Set columns as Output
        for i, col in enumerate(self.cols):
            col.direction = digitalio.Direction.OUTPUT
            #checks if the current col has switches if so copies the col to the switch list
            if i in switch_col_pins:
                self.switch_cols.append(col)
        # self.switch_cols = self.cols
        #Set rows as Input pull down
        for row in self.rows:
            row.direction = digitalio.Direction.INPUT
            row.pull = digitalio.Pull.DOWN
        for row in self.switch_rows:
            row.direction = digitalio.Direction.INPUT
            row.pull = digitalio.Pull.DOWN

        # Sets the Mode switcher button
        self.MODE = MODE



    def check(self):
        for col_num, col in enumerate(self.cols):
            col.value = 1
            # print(f"col: {col_num}")
            for row_num, row in enumerate(self.rows):
                # print(f"\t row: {row_num} \t val: {row.value}")
                # time.sleep(1)
                if row.value != 1: continue

                if col_num == 5:
                    button_num = 38 + row_num 
                else:
                    button_num = (row_num + 2)* 5 + col_num + 1
     
                # Checks If the pressed button is the Mode switcher
                if button_num ==  self.MODE:
                    start = time.monotonic()
                    while row.value == 1:
                        continue
                    end = time.monotonic()
                    col.value = 0
                    # Returns -1 for a short press and -2 for a long press
                    print(end-start)
                    if end-start < 0.5: return -1
                    else: return -2
                time.sleep(0.2)
                col.value = 0
                self.ClickButton(button_num)
                return button_num
            col.value = 0


    def SwitchCheck(self):
        for col_num, col in enumerate(self.switch_cols):
            col.value = 1
            for row_num, row in enumerate(self.switch_rows):
                num = row_num * 6 + col_num
                if row.value == self.switch_status[num]: continue
                self.switch_status[num] = row.value
                if col_num == 5:
                    button_num = 36 + row_num
                else:
                    button_num = (row_num)* 5 + col_num + 1
                if row.value == 1:
                    self.PressButton(button_num)
                else:
                    self.ReleaseButton(button_num)
            col.value = 0




    def ClickButton(self, button):
        print(f"Click Button; {button}")
    
    def PressButton(self, button):
        print(f"Press Button; {button}")

    def ReleaseButton(self, button):
        print(f"Release Button; {button}")


class Encoders:

    def __init__(self, encoder_pins):
        
        self.a = []
        self.b = []
        self.last = [0] * len(encoder_pins)
        for pin in encoder_pins:
            encoder_a = digitalio.DigitalInOut(pin[0])
            encoder_b = digitalio.DigitalInOut(pin[1])

            encoder_a.switch_to_input(pull = digitalio.Pull.DOWN)
            encoder_b.switch_to_input(pull = digitalio.Pull.DOWN)

            self.a.append(encoder_a)
            self.b.append(encoder_b)

    def check(self):
        for i, (enc_a, enc_b) in enumerate(zip(self.a, self.b)):
            a_current = enc_a.value
            b_current = enc_b.value
            # Checks movement
            if self.last[i] != a_current & a_current == 1:
                # Anticlockwise 
                if a_current != b_current:
                    self.ClickButton(2 * i + 26)
                # Clockwise
                else:
                    self.ClickButton(2 * i + 27)
            self.last[i] = a_current
    

    def ClickButton(self, button):
        print(f"Click Button; {button}")
    
    def PressButton(self, button):
        print(f"Press Button; {button}")

    def ReleaseButton(self, button):
        print(f"Release Button; {button}")