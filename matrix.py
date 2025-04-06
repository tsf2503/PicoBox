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
    def __init__(self, col_pins, row_pins, MODE):
        # Initialize the buttons
        self.rows = [digitalio.DigitalInOut(pin) for pin in row_pins]
        self.cols = [digitalio.DigitalInOut(pin) for pin in col_pins]

        # List holds the status of each switch
        self.switch_status = [0] * (len(col_pins) * len(row_pins))

        # Set columns as output
        for col in self.cols:
            col.direction = digitalio.Direction.OUTPUT

        # Set rows as input with pull-down resistors
        for row in self.rows:
            row.direction = digitalio.Direction.INPUT
            row.pull = digitalio.Pull.DOWN

    """
    Checks the switch matrix for changes in switch states.

    Returns:
        int: The button number for a pressed switch (positive for press, negative for release).

    Side Effects:
        - Updates the `switch_status` list.
        - Prints debug information about switch state changes.
    """
    def check(self):
        for col_num, col in enumerate(self.cols):
            # print("\t Col:", col_num)
            col.value = 1  # Activate the column
            for row_num, row in enumerate(self.rows):
                index = row_num * 6 + col_num
                value = row.value
                # print(col_num, row_num, index, self.switch_status[index], row.value)
                # input("enter:")
                if value == self.switch_status[index]:
                    continue
                self.switch_status[index] = value
                print("after", col_num, row_num, index, self.switch_status[index], row.value)

                # Calculate the button number
                if col_num == 5:
                    button_num = 36 + row_num
                else:
                    button_num = row_num * 5 + col_num + 1

                # on press return button number
                col.value = 0
                if value == 1:
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
                    return(2 * i + 26)
                # Clockwise
                else:
                    return(2 * i + 27)
            self.last[i] = a_current
        return 