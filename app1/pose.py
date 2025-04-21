import cv2
import time
import mediapipe as mp
import numpy as np
import pygame  # Import pygame for sound playback

# Initialize pygame mixer for sound
pygame.mixer.init()

# Load a sound (make sure the sound file exists in your directory)
correct_pose_sound = pygame.mixer.Sound("C:\\Users\\Rohit\\Downloads\\school-bell-87744.mp3")

# Initialize MediaPipe Pose module
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils  # For drawing landmarks

reference_landmarks=[
    {
        "x": 0.5818443298339844,
        "y": 0.1412491798400879,
        "z": -0.19525586068630219,
        "visibility": 0.9999356269836426
    },
    {
        "x": 0.5727018713951111,
        "y": 0.11921551823616028,
        "z": -0.16150297224521637,
        "visibility": 0.999803364276886
    },
    {
        "x": 0.5716649889945984,
        "y": 0.11879006773233414,
        "z": -0.16161029040813446,
        "visibility": 0.9998435974121094
    },
    {
        "x": 0.5704913139343262,
        "y": 0.1183575987815857,
        "z": -0.16173163056373596,
        "visibility": 0.999783456325531
    },
    {
        "x": 0.5681995153427124,
        "y": 0.11941894888877869,
        "z": -0.19858919084072113,
        "visibility": 0.9998422861099243
    },
    {
        "x": 0.5647875070571899,
        "y": 0.1194138452410698,
        "z": -0.1986723691225052,
        "visibility": 0.9998399019241333
    },
    {
        "x": 0.5611225366592407,
        "y": 0.11954840272665024,
        "z": -0.19866880774497986,
        "visibility": 0.9996985197067261
    },
    {
        "x": 0.5489223599433899,
        "y": 0.13014665246009827,
        "z": -0.01699467934668064,
        "visibility": 0.9997546076774597
    },
    {
        "x": 0.5363806486129761,
        "y": 0.13272252678871155,
        "z": -0.19033533334732056,
        "visibility": 0.9997966885566711
    },
    {
        "x": 0.5784633755683899,
        "y": 0.16334065794944763,
        "z": -0.14354437589645386,
        "visibility": 0.9992188215255737
    },
    {
        "x": 0.5729540586471558,
        "y": 0.16484114527702332,
        "z": -0.1936231106519699,
        "visibility": 0.9993841648101807
    },
    {
        "x": 0.592509925365448,
        "y": 0.26039084792137146,
        "z": 0.04233052209019661,
        "visibility": 0.9995961785316467
    },
    {
        "x": 0.45916372537612915,
        "y": 0.26136982440948486,
        "z": -0.20343279838562012,
        "visibility": 0.9990634322166443
    },
    {
        "x": 0.7132081985473633,
        "y": 0.23053929209709167,
        "z": 0.03791067376732826,
        "visibility": 0.9912757873535156
    },
    {
        "x": 0.33558452129364014,
        "y": 0.25319045782089233,
        "z": -0.261917382478714,
        "visibility": 0.991363525390625
    },
    {
        "x": 0.8113421201705933,
        "y": 0.2204517424106598,
        "z": -0.1041133776307106,
        "visibility": 0.9930251836776733
    },
    {
        "x": 0.22248703241348267,
        "y": 0.24889490008354187,
        "z": -0.3317353129386902,
        "visibility": 0.9791691899299622
    },
    {
        "x": 0.8466123342514038,
        "y": 0.2185375988483429,
        "z": -0.12368699163198471,
        "visibility": 0.9753912687301636
    },
    {
        "x": 0.18782967329025269,
        "y": 0.24404388666152954,
        "z": -0.3561118245124817,
        "visibility": 0.9502294063568115
    },
    {
        "x": 0.8525075912475586,
        "y": 0.2157442271709442,
        "z": -0.17790725827217102,
        "visibility": 0.9790985584259033
    },
    {
        "x": 0.183305025100708,
        "y": 0.24313275516033173,
        "z": -0.3964243531227112,
        "visibility": 0.9574136137962341
    },
    {
        "x": 0.8400447964668274,
        "y": 0.22047042846679688,
        "z": -0.13829529285430908,
        "visibility": 0.9825550317764282
    },
    {
        "x": 0.19297906756401062,
        "y": 0.24808433651924133,
        "z": -0.355399489402771,
        "visibility": 0.955932080745697
    },
    {
        "x": 0.5523563623428345,
        "y": 0.5918285846710205,
        "z": 0.07114867120981216,
        "visibility": 0.9991369843482971
    },
    {
        "x": 0.46440744400024414,
        "y": 0.5874856114387512,
        "z": -0.07107548415660858,
        "visibility": 0.9985918402671814
    },
    {
        "x": 0.7101365327835083,
        "y": 0.683070182800293,
        "z": -0.09666784107685089,
        "visibility": 0.9974459409713745
    },
    {
        "x": 0.35859596729278564,
        "y": 0.7470400929450989,
        "z": -0.10149088501930237,
        "visibility": 0.9982591271400452
    },
    {
        "x": 0.7387765049934387,
        "y": 0.8999748826026917,
        "z": -0.006911467295140028,
        "visibility": 0.9954889416694641
    },
    {
        "x": 0.24524182081222534,
        "y": 0.9017810821533203,
        "z": 0.04884378984570503,
        "visibility": 0.9984501600265503
    },
    {
        "x": 0.7198528051376343,
        "y": 0.9436120986938477,
        "z": -0.006864698138087988,
        "visibility": 0.9909161925315857
    },
    {
        "x": 0.23861591517925262,
        "y": 0.9189350605010986,
        "z": 0.053442180156707764,
        "visibility": 0.9641169309616089
    },
    {
        "x": 0.8119957447052002,
        "y": 0.9355286359786987,
        "z": -0.14355970919132233,
        "visibility": 0.9926274418830872
    },
    {
        "x": 0.21289896965026855,
        "y": 0.9594498872756958,
        "z": -0.11922816187143326,
        "visibility": 0.9926179051399231
    }
]
def calculate_distance(p1, p2):
    return np.linalg.norm([p1['x'] - p2['x'], p1['y'] - p2['y'], p1['z'] - p2['z']])

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize variables
pose_correct_duration = 0
pose_is_correct = False
start_time = None
threshold = 0.35 # Euclidean distance threshold for keypoint matching (smaller means stricter)

