# SPDX-FileCopyrightText: 2018 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`Gamepad`
====================================================

* Author(s): Dan Halbert, Tiago Ferreira
"""

import struct
import time

from adafruit_hid import find_device

class Gamepad:
    """Emulate 2 generic gamepad controller with 32 buttons,
    numbered 1-32 and 33-64"""

    def __init__(self, devices):
        """Create a Gamepad object that will send USB gamepad HID reports.

        Devices can be a list of devices that includes a gamepad device or a gamepad device
        itself. A device is any object that implements ``send_report()``, ``usage_page`` and
        ``usage``.
        """
        self._gamepad_device = (find_device(devices, usage_page=0x1, usage=0x05), 
                                find_device(devices, usage_page=0x1, usage=0x04))

        
        # self._gamepad_device = tuple(
        #     dev for dev in devices
        #     if (dev.usage_page == 0x1 and dev.usage == 0x05 and hasattr(dev, "send_report"))
        # )
        
        if len(self._gamepad_device) != 2:
            raise RuntimeError("No gamepad devices found!")

        # Store settings separately before putting into report. Saves code
        # especially for buttons.
        self._buttons_state = 0
        # Remember the last buttons state as well, so we can avoid sending
        # duplicate reports.
        self._last_state = (bytearray(4), bytearray(4)) 

        # Send an initial report to test if HID device is ready.
        # If not, wait a bit and try once more.
        try:
            self.reset_all()
        except OSError:
            time.sleep(1)
            self.reset_all()

    def press_buttons(self, *buttons):
        """Press and hold the given buttons."""
        for button in buttons:
            self._buttons_state |= 1 << self._validate_button_number(button) - 1
        self._send()

    def release_buttons(self, *buttons):
        """Release the given buttons."""
        for button in buttons:
            self._buttons_state &= ~(1 << self._validate_button_number(button) - 1)
        self._send()

    def release_all_buttons(self):
        """Release all the buttons."""

        self._buttons_state = 0
        self._send()

    def click_buttons(self, *buttons):
        """Press and release the given buttons."""
        self.press_buttons(*buttons)
        self.release_buttons(*buttons)

    def move_joysticks(self, x=None, y=None, z=None, r_z=None):
        """Set and send the given joystick values.
        The joysticks will remain set with the given values until changed

        One joystick provides ``x`` and ``y`` values,
        and the other provides ``z`` and ``r_z`` (z rotation).
        Any values left as ``None`` will not be changed.

        All values must be in the range -127 to 127 inclusive.

        Examples::

            # Change x and y values only.
            gp.move_joysticks(x=100, y=-50)

            # Reset all joystick values to center position.
            gp.move_joysticks(0, 0, 0, 0)
        """
        # if x is not None:
        #     self._joy_x = self._validate_joystick_value(x)
        # if y is not None:
        #     self._joy_y = self._validate_joystick_value(y)
        # if z is not None:
        #     self._joy_z = self._validate_joystick_value(z)
        # if r_z is not None:
        #     self._joy_r_z = self._validate_joystick_value(r_z)
        self._send()

    def reset_all(self):
        """Release all buttons and set joysticks to zero."""
        self._buttons_state = 0
        # self._joy_x = 0
        # self._joy_y = 0
        # self._joy_z = 0
        # self._joy_r_z = 0
        self._send(always=True)

    def _send(self, always=False):
        """Send a report with all the existing settings.
        If ``always`` is ``False`` (the default), send only if there have been changes.
        """
        button_states = (self._buttons_state & 0xFFFFFFFF, (self._buttons_state >> 32) & 0xFFFFFFFF)
        for i in range(len(self._gamepad_device)):
            if always or button_states[i] != int.from_bytes(self._last_state[i], "little"):
                # Store current state
                self._last_state[i][:] = button_states[i].to_bytes(4, 'little')
                # Prepare report - uses memoryviews to avoid copies
                report = bytearray(4)  # Buttons 1-32 (REPORT_ID=2)
                memoryview(report)

                struct.pack_into("<I", report, 0, button_states[i])
                print(' '.join(f'{b:02X}' for b in report))

                self._gamepad_device[i].send_report(report)

        
    @staticmethod
    def _validate_button_number(button):
        if not 1 <= button <= 64:
            raise ValueError("Button number must in range 1 to 64")
        return button 

    @staticmethod 
    def _validate_joystick_value(value):
        if not -127 <= value <= 127:
            raise ValueError("Joystick value must be in range -127 to 127")
        return value
