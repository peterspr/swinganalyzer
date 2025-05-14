from fastapi import FastAPI, BackgroundTasks
import shutil
import os

app = FastAPI()

UPLOAD_DIR = "./uploads"
PROCESSED_DIR = "./processed"

@app.post("/process-video")
async def process_video(file_path: str):
    # Fake processing: just copy file to processed folder
    basename = os.path.basename(file_path)
    processed_path = os.path.join(PROCESSED_DIR, f"processed_{basename}")
    shutil.copy(file_path, processed_path)

    return {"status": "completed", "processed_path": processed_path}