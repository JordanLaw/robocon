import time

speed_Max = 300
speed_Min = -300

motor_pole = 14

byte_speed_array = [0, 0, 0, 0]
speed = 0

def PID_control(current_x, target_x, prev_time, e_prev, integral_acc, kp, ki, kd, reverse):
    global speed

    theta = current_x
    theta_d = target_x

    start_time = time.perf_counter()
    dt = (start_time - prev_time)

    e = theta_d - theta
    integral_value = integral_acc + dt * e
    derivative_pid = (e - e_prev) / dt

    speed = kp * e + ki * integral_value + kd * derivative_pid

    # print(f"cx: {current_x} integ: {integral_value} speed: {speed}")

    if speed >= speed_Max:
        speed = speed_Max

    if speed <= speed_Min:
        speed = speed_Min

    if not reverse:
        speed = speed * motor_pole / 2
    else:
        speed = -speed * motor_pole / 2

    # print("start_time", start_time, "e: ", e, "inte: ", integral_value, "dt: ", dt, "speed: ",

    byte_speed_array[0] = (int(speed) >> 24) & 0xff
    byte_speed_array[1] = (int(speed) >> 16) & 0xff
    byte_speed_array[2] = (int(speed) >> 8) & 0xff
    byte_speed_array[3] = int(speed) & 0xff

    e_prev_update = e
    time_prev_update = start_time

    return (time_prev_update, e_prev_update, integral_value,
            byte_speed_array[0], byte_speed_array[1],
            byte_speed_array[2], byte_speed_array[3])

