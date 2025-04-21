import cv2
import mediapipe as mp
import json
import os

def extract_landmarks(image_path, output_json_path):
    """Extract pose landmarks from an image and save them as a list of dictionaries."""
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
    
    image = cv2.imread(image_path)
    if image is None:
        print("❌ Error: Could not read the image.")
        return
    
    # Convert to RGB for MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    
    if not results.pose_landmarks:
        print("⚠️ No pose landmarks detected.")
        return
    
    # Store landmarks as a list of dictionaries
    landmarks = []
    for landmark in results.pose_landmarks.landmark:
        landmarks.append({
            "x": landmark.x,
            "y": landmark.y,
            "z": landmark.z,
            "visibility": landmark.visibility
        })
    
    # Save as JSON
    with open(output_json_path, "w") as f:
        json.dump(landmarks, f, indent=4)
    
    print(f"✅ Landmarks saved to {output_json_path}")

if __name__ == "__main__":
    input_image = "C:\\Users\\Rohit\\Downloads\\plank3.jpg"  # Change to your image path
    output_json = "pose_landmarks.json"
    extract_landmarks(input_image, output_json)
