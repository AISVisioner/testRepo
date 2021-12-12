from misc import *
from datetime import datetime
import numpy as np
import zmq
import sys
import multiprocessing
import uuid
import cv2
import base64
import face_recognition
import asyncio


def tprint(msg):
    print(msg)
    sys.stdout.flush()

class ServerTask(multiprocessing.Process):
    def __init__(self, num_workers=5):
        multiprocessing.Process.__init__(self)
        self.num_workers = num_workers

    def run(self):
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind('tcp://*:5570')

        backend = context.socket(zmq.DEALER)
        backend.bind('inproc://backend')

        workers = []
        for _ in range(self.num_workers):
            worker = ServerWorker(context)
            worker.start()
            workers.append(worker)


        zmq.proxy(frontend, backend)

        frontend.close()
        backend.close()
        context.term()

class ServerWorker(multiprocessing.Process):
    def __init__(self, context):
        multiprocessing.Process.__init__ (self)
        self.context = context
        self.id = uuid.uuid4()

    def run(self):
        worker = self.context.socket(zmq.DEALER)
        worker.connect('inproc://backend')
        identity = f"Worker-{str(self.id).split('-')[-1]}"
        tprint(f"[{identity}] started")
        while True:
            ident, msg = worker.recv_multipart()
            msg = str(msg, encoding='ascii')
            shape_str, msg = str(msg).split('__', 1)
            shape = tuple(map(int, shape_str.split('_')))

            msg = base64.decodebytes(bytes(msg, encoding='ascii'))
            msg = np.frombuffer(msg, dtype=np.uint8)
            frame = np.reshape(msg, shape)
            image = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
            boxes = face_recognition.face_locations(image)
            for box in boxes:
                facevec = face_recognition.face_encodings(image, [box])[0]
                worker.send_multipart([ident, base64.b64encode(facevec)])
                tprint(f"[{identity}] ...pong")
                break
        worker.close()

class ClientTask(multiprocessing.Process):
    def __init__(self, url=0):
        multiprocessing.Process.__init__(self)
        self.id = uuid.uuid4()
        self.url = url

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        identity = f"Client-{str(self.id).split('-')[-1]}"
        socket.identity = identity.encode('ascii')
        socket.connect('tcp://localhost:5570')
        tprint(f"{socket.identity} started")
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)

        cv2.namedWindow(identity, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(identity, 800, 800)
        font = cv2.FONT_HERSHEY_SIMPLEX

        cap = cv2.VideoCapture(self.url)
        fps = FPS()
        __start = datetime.now()
        while True:
            ret, frame = cap.read()
            if not ret:
                raise ValueError

            key = cv2.waitKey(1)
            if key == 27:
                tprint(f"[{identity}] exit")
                break

            cv2.imshow(identity, frame)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.resize(frame, dsize=(320, 240))
            # frame = cv2.resize(frame, dsize=(192, 144))

            # cv2.imshow(identity, frame)

            shape_bytes = ''
            for i in frame.shape:
                shape_bytes += str(i) + '_'
            shape_bytes += '_'
            shape_bytes = bytes(shape_bytes, encoding='ascii')

            socket.send_string(str(shape_bytes + base64.b64encode(frame), encoding='ascii'))
            tprint(f"[{identity}] ping...")

            sockets = dict(poll.poll(500))
            if socket in sockets:
                msg = socket.recv()
                tprint(f"[{identity}] received {msg}")
            
            tprint(f"FPS\t{fps}\n")

        cap.release()
        cv2.destroyAllWindows()

        __end = datetime.now()
        tprint(f"start_ts  {__start}")
        tprint(f"end_ts    {__end}")
        tprint(f"uptime    {__end - __start}")

        socket.close()
        context.term()

def main():
    server = ServerTask(num_workers=5)
    server.start()

    time.sleep(1)

    client = ClientTask(url=0)
    client.start()

    server.join()


if __name__ == "__main__":
    main()