import sys
import cv2 as cv
import face_recognition # depencancy on dlib

def main(argv):
    url = None
    if len(argv) < 1:
        raise ValueError("No input error")
    if argv[0].startswith("rtsp://"):
        url = argv[0]
    else:
        print("Invalid rtsp url. Initializing url as default webcam (0)")
        url = 0
    
    cap = cv.VideoCapture(url)
    encodings = []
    matched = False
    while True:
        ret, frame = cap.read()
        if not ret:
            raise ValueError("No frame error")
        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(image)
        for box in boxes:
            encoding = face_recognition.face_encodings(image, [box])[0]
            if len(encodings) >= 5:
                matches = face_recognition.compare_faces(encodings, encoding)
                del encodings[0]
                if False not in matches:
                    matched = encodings[0]
            encodings.append(encoding)
            break
        if matched:
            pass
        matched = False

if __name__ == "__main__":
    main(sys.argv[1:])