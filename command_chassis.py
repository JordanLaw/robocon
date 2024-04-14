import serial

fr_speed = [0, 0, 0, 0]
fl_speed = [0, 0, 0, 0]
br_speed = [0, 0, 0, 0]
bl_speed = [0, 0, 0, 0]

def control_command_speed(wheel_command, rpm, ser):
    fr_speed[0] = (int(wheel_command[0] * rpm) >> 24) & 0xff
    fr_speed[1] = (int(wheel_command[0] * rpm) >> 16) & 0xff
    fr_speed[2] = (int(wheel_command[0] * rpm) >> 8) & 0xff
    fr_speed[3] = int(wheel_command[0] * rpm) & 0xff

    # id: 12. front-right
    fr_rpm = [0x41, 0x54, 0x00, 0x00, 0x18, 0x64, 0x04,
              fr_speed[0], fr_speed[1], fr_speed[2], fr_speed[3],
              0x0D, 0x0A]

    # # id: 12, front-right
    ser.write(serial.to_bytes(fr_rpm))

    bl_speed[0] = (int(wheel_command[2] * rpm) >> 24) & 0xff
    bl_speed[1] = (int(wheel_command[2] * rpm) >> 16) & 0xff
    bl_speed[2] = (int(wheel_command[2] * rpm) >> 8) & 0xff
    bl_speed[3] = int(wheel_command[2] * rpm) & 0xff

    # id: 20, back-left
    bl_rpm = [0x41, 0x54, 0x00, 0x00, 0x18, 0xA4, 0x04,
              bl_speed[0], bl_speed[1], bl_speed[2], bl_speed[3],
              0x0D, 0x0A]

    # id: 20, back-left
    ser.write(serial.to_bytes(bl_rpm))

    fl_speed[0] = (int(wheel_command[1] * rpm) >> 24) & 0xff
    fl_speed[1] = (int(wheel_command[1] * rpm) >> 16) & 0xff
    fl_speed[2] = (int(wheel_command[1] * rpm) >> 8) & 0xff
    fl_speed[3] = int(wheel_command[1] * rpm) & 0xff

    # id: 8, front-left
    fl_rpm = [0x41, 0x54, 0x00, 0x00, 0x18, 0x44, 0x04,
              fl_speed[0], fl_speed[1], fl_speed[2], fl_speed[3],
              0x0D, 0x0A]

    # # id: 8, front-left
    ser.write(serial.to_bytes(fl_rpm))

    br_speed[0] = (int(wheel_command[3] * rpm) >> 24) & 0xff
    br_speed[1] = (int(wheel_command[3] * rpm) >> 16) & 0xff
    br_speed[2] = (int(wheel_command[3] * rpm) >> 8) & 0xff
    br_speed[3] = int(wheel_command[3] * rpm) & 0xff

    # id: 16, back-right
    br_rpm = [0x41, 0x54, 0x00, 0x00, 0x18, 0x84, 0x04,
              br_speed[0], br_speed[1], br_speed[2], br_speed[3],
              0x0D, 0x0A]

    # id: 16, back-right
    ser.write(serial.to_bytes(br_rpm))
