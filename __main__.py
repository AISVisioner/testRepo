from settings import settings
from multiprocessing import Process
from threading import Thread
import time
import cv2
import face_recognition

def detect(frame):
    # current_ts - caputred_ts < 0.2
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(frame)
    encoding = None
    for box in boxes:
        encoding = face_recognition.face_encodings(frame, [box])[0]
        break
    print(clock)
    return encoding

fpss = []

cap = cv2.VideoCapture(settings['url'])
clock = 0
# procs = []
while True:
    if not clock:
        clock = time.perf_counter()

    start_ts = time.perf_counter()

    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Kiosk', frame)
    c = cv2.waitKey(1)
    if c == 27:
        break
    
    #TODO: pass arg(ts)
    proc = Process(target=detect, args=[frame])
    proc.start()
    # procs.append(proc)

    end_ts = time.perf_counter()

    if end_ts - clock > 0.1:
        print(f'{1/(end_ts-start_ts):>5.1f} FPS ', end='\r')
        fpss.append(1/(end_ts-start_ts))
        print("fpss", sum(fpss)/len(fpss))
        clock = 0



cap.release()
cv2.destroyAllWindows()