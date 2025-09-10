import asyncio
import os
import websockets
import numpy as np
from pydub import AudioSegment
import io
from dotenv import load_dotenv
from speech_to_text import SpeechToText
import tts.TextToSpeech as tts
import soundfile as sf

load_dotenv()

stt = SpeechToText()
samplerate = int(os.environ["SPARK_SAMPLE_RATE"])
model_dir = "models/" + os.environ["SPARK_AUDIO_MODEL"]
tts_instance = tts.TextToSpeech(model_dir, ".", "0")


def process_message(message):
    buffer = io.BytesIO()
    output = tts_instance.generate(message)
    # Convert ndarray to audio file in memory
    sf.write(buffer, output, samplerate, format="WAV")
    buffer.seek(0)
    return buffer.read()


async def audio_handler(websocket):
    print("Client connected")
    async for message in websocket:
        print("Received audio data")
        # message is a bytes object (the audio blob)
        audio_bytes = message

        # Generate unique output filename
        output_wav_path = f"tmp/output_{asyncio.get_event_loop().time()}.wav"

        # Convert WebM/Opus 48,000Hz to WAV in memory using pydub
        audio = AudioSegment.from_file(
            io.BytesIO(audio_bytes),
            format="webm",
            sample_width=4,
            channels=1,
            frame_rate=48000,
            codec="opus",
        )
        wav_io = io.BytesIO()

        # Export to WAV 16Hz 16-bit mono
        audio.export(
            wav_io,
            format="wav",
            codec="pcm_s16le",
            parameters=["-ar", "16000", "-ac", "1"],
        )
        wav_io.seek(0)

        # Read WAV into numpy array
        # wav_audio = AudioSegment.from_wav(wav_io)
        # samples = np.array(wav_audio.get_array_of_samples())
        # if wav_audio.channels == 2:
        #     samples = samples.reshape((-1, 2))  # Stereo

        # Store audio to file
        with open(output_wav_path, "wb") as f:
            f.write(wav_io.getvalue())

        text = stt.transcribe(output_wav_path, language="en")
        await websocket.send(process_message(text))


async def main():
    async with websockets.serve(audio_handler, "0.0.0.0", 6789) as start_server:
        print("WebSocket server started on ws://localhost:6789")
        await start_server.wait_closed()


if __name__ == "__main__":
    # Empty tmp folder
    if os.path.exists("tmp"):
        for f in os.listdir("tmp"):
            os.remove(os.path.join("tmp", f))
    # If tmp folder doesn't exist, create it
    else:
        os.makedirs("tmp")

    asyncio.run(main())
