from PIL import Image, ImageSequence
from pathlib import Path
from datetime import datetime
from misc import FPS
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

cap = cv2.VideoCapture(0)
recent_face_check_ts = time.perf_counter()
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

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = []
    if not sleep or (sleep and (time.perf_counter() - recent_face_check_ts > 1)):
        face_locations = face_recognition.face_locations(image)
        recent_face_check_ts = time.perf_counter()

    if face_locations:
        sleep = False
        # add algo
    else:
        sleep = True


    if sleep:
        frame_count += 1
        frame_count %= len(gif)
        frame = gif[frame_count]

    cv2.imshow('Kiosk', frame)

    print(fps)
        
cap.release()
cv2.destroyAllWindows()

__end = datetime.now()
print(f"start_ts  {__start}")
print(f"end_ts    {__end}")
print(f"uptime    {__end - __start}")
