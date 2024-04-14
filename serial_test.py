import serial

ser_read_data = serial.Serial('COM12', baudrate=921600)
# value = b'\x00\x00\x00\x00'

while True:
    val = ser_read_data.read(1)
    print(val)
    if val == b'\xaa':
        val = ser_read_data.read(1)
        if val == b'\xbb':
            val = ser_read_data.read(24)
            val_front = int.from_bytes(val[0:4], byteorder='big', signed=True)
            val_left = int.from_bytes(val[5:8], byteorder='big', signed=True)
            val_right = int.from_bytes(val[9:12], byteorder='big', signed=True)
            val_odom_front = int.from_bytes(val[13:16], byteorder='big', signed=True)
            val_odom_left = int.from_bytes(val[17:20], byteorder='big', signed=True)
            val_odom_right = int.from_bytes(val[21:24], byteorder='big', signed=True)
            # print(val)
            # print(val)
            print(val_front, " ", val_left, " ", val_right, " ", val_odom_front, " ", val_odom_left, " ", val_odom_right)

    # value_int = int.from_bytes(value, byteorder='big')
    # print(value_int)