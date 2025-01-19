import cv2
import mediapipe as mp
import numpy as np
import time

class CameraError(Exception):
    """Camera Error"""
    pass

class SwingDetector: 
    def __init__(self): 
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_draw = mp.solutions.drawing_utils

        self.swing_threshhold = 0.27
        self.swing_threshhold2 = 0.6
        self.min_sustained_frames = 2
        self.has_hit= False
        self.terminate = False

    def detect_swing(self) :
        # Initialize camera
        cap = cv2.VideoCapture(0)

        # Raise error if camera doesn't work
        ret, frame = cap.read()
        if not ret:
            raise CameraError("Camera doesn't work")

        prev_wrist_position_right = None
        prev_wrist_position_left = None
        sustained_velocity_frames = 0
        velocity_list = []

        while not self.terminate:
            ret, frame = cap.read()
            if not ret:
                break  # Exit if no frame is captured

            # Convert frame to RGB as MediaPipe expects RGB input
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb_frame)

            if results.pose_landmarks:
                self.mp_draw.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

                # Extract wrist coordinates
                landmarks = results.pose_landmarks.landmark
                right_wrist = landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST]
                left_wrist = landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST]

                # cv2.imshow("Arm Swing Detection", frame)

                if prev_wrist_position_right is not None and prev_wrist_position_left is not None:
                    # Calculate velocity
                    right_velocity = round(np.abs(right_wrist.z - prev_wrist_position_right),2)
                    left_velocity = round(np.abs(left_wrist.z - prev_wrist_position_left),2)
                    velocity_list.append(right_velocity)

                    # Check if velocity is above threshold
                    if (right_velocity > self.swing_threshhold2):
                        self.has_hit = True
                        time.sleep(1)
                        self.has_hit = False
                    elif (left_velocity > self.swing_threshhold2): 
                        self.has_hit = True
                        time.sleep(1)
                        self.has_hit= False
                    elif (right_velocity > self.swing_threshhold):
                        sustained_velocity_frames += 1
                        if sustained_velocity_frames >= self.min_sustained_frames:
                            self.has_hit= True
                            time.sleep(1)
                            self.has_hit= False
                    elif (left_velocity > self.swing_threshhold):
                        sustained_velocity_frames += 1
                        if sustained_velocity_frames >= self.min_sustained_frames:
                            self.has_hit= True
                            time.sleep(0.5)
                            self.has_hit= False
                    else:
                        sustained_velocity_frames = 0  # Reset if velocity drops below threshold

                # Update previous wrist positions
                prev_wrist_position_right = right_wrist.z
                prev_wrist_position_left = left_wrist.z


            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()

        cap.release()
        cv2.destroyAllWindows()

    def hasHit(self): 
        return self.has_hit

    def end(self): 
        self.terminate = True

sd = SwingDetector()
sd.detect_swing()
