// E:\gamepadDescriptor.h


char ReportDescriptor[28] = {
    0x05, 0x01,                    // USAGE_PAGE (Generic Desktop)
    0x09, 0x05,                    // USAGE (Game Pad)
    0xa1, 0x01,                    // COLLECTION (Application)
    0xa1, 0x00,                    //   COLLECTION (Physical)
    0x85, 0x04,                    //     REPORT_ID (4)
    0x05, 0x09,                    //     USAGE_PAGE (Button)
    0x19, 0x01,                    //     USAGE_MINIMUM (Button 1)
    0x29, 0x25,                    //     USAGE_MAXIMUM (Button 37)
    0x15, 0x00,                    //     LOGICAL_MINIMUM (0)
    0x25, 0x01,                    //     LOGICAL_MAXIMUM (1)
    0x75, 0x01,                    //     REPORT_SIZE (1)
    0x95, 0x1b,                    //     REPORT_COUNT (27)
    0x81, 0x00,                    //     INPUT (Data,Ary,Abs)
    0xc0,                          //     END_COLLECTION
    0xc0                           // END_COLLECTION
};

