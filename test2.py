import time

import oak_imu
from multiprocessing import Process, Value, Lock

def a(pos_x):
    gyroTs = 0
    gyroValues = 0
    old_gyroTs = 0

    while True:
        # t = time.perf_counter()

        gyroValues, gyroTs, baseTs = imu_start.data_get(imuQueue, baseTs)

        with Lock():
            pos_x.value = pos_x.value + gyroValues.x * (gyroTs - old_gyroTs) / 1000 * 57.296

        old_gyroTs = gyroTs

        # print(time.perf_counter() - t)


def b(pos_x):
    while True:
        print(f"{pos_x.value:.2f}")
        time.sleep(1)


if __name__ == "__main__":
    imu_setup = oak_imu.imu_setup()
    imu_start = oak_imu.imu_start()
    imu_setup.set()

    imuQueue = imu_setup.imuQueue
    baseTs = imu_setup.baseTs

    share_pos_x = Value('f', 0)
    process_a = Process(target=a, args=(share_pos_x,))
    # process_b = Process(target=b, args=(queue,))
    process_b = Process(target=b, args=(share_pos_x,))
    process_a.start()
    # process_b.start()
    process_b.start()

    try:
        while True:
            pass

    except KeyboardInterrupt:
        process_a.terminate()
        # process_b.terminate()
        process_b.terminate()
        process_a.join()
        process_b.join()
        # process_c.join()
        # queue.end()
        print("Processes terminated")
