import cv2
import os

video_path = '/Users/prestonpetersen/Personal_Projects/swinganalyzer/uploads/swingmontage.mp4'
output_folder = '/Users/prestonpetersen/Personal_Projects/swinganalyzer/fast-api/Training/datasets/training_images'
os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(video_path)
frame_count = 0
save_every_n_frames = 5

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    if frame_count % save_every_n_frames == 0:
        cv2.imwrite(os.path.join(output_folder, f"frame_{frame_count}.jpg"), frame)

    frame_count += 1

cap.release()
print("✅ Frame extraction complete!")