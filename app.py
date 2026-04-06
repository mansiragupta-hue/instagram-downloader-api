from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": True,
        "message": "Instagram Downloader API Running"
    })

@app.route("/download")
def download():
    url = request.args.get("url")

    if not url:
        return jsonify({
            "status": False,
            "message": "URL required"
        })

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'forcejson': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "status": True,
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "video_url": info.get("url")
            })
    except Exception as e:
        return jsonify({
            "status": False,
            "error": str(e)
        })

if __name__ == "__main__":
    app.run()
