AI_Teaching_Assistant — Version 1 (Text-based AI Assistant)

Goal
Build a simple text-based AI teaching assistant that:

1. Accepts text input from user.
2. Sends the text to an AI (OpenAI Chat API) to generate a clear, student-friendly explanation.
3. Stores the chat history locally in `data/chat_history.json`.
4. Is simple to run locally and easy to extend later (voice input/output, YouTube transcript, board UI).

Folder structure (suggested)
AI_Teaching_Assistant/
├── main.py
├── requirements.txt
├── data/
│   └── chat_history.json
└── README.md  (this file)

Requirements

* Python 3.8+
* pip packages: openai, python-dotenv

How it works (short)

1. User types a question.
2. Script sends the question to the OpenAI ChatCompletion API.
3. The assistant replies with a clear explanation.
4. The Q&A is appended to `data/chat_history.json`.

Setup

1. Create a project folder and copy `main.py` there.
2. Create a `.env` file containing:
   OPENAI_API_KEY="your_openai_api_key_here"
3. Create folder `data/` and make an empty `chat_history.json` with contents: `[]`
4. Install requirements:
   pip install -r requirements.txt

Run
python main.py
Type your question and press Enter. Type `exit` or `quit` to stop.

Notes & Next steps

* If you don’t have an OpenAI API key, you can still test by replacing the `call_openai` function with a dummy function returning canned replies.
* To add voice input/output later: use `speech_recognition` for input and `gTTS` or `pyttsx3` for output.
* To add YouTube support later: use `youtube-transcript-api` or `whisper` to extract transcript then pass to the assistant.
* To create a board UI: use Streamlit + canvas/JS animation to render text line-by-line while playing voice.

Academic demo tip
Record a short demo video: show typing a question, show the assistant reply, then show saved file `data/chat_history.json`. For presentation, prepare a short explanation of components (frontend, backend, storage).
