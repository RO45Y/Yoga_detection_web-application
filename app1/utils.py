import mediapipe as mp
import cv2
import numpy as np
from math import sqrt

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Function to compare detected landmarks with reference landmarks
def compare_landmarks_with_reference(detected_landmarks, reference_landmarks, threshold=0.25):
    """
    Compare detected landmarks with reference landmarks based on improved Euclidean distance.
    If the average distance is below the threshold, return 'correct', else 'incorrect'.
    """
    if not detected_landmarks or not reference_landmarks:
        return 'no_landmarks'

    total_distance = 0
    valid_points = 0

    for det, ref in zip(detected_landmarks, reference_landmarks):
        # Skip comparison if x/y/z is zero (landmark likely not visible)
        if det['x'] == 0 or ref['x'] == 0:
            continue

        # Calculate distance using numpy for better performance and clarity
        distance = np.linalg.norm([
            det['x'] - ref['x'],
            det['y'] - ref['y'],
            det['z'] - ref['z']
        ])
        total_distance += distance
        valid_points += 1

    if valid_points == 0:
        return 'no_landmarks'

    average_distance = total_distance / valid_points
    return 'correct' if average_distance < threshold else 'incorrect'


# Extract landmarks from an image
def get_landmarks_from_image(frame):
    """
    Extract pose landmarks from an image using MediaPipe Pose.
    """
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        landmarks = [{'x': lm.x, 'y': lm.y, 'z': lm.z} for lm in results.pose_landmarks.landmark]
        return landmarks
    return []

# Function to draw landmarks and connect them properly
def draw_landmarks(image, landmarks):
    """
    Draw landmarks on an image with proper connections.
    """
    image = image.copy()
    
    if landmarks:
        height, width, _ = image.shape
        pose_landmarks = mp_pose.PoseLandmark

        # Convert dictionary format to MediaPipe format
        landmark_points = []
        for i, lm in enumerate(landmarks):
            x, y = int(lm['x'] * width), int(lm['y'] * height)
            landmark_points.append((x, y))

        # Draw landmark connections
        for connection in mp_pose.POSE_CONNECTIONS:
            start_idx, end_idx = connection
            if start_idx < len(landmark_points) and end_idx < len(landmark_points):
                cv2.line(image, landmark_points[start_idx], landmark_points[end_idx], (0, 255, 0), 2)

        # Draw landmark points
        for point in landmark_points:
            cv2.circle(image, point, 5, (0, 0, 255), -1)

    return image
