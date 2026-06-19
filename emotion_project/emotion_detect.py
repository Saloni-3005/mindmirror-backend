import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os
import time
from collections import Counter

# BASE_DIR = os.path.dirname(__file__)
# model_path = os.path.join(BASE_DIR, "emotion_model.keras")
# model = load_model(model_path)

BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "emotion_model.keras")
model = None

def get_model():
    global model
    if model is None:
        model = load_model(model_path)
    return model
emotion_labels = ['Angry','Disgust','Fear','Happy','Sad','Surprise','Neutral']

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

def detect_face_emotion():

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 640)
    cap.set(4, 480)

    emotion_list = []

    start_time = time.time()

    print("Detecting face emotion for 30 seconds...")

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Camera frame not received")
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:

            face = frame[y:y+h,x:x+w]

            face = cv2.resize(face,(48,48))
            face = face/255.0
            face = np.reshape(face,(1,48,48,3))

            prediction = get_model().predict(face, verbose=0)
            emotion = emotion_labels[np.argmax(prediction)]

            emotion_list.append(emotion)

            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

            cv2.putText(frame,emotion,(x,y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

        cv2.imshow("Emotion Detector",frame)

        # 30 seconds complete
        if time.time() - start_time > 30:
            break

        # emergency exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if len(emotion_list) > 0:
        final_emotion = Counter(emotion_list).most_common(1)[0][0]
    else:
        final_emotion = "Neutral"

    print("Final Detected Face Emotion:", final_emotion)

    return final_emotion

# ✅ NAYA FUNCTION — API use karega
def detect_emotion_from_image(image_bytes: bytes) -> str:
    nparr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if frame is None:
        return "Neutral"
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 3, minSize=(30, 30))
    emotion_list = []
    for (x, y, w, h) in faces:
        face = cv2.resize(frame[y:y+h, x:x+w], (48, 48))
        face = np.reshape(face / 255.0, (1, 48, 48, 3))
        prediction = get_model().predict(face, verbose=0)
        emotion_list.append(emotion_labels[np.argmax(prediction)])
    return Counter(emotion_list).most_common(1)[0][0] if emotion_list else "Neutral"