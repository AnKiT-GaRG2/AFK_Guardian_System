try:
    import cv2
except ImportError:
    cv2 = None
try:
    import mediapipe as mp
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
except (AttributeError, ImportError):
    # Fallback if mediapipe is not available or doesn't have solutions
    mp = None
    mp_face_mesh = None
    face_mesh = None
try:
    import numpy as np
except ImportError:
    np = None
import os
import time
import threading
from threading import Lock
from collections import deque, Counter

# Eye landmark indices
LEFT_EYE = [33, 133]
RIGHT_EYE = [362, 263]
LEFT_EYE_VERTICAL = [159, 145]
RIGHT_EYE_VERTICAL = [386, 374]

EAR_THRESHOLD = 0.25

# Detection bandwidth/tuning (can be overridden via environment variables)
STATE_SMOOTHING_FRAMES = int(os.getenv("EYE_STATE_SMOOTHING_FRAMES", "12"))
FACE_MIN_NEIGHBORS = int(os.getenv("EYE_FACE_MIN_NEIGHBORS", "4"))
EYE_MIN_NEIGHBORS = int(os.getenv("EYE_MIN_NEIGHBORS", "4"))
MIN_FACE_SIZE = int(os.getenv("EYE_MIN_FACE_SIZE", "40"))
MIN_EYE_RATIO = float(os.getenv("EYE_MIN_EYE_RATIO", "0.07"))
MAX_EYE_RATIO = float(os.getenv("EYE_MAX_EYE_RATIO", "0.60"))

# OpenCV capture
cap = cv2.VideoCapture(0) if cv2 is not None else None

# Eye state tracking variables
eyes_open = 0
eyes_closed = 0
eyes_not_detected = 0
open_time = 0
closed_time = 0
away_time = 0
last_state = None
state_start_time = time.time()
state_lock = Lock()
state_history = deque(maxlen=max(1, STATE_SMOOTHING_FRAMES))

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') if cv2 is not None else None
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml') if cv2 is not None else None


def _smooth_state(raw_state):
    state_history.append(raw_state)
    state_counts = Counter(state_history)
    return state_counts.most_common(1)[0][0]

def update_state_time(current_state):
    """Update time spent in each state."""
    global last_state, state_start_time, open_time, closed_time, away_time
    with state_lock:
        current_time = time.time()
        if last_state != current_state:
            elapsed = current_time - state_start_time
            if last_state == "open":
                open_time += elapsed
            elif last_state == "closed":
                closed_time += elapsed
            elif last_state == "away":
                away_time += elapsed
            last_state = current_state
            state_start_time = current_time

def return_data():
    """Return the eye tracking statistics."""
    with state_lock:
        current_time = time.time()
        elapsed_current_state = current_time - state_start_time

        current_open_time = open_time
        current_closed_time = closed_time
        current_away_time = away_time

        if last_state == "open":
            current_open_time += elapsed_current_state
        elif last_state == "closed":
            current_closed_time += elapsed_current_state
        elif last_state == "away":
            current_away_time += elapsed_current_state

        return {
            "eyes_open_time": round(current_open_time, 2),
            "eyes_closed_time": round(current_closed_time, 2),
            "eyes_not_detected_time": round(current_away_time, 2)
        }

def reset_data():
    """Reset the time counters every minute."""
    global open_time, closed_time, away_time, state_start_time
    with state_lock:
        open_time = 0
        closed_time = 0
        away_time = 0
        state_start_time = time.time()


def _get_state_from_frame(image):
    if cv2 is None:
        return "away"

    if face_mesh is not None:
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_image)
        if not results.multi_face_landmarks:
            return "away"

        face_landmarks = results.multi_face_landmarks[0].landmark

        left_horizontal = abs(face_landmarks[LEFT_EYE[0]].x - face_landmarks[LEFT_EYE[1]].x)
        right_horizontal = abs(face_landmarks[RIGHT_EYE[0]].x - face_landmarks[RIGHT_EYE[1]].x)
        left_vertical = abs(face_landmarks[LEFT_EYE_VERTICAL[0]].y - face_landmarks[LEFT_EYE_VERTICAL[1]].y)
        right_vertical = abs(face_landmarks[RIGHT_EYE_VERTICAL[0]].y - face_landmarks[RIGHT_EYE_VERTICAL[1]].y)

        left_ear = left_vertical / left_horizontal if left_horizontal > 0 else 0
        right_ear = right_vertical / right_horizontal if right_horizontal > 0 else 0
        avg_ear = (left_ear + right_ear) / 2

        return "open" if avg_ear >= EAR_THRESHOLD else "closed"

    if face_cascade is not None and eye_cascade is not None:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=max(1, FACE_MIN_NEIGHBORS),
            minSize=(MIN_FACE_SIZE, MIN_FACE_SIZE)
        )
        if len(faces) == 0:
            return "away"

        x, y, w, h = max(faces, key=lambda region: region[2] * region[3])
        roi_gray = gray[y:y + h, x:x + w]
        min_eye_size = max(8, int(min(w, h) * MIN_EYE_RATIO))
        max_eye_size = max(min_eye_size + 1, int(min(w, h) * MAX_EYE_RATIO))

        eyes = eye_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.03,
            minNeighbors=max(1, EYE_MIN_NEIGHBORS),
            minSize=(min_eye_size, min_eye_size),
            maxSize=(max_eye_size, max_eye_size)
        )

        if len(eyes) >= 1:
            return "open"

        # Face present but eyes not detected in this frame: keep user as open instead of over-penalizing.
        return "open"

    return "away"

def detect_eyes():
    """Main function to run eye tracking."""
    global eyes_not_detected, last_state

    if cv2 is None or cap is None:
        print("OpenCV not available, skipping eye tracking")
        return

    if face_mesh is None:
        print("MediaPipe not available, using OpenCV fallback for eye state")

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Failed to capture frame")
            continue

        image = cv2.flip(image, 1)
        current_state = _smooth_state(_get_state_from_frame(image))
        update_state_time(current_state)

        cv2.imshow('Eye Tracking', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            update_state_time(last_state)
            break

    cap.release()
    cv2.destroyAllWindows()

def start_eye_tracking():
    """Start the eye tracking in a separate thread."""
    tracking_thread = threading.Thread(target=detect_eyes, daemon=True)
    tracking_thread.start()

# Only run tracking if script is executed directly
if __name__ == "__main__":
    start_eye_tracking()
