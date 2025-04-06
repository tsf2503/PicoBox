import digitalio
import rotaryio

"""
Represents a button matrix for handling button presses and mode switching.
"""
class ButtonMatrix:
    """
    Initializes the ButtonMatrix object.

    Args:
        col_pins (list): List of pins for the matrix columns.
        row_pins (list): List of pins for the matrix rows.
        MODE (int): The button number for the mode switcher.

    Side Effects:
        - Configures pins as input or output.
        - Initializes internal state for button tracking.
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
    Checks the button matrix for changes in button states.

    Returns:
        int: The button number for a pressed button (positive for press, negative for release).

    Side Effects:
        - Updates the `switch_status` list.
        - Prints debug information about button state changes.
    """
    def check(self):
        for col_num, col in enumerate(self.cols):
            col.value = 1  # Activate the column
            for row_num, row in enumerate(self.rows):
                index = row_num * 6 + col_num
                value = row.value

                if value == self.switch_status[index]:
                    continue
                self.switch_status[index] = value

                # Calculate the button number
                if col_num == 5:
                    button_num = 36 + row_num
                else:
                    button_num = row_num * 5 + col_num + 1

                # On press, return the button number
                col.value = 0
                if value == 1:
                    return button_num
                # On release, return the negative button number
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
        - Initializes internal state for encoder tracking.
    """
    def __init__(self, encoder_pins):
        self.encoders = []

        for pin_a, pin_b in encoder_pins:
            self.encoders.append(rotaryio.IncrementalEncoder(pin_a, pin_b))
        
        self.last = []
        for enc in self.encoders:
            self.last.append(enc.position)

    """
    Checks the encoders for rotation.

    Returns:
        int: The button number for clockwise or counterclockwise rotation.

    Side Effects:
        - Updates the internal state of the encoder.
    """
    def check(self):
        for i, enc in enumerate(self.encoders):
            current = enc.position
            diff = current - self.last[i]
            if diff > 0:
                # Clockwise rotation
                self.last[i] = current
                return 26 + 2 * i
            elif diff < 0:
                # Counterclockwise rotation
                self.last[i] = current
                return 27 + 2 * i