import cv2
import mediapipe as mp
import os
from ultralytics import YOLO

# Initialize Club Tracking Model
model = YOLO('/Users/prestonpetersen/Personal_Projects/swinganalyzer/fast-api/Training/yolov8n.pt')

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

# For drawing pose landmarks
mp_drawing = mp.solutions.drawing_utils

# Input video path (change this as needed)
input_video_path = '../uploads/TestVideo-2.mp4'
input_filename = os.path.basename(input_video_path)
input_name, input_ext = os.path.splitext(input_filename)

# Create processed output directory
output_dir = '../processed'
os.makedirs(output_dir, exist_ok=True)

# Output video path
output_video_path = os.path.join(output_dir, f'{input_name}_annotated.mp4')

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

# Lists to store wrist and club head positions
hand_positions = []
club_positions = []

frame_idx = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Convert the image to RGB (MediaPipe uses RGB)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame with MediaPipe Pose
    results = pose.process(image_rgb)

    wrist_coords = None

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

        # Store wrist position
        hand_positions.append(wrist_coords)

        # Draw current wrist
        cv2.circle(frame, wrist_coords, 5, (0, 255, 255), -1)  # Yellow dot

    # Club head detection using smarter contour selection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Run YOLOv8 inference on the frame
    results = model.predict(source=frame, imgsz=640, conf=0.5, device='cpu')  # or 'cuda:0' if GPU

    # results[0] contains boxes
    for box in results[0].boxes.xyxy:
        x1, y1, x2, y2 = map(int, box)
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        club_center = (cx, cy)

        club_positions.append(club_center)

        # Draw box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)  # Purple box
        cv2.circle(frame, club_center, 5, (0, 0, 255), -1)  # Red dot


    # # Define color range for club head detection (dark gray to black)
    # lower_color = (0, 0, 0)
    # upper_color = (180, 255, 80)
    # mask = cv2.inRange(hsv, lower_color, upper_color)

    # contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # best_contour = None
    # min_distance = float('inf')

    # if wrist_coords and contours:
    #     for contour in contours:
    #         area = cv2.contourArea(contour)
    #         if area > 50:  # basic noise filter
    #             M = cv2.moments(contour)
    #             if M["m00"] != 0:
    #                 cx = int(M["m10"] / M["m00"])
    #                 cy = int(M["m01"] / M["m00"])

    #                 # Score based on proximity to wrist and being lower vertically
    #                 dist = ((cx - wrist_coords[0])**2 + (cy - wrist_coords[1])**2)**0.5
    #                 if cy > wrist_coords[1] and dist < min_distance:
    #                     best_contour = contour
    #                     min_distance = dist

    # if best_contour is not None:
    #     M = cv2.moments(best_contour)
    #     cx = int(M["m10"] / M["m00"])
    #     cy = int(M["m01"] / M["m00"])
    #     club_center = (cx, cy)

    #     # Store club head position
    #     club_positions.append(club_center)

    #     # Draw current club head
    #     cv2.circle(frame, club_center, 5, (0, 0, 255), -1)  # Red dot

    # # Draw wrist (hand) path
    # for i in range(1, len(hand_positions)):
    #     cv2.line(frame, hand_positions[i-1], hand_positions[i], (255, 0, 0), 3)  # Blue path

    # Draw club head path
    for i in range(1, len(club_positions)):
        cv2.line(frame, club_positions[i-1], club_positions[i], (0, 0, 255), 2)  # Red path

    # Write the annotated frame to output
    out.write(frame)

    frame_idx += 1

cap.release()
out.release()
pose.close()

print(f"✅ Processing complete. Annotated video saved at: {output_video_path}")
