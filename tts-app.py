import tts.TextToSpeech as tts
import os
from dotenv import load_dotenv

import soundfile as sf

DEFAULT_SAMPLE_RATE = 16000

load_dotenv()

text = "Once upon a time, in a land far away from mankind, lived a gorgeous little fox. Her name was foxy, and she loved dancing in the flower fields. One day she went near the river to drink a bit of water."
model_dir = "models/" + os.environ["SPARK_AUDIO_MODEL"]

tts_instance = tts.TextToSpeech(model_dir, ".", "0")

output = tts_instance.generate(text)
sf.write("output.mp3", output, samplerate=DEFAULT_SAMPLE_RATE, format="mp3")
