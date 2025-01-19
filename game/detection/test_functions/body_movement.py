import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

def calculate_distance(point1, point2):
    """
    Calculate the Euclidean distance between two 3D points.
    
    Parameters:
        point1 (list or array): [x, y, z] coordinates of the first point.
        point2 (list or array): [x, y, z] coordinates of the second point.

    Returns:
        float: Euclidean distance between the two points.
    """
    return np.sqrt((point1[0] - point2[0])**2 +
                   (point1[1] - point2[1])**2 +
                   (point1[2] - point2[2])**2)

def measure_wrist_to_shoulder_distances():
    """
    Measure the distances between wrists and shoulders in real-time using a webcam.
    """
    cap = cv2.VideoCapture(1)

    right_wrist_distances = []
    left_wrist_distances = []

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

            # Get wrist and shoulder coordinates
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y,
                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST].z]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y,
                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].z]
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].z]
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].z]

            # Calculate distances
            left_distance = calculate_distance(left_wrist, left_shoulder)
            right_distance = calculate_distance(right_wrist, right_shoulder)

            right_wrist_distances.append(left_distance)
            left_wrist_distances.append(right_distance)

            # Display distances on the video feed
            

        # Show the video feed
        cv2.imshow("Wrist to Shoulder Distance", frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(right_wrist_distances)
    print(left_wrist_distances)


def register_movement():
    """
    Measure the distances between wrists and shoulders in real-time using a webcam.
    """
    cap = cv2.VideoCapture(0)

    hip_movement_array = []
    previous_mid_point = None

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

            # Get wrist and shoulder coordinates
            mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            landmarks = results.pose_landmarks.landmark

            # Get key points for posture analysis
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP].y,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP].z,]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y,
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP].z]

            # Calculate shoulder and hip midpoint
            hips_midpoint = np.mean([left_hip, right_hip], axis=0)

            if previous_mid_point:
               movement = np.abs(np.array(hips_midpoint) - np.array(hips_midpoint))
               previous_mid_point = hips_midpoint
               hip_movement_array.append(movement)
            

        # Show the video feed
        cv2.imshow("Wrist to Shoulder Distance", frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(hip_movement_array)


def calculate_angle(point_a, point_b, point_c):
    """
    Calculate the angle between three points: A (shoulder), B (elbow), and C (wrist).
    Parameters:
        point_a (list): [x, y, z] coordinates of point A (shoulder).
        point_b (list): [x, y, z] coordinates of point B (elbow).
        point_c (list): [x, y, z] coordinates of point C (wrist).
    Returns:
        float: Angle in degrees.
    """
    a = np.array(point_a)
    b = np.array(point_b)
    c = np.array(point_c)

    # Vectors
    ba = a - b  # Vector from B to A
    bc = c - b  # Vector from B to C

    # Calculate cosine of the angle using the dot product formula
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
    return angle

def measure_arm_angle(arm:str):
    """
    Measure the angle between the arm and body in real-time using MediaPipe Pose.
    """
    cap = cv2.VideoCapture(1)
    angles = []

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
                                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y,
                                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].z]
                elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y,
                            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].z]
                wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y,
                            landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].z]
            else:
                # Get key landmarks for the left arm
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].z]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y,
                            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].z]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y,
                            landmarks[mp_pose.PoseLandmark.LEFT_WRIST].z]

            
            arm_angle = calculate_angle(shoulder, elbow, wrist)
            angles.append(arm_angle)

        # Show the video feed
        cv2.imshow("Arm Angle Measurement", frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(angles)

def measure_wrist_to_hip_distances():
    """
    Measure the distances between wrists and shoulders in real-time using a webcam.
    """
    cap = cv2.VideoCapture(1)

    right_wrist_distances = []
    left_wrist_distances = []

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

            # Get wrist and shoulder coordinates
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y,
                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST].z]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y,
                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].z]
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_HIP].y,
                              landmarks[mp_pose.PoseLandmark.LEFT_HIP].z]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y,
                              landmarks[mp_pose.PoseLandmark.RIGHT_HIP].z]

            # Calculate distances
            left_distance = calculate_distance(left_wrist, left_hip)
            right_distance = calculate_distance(right_wrist, right_hip)

            right_wrist_distances.append(left_distance)
            left_wrist_distances.append(right_distance)

            # Display distances on the video feed
            

        # Show the video feed
        cv2.imshow("Wrist to Shoulder Distance", frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(right_wrist_distances)

measure_wrist_to_hip_distances()