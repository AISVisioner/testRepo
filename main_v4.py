from pathlib import Path
from datetime import datetime
from misc import History, FPS
import asyncio
import threading
import cv2
import face_recognition
import time


def capture(url=0):
    cv2.namedWindow('Kiosk', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Kiosk', 800, 800)
    font = cv2.FONT_HERSHEY_SIMPLEX

    history = History(size=60)
    lock = asyncio.Lock()

    cap = cv2.VideoCapture(url)
    fps = FPS()
    __start = datetime.now()
    while True:
        ret, frame = cap.read()
        if not ret:
            raise ValueError

        key = cv2.waitKey(1)
        if key == 27:
            print("Exiting...")
            break

        ts = time.perf_counter()
        history.enqueue([ts, None])
        threading.Thread()
        # encode_face

        cv2.imshow('Kiosk', frame)
        print(fps)
        print(history)
        print()

    cap.release()
    cv2.destroyAllWindows()

    __end = datetime.now()
    print(f"start_ts  {__start}")
    print(f"end_ts    {__end}")
    print(f"uptime    {__end - __start}")

if __name__ == '__main__':
    capture()