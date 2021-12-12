from pathlib import Path
from datetime import datetime
from face_recognition.api import compare_faces, face_locations
from misc import History, FPS
import asyncio
import threading
import numpy as np
import cv2
import face_recognition
import os
import time


async def encode_face(lock, history, ts, frame):
    print('started')
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(frame)
    if boxes:
        for box in boxes:
            encoding = face_recognition.face_encodings(frame, [box])[0]
            break
    else: return
    async with lock:
        idx = history.find(value=ts, place=lambda x: x[0])
        if idx is not None:
            history[idx][1] = encoding

async def capture(url=0):
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
        task = asyncio.create_task(encode_face(lock, history, ts, frame))

        time.sleep(1)
        
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
    asyncio.run(capture())