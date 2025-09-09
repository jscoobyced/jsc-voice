import soundfile as sf
import io
import os
import uuid as u
import util.logger as log
import tts.TextToSpeech as tts
from dotenv import load_dotenv
import asyncio
from websockets.asyncio.server import serve
from speech_to_text import SpeechToText
import wave

load_dotenv()


def process_message(message):
    model_dir = "models/" + os.environ["SPARK_AUDIO_MODEL"]
    tts_instance = tts.TextToSpeech(model_dir, ".", "0")
    buffer = io.BytesIO()
    output = tts_instance.generate(message)
    sf.write("o.wav", output, samplerate, format="WAV")
    buffer.seek(0)
    return buffer.read()


stt = SpeechToText()
samplerate = int(os.environ["SPARK_SAMPLE_RATE"])


async def echo(websocket):
    async for message in websocket:
        print("Received message")
        output_filename = f"output_{u.uuid4().hex}.wav"
        wf = wave.open(output_filename, "wb")
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(44100)  # 44.1 kHz
        try:
            if isinstance(message, bytes):
                wf.writeframes(message)
                print("Written to file from bytes of length:", len(message))
            else:
                print("Received non-binary data, skipping.")

        except websockets.exceptions.ConnectionClosedOK:
            print("WebSocket connection closed normally.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            wf.close()
            print(f"Audio saved to {output_filename}")

        await websocket.send(message)


async def main():
    async with serve(echo, "0.0.0.0", 6789) as server:
        print("WebSocket server started on ws://192.168.1.41:6789")
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
