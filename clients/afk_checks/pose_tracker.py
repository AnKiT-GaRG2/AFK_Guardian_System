import cv2 as cv
import mediapipe as mp
import time

# Initialize mediapipe pose class and drawing utilities
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

# Start video capture
cap = cv.VideoCapture(0)

# Initialize time tracking variables
start_time = time.time()
standing_time = 0
sitting_time = 0
hands_up_time = 0
last_state = None
state_start_time = time.time()

def update_state_time(current_state):
    """Update time spent in each state"""
    global last_state, state_start_time, standing_time, sitting_time, hands_up_time
    
    current_time = time.time()
    if last_state != current_state:
        elapsed = current_time - state_start_time
        if last_state == "Standing":
            standing_time += elapsed
        elif last_state == "Sitting":
            sitting_time += elapsed
        elif last_state == "Hands Up":
            hands_up_time += elapsed
            
        last_state = current_state
        state_start_time = current_time

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture frame")
        continue

    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        
        # Check visibility of landmarks
        left_hip = results.pose_landmarks.landmark[23]
        right_hip = results.pose_landmarks.landmark[24]
        left_wrist = results.pose_landmarks.landmark[15]
        right_wrist = results.pose_landmarks.landmark[16]
        VISIBILITY_THRESHOLD = 0.5
        
        # Determine states
        both_hips_visible = (left_hip.visibility > VISIBILITY_THRESHOLD and 
                           right_hip.visibility > VISIBILITY_THRESHOLD)
        both_hands_up = (left_wrist.visibility > VISIBILITY_THRESHOLD and 
                        right_wrist.visibility > VISIBILITY_THRESHOLD)
        
        # Determine current state
        if both_hands_up:
            current_state = "Hands Up"
            color = (255, 165, 0)  # Orange
        else:
            current_state = "Standing" if both_hips_visible else "Sitting"
            color = (0, 255, 0) if both_hips_visible else (0, 0, 255)
        
        update_state_time(current_state)
        
        # Draw status on image
        cv.putText(img, f"State: {current_state}", (10, 30),
                  cv.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        # Display time statistics
        cv.putText(img, f"Standing Time: {standing_time:.1f}s", (10, 70),
                  cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv.putText(img, f"Sitting Time: {sitting_time:.1f}s", (10, 100),
                  cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv.putText(img, f"Hands Up Time: {hands_up_time:.1f}s", (10, 130),
                  cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Print real-time statistics to console
        print(f"\rStanding: {standing_time:.1f}s | Sitting: {sitting_time:.1f}s | Hands Up: {hands_up_time:.1f}s", end="")
    
    cv.imshow("Pose Detection", img)

    if cv.waitKey(1) & 0xFF == ord('d'):
        update_state_time(current_state)
        break

# Print final statistics
print("\n\nFinal Statistics:")
print(f"Total Standing Time: {standing_time:.1f} seconds")
print(f"Total Sitting Time: {sitting_time:.1f} seconds")
print(f"Total Hands Up Time: {hands_up_time:.1f} seconds")

cap.release()
cv.destroyAllWindows()