from multiprocessing import Process, Queue
import oak_imu
import time

import serial
import cv2

import can_bus
import kinematics
import odometry_test
import speed_pid
import numpy as np

from quick_queue import QQueue



# imu_setup = oak_imu.imu_setup()
# imu_start = oak_imu.imu_start()
#
# imu_setup.set()

# imuQueue = imu_setup.imuQueue
# baseTs = imu_setup.baseTs

# prev_time, prev_e, integral_accumulate, four bytes of speed
PID_fl = [0, 0, 0, 0, 0, 0, 0]
PID_value_fl = [0.01, 0.0, 0.0]
# PID_value_fl = [0.265, 0.01, 0.0]

# prev_time, prev_e, integral_accumulate, four bytes of speed
PID_fr = [0, 0, 0, 0, 0, 0, 0]
PID_value_fr = [0.01, 0.0, 0.0]
# PID_value_fr = [0.265, 0.01, 0.0]

# prev_time, prev_e, integral_accumulate, four bytes of speed
PID_br = [0, 0, 0, 0, 0, 0, 0]
PID_value_br = [0.01, 0.0, 0.0]
# PID_value_br = [0.265, 0.01, 0.0]

# prev_time, prev_e, integral_accumulate, four bytes of speed
PID_bl = [0, 0, 0, 0, 0, 0, 0]
PID_value_bl = [0.01, 0.0, 0.0]
# PID_value_bl = [0.265, 0.01, 0.0]

# 0 = not yet home, 1 = home already
# fr, fl, br, bl
home_status = [0, 0, 0, 0]
home_tick = [0, 0, 0, 0]  # off-set tick which change the start tick to zero

data_read = [0, 0, 0, 0, 0, 0, 0, 0]
actual_data = [0, 0, 0, 0]  # data read off-set the home tick




def a(queue):
    imu_setup = oak_imu.imu_setup()
    imu_start = oak_imu.imu_start()

    imu_setup.set()

    imuQueue = imu_setup.imuQueue
    baseTs = imu_setup.baseTs

    pos_x = 0
    old_gyroTs = 0

    while True:
        pos_x, old_gyroTs, baseTs = imu_start.data_get(imuQueue, baseTs, pos_x, old_gyroTs)

        # print(f"x: {pos_x}")

        queue.put(int(pos_x))


def b(queue):
    while True:
        data = queue.get()
        print(f"x: {data}")



def c(queue):
    ser = serial.Serial('COM5', baudrate=921600)
    can_bus.connect(ser)

    # WS1: fr, WS2: fl, WS3: bl, WS4: br
    # WA1: fr, WA2: fl, WA3: bl, WA4: br
    wheel_command = [0, 0, 0, 0, 0, 0, 0, 0]

    motor_pole = 14

    angular_speed_Max = 8000
    angular_speed_Min = -8000
    byte_angular_speed = 0
    byte_angular_speed_array = [0, 0, 0, 0]

    tick_per_round = 76700
    tick_per_round_br = 78000

    def data_off_set():
        actual_data[0] = data_read[0] - home_tick[0]
        actual_data[1] = data_read[1] - home_tick[1]
        actual_data[2] = data_read[2] - home_tick[2]
        actual_data[3] = data_read[3] - home_tick[3]

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

        # print(f"inte: {integral_value}")
        # print(f"derivative: {derivative_pid}")
        # print(angular_speed)
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

        message1 = 0
        message2 = 0
        message3 = 0
        message4 = 0

        while True:
            value_read = ser.read(1)
            if value_read == b'A':
                value_read = ser.read(1)
                # print(value_read)
                if value_read == b'T':
                    value_read = ser.read(4)
                    # print(value_read)
                    if value_read[0] + value_read[1] + value_read[2] + value_read[3] == 32:
                        value_read = ser.read(11)
                        # print(value_read)
                        bytes_fr = value_read[2:5]
                        bytes_fl = value_read[6:9]
                        data_read[0] = int.from_bytes(bytes_fr, byteorder='big', signed=True)
                        data_read[1] = int.from_bytes(bytes_fl, byteorder='big', signed=True)
                        message1 = 1

                    elif value_read[0] + value_read[1] + value_read[2] + value_read[3] == 64:
                        value_read = ser.read(5)
                        data_read[4] = value_read[1]
                        data_read[5] = value_read[2]
                        # data_read[6] = value_read[3]
                        # data_read[7] = value_read[4]
                        message2 = 1

                    elif value_read[0] + value_read[1] + value_read[2] + value_read[3] == 96:
                        value_read = ser.read(11)
                        bytes_br = value_read[2:5]
                        bytes_bl = value_read[6:9]
                        data_read[2] = int.from_bytes(bytes_br, byteorder='big', signed=True)
                        data_read[3] = int.from_bytes(bytes_bl, byteorder='big', signed=True)
                        message3 = 1

                    elif value_read[0] + value_read[1] + value_read[2] + value_read[3] == 128:
                        value_read = ser.read(5)
                        # print(value_read)
                        # data_read[4] = value_read[1]
                        # data_read[5] = value_read[2]
                        data_read[6] = value_read[1]
                        data_read[7] = value_read[2]
                        message4 = 1

            if message1 == 1 and message2 == 1 and message3 == 1 and message4 == 1:
                break

    # rpm setting
    byte_rpm_speed_array = [0, 0, 0, 0]
    rpm = 500
    byte_rpm_speed_array[0] = (int(rpm) >> 24) & 0xff
    byte_rpm_speed_array[1] = (int(rpm) >> 16) & 0xff
    byte_rpm_speed_array[2] = (int(rpm) >> 8) & 0xff
    byte_rpm_speed_array[3] = int(rpm) & 0xff

    # id: 16, back-right
    br_rpm = [0x41, 0x54, 0x00, 0x00, 0x18, 0x84, 0x04,
              byte_rpm_speed_array[0], byte_rpm_speed_array[1], byte_rpm_speed_array[2], byte_rpm_speed_array[3],
              0x0D, 0x0A]

    # id: 12. front-right
    fr_rpm = [0x41, 0x54, 0x00, 0x00, 0x18, 0x64, 0x04,
              byte_rpm_speed_array[0], byte_rpm_speed_array[1], byte_rpm_speed_array[2], byte_rpm_speed_array[3],
              0x0D, 0x0A]

    # id: 20, back-left
    bl_rpm = [0x41, 0x54, 0x00, 0x00, 0x18, 0xA4, 0x04,
              byte_rpm_speed_array[0], byte_rpm_speed_array[1], byte_rpm_speed_array[2], byte_rpm_speed_array[3],
              0x0D, 0x0A]

    # id: 8, front-left
    fl_rpm = [0x41, 0x54, 0x00, 0x00, 0x18, 0x44, 0x04,
              byte_rpm_speed_array[0], byte_rpm_speed_array[1], byte_rpm_speed_array[2], byte_rpm_speed_array[3],
              0x0D, 0x0A]

    br_speed = [0, 0, 0, 0]
    bl_speed = [0, 0, 0, 0]
    fr_speed = [0, 0, 0, 0]
    fl_speed = [0, 0, 0, 0]

    def control_command_speed():
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

    def PID_direaction_cal():
        global PID_fl, PID_bl, PID_br, PID_fr

        data_can_read()
        data_off_set()

        PID_fl = PID_control(actual_data[1], tick_per_round / 360 * wheel_command[5],
                             PID_fl[0], PID_fl[1], PID_fl[2],
                             PID_value_fl[0], PID_value_fl[1], PID_value_fl[2])

        # data_can_read()
        # data_off_set()

        PID_fr = PID_control(actual_data[0], tick_per_round / 360 * wheel_command[4],
                             PID_fr[0], PID_fr[1], PID_fr[2],
                             PID_value_fr[0], PID_value_fr[1], PID_value_fr[2])

        # data_can_read()
        # data_off_set()

        PID_br = PID_control(actual_data[2], tick_per_round / 360 * wheel_command[7],
                             PID_br[0], PID_br[1], PID_br[2],
                             PID_value_br[0], PID_value_br[1], PID_value_br[2])

        # data_can_read()
        # data_off_set()

        PID_bl = PID_control(actual_data[3], tick_per_round / 360 * wheel_command[6],
                             PID_bl[0], PID_bl[1], PID_bl[2],
                             PID_value_bl[0], PID_value_bl[1], PID_value_bl[2])

    def control_command_direction():
        PID_direaction_cal()

        # control front-left wheel direction (0x18, 0x54 = id 10)
        value_fl = [0x41, 0x54, 0x00, 0x00, 0x18, 0x54, 0x04,
                    PID_fl[3], PID_fl[4], PID_fl[5], PID_fl[6],
                    0x0D, 0x0A]
        ser.write(serial.to_bytes(value_fl))

        # control front-right wheel direction (0x19, 0xCC = id 57)
        value_fr = [0x41, 0x54, 0x00, 0x00, 0x19, 0xCC, 0x04,
                    PID_fr[3], PID_fr[4], PID_fr[5], PID_fr[6],
                    0x0D, 0x0A]
        ser.write(serial.to_bytes(value_fr))

        # control back-right wheel direction (0x18, 0xC4 = id 24)
        value_br = [0x41, 0x54, 0x00, 0x00, 0x18, 0xC4, 0x04,
                    PID_br[3], PID_br[4], PID_br[5], PID_br[6],
                    0x0D, 0x0A]
        ser.write(serial.to_bytes(value_br))

        # control back-left wheel direction (0x18, 0xC4 = id 28)
        value_bl = [0x41, 0x54, 0x00, 0x00, 0x18, 0xE4, 0x04,
                    PID_bl[3], PID_bl[4], PID_bl[5], PID_bl[6],
                    0x0D, 0x0A]
        ser.write(serial.to_bytes(value_bl))



    # home speed setting
    byte_home_speed_array = [0, 0, 0, 0]
    home_speed = 400
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

    def control_command_home():
        global home_status, home_tick

        print(f"home status: {home_status}")

        # id: 24, back-right
        # if home_status[2] == 0:
        #     data_can_read()
        #     if data_read[6] == 0:
        #         ser.write(serial.to_bytes(br_home))
        #
        #     else:
        #         ser.write(serial.to_bytes(br_home_stop))
        #         home_tick[2] = data_read[2]
        #         home_status[2] = 1

        # id: 57, front-right
        if home_status[0] == 0:
            data_can_read()
            if data_read[4] == 0:
                ser.write(serial.to_bytes(fr_home))

            else:
                ser.write(serial.to_bytes(fr_home_stop))
                home_tick[0] = data_read[0]
                home_status[0] = 1

        # id: 10, front-left
        # if home_status[1] == 0:
        #     data_can_read()
        #     if data_read[5] == 0:
        #         ser.write(serial.to_bytes(fl_home))
        #
        #     else:
        #         ser.write(serial.to_bytes(fl_home_stop))
        #         home_tick[1] = data_read[1]
        #         home_status[1] = 1

        # id: 28, back-left
        # if home_status[3] == 0:
        #     data_can_read()
        #     if data_read[7] == 0:
        #         ser.write(serial.to_bytes(bl_home))
        #
        #     else:
        #         ser.write(serial.to_bytes(bl_home_stop))
        #         home_tick[3] = data_read[3]
        #         home_status[3] = 1

    def emer_stop():
        ser.write(serial.to_bytes(fr_home))
        ser.write(serial.to_bytes(fl_home))
        ser.write(serial.to_bytes(br_home))
        ser.write(serial.to_bytes(bl_home))
        print("stop")

    def PID_time_reset():
        global PID_fl, PID_bl, PID_br, PID_fr

        PID_fl[0] = time.perf_counter()
        PID_bl[0] = time.perf_counter()
        PID_fr[0] = time.perf_counter()
        PID_br[0] = time.perf_counter()

    target = 45

    # prev_time, prev_e, integral_accumulate, four bytes of speed
    PID_fl = [0, 0, 0, 0, 0, 0, 0]
    PID_value_fl = [0.01, 0.0, 0.0]
    # PID_value_fl = [0.265, 0.01, 0.0]

    # prev_time, prev_e, integral_accumulate, four bytes of speed
    PID_fr = [0, 0, 0, 0, 0, 0, 0]
    PID_value_fr = [0.01, 0.0, 0.0]
    # PID_value_fr = [0.265, 0.01, 0.0]

    # prev_time, prev_e, integral_accumulate, four bytes of speed
    PID_br = [0, 0, 0, 0, 0, 0, 0]
    PID_value_br = [0.01, 0.0, 0.0]
    # PID_value_br = [0.265, 0.01, 0.0]

    # prev_time, prev_e, integral_accumulate, four bytes of speed
    PID_bl = [0, 0, 0, 0, 0, 0, 0]
    PID_value_bl = [0.01, 0.0, 0.0]
    # PID_value_bl = [0.265, 0.01, 0.0]

    speed_PID = [time.perf_counter(), 0, 0, 0, 0, 0, 0]
    speed_PID_value = [3.5, 0.3, 0.1]

    x_target = -180
    y_target = 180

    home_done = 0
    time_delay = 0

    step = 1

    while True:
        t = time.perf_counter()

        data = queue.get()
        print(f"x: {data}")

        if step == 0:
            data_can_read()
            print(data_read)

            # wheel_command = kinematics.move_cal(0, -1, 0)
            # print(
            #     f"WS1: {wheel_command[0]:.2f} WS2: {wheel_command[1]:.2f} WS3: {wheel_command[2]:.2f} WS4: {wheel_command[3]:.2f}")
            # print(
            #     f"WA1: {wheel_command[4]:.2f} WA2: {wheel_command[5]:.2f} WA3: {wheel_command[6]:.2f} WA4: {wheel_command[7]:.2f}")

        if step == 1:

            # home action
            if home_done == 0:
                if home_status[0] == 0 or home_status[1] == 0 or home_status[2] == 0 or home_status[3] == 0:
                    control_command_home()
                    print(data_read)

                else:
                    home_done = 1
                    data_can_read()
                    print(data_read)
                    print(home_tick)
                    print("ready")

            else:
                step = 2
                wheel_command = kinematics.move_cal(0, -1, 0)
                PID_time_reset()
                time_delay = time.perf_counter()

        if step == 2:
            control_command_direction()
            print("123")

            # time_count = time.perf_counter() - time_delay
            # print(time_count)
            #
            # if time_count < 3:
            #
            #     control_command_direction()
            #
            # else:
            #     control_command_direction()
            # control_command_speed()

            # if -19500 < actual_data[0] < -19000 and -19500 < actual_data[1] < -19000 and -19500 < actual_data[2] < 19000 and -19500 < actual_data[3] < -19000:
            #     print("run")
            #     control_command_direction()
            #     # control_command_speed()
            # else:
            #     control_command_direction()

        data_can_read()
        data_off_set()

        if tick_per_round < actual_data[0] < -tick_per_round or tick_per_round < actual_data[
            1] < -tick_per_round or tick_per_round < actual_data[2] < -tick_per_round or tick_per_round < actual_data[
            3] < -tick_per_round:
            emer_stop()

        print(actual_data)
        print(f"time finish: {(time.perf_counter() - t):.6f}")


if __name__ == "__main__":
    queue = Queue()
    process_a = Process(target=a, args=(queue,))
    # process_b = Process(target=b, args=(queue,))
    process_c = Process(target=c, args=(queue,))
    process_a.start()
    # process_b.start()
    process_c.start()

    try:
        while True:
            pass

    except KeyboardInterrupt:
        process_a.terminate()
        # process_b.terminate()
        process_c.terminate()
        process_a.join()
        # process_b.join()
        process_c.join()
        # queue.end()
        print("Processes terminated")







