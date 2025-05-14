import cv2
import mediapipe as mp
import os

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

# For drawing pose landmarks
mp_drawing = mp.solutions.drawing_utils

# Input and output files
input_video_path = './uploads/your_input_video.mp4'
output_video_path = './processed/annotated_output.mp4'

# Create processed directory if it doesn't exist
os.makedirs('./processed', exist_ok=True)

# OpenCV Video Reader
cap = cv2.VideoCapture(input_video_path)
if not cap.isOpened():
    raise IOError(f"Cannot open video file: {input_video_path}")

# Video Writer setup
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(
    output_video_path,
    fourcc,
    int(cap.get(cv2.CAP_PROP_FPS)),
    (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
)

# List to store wrist positions for swing path tracking
hand_positions = []

frame_idx = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Convert the image to RGB (MediaPipe uses RGB)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame with MediaPipe Pose
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        # Draw full body pose landmarks
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
        )

        # Extract wrist coordinates (for swing path)
        landmarks = results.pose_landmarks.landmark
        wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]

        h, w, _ = frame.shape
        wrist_coords = (int(wrist.x * w), int(wrist.y * h))

        # Store the wrist position
        hand_positions.append(wrist_coords)

        # Draw current wrist position
        cv2.circle(frame, wrist_coords, 5, (0, 255, 255), -1)

    # After extracting wrist, draw the full path
    for i in range(1, len(hand_positions)):
        cv2.line(frame, hand_positions[i-1], hand_positions[i], (255, 0, 0), 2)

    # Write the annotated frame to output video
    out.write(frame)

    frame_idx += 1

cap.release()
out.release()
pose.close()

print(f"✅ Processing complete. Annotated video saved at: {output_video_path}")
