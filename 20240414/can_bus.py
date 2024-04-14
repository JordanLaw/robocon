import serial

check_can_bus = False
work_mode = [0x41, 0x54, 0x2B, 0x43, 0x41, 0x4E, 0x5F, 0x4D, 0x4F, 0x44, 0x45, 0x3D, 0x30, 0x0D, 0x0A]
check_mode = [0x41, 0x54, 0x2B, 0x43, 0x41, 0x4E, 0x5F, 0x4D, 0x4F, 0x44, 0x45, 0x3D, 0x3F, 0x0D, 0x0A]
AT_mode = [0x41, 0x54, 0x2b, 0x41, 0x54, 0x0D, 0x0A]
CG_mode = [0x41, 0x54, 0x2b, 0x43, 0x47, 0x0D, 0x0A]

stop = 0


def connect(ser):
    global check_can_bus

    while not check_can_bus:
        ser.write(serial.to_bytes(CG_mode))
        check = ser.read(4)
        print(f"1: {check}")
        if check == b'OK\r\n' or b'K\r\nO':
            ser.write(serial.to_bytes(work_mode))
            check = ser.read(4)
            print(f"2: {check}")
            if check == b'OK\r\n' or b'K\r\nO':
                ser.write(serial.to_bytes(check_mode))
                check = ser.read(13)
                print(f"3: {check}")
                if check == b'+CAN_MODE:0\r\n' or b'N_MODE:0\r\nOK\r':
                    check_can_bus = True
                    ser.write(AT_mode)
                    print("can_bus ready")