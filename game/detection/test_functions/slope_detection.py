import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

def calculate_slope(point1, point2):
    """
    Calculate the slope of a line given two points.

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
    slope = round(((y2 - y1) / (x2 - x1)),2)
    return slope


def measure_arm_slope(arm:str):
    """
    Measure the angle between the arm and body in real-time using MediaPipe Pose.
    """
    cap = cv2.VideoCapture(1)
    slopes = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            landmarks = results.pose_landmarks.landmark

            if arm == "right":
                # Get key landmarks for the right arm
                shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y,]
                elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y,]
            else:
                # Get key landmarks for the left arm
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y,]

            
            arm_slope = calculate_slope(shoulder, elbow)
            slopes.append(arm_slope)

        # Show the video feed
        cv2.imshow("Arm Angle Measurement", frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(slopes)

measure_arm_slope("right")



