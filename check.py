import serial
import time

ser = serial.Serial('COM4', baudrate=921600)
# time.sleep(0.1)
check_can_bus = False
work_mode = [0x41, 0x54, 0x2B, 0x43, 0x41, 0x4E, 0x5F, 0x4D, 0x4F, 0x44, 0x45, 0x3D, 0x30, 0x0D, 0x0A]
check_mode = [0x41, 0x54, 0x2B, 0x43, 0x41, 0x4E, 0x5F, 0x4D, 0x4F, 0x44, 0x45, 0x3D, 0x3F, 0x0D, 0x0A]
AT_mode = [0x41, 0x54, 0x2b, 0x41, 0x54, 0x0D, 0x0A]
CG_mode = [0x41, 0x54, 0x2b, 0x43, 0x47, 0x0D, 0x0A]

while not check_can_bus:
    # ser.write(serial.to_bytes(AT_mode))
    # check = ser.read(2)
    # print(check)

    ser.write(serial.to_bytes(CG_mode))
    check = ser.read(4)
    # print(check)
    if check == b'OK\r\n':
        ser.write(serial.to_bytes(work_mode))
        check = ser.read(4)
        # print(check)
        if check == b'OK\r\n':
            ser.write(serial.to_bytes(check_mode))
            check = ser.read(13)
            if check == b'+CAN_MODE:0\r\n':
                check_can_bus = True
                print("can_bus ready")
# AT_mode = [0x41, 0x54, 0x2b, 0x41, 0x54]
# ser.write(serial.to_bytes(AT_mode))