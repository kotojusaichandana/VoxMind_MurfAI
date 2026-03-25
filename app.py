from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import requests
import os

app = Flask(__name__)

# API Keys (set in environment variables)
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MURF_API_KEY = os.getenv("MURF_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data["message"]
    mode = data.get("mode", "friendly")
    language = data.get("language", "English")

    try:
        # 🔹 OpenAI response
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a {mode} AI assistant. Reply in {language} in a natural way."
                },
                {"role": "user", "content": user_input}
            ]
        )

        reply = response.choices[0].message.content

        # 🔹 Murf AI Text-to-Speech
        murf_response = requests.post(
            "https://api.murf.ai/v1/speech/generate",
            headers={
                "api-key": MURF_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "text": reply,
                "voiceId": "en-US-natalie",  # change based on language
                "format": "mp3"
            }
        )

        audio_url = murf_response.json().get("audioFile")

    except Exception as e:
        print("ERROR:", e)
        reply = "Something went wrong."
        audio_url = None

    return jsonify({"reply": reply, "audio": audio_url})

if __name__ == "__main__":
    app.run(debug=True)