import sys
import cv2 as cv
import face_recognition # depencancy on dlib
import uuid

COUNT = 5

users = {}

img_array = []

def main(argv):
    url = None
    if len(argv) < 1:
        raise ValueError("No input error")
    if argv[0] == '0':
        url = 0
        print("Initializing url as default webcam (0)")
    elif argv[0].startswith("rtsp://"):
        url = argv[0]
        print("Initializing with RTSP")
    else:
        url = argv[0]
        print("Initializing with custom source")
    
    cap = cv.VideoCapture(url)
    encodings = []
    matched = False



    ###
    count = None
    while True:
        ret, frame = cap.read()
        if not ret:
            out = cv.VideoWriter('lav_roi.avi', cv.VideoWriter_fourcc(*'DIVX'), 29.97, (608, 1080))
            for img in img_array:
                out.write(img)
            out.release()
            print('done!')
            break

            # raise ValueError("No frame error")

        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(image)
        for box in boxes:
            encoding = face_recognition.face_encodings(image, [box])[0]
            if len(encodings) >= COUNT:
                matches = face_recognition.compare_faces(encodings, encoding)
                del encodings[0]
                if False not in matches:
                    matched = True
            encodings.append(encoding)
            break

        ###
        frame = cv.putText(frame, f'matched {matched}', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv.LINE_AA)

        if matched:
            registered = False
            user_matched = face_recognition.compare_faces(list(users.values()), encoding)
            for i, user_matched in enumerate(user_matched):
                if user_matched:
                    print(f'matched no.{i} {list(users)[i]}')

                    ###
                    frame = cv.putText(frame, f'matched no.{i}', (10, 60), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv.LINE_AA)

                    registered = True
            if not registered:
                user_id = str(uuid.uuid4())
                users[user_id] = encoding
                print(f'new user {user_id}')

                ###
                frame = cv.putText(frame, f'new user', (10, 90), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv.LINE_AA)
                count = 1


            frame = cv.rectangle(frame, (boxes[-1][1], boxes[-1][0]) , (boxes[-1][3], boxes[-1][2]), (0,255,0), 1)

        if count is not None:
            frame = cv.putText(frame, f'new user', (10, 90), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv.LINE_AA)
            count += 1
            if count > 25:
                count = None

        img_array.append(frame)

        matched = False
    
    # out = cv.VideoWriter('fullhouse_roi.avi', cv.VideoWriter_fourcc(*'DIVX'), 15, (640, 480))
    # for img in img_array:
    #     out.write(img)
    # out.release()

if __name__ == "__main__":
    main(sys.argv[1:])