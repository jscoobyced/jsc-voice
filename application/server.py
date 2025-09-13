import asyncio
import os
import websockets

# import numpy as np
from pydub import AudioSegment
import io
import json
from dotenv import load_dotenv
from speech_to_text import SpeechToText
import tts.TextToSpeech as tts
import storyteller.conversation as convo
import soundfile as sf
import util.logger as log

load_dotenv()

samplerate = int(os.environ["SPARK_SAMPLE_RATE"])
stt_model_dir = "models/" + os.environ["SPARK_AUDIO_MODEL"]
ollama_model = os.environ["OLLAMA_MODEL"]
server_url = os.environ["SERVER_URL"]
server_port = int(os.environ["SERVER_PORT"])
tmp_folder = "tmp"
stt = SpeechToText()
story_teller = convo.OllamaConversation(ollama_model)
logger = log.Logger()


def process_message(message):
    buffer = io.BytesIO()
    tts_instance = tts.TextToSpeech(stt_model_dir, ".", "0")
    output = tts_instance.generate(message)
    # Convert ndarray to audio file in memory
    sf.write(buffer, output, samplerate, format="WAV")
    buffer.seek(0)
    return buffer.read()


async def format_text_and_send(
    type: str, content: str, websocket: websockets.ServerConnection
):
    data = {"type": type, "content": content}
    message = json.dumps(data)
    await websocket.send(message)


async def audio_handler(websocket):
    logger.info("Client connected")
    async for message in websocket:
        logger.info("Received audio data")
        # message is a bytes object (the audio blob)
        audio_bytes = message

        # Generate unique output filename
        output_wav_path = f"{tmp_folder}/output_{asyncio.get_event_loop().time()}.wav"

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
        await format_text_and_send("user", text, websocket)
        await format_text_and_send("teller", "OK let me think...", websocket)
        answer = story_teller.ask(text)
        answer = answer.replace("A)", " ")
        answer = answer.replace("B)", " ")
        answer = answer.replace("C)", " ")
        voice_answer = process_message(answer)
        await format_text_and_send("teller", answer, websocket)
        await websocket.send(voice_answer)
        if os.path.exists(output_wav_path):
            os.remove(output_wav_path)


async def main():
    async with websockets.serve(audio_handler, server_url, server_port) as start_server:
        print(f"WebSocket server started on ws://{server_url}:{server_port}")
        await start_server.wait_closed()


if __name__ == "__main__":
    # Empty tmp folder
    if os.path.exists(tmp_folder):
        for f in os.listdir(tmp_folder):
            os.remove(os.path.join(tmp_folder, f))
    # If tmp folder doesn't exist, create it
    else:
        os.makedirs("tmp_folder")

    asyncio.run(main())
