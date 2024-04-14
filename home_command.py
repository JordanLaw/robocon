# 0 = not yet home, 1 = home already
# fr, fl, br, bl
home_status = [0, 0, 0, 0]
home_tick = [0, 0, 0, 0]    # off-set tick which change the start tick to zero

# home speed setting
byte_home_speed_array = [0, 0, 0, 0]
home_speed = -750
byte_home_speed_array[0] = (int(home_speed) >> 24) & 0xff
byte_home_speed_array[1] = (int(home_speed) >> 16) & 0xff
byte_home_speed_array[2] = (int(home_speed) >> 8) & 0xff
byte_home_speed_array[3] = int(home_speed) & 0xff

# id: 24, back-right
br_home = [0x41, 0x54, 0x00, 0x00, 0x18, 0xC4, 0x04,
           byte_home_speed_array[0], byte_home_speed_array[1], byte_home_speed_array[2], byte_home_speed_array[3],
           0x0D, 0x0A]
br_home_stop = [0x41, 0x54, 0x00, 0x00, 0x18, 0xC4, 0x04, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x0A]

# id: 57, front-right
fr_home = [0x41, 0x54, 0x00, 0x00, 0x19, 0xCC, 0x04,
           byte_home_speed_array[0], byte_home_speed_array[1], byte_home_speed_array[2], byte_home_speed_array[3],
           0x0D, 0x0A]
fr_home_stop = [0x41, 0x54, 0x00, 0x00, 0x19, 0xCC, 0x04, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x0A]

# id: 10, front-left
fl_home = [0x41, 0x54, 0x00, 0x00, 0x18, 0x54, 0x04,
           byte_home_speed_array[0], byte_home_speed_array[1], byte_home_speed_array[2], byte_home_speed_array[3],
           0x0D, 0x0A]
fl_home_stop = [0x41, 0x54, 0x00, 0x00, 0x18, 0x54, 0x04, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x0A]

# id: 28, back-left
bl_home = [0x41, 0x54, 0x00, 0x00, 0x18, 0xE4, 0x04,
           byte_home_speed_array[0], byte_home_speed_array[1], byte_home_speed_array[2], byte_home_speed_array[3],
           0x0D, 0x0A]
bl_home_stop = [0x41, 0x54, 0x00, 0x00, 0x18, 0xE4, 0x04, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x0A]


class home_command:

    def __int__(self):
        pass

    def control_command_home():
        global home_status, home_status

        # id: 24, back-right
        data_can_read()
        if data_read[6] == 0:
            ser.write(serial.to_bytes(br_home))

        else:
            ser.write(serial.to_bytes(br_home_stop))
            home_tick[2] = data_read[2]
            home_status[2] = 1

        # id: 57, front-right
        data_can_read()
        if data_read[4] == 0:
            ser.write(serial.to_bytes(fr_home))

        else:
            ser.write(serial.to_bytes(fr_home_stop))
            home_tick[0] = data_read[0]
            home_status[0] = 1

        # id: 10, front-left
        data_can_read()
        if data_read[5] == 0:
            ser.write(serial.to_bytes(fl_home))

        else:
            ser.write(serial.to_bytes(fl_home_stop))
            home_tick[1] = data_read[1]
            home_status[1] = 1

        # id: 28, back-left
        data_can_read()
        if data_read[7] == 0:
            ser.write(serial.to_bytes(bl_home))

        else:
            ser.write(serial.to_bytes(bl_home_stop))
            home_tick[3] = data_read[3]
            home_status[3] = 1