def compare_landmarks(reference_landmarks, current_landmarks):
    """
    Compare the detected keypoints to the reference keypoints
    by calculating Euclidean distance.
    """
    if len(reference_landmarks) != len(current_landmarks):
        return 0  # If the number of landmarks don't match, return 0 match

    matching_keypoints = 0
    total_landmarks = len(reference_landmarks)

    for ref_landmark, cur_landmark in zip(reference_landmarks, current_landmarks):
        # Only compare landmarks with visibility greater than 0.5
        if ref_landmark['x'] != 0 and cur_landmark['x'] != 0:  # Check for visible points
            # Calculate Euclidean distance between corresponding landmarks
            dist = calculate_distance(ref_landmark, cur_landmark)

            # If distance is below threshold, count it as a match
            if dist < threshold:
                matching_keypoints += 1

    # Return the ratio of matching landmarks
    return matching_keypoints / total_landmarks

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the current frame to RGB for MediaPipe processing
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    # Check if the pose landmarks are detected
    if results.pose_landmarks:
        current_landmarks = [
            {"x": lm.x, "y": lm.y, "z": lm.z} for lm in results.pose_landmarks.landmark
        ]

        # Draw landmarks on the frame
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Compare the detected pose with the reference pose
        matching_ratio = compare_landmarks(reference_landmarks, current_landmarks)

        # If the matching ratio exceeds the threshold, the pose is correct
        if matching_ratio >= 0.8:
            if not pose_is_correct:
                pose_is_correct = True
                start_time = time.time()  # Start the 3 seconds timer
                correct_pose_sound.play(-1)  # Start playing sound (loop indefinitely)
        else:
            pose_is_correct = False
            correct_pose_sound.stop()  # Stop sound if pose is incorrect

    # Display the status
    if pose_is_correct:
        # If pose is correct, display "Done" for 3 seconds
        elapsed_time = time.time() - start_time
        if elapsed_time >= 3:
            cv2.putText(frame, "Done!", (250, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            # Stop the webcam after 3 seconds
            cap.release()
            cv2.destroyAllWindows()
            break
        else:
            cv2.putText(frame, "Pose Matched! Hold for 3 seconds.", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        # If pose is incorrect, show a red message
        cv2.putText(frame, "Pose Incorrect. Try Again!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Display the frame
    cv2.imshow('Pose Comparison', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()


# import base64

# def base64_to_image(base64_string, output_image_path):
#     # Decode the base64 string
#     image_data = base64.b64decode(base64_string)
    
#     # Write the image data to a file
#     with open(output_image_path, 'wb') as image_file:
#         image_file.write(image_data)
        
#     print(f"Image saved as {output_image_path}")

# # Example usage:
# base64_string = "your_base64_encoded_string_here"
# output_image_path = "output_image.png"

# base64_to_image(base64_string, output_image_path)
