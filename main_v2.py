from asyncio.tasks import create_task
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

__start = datetime.now()

cv2.namedWindow('Kiosk', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Kiosk', 800, 800)
font = cv2.FONT_HERSHEY_SIMPLEX

root_path = Path(__file__).parent
gif_path = root_path / 'img' / 'loading_04.gif'
cap = cv2.VideoCapture(str(gif_path))
gif = []

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gif.append(frame)
cap.release()

history = History(size=4)
lock = threading.Lock()

def encode_face(lock, ts, frame):
    global history
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(frame)
    if boxes:
        for box in boxes:
            encoding = face_recognition.face_encodings(frame, [box])[0]
            break
    else:
        return
    lock.acquire()
    idx = history.find(value=ts, place=lambda x: x[0])
    if idx is not None:
        history[idx][1] = encoding
    lock.release()

def compare_faces(lock, encodings, encoding):
    global specifiable
    global started_comparing
    match = all(face_recognition.compare_faces(encoding_history, detected_encoding))
    lock.acquire()
    specifiable = started_comparing = match
    lock.release()

def lock_delay(lock, duration):
    global specifiable
    global sleep
    time.sleep(duration)
    lock.acquire()
    specifiable = False
    sleep = True
    lock.release()

async def create_thread():
    threading.Thread(target=encode_face, args=(lock, ts, frame), daemon=True).start()


cap = cv2.VideoCapture(0)
sleep = True
frame_count = -1

fps = FPS()
while True:
    ret, frame = cap.read()
    if not ret:
        raise ValueError

    key = cv2.waitKey(1)
    if key == 27 or key == ord('q'):
        print("Exiting...")
        break

    ts = time.perf_counter()
    history.enqueue([ts, None])
    task = asyncio.create_task(create_thread())
    # threading.Thread(target=encode_face, args=(lock, ts, frame), daemon=True).start()
    # thread.start()

    # detected_ts = None
    # detected_encoding = None
    # for ts, encoding in reversed(history):
    #     if encoding is not None and time.perf_counter() - ts < 1:
    #         sleep = False
    #         detected_ts = ts
    #         detected_encoding = encoding
    #         break

    

    # if started_comparing:
    #     sleep = False

    # if not specifiable and not started_comparing:
    #     ts = time.perf_counter()
    #     history.enqueue([ts, None])
    #     thread = threading.Thread(target=encode_face, args=(lock, ts, frame), daemon=True)
    #     thread.start()

    #     sleep = True
    #     detected_ts = None
    #     detected_encoding = None
    #     for ts, encoding in reversed(history):
    #         if encoding is not None and time.perf_counter() - ts < 1:
    #             sleep = False
    #             detected_ts = ts
    #             detected_encoding = encoding
    #             break

    #     if detected_encoding is not None:
    #         encoding_history = [face_locations for ts, face_locations in history if detected_ts > ts >= detected_ts-0.5]
    #         if len([x for x in encoding_history if x is None]) == 0:
    #             thread = threading.Thread(target=compare_faces, args=(lock, encoding_history, detected_encoding), daemon=True)
    #             thread.start()
    #             started_comparing = True

    # elif specifiable:
    #     started_comparing = False
    #     thread = threading.Thread(target=lock_delay, args=(lock, 3), daemon=True)
    #     thread.start()

    
    # if sleep:
    #     frame_count += 1
    #     frame_count %= len(gif)
    #     frame = gif[frame_count]
    # else:
    #     cv2.flip(frame, 1)
    

    print(history)
    # time.sleep(.05)

    cv2.imshow('Kiosk', frame)

    print(fps)

cap.release()
cv2.destroyAllWindows()

__end = datetime.now()
print(f"start_ts  {__start}")
print(f"end_ts    {__end}")
print(f"uptime    {__end - __start}")
