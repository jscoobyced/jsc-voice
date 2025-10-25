import tts.TextToSpeech as tts
import os
from dotenv import load_dotenv
import soundfile as sf

load_dotenv()

text = "Oh hello there! How are you today? I wish you a lovely day and see you soon!"
model_dir = "models/" + os.environ["SPARK_AUDIO_MODEL"]

tts_instance = tts.TextToSpeech(model_dir, ".", "0")
output = tts_instance.generate(text)
sf.write("output.wav", output, 16000, format="WAV")
