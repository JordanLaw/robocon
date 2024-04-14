import concurrent.futures

import serial
import time
import kinematics
import multiprocessing
import odometry_test
import speed_pid
import numpy as np

# Check and change the COM port to match with your Arduino connection
# ser_read_data = serial.Serial('COM12', baudrate=230400, bytesize=8, parity='N', stopbits=1)
ser = serial.Serial('COM5', baudrate=921600)

data_read = [0, 0, 0, 0, 0, 0]

motor_pole = 14

angular_speed_Max = 8000
angular_speed_Min = -8000
byte_angular_speed = 0
byte_angular_speed_array = [0, 0, 0, 0]

# front_tick = 77033
front_tick = 73698
left_tick = 76869
right_tick = 76698


def PID_control(current_turn, angle, prev_time, e_prev, integral_acc, kp, ki, kd):
    # data_can_read()

    theta = current_turn
    theta_d = angle

    start_time = time.perf_counter()
    dt = (start_time - prev_time)

    e = theta_d - theta
    integral_value = integral_acc + dt * e
    derivative_pid = (e - e_prev) / dt

    angular_speed = kp * e + ki * integral_value + kd * derivative_pid

    if angular_speed >= angular_speed_Max:
        angular_speed = angular_speed_Max

    if angular_speed <= angular_speed_Min:
        angular_speed = angular_speed_Min

    angular_speed = angular_speed * motor_pole / 2

    # print("start_time", start_time, "e: ", e, "inte: ", integral_value, "dt: ", dt, "speed: ",

    byte_angular_speed_array[0] = (int(angular_speed) >> 24) & 0xff
    byte_angular_speed_array[1] = (int(angular_speed) >> 16) & 0xff
    byte_angular_speed_array[2] = (int(angular_speed) >> 8) & 0xff
    byte_angular_speed_array[3] = int(angular_speed) & 0xff

    e_prev_update = e
    time_prev_update = start_time

    return (time_prev_update, e_prev_update, integral_value,
            byte_angular_speed_array[0], byte_angular_speed_array[1],
            byte_angular_speed_array[2], byte_angular_speed_array[3])


def data_can_read():
    global data_read

    value_read = ser.read(1)
    # print(value_read)
    # if value_read == b'A' + b'T':
    #     value_read = ser.read(15)
        # print(value_read)
    if value_read == b'A':
        value_read = ser.read(1)
        # print(value_read)
        if value_read == b'T':
            value_read = ser.read(15)
            # print(value_read)
            if value_read[0] + value_read[1] + value_read[2] + value_read[3] == 32:
                bytes_f = value_read[6:9]
                bytes_odom_f = value_read[10:13]
                data_read[0] = int.from_bytes(bytes_f, byteorder='big', signed=True)
                data_read[3] = int.from_bytes(bytes_odom_f, byteorder='big', signed=True)

            elif value_read[0] + value_read[1] + value_read[2] + value_read[3] == 64:
                bytes_l = value_read[6:9]
                bytes_odom_l = value_read[10:13]
                data_read[1] = int.from_bytes(bytes_l, byteorder='big', signed=True)
                data_read[4] = int.from_bytes(bytes_odom_l, byteorder='big', signed=True)

            elif value_read[0] + value_read[1] + value_read[2] + value_read[3] == 96:
                bytes_r = value_read[6:9]
                bytes_odom_r = value_read[10:13]
                data_read[2] = int.from_bytes(bytes_r, byteorder='big', signed=True)
                data_read[5] = int.from_bytes(bytes_odom_r, byteorder='big', signed=True)


# def data_serial_read():
#     global data_read
#
#     val = ser_read_data.read(1)
#     if val == b'\xaa':
#         val = ser_read_data.read(1)
#         if val == b'\xbb':
#             val = ser_read_data.read(24)
#             data_read[0] = int.from_bytes(val[0:4], byteorder='big', signed=True)
#             data_read[1] = int.from_bytes(val[5:8], byteorder='big', signed=True)
#             data_read[2] = int.from_bytes(val[9:12], byteorder='big', signed=True)
#             data_read[3] = int.from_bytes(val[13:16], byteorder='big', signed=True)
#             data_read[4] = int.from_bytes(val[17:20], byteorder='big', signed=True)
#             data_read[5] = int.from_bytes(val[21:24], byteorder='big', signed=True)
# print(val)
# print(val)
# print(val_front, " ", val_left, " ", val_right, " ", val_odom_front, " ", val_odom_left, " ", val_odom_right)

def control_command_speedstop():
    value = [0x41, 0x54, 0x00, 0x00, 0x19, 0xEC, 0x04,
             0x00, 0x00, 0x00, 0x00,
             0x0D, 0x0A]
    ser.write(serial.to_bytes(value))

    value = [0x41, 0x54, 0x00, 0x00, 0x18, 0xA4, 0x04,
             0x00, 0x00, 0x00, 0x00,
             0x0D, 0x0A]
    ser.write(serial.to_bytes(value))

    value = [0x41, 0x54, 0x00, 0x00, 0x1B, 0x94, 0x04,
             0x00, 0x00, 0x00, 0x00,
             0x0D, 0x0A]
    ser.write(serial.to_bytes(value))

def control_command_speed():
    value = [0x41, 0x54, 0x00, 0x00, 0x19, 0xEC, 0x04,
             speed_PID[3], speed_PID[4], speed_PID[5], speed_PID[6],
             0x0D, 0x0A]
    ser.write(serial.to_bytes(value))

    value = [0x41, 0x54, 0x00, 0x00, 0x18, 0xA4, 0x04,
             speed_PID[3], speed_PID[4], speed_PID[5], speed_PID[6],
             0x0D, 0x0A]
    ser.write(serial.to_bytes(value))

    value = [0x41, 0x54, 0x00, 0x00, 0x1B, 0x94, 0x04,
             speed_PID[3], speed_PID[4], speed_PID[5], speed_PID[6],
             0x0D, 0x0A]
    ser.write(serial.to_bytes(value))


def control_command_direction():
    # control front wheel direction (0x19, 0xCC = id 57)
    value = [0x41, 0x54, 0x00, 0x00, 0x19, 0xCC, 0x04,
             PID_front[3], PID_front[4], PID_front[5], PID_front[6],
             0x0D, 0x0A]
    ser.write(serial.to_bytes(value))

    # control left wheel direction (0x18, 0x34 = id 6)
    value = [0x41, 0x54, 0x00, 0x00, 0x18, 0x34, 0x04,
             PID_left[3], PID_left[4], PID_left[5], PID_left[6],
             0x0D, 0x0A]
    ser.write(serial.to_bytes(value))

    # control right wheel direction (0x18, 0x54 = id 10)
    value = [0x41, 0x54, 0x00, 0x00, 0x18, 0x54, 0x04,
             PID_right[3], PID_right[4], PID_right[5], PID_right[6],
             0x0D, 0x0A]
    ser.write(serial.to_bytes(value))

target = 0

# prev_time, prev_e, integral_accumulate, four bytes of speed
PID_front = [time.perf_counter(), 0, 0, 0, 0, 0, 0]
PID_value_front = [0.195, 0.01, 0.0001]

PID_left = [time.perf_counter(), 0, 0, 0, 0, 0, 0]
PID_value_left = [0.079, 0.01, 0.0005]

PID_right = [time.perf_counter(), 0, 0, 0, 0, 0, 0]
PID_value_right = [0.125, 0.01, 0.0001]

speed_PID = [time.perf_counter(), 0, 0, 0, 0, 0, 0]
speed_PID_value = [3.5, 0.3, 0.1]

x_target = -180
y_target = 180

while True:
    t = time.perf_counter()

    data_can_read()
    print(data_read)
    # odometry_test.odometry(data_read[3], data_read[4], data_read[5])

    # data_serial_read()

    # if 97.5 <= odometry_test.pos_x <= 102.5:
    #     control_command_speedstop()
    #     print(f"x: {odometry_test.pos_x}")
    # else:

    # PID_front = PID_control(data_read[0], front_tick / 360 * target,
    #                         PID_front[0], PID_front[1], PID_front[2],
    #                         PID_value_front[0], PID_value_front[1], PID_value_front[2])
    #
    # PID_left = PID_control(data_read[1], left_tick / 360 * target,
    #                        PID_left[0], PID_left[1], PID_left[2],
    #                        PID_value_left[0], PID_value_left[1], PID_value_left[2])
    #
    # PID_right = PID_control(data_read[2], right_tick / 360 * target,
    #                         PID_right[0], PID_right[1], PID_right[2],
    #                         PID_value_right[0], PID_value_right[1], PID_value_right[2])
    #
    # control_command_direction()
    #
    # speed_PID = speed_pid.PID_control(odometry_test.pos_x, x_target,
    #                                   speed_PID[0], speed_PID[1], speed_PID[2],
    #                                   speed_PID_value[0], speed_PID_value[1], speed_PID_value[2], False)

    # speed_PID = speed_pid.PID_control(odometry_test.pos_y, y_target,
    #                                   speed_PID[0], speed_PID[1], speed_PID[2],
    #                                   speed_PID_value[0], speed_PID_value[1], speed_PID_value[2], True)

    # control_command_speed()
    #
    # print(f"speed: {speed_pid.speed} pos_x: {odometry_test.pos_x} pos_y: {odometry_test.pos_y}")

    # print(data_read)

    # print(f"data: {data_read} "
    #       f"finish time: {time.perf_counter() - t} "
    #       f"pos_x: {odometry_test.pos_x} "
    #       f"pos_y: {odometry_test.pos_y} "
    #       f"angle: {odometry_test.angle_turn}")

    # time.sleep(0.5)
