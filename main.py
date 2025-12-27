from flask import Flask, request, jsonify, render_template_string
import os, json, re, csv, threading
import pyttsx3

app = Flask(__name__)

# -------------------- VOICE --------------------
VOICE_CHOICE = "female"
tts_lock = threading.Lock()

def remove_emojis(text):
    emoji_pattern = re.compile(
        "["                     
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002500-\U00002BEF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)

def clean_text(text):
    return remove_emojis(text).lower().strip()

def speak_audio(text):
    with tts_lock:
        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        voices = engine.getProperty("voices")

        for v in voices:
            if VOICE_CHOICE == "female" and "female" in v.name.lower():
                engine.setProperty("voice", v.id)
                break

        if not os.path.exists("static"):
            os.makedirs("static")

        path = "static/output.mp3"
        engine.save_to_file(text, path)
        engine.runAndWait()
        return path

# -------------------- DATASET --------------------
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def load_local_data():
    db = {}

    for file in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, file)

        # JSON FILES
        if file.endswith(".json"):
            with open(path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    for q, a in data.items():
                        db[clean_text(q)] = a
                except:
                    pass

        # CSV FILES
        elif file.endswith(".json"):
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    q = row.get("Question")
                    a = row.get("Answer")
                    if q and a:
                        db[clean_text(q)] = a

    return db

local_db = load_local_data()

def get_answer(query):
    return local_db.get(clean_text(query))

# -------------------- PROCESS --------------------
def process_input(text):
    answer = get_answer(text)
    if answer:
        return f"• {answer}"
    return "• Sorry, I don’t have an answer for that."

# -------------------- FRONTEND --------------------
with open("frontend.html", "r", encoding="utf-8") as f:
    FRONTEND_HTML = f.read()

@app.route("/")
def index():
    return render_template_string(FRONTEND_HTML)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    text = data.get("text", "")
    speak = data.get("speak", False)

    response_text = process_input(text)
    response = {"answer": response_text}

    if speak:
        audio = speak_audio(response_text)
        response["audio"] = "/" + audio

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
