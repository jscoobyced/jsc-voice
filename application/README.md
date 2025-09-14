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
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

5. Create your `.env` file
```
cp .env.example .env
```
You will need `HUGGINGFACE_TOKEN` to download the models.

6. Prerequisites
First time only, download the models
```
python tts-init.py
```

7. Running the application
Then simply run:
```
python server.py
```

Application logs are in `application.log`.