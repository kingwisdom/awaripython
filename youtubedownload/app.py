import yt_dlp
import os
import flask
from flask import request, jsonify
from flask_cors import CORS

# app = FastAPI()
app = flask.Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

# Directory where videos will be downloaded
DOWNLOAD_DIR = "./downloads"

# Ensure the directory exists when the app starts
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI"}
@app.route('/download', methods=['POST'])
def download_video():
    try:
        # Accessing JSON data from the request
        data = request.json  # No need to pass 'request' as a parameter
        video_url = data.get('url')  # Get the video URL from the request JSON

        if not video_url:
            return jsonify({"error": "URL is required"}), 400

        # yt-dlp options
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'format': 'best',
        }

        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', 'unknown_video')
            video_ext = info_dict.get('ext', 'mp4')
            video_filename = f"{video_title}.{video_ext}"

        # Return download link for the file
        return jsonify({"download_url": f"/files/{video_filename}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Serving the downloaded files
@app.route('/files/<filename>', methods=['GET'])
def serve_file(filename):
    file_path = os.path.join(DOWNLOAD_DIR, filename)
    if os.path.exists(file_path):
        return jsonify({"message": f"Download {filename}"}), 200
    else:
        return jsonify({"error": "File not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)