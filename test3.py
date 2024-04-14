import time
import ctypes
import oak_camera
from multiprocessing import Process, Value, Lock, Array, Queue
import cv2
import numpy as np

def a(share_frame):
    def frameNorm(frame, bbox):
        normVals = np.full(len(bbox), frame.shape[0])
        normVals[::2] = frame.shape[1]
        return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)

    def displayFrame(name, frame, detections):
        color = (255, 0, 0)
        for detection in detections:
            bbox = frameNorm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
            cv2.putText(frame, labels[detection.label], (bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.putText(frame, f"{int(detection.confidence * 100)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
        # Show the frame
        # cv2.imshow(name, frame)

        share_frame.put(frame)

    labels = ["Class_0", "Class_1", "Class_2", "Class_3", "Class_4"]

    frame = None
    detections = []
    startTime = time.monotonic()
    counter = 0
    color2 = (255, 255, 255)

    camera = oak_camera.setup()
    camera.function_setup()

    while True:
        t = time.perf_counter()
        inRgb = camera.qRgb.get()
        inDet = camera.qDet.get()

        if inRgb is not None:
            frame = inRgb.getCvFrame()
            cv2.putText(frame, "NN fps: {:.2f}".format(counter / (time.monotonic() - startTime)),
                        (2, frame.shape[0] - 4), cv2.FONT_HERSHEY_TRIPLEX, 0.4, color2)

        if inDet is not None:
            detections = inDet.detections
            counter += 1

        if frame is not None:
            displayFrame("rgb", frame, detections)





def b(share_frame):
    while True:
        # t =time.perf_counter()
        if not share_frame.empty():
            frame = share_frame.get()
            cv2.imshow("img", frame)
        # print(f"{(time.perf_counter() - t):.6f}")
        if cv2.waitKey(1) == ord('q'):
            break


        # print("123")
        # time.sleep(1)
        # print(share_frame)

if __name__ == "__main__":
    q = Queue()
    share = Array(ctypes.c_int, 320)
    process_a = Process(target=a, args=(q,))
    # process_b = Process(target=b, args=(queue,))
    process_b = Process(target=b, args=(q,))
    process_a.start()
    process_b.start()
    # process_b.start()

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
