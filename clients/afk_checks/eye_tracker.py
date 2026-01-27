import cv2
try:
    import mediapipe as mp
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
except (AttributeError, ImportError):
    # Fallback if mediapipe is not available or doesn't have solutions
    mp = None
    mp_face_mesh = None
    face_mesh = None
import numpy as np
import time
import threading

# Eye landmark indices
LEFT_EYE = [33, 133]
RIGHT_EYE = [362, 263]
LEFT_EYE_VERTICAL = [159, 145]
RIGHT_EYE_VERTICAL = [386, 374]

EAR_THRESHOLD = 0.25

# OpenCV capture
cap = cv2.VideoCapture(0)

# Eye state tracking variables
eyes_open = 0
eyes_closed = 0
eyes_not_detected = 0
open_time = 0
closed_time = 0
away_time = 0
last_state = None
state_start_time = time.time()

def update_state_time(current_state):
    """Update time spent in each state."""
    global last_state, state_start_time, open_time, closed_time, away_time
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
    return {
        "eyes_open_time": open_time,
        "eyes_closed_time": closed_time,
        "eyes_not_detected_time": away_time
    }

def reset_data():
    """Reset the time counters every minute."""
    global open_time, closed_time, away_time
    open_time = 0
    closed_time = 0
    away_time = 0

def detect_eyes():
    """Main function to run eye tracking."""
    global eyes_not_detected, last_state

    if face_mesh is None:
        print("MediaPipe not available, skipping eye tracking")
        return

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Failed to capture frame")
            continue

        image = cv2.flip(image, 1)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_image)

        if not results.multi_face_landmarks:
            eyes_not_detected += 2
            update_state_time("away")
        else:
            update_state_time("open")

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
