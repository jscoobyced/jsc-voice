# Quick start

1. Requirements
This has been tested so far on this environment:
- Ubuntu Linux
- Python 3.12
- Nvida GPU RTX 3090 (should work on any comptatible nvidia GPU)

2. Clone the repository:
```
git clone https://github.com/jscoobyced/jsc-voice.git
```

3. Navigate to the project tts directory:
```
cd jsc-voice/application
```

4. Install dependencies:
```
uv sync
source .venv/bin/activate
```

5. Create your `.env` file
```
cp .env.example .env
```
You will need `HUGGINGFACE_TOKEN` to download the models.

6. Prerequisites

First time only, download the models
```
uv run tts-init.py
```

7. Running the application
Then simply run:
```
uv run server.py
```

Application logs are in `application.log`.