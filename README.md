## Jsc Dia MCP

JSC Voice - A simple API to transcript voice or generate voice from text.
Internally using code from:
- [Nari Labs's Dia](https://github.com/nari-labs/dia) for Text To Speech
- [OpenAI Whisper](https://github.com/openai/whisper) for Voice To Text

# Quick start

1. Clone the repository:
```
git clone https://github.com/jscoobyced/jsc-voice.git
```

2. Navigate to the project directory:
```
cd jsc-voice
```

3. Install dependencies:
```
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

4. Create your `.env` file
```
cp .env.example .env
```
You don't need `HUGGINGFACE_TOKEN` for dia. Only for Orpheus.

5. Run the application:
5.1. Text to speech
```
python tts-app.py
```

5.2. Voice to text
```
python vtt-app.py
```