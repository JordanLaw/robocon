import time
import data_read

data_read = data_read.data_connect()

angular_speed_Max = 8000
angular_speed_Min = -8000
motor_pole = 14

byte_angular_speed_array = [0, 0, 0, 0]

# prev_time, prev_e, integral_accumulate, four bytes of speed
PID_fl = [0, 0, 0, 0, 0, 0, 0]
PID_value_fl = [0.08, 0.015, 0.0]

# prev_time, prev_e, integral_accumulate, four bytes of speed
PID_fr = [0, 0, 0, 0, 0, 0, 0]
PID_value_fr = [0.08, 0.015, 0.0]

# prev_time, prev_e, integral_accumulate, four bytes of speed
PID_br = [0, 0, 0, 0, 0, 0, 0]
PID_value_br = [0.08, 0.015, 0.0]

# prev_time, prev_e, integral_accumulate, four bytes of speed
PID_bl = [0, 0, 0, 0, 0, 0, 0]
PID_value_bl = [0.08, 0.015, 0.0]


class direction_PID:

    def __int__(self):
        pass

    def PID_control(self, current_turn, angle, prev_time, e_prev, integral_acc, kp, ki, kd):
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

        print(f"inte: {integral_value}")
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

    def PID_direaction_cal(self, ser):
        global PID_fl, PID_bl, PID_br, PID_fr

        data_read.data_can_read(ser)
        data_off_set()

        PID_fl = PID_control(-actual_data[1], tick_per_round / 360 * target,
                             PID_fl[0], PID_fl[1], PID_fl[2],
                             PID_value_fl[0], PID_value_fl[1], PID_value_fl[2])

        # data_can_read()
        # data_off_set()

        PID_fr = PID_control(-actual_data[0], tick_per_round / 360 * target,
                             PID_fr[0], PID_fr[1], PID_fr[2],
                             PID_value_fr[0], PID_value_fr[1], PID_value_fr[2])

        # data_can_read()
        # data_off_set()

        PID_br = PID_control(-actual_data[2], tick_per_round / 360 * target,
                             PID_br[0], PID_br[1], PID_br[2],
                             PID_value_br[0], PID_value_br[1], PID_value_br[2])

        # data_can_read()
        # data_off_set()

        PID_bl = PID_control(-actual_data[3], tick_per_round / 360 * target,
                             PID_bl[0], PID_bl[1], PID_bl[2],
                             PID_value_bl[0], PID_value_bl[1], PID_value_bl[2])
