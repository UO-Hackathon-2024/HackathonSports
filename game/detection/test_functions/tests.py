import cv2
import mediapipe as mp
import numpy as np
import time
import matplotlib.pyplot as plt

# Initialize MediaPipe Pose and drawing utilities
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

# Thresholds
SWING_THRESHOLD = 0.3  # Increase to filter only fast movements
CHEST_DISTANCE_THRESHOLD = 1.0
MIN_SUSTAINED_FRAMES = 3  # Minimum frames with high velocity to qualify as a swing

# Variables
prev_wrist_position_right = None
prev_wrist_position_left = None
last_swing_time = 0
timestamps = []
right_wrist_velocities = []
sustained_velocity_frames = 0

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)

print("Press 'q' to exit.")
start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB as MediaPipe expects RGB input
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    # Draw pose landmarks and process detection
    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Extract wrist coordinates
        landmarks = results.pose_landmarks.landmark
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]

        chest_x = (right_shoulder.x + left_shoulder.x) / 2
        chest_y = (right_shoulder.y + left_shoulder.y) / 2

        right_wrist_distance = np.sqrt((right_wrist.x - chest_x) ** 2 + (right_wrist.y - chest_y) ** 2)
        left_wrist_distance = np.sqrt((left_wrist.x - chest_x) ** 2 + (left_wrist.y - chest_y) ** 2)

        # Detect swing for the right wrist
        current_time = time.time() - start_time
        if prev_wrist_position_right and ((current_time-last_swing_time) > 0.8):
            # Calculate velocity
            right_velocity = np.abs(right_wrist.z - prev_wrist_position_right)
            left_velocity = np.abs(left_wrist.z - prev_wrist_position_left)

            # Check if velocity is above threshold
            if (right_velocity > SWING_THRESHOLD or left_velocity > SWING_THRESHOLD) and (
                    right_wrist_distance < CHEST_DISTANCE_THRESHOLD or
                    left_wrist_distance < CHEST_DISTANCE_THRESHOLD):
                sustained_velocity_frames += 1
                if sustained_velocity_frames >= MIN_SUSTAINED_FRAMES:
                    cv2.putText(frame, "Swing Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    print("Swing detected!")
                    last_swing_time = current_time
                    timestamps.append(current_time)
                    right_wrist_velocities.append(right_velocity)
                    sustained_velocity_frames = 0  # Reset sustained velocity counter
            else:
                sustained_velocity_frames = 0  # Reset if velocity drops below threshold
        # Update previous wrist position
        prev_wrist_position_right = right_wrist.z
        prev_wrist_position_left = left_wrist.z

    # Show the video feed
    cv2.imshow("Arm Swing Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Plot the velocity over time
if timestamps and right_wrist_velocities:
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, right_wrist_velocities, label='Right Wrist Velocity')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity')
    plt.title('Right Wrist Velocity Over Time')
    plt.legend()
    plt.grid()
    plt.show()





