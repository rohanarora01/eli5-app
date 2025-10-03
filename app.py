from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import requests

load_dotenv()
app = Flask(__name__)

# Fix: Use environment variable name, not the actual key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/explain", methods=["POST"])
def explain():
    user_input = request.json.get("text", "")
    prompt = f"Explain this like I'm 5:\n\n{user_input}"

    # Fix: Updated to use correct model name and stable v1 API
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = { "Content-Type": "application/json" }
    params = { "key": GEMINI_API_KEY }
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(url, headers=headers, params=params, json=payload)
    
    if response.status_code == 200:
        try:
            text = response.json()['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"result": text})
        except Exception as e:
            return jsonify({"result": f"Parsing error: {str(e)}"})
    else:
        return jsonify({"result": f"API error {response.status_code}: {response.text}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
