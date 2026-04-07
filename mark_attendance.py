import cv2
import face_recognition
import pickle
import random
import csv
from datetime import datetime
from scipy.spatial import distance as dist
import numpy as np
import pyttsx3
from ui import draw_ui

# ===== VOICE ENGINE =====
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ========== LOAD ENCODINGS ==========
with open("encodings.pkl", "rb") as f:
    data = pickle.load(f)

known_encodings = data["encodings"]
known_names = data["names"]

# ========== BLINK FUNCTION ==========
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

# ========== ATTENDANCE ==========
marked_students = set()

def mark_attendance(name):
    if name not in marked_students:
        with open("attendance.csv", "a", newline="") as f:
            writer = csv.writer(f)
            time_now = datetime.now().strftime("%H:%M:%S")
            writer.writerow([name, time_now])

        marked_students.add(name)
        speak(f"{name} attendance marked")
        return f"{name} Marked ✅"
    return f"{name} Already ❌"

# ========== CHALLENGE ==========
challenges = ["BLINK", "LEFT", "RIGHT"]
current_challenge = random.choice(challenges)

speak(f"Please do {current_challenge}")

# ========== CAMERA ==========
cap = cv2.VideoCapture(0)

prev_positions = {}
status_msg = "Waiting..."

while True:
    ret, frame = cap.read()
    if not ret:
        break

    face_names = []
    verified_list = []

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, faces)

    for i, ((top, right, bottom, left), face_enc) in enumerate(zip(faces, encodings)):

        # ===== RECOGNITION =====
        name = "Unknown"
        if len(known_encodings) > 0:
            matches = face_recognition.compare_faces(known_encodings, face_enc, tolerance=0.5)
            distances = face_recognition.face_distance(known_encodings, face_enc)

            if len(distances) > 0:
                best_match_index = np.argmin(distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]

        face_names.append(name)

        # ===== MOVEMENT =====
        verified = False

        if name not in prev_positions:
            prev_positions[name] = left

        movement = None
        if left - prev_positions[name] > 5:
            movement = "RIGHT"
        elif prev_positions[name] - left > 5:
            movement = "LEFT"

        prev_positions[name] = left

        # ===== BLINK =====
        landmarks = face_recognition.face_landmarks(rgb)
        blink_detected = False

        if landmarks:
            for lm in landmarks:
                leftEye = lm['left_eye']
                rightEye = lm['right_eye']
                ear = (eye_aspect_ratio(leftEye) + eye_aspect_ratio(rightEye)) / 2.0

                if ear < 0.21:
                    blink_detected = True

        # ===== VERIFY =====
        if current_challenge == "BLINK" and blink_detected:
            verified = True
        elif current_challenge == "LEFT" and movement == "LEFT":
            verified = True
        elif current_challenge == "RIGHT" and movement == "RIGHT":
            verified = True

        verified_list.append(verified)

        # ===== ATTENDANCE =====
        if verified and name != "Unknown":
            status_msg = mark_attendance(name)

    # ===== UI =====
    frame = draw_ui(frame, faces, face_names, verified_list, current_challenge, status_msg)

    cv2.imshow("🔥 PRO MAX Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()