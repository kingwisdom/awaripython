import yt_dlp
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Directory where videos will be downloaded
DOWNLOAD_DIR = "./downloads"

# Ensure the directory exists when the app starts
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

class DownloadRequest(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI"}
@app.post("/download/")
def download_video(request: DownloadRequest):
    try:
        # yt-dlp options
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),  # Save as title.ext
            'format': 'best',  # Download the best available quality
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(request.url, download=True)  
            video_title = info_dict.get('title', 'unknown_video') 
            video_ext = info_dict.get('ext', 'mp4') 
            video_filename = f"{video_title}.{video_ext}"

            # Full path to the downloaded file
            video_filepath = os.path.join(DOWNLOAD_DIR, video_filename)

        # Return a downloadable link for the file
        return {"download_url": f"/files/{video_filename}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading video: {str(e)}")

@app.get("/files/{filename}")
def serve_file(filename: str):
    # Construct full file path
    file_path = os.path.join(DOWNLOAD_DIR, filename)

    # Check if file exists
    if os.path.exists(file_path):
        # Serve the file for downloading
        return FileResponse(path=file_path, media_type="video/mp4", filename=filename)
    else:
        raise HTTPException(status_code=404, detail="File not found")
