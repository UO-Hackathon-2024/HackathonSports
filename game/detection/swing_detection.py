import cv2
import mediapipe as mp
import numpy as np
import time

class CameraError(Exception):
    """camera Error"""
    pass


def swing_detection()->bool:
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_draw = mp.solutions.drawing_utils

    # Threshold for swing detection
    SWING_THRESHOLD = 0.1  # Adjust based on sensitivity
    CHEST_DISTANCE_THREASHOLD = 1
    prev_wrist_position = None  # To store previous wrist position
    last_swing_time = 0  # To track time of the last swing

    # Start capturing video from the webcam
    cap = cv2.VideoCapture(1)

    print("Press 'q' to exit.")
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
            current_time = time.time()
            if prev_wrist_position and (current_time - last_swing_time >= 5):  # Wait 5 seconds
                right_velocity = np.sqrt(
                    (right_wrist.x - prev_wrist_position[0]) ** 2 +
                    (right_wrist.y - prev_wrist_position[1]) ** 2
                )
                left_velocity= np.sqrt(
                    (right_wrist.x - prev_wrist_position[0]) ** 2 +
                    (right_wrist.y - prev_wrist_position[1]) ** 2
                )
                if (right_velocity > SWING_THRESHOLD and left_velocity > SWING_THRESHOLD and right_wrist_distance < CHEST_DISTANCE_THREASHOLD
                and left_wrist_distance < CHEST_DISTANCE_THREASHOLD):
                    cv2.putText(frame, "Swing Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    print("Swing detected!")
                    last_swing_time = current_time  # Update last swing time

            # Update previous wrist position
            prev_wrist_position = (right_wrist.x, right_wrist.y)

        # Show the video feed
        cv2.imshow("Arm Swing Detection", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


swing_detection()