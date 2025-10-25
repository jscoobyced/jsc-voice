import asyncio
import io
import json
import os
from typing import Any
from dotenv import load_dotenv
from pydub import AudioSegment
import websockets
from storyteller.story_client import StoryClient
from speech_to_text import SpeechToText
import tts.TextToSpeech as tts
import soundfile as sf

load_dotenv()

tmp_folder = os.environ["TMP_FOLDER"]
stt = SpeechToText()
stt_model_dir = "models/" + os.environ["SPARK_AUDIO_MODEL"]
samplerate = int(os.environ["SPARK_SAMPLE_RATE"])


class StoryProcessor:

    async def process(self, message: Any, client: StoryClient):
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

        # Store audio to file
        with open(output_wav_path, "wb") as f:
            f.write(wav_io.getvalue())

        text = stt.transcribe(output_wav_path, language="en")
        await self.format_text_and_send("user", text, client.socket)
        await self.format_text_and_send("teller", "OK let me think...", client.socket)
        answer = client.conversation.ask(text)
        answer = answer.replace("A)", " ")
        answer = answer.replace("B)", " ")
        answer = answer.replace("C)", " ")
        answer = answer.replace("D)", " ")
        answer = answer.replace("E)", " ")
        voice_answer = self.process_message(answer)
        await self.format_text_and_send("teller", answer, client.socket)
        await client.socket.send(voice_answer)
        if os.path.exists(output_wav_path):
            os.remove(output_wav_path)

    async def format_text_and_send(
        self, type: str, content: str, websocket: websockets.ServerConnection
    ):
        data = {"type": type, "content": content}
        message = json.dumps(data)
        await websocket.send(message)

    def process_message(self, message):
        buffer = io.BytesIO()
        tts_instance = tts.TextToSpeech(stt_model_dir, ".", "0")
        output = tts_instance.generate(message)
        # Convert ndarray to audio file in memory
        sf.write(buffer, output, samplerate, format="WAV")
        buffer.seek(0)
        return buffer.read()
