from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": True,
        "message": "Instagram Media API Running"
    })

@app.route("/download")
def download():
    url = request.args.get("url")

    if not url:
        return jsonify({
            "status": False,
            "message": "URL parameter missing"
        })

    api_url = "https://instagram-media-api.p.rapidapi.com/media"

    headers = {
        "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",
        "X-RapidAPI-Host": "instagram-media-api.p.rapidapi.com"
    }

    response = requests.get(api_url, headers=headers, params={"url": url})

    return jsonify(response.json())

if __name__ == "__main__":
    app.run()
