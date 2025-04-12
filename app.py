from flask import Flask, request, jsonify
import openai
import json
from dotenv import load_dotenv
load_dotenv()

import os
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze_text():
    data = request.get_json()
    testo = data.get("text", "")

    if not testo.strip():
        return jsonify({"error": "Testo vuoto"}), 400

    # Prompt che chiede un punteggio e una spiegazione
    prompt = """
Sei un'intelligenza artificiale esperta nel riconoscere fake news.

Analizza il seguente testo e restituisci SOLO un JSON così:
{{
  "fake_news_score": numero da 0 a 100,
  "explanation": "testo spiegazione"
}}

Testo:
\"\"\"{testo}\"\"\"
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Rispondi solo con JSON valido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )

        reply = response.choices[0].message["content"].strip()
        result = json.loads(reply)

        return jsonify({
            "text": testo,
            "fake_news_score": result["fake_news_score"],
            "explanation": result["explanation"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
