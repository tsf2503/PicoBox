import board
import digitalio
import usb_hid
import time

"""
Represents a button matrix for handling button presses and mode switching.
"""
class ButtonMatrix:

    """
    Initializes the ButtonMatrix object.

    Args:
        col_pins (list): List of pins for the matrix columns.
        row_pins (list): List of pins for the matrix rows.
        switch_col_pins (list): List of column pins for switches.
        switch_row_pins (list): List of row pins for switches.
        MODE (int): The button number for the mode switcher.

    Side Effects:
        - Configures pins as input or output.
        - Initializes internal state for button and switch tracking.
    """
    def __init__(self, col_pins, row_pins, switch_col_pins, switch_row_pins, MODE):
        # Initialize the buttons
        self.cols = [digitalio.DigitalInOut(pin) for pin in col_pins]
        self.rows = [digitalio.DigitalInOut(pin) for pin in row_pins]

        # Initialize the rows for switches
        self.switch_rows = [digitalio.DigitalInOut(pin) for pin in switch_row_pins]

        # List to hold switch columns (filled in column set loop)
        self.switch_cols = []
        # List holds the status of each switch
        self.switch_status = [0] * len(switch_col_pins) * len(switch_row_pins)

        # Set columns as output
        for i, col in enumerate(self.cols):
            col.direction = digitalio.Direction.OUTPUT
            # Checks if the current column has switches; if so, copies the column to the switch list
            if i in switch_col_pins:
                self.switch_cols.append(col)

        # Set rows as input with pull-down resistors
        for row in self.rows:
            row.direction = digitalio.Direction.INPUT
            row.pull = digitalio.Pull.DOWN
        for row in self.switch_rows:
            row.direction = digitalio.Direction.INPUT
            row.pull = digitalio.Pull.DOWN

        # Sets the mode switcher button
        self.MODE = MODE

    """
    Checks the button matrix for pressed buttons.

    Returns:
        int: The button number that was pressed.
                -1 for a short press of the mode switcher.
                -2 for a long press of the mode switcher.

    Side Effects:
        - Prints debug information about button presses.
    """
    def check(self):
        for col_num, col in enumerate(self.cols):
            col.value = 1  # Activate the column
            for row_num, row in enumerate(self.rows):
                if row.value != 1: 
                    continue

                # Calculate the button number
                if col_num == 5:
                    button_num = 38 + row_num
                else:
                    button_num = (row_num + 2) * 5 + col_num + 1

                # Check if the pressed button is the mode switcher
                if button_num == self.MODE:
                    start = time.monotonic()
                    while row.value == 1:
                        continue
                    end = time.monotonic()
                    col.value = 0
                    # Returns -1 for a short press and -2 for a long press
                    if end - start < 0.5: 
                        return -1
                    else: 
                        return -2

                time.sleep(0.2)  # Debounce delay
                col.value = 0
                return button_num
            col.value = 0

    """
    Checks the switch matrix for changes in switch states.

    Returns:
        int: The button number for a pressed switch (positive for press, negative for release).

    Side Effects:
        - Updates the `switch_status` list.
        - Prints debug information about switch state changes.
    """
    def SwitchCheck(self):
        for col_num, col in enumerate(self.switch_cols):
            col.value = 1  # Activate the column
            for row_num, row in enumerate(self.switch_rows):
                num = row_num * 6 + col_num
                if row.value == self.switch_status[num]: 
                    continue
                self.switch_status[num] = row.value

                # Calculate the button number
                if col_num == 5:
                    button_num = 36 + row_num
                else:
                    button_num = row_num * 5 + col_num + 1

                # on press return button number
                if row.value == 1:
                    return button_num
                # On release return -button number
                else:
                    return -button_num
            col.value = 0


"""
Represents rotary encoders for detecting rotation and button presses.
"""
class Encoders:

    """
    Initializes the Encoders object.

    Args:
        encoder_pins (list): List of tuples containing pins for each encoder (A and B).

    Side Effects:
        - Configures pins as input with pull-down resistors.
        - Initializes internal state for encoder tracking.
    """
    def __init__(self, encoder_pins):
        self.a = []
        self.b = []
        self.last = [0] * len(encoder_pins)

        for pin in encoder_pins:
            encoder_a = digitalio.DigitalInOut(pin[0])
            encoder_b = digitalio.DigitalInOut(pin[1])

            encoder_a.switch_to_input(pull=digitalio.Pull.DOWN)
            encoder_b.switch_to_input(pull=digitalio.Pull.DOWN)

            self.a.append(encoder_a)
            self.b.append(encoder_b)

    """
    Checks the encoders for rotation.

    Side Effects:
        - Calls `ClickButton` for clockwise or counterclockwise rotation.
        - Updates the internal state of the encoder.
    """
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