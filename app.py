from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import uuid
import threading
import time

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def delete_file_later(path, delay=60):
    def delete():
        time.sleep(delay)
        if os.path.exists(path):
            os.remove(path)
    threading.Thread(target=delete).start()


@app.route("/")
def home():
    return jsonify({
        "status": True,
        "message": "Advanced Instagram Downloader API Running"
    })


@app.route("/download")
def download():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "URL required"})

    unique_id = str(uuid.uuid4())
    filepath = os.path.join(DOWNLOAD_FOLDER, unique_id + ".mp4")

    ydl_opts = {
        'outtmpl': filepath,
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': True,
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        delete_file_later(filepath, 120)

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/info")
def info():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "URL required"})

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return jsonify({
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "uploader": info.get("uploader")
        })

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run()
