import usb_hid
import supervisor
import time
import storage
import board
import digitalio
# supervisor.runtime.autoreload = False  # CirPy 8 and above
# print("supervisor.runtime.autoreload = False")


col = digitalio.DigitalInOut(board.GP5)
col.direction = digitalio.Direction.OUTPUT
col.value = 1
switch = digitalio.DigitalInOut(board.GP6)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.DOWN

if (switch.value == 0):
    storage.disable_usb_drive()

col.value = 0
col.deinit()
switch.deinit()

CUSTOM_VID = 0xDDFD  # Non-registered VID
CUSTOM_PID = 0x5050  # Non-registered PID
PRODUCT_NAME = "PicoBox"
MANUFACTURER_NAME = "TSF"

# Set USB identification
supervisor.set_usb_identification(vid=CUSTOM_VID, pid=CUSTOM_PID, manufacturer=MANUFACTURER_NAME, product=PRODUCT_NAME)

GAMEPAD_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,        # USAGE_PAGE (Generic Desktop)
    0x09, 0x05,        # USAGE (Gamepad)
    0xA1, 0x01,        # COLLECTION (Application)
    0x85, 0x02,        #   REPORT_ID (1) - Will be changed per device
    0x05, 0x09,        #   USAGE_PAGE (Button)
    0x19, 0x01,        #   USAGE_MINIMUM (Button 1)
    0x29, 0x20,        #   USAGE_MAXIMUM (Button 32)
    0x15, 0x00,        #   LOGICAL_MINIMUM (0)
    0x25, 0x01,        #   LOGICAL_MAXIMUM (1)
    0x75, 0x01,        #   REPORT_SIZE (1)
    0x95, 0x20,        #   REPORT_COUNT (32)
    0x81, 0x02,        #   INPUT (Data,Var,Abs)
    0xC0,              # END_COLLECTION
))

GAMEPAD2_DESC = (
    GAMEPAD_REPORT_DESCRIPTOR
    .replace(bytes([0x85, 0x02]), bytes([0x85, 0x03]))  # Change Report ID
    .replace(bytes([0x09, 0x05]), bytes([0x09, 0x04]))  # Change Usage
)

# Create two gamepad devices with different Report IDs
gamepad1 = usb_hid.Device(
    report_descriptor=GAMEPAD_REPORT_DESCRIPTOR,
    usage_page=0x01,           # Generic Desktop Control
    usage=0x05,                # Gamepad
    report_ids=(2,),           # First gamepad uses Report ID 1
    in_report_lengths=(4,),    # 4 bytes (32 buttons)
    out_report_lengths=(0,),   # No output reports
)

gamepad2 = usb_hid.Device(
    report_descriptor=GAMEPAD2_DESC,
    usage_page=0x01,
    usage=0x04,
    report_ids=(3,),           # Second gamepad uses Report ID 3
    in_report_lengths=(4,),
    out_report_lengths=(0,),
)

time.sleep(0.5)

usb_hid.enable(
    (
    usb_hid.Device.KEYBOARD,
    gamepad1,
    gamepad2
    )
)
usb_hid.set_interface_name("ButtonBox")


