import cv2
import mediapipe as mp
import time

mp_face_mesh = mp.solutions.face_mesh


def check_attention():

    cap = cv2.VideoCapture(0)

    blink_count = 0
    attention_frames = 0
    total_frames = 0
    drowsy_frames = 0
    closed_eyes_frames = 0
    recent_scores = []
    attention_score = 0
    last_print = time.time()

    with mp_face_mesh.FaceMesh(
        max_num_faces=5,          # Multiple face detect
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:

        
        start_time = time.time()
        
        while True:

            success, frame = cap.read()
            if not success:
                break

            total_frames += 1

            frame = cv2.flip(frame, 1)   # Mirror view
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = face_mesh.process(rgb)

            head_direction = "No Face"
            eye_contact = "No"
            sleep_status = "Awake"
            phone_status = "No"
            multiple_faces = 0
            yaw_degree = 0
            pitch_degree = 0

            if results.multi_face_landmarks:

                multiple_faces = len(results.multi_face_landmarks)

                # Use first face as main face
                face_landmarks = results.multi_face_landmarks[0]

                # -------------------------------
                # LANDMARKS
                # -------------------------------
                nose = face_landmarks.landmark[1]

                left_eye_top = face_landmarks.landmark[159]
                left_eye_bottom = face_landmarks.landmark[145]

                right_eye_top = face_landmarks.landmark[386]
                right_eye_bottom = face_landmarks.landmark[374]

                # Iris landmarks
                left_iris = face_landmarks.landmark[468]
                right_iris = face_landmarks.landmark[473]

                # Eye corners
                left_eye_left = face_landmarks.landmark[33]
                left_eye_right = face_landmarks.landmark[133]

                right_eye_left = face_landmarks.landmark[362]
                right_eye_right = face_landmarks.landmark[263]

                # -------------------------------
                # REAL BLINK DETECTION
                # -------------------------------
                left_eye_height = abs(left_eye_top.y - left_eye_bottom.y)
                right_eye_height = abs(right_eye_top.y - right_eye_bottom.y)

                avg_eye_height = (left_eye_height + right_eye_height) / 2

                if avg_eye_height < 0.012:
                    closed_eyes_frames += 1
                else:
                    if closed_eyes_frames > 2:
                        blink_count += 1
                    closed_eyes_frames = 0

                # -------------------------------
                # SLEEP DETECTION
                # -------------------------------
                if closed_eyes_frames > 25:
                    drowsy_frames += 1
                    sleep_status = "Sleepy"

                # -------------------------------
                # HEAD ANGLE DEGREE DETECTION
                # -------------------------------
                head_x = nose.x - 0.5
                head_y = nose.y - 0.5

                yaw_degree = int(head_x * 120)
                pitch_degree = int(head_y * 120)

                if yaw_degree < -12:
                    head_direction = "Looking Left"

                elif yaw_degree > 12:
                    head_direction = "Looking Right"

                elif pitch_degree < -10:
                    head_direction = "Looking Up"

                elif pitch_degree > 12:
                    head_direction = "Looking Down"

                else:
                    head_direction = "Looking Center"

                # -------------------------------
                # IRIS BASED EYE CONTACT
                # -------------------------------
                left_ratio = (
                    (left_iris.x - left_eye_left.x) /
                    (left_eye_right.x - left_eye_left.x + 0.0001)
                )

                right_ratio = (
                    (right_iris.x - right_eye_left.x) /
                    (right_eye_right.x - right_eye_left.x + 0.0001)
                )

                avg_ratio = (left_ratio + right_ratio) / 2

                if 0.35 < avg_ratio < 0.65 and head_direction == "Looking Center":
                    eye_contact = "Yes"
                else:
                    eye_contact = "No"

                # -------------------------------
                # ATTENTION SCORE
                # -------------------------------
                if eye_contact == "Yes" and head_direction == "Looking Center":
                    pass

                # SIMPLE PHONE DETECT
                phone_status = "No"

                if head_direction == "Looking Down":
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray, 80, 180)

                    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    for cnt in contours:
                        x, y, w, h = cv2.boundingRect(cnt)
                        area = w * h
                        ratio = h / (w + 0.01)

                        if area > 20000 and 1.5 < ratio < 2.4:
                            phone_status = "Phone Detected"
                            break

            # -------------------------------
            # FINAL ATTENTION %
            # -------------------------------
            current_focus = 0

            if multiple_faces == 0:
                current_focus = 0

            else:
                if eye_contact == "Yes":
                    current_focus += 35
                else:
                    current_focus += 5

                if head_direction == "Looking Center":
                    current_focus += 30
                elif head_direction in ["Looking Left", "Looking Right"]:
                    current_focus += 15
                else:
                    current_focus += 5

                if sleep_status == "Awake":
                    current_focus += 20

                if phone_status == "No":
                    current_focus += 15
                else:
                    current_focus -= 15

                if multiple_faces > 1:
                    current_focus -= 10

                if blink_count > 35:
                    current_focus -= 10

            current_focus = max(0, min(100, current_focus))

            recent_scores.append(current_focus)

            if len(recent_scores) > 50:
                recent_scores.pop(0)

            attention_score = sum(recent_scores) / len(recent_scores)
            # -------------------------------
            # PRINT EVERY 2 SEC
            # -------------------------------
            if time.time() - last_print > 2:

                print("Head Direction:", head_direction)
                print("Eye Contact:", eye_contact)
                print("Yaw Degree:", yaw_degree if results.multi_face_landmarks else 0)
                print("Pitch Degree:", pitch_degree if results.multi_face_landmarks else 0)
                print("Blink Count:", blink_count)
                print("Sleep Status:", sleep_status)
                print("Phone Use:", phone_status)
                print("Faces Detected:", multiple_faces)
                print("Attention %:", int(attention_score))
                print("--------------------------")

                last_print = time.time()

            cv2.imshow("Attention Tracking", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break
            if time.time() - start_time > 30:
               break

    cap.release()
    cv2.destroyAllWindows()

    # -------------------------------
    # FOCUS LEVEL
    # -------------------------------
    if attention_score > 70:
        focus_level = "High"
    elif attention_score > 40:
        focus_level = "Medium"
    else:
        focus_level = "Low"

    print("\nFinal Focus Level:", focus_level)
    print("Total Blinks:", blink_count)
    print("Drowsy Frames:", drowsy_frames)

    return {
        "focus": focus_level,
        "blinks": blink_count,
        "attention_percent": int(attention_score),
        "drowsy": drowsy_frames
    }

# ✅ NAYA FUNCTION — single frame se attention check
def detect_attention_from_image(image_bytes: bytes) -> dict:
    frame = cv2.imdecode(
        bytearray(image_bytes),
        cv2.IMREAD_COLOR
    )
    if frame is None:
        return {"focus": "Low", "attention_percent": 0, "blinks": 0, "drowsy": 0}

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    with mp_face_mesh.FaceMesh(
        max_num_faces=5,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:
        results = face_mesh.process(rgb)

    if not results.multi_face_landmarks:
        return {"focus": "Low", "attention_percent": 0, "blinks": 0, "drowsy": 0}

    face_landmarks = results.multi_face_landmarks[0]
    nose = face_landmarks.landmark[1]
    head_x = nose.x - 0.5
    yaw_degree = int(head_x * 120)

    left_iris = face_landmarks.landmark[468]
    left_eye_left = face_landmarks.landmark[33]
    left_eye_right = face_landmarks.landmark[133]
    right_eye_left = face_landmarks.landmark[362]
    right_eye_right = face_landmarks.landmark[263]

    left_ratio = (left_iris.x - left_eye_left.x) / (left_eye_right.x - left_eye_left.x + 0.0001)
    right_ratio = (left_iris.x - right_eye_left.x) / (right_eye_right.x - right_eye_left.x + 0.0001)
    avg_ratio = (left_ratio + right_ratio) / 2

    looking_center = abs(yaw_degree) < 12
    eye_contact = 0.35 < avg_ratio < 0.65 and looking_center

    score = 0
    if eye_contact:
        score += 35
    if looking_center:
        score += 30
    score += 20  # awake assumed
    score += 15  # no phone assumed

    focus_level = "High" if score > 70 else "Medium" if score > 40 else "Low"
    return {
        "focus": focus_level,
        "attention_percent": score,
        "blinks": 0,
        "drowsy": 0
    }
