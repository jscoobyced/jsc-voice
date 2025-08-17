## Jsc Dia MCP

JSC Voice - A simple API to transcript voice or generate voice from text.
Internally using code from:
- [Spark TTS](https://github.com/SparkAudio/Spark-TTS.git) for Text To Speech
- [OpenAI Whisper](https://github.com/openai/whisper) for Voice To Text (not yet implemented)

# Quick start

1. Requirements
THis has been tested so far on this environment:
- Ubuntu Linux
- Python 3.12
- Nvida GPU RTX 3090 (should work on any comptatible nvidia GPU)

2. Clone the repository:
```
git clone https://github.com/jscoobyced/jsc-voice.git
```

3. Navigate to the project server directory:
```
cd jsc-voice/server
```

4. Install dependencies:
```
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

5. Create your `.env` file
```
cp .env.example .env
```
You will need `HUGGINGFACE_TOKEN` to download the models.

6. Run the application:
6.1. First time only
Download the models
```
python tts-init.py
```

6.2. Text to speech
```
python tts-app.py
```

6.3. Voice to text (not implemented yet)
```
python vtt-app.py
```