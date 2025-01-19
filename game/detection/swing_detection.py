import cv2
import mediapipe as mp
import numpy as np
import time

class CameraError(Exception):
    """Camera Error"""
    pass

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

# Threshold for swing detection
SWING_THRESHOLD = 0.4  # Adjust based on sensitivity
SWING_THRESHOLD_2 = 0.7 # Adjust based on sensitivity
MIN_SUSTAINED_FRAMES = 2 # Adjust based on sensitivity
SHOULDER_TO_ELBOW_THRESHOLD = 2.5 # Adjust based on sensitivity

def calculate_slope(point1, point2):
    """
    Calculate the slope of a line given two points.

<<<<<<< Updated upstream
    # Start capturing video from the webcam
    cap = cv2.VideoCapture(1)
=======
    Args:
        point1 (tuple): Coordinates of the first point (x1, y1).
        point2 (tuple): Coordinates of the second point (x2, y2).

    Returns:
        float: The slope of the line. Returns np.inf if the line is vertical.
    """
    x1, y1 = point1
    x2, y2 = point2
    
    # Check for vertical line to avoid division by zero
    if np.isclose(x1, x2):
        return None  # Infinite slope for a vertical line
    
    # Calculate the slope
    slope = np.abs(round(((y2 - y1) / (x2 - x1)),2))
    return slope

def detect_swing() -> bool:
    # Initialize camera
    cap = cv2.VideoCapture(0)


    # Raise error if camera doesn't work
    ret, frame = cap.read()
    if not ret:
        raise CameraError("Camera doesn't work")

    prev_wrist_position_right = None
    prev_wrist_position_left = None
    sustained_velocity_frames = 0
    slope_list = []
    velocity_list = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Exit if no frame is captured

        # Convert frame to RGB as MediaPipe expects RGB input
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Extract wrist coordinates
            landmarks = results.pose_landmarks.landmark
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]

            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
            left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]

            right_elbow_slope = calculate_slope((right_elbow.x,right_elbow.y),(right_shoulder.x,right_shoulder.y))
            left_elbow_slope = calculate_slope((left_elbow.x,left_elbow.y),(left_shoulder.x,left_shoulder.y))


            if prev_wrist_position_right is not None and prev_wrist_position_left is not None:
                # Calculate velocity
                right_velocity = round(np.abs(right_wrist.z - prev_wrist_position_right),2)
                left_velocity = round(np.abs(left_wrist.z - prev_wrist_position_left),2)
                velocity_list.append(right_velocity)
                slope_list.append(right_elbow_slope)

                # Check if velocity is above threshold
                if (right_velocity > SWING_THRESHOLD_2) and (right_elbow_slope < SHOULDER_TO_ELBOW_THRESHOLD):
                    cv2.putText(frame, "Swing Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    print(right_velocity,right_elbow_slope)
                    print("Swing detected!")
                    break
                elif (left_velocity > SWING_THRESHOLD_2) and (left_elbow_slope < SHOULDER_TO_ELBOW_THRESHOLD):
                    cv2.putText(frame, "Swing Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    print(left_velocity,left_elbow_slope)
                    print("Swing detected!")
                    break
                elif (right_velocity > SWING_THRESHOLD) and (right_elbow_slope < SHOULDER_TO_ELBOW_THRESHOLD):
                    sustained_velocity_frames += 1
                    if sustained_velocity_frames >= MIN_SUSTAINED_FRAMES:
                        cv2.putText(frame, "Swing Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        print("Swing detected!")
                        break
                elif (left_velocity > SWING_THRESHOLD) and (left_elbow_slope < SHOULDER_TO_ELBOW_THRESHOLD):
                    sustained_velocity_frames += 1
                    if sustained_velocity_frames >= MIN_SUSTAINED_FRAMES:
                        cv2.putText(frame, "Swing Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        print("Swing detected!")
                        break
                else:
                    sustained_velocity_frames = 0  # Reset if velocity drops below threshold

            # Update previous wrist positions
            prev_wrist_position_right = right_wrist.z
            prev_wrist_position_left = left_wrist.z

        # Show the video feed
        cv2.imshow("Arm Swing Detection", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            print(velocity_list)
            print(slope_list)
            return False

    cap.release()
    cv2.destroyAllWindows()
    print(velocity_list)
    print(slope_list)
    return True

# Run the function
detect_swing()
