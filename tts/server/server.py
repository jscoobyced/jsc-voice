import soundfile as sf
import io
import os
import uuid as u
import util.logger as log
import tts.TextToSpeech as tts
from flask import Flask, Response, request
from dotenv import load_dotenv

load_dotenv()

app = Flask("JSC-Voice")
samplerate = int(os.environ["SPARK_SAMPLE_RATE"])
model_dir = "models/" + os.environ["SPARK_AUDIO_MODEL"]
tts_instance = tts.TextToSpeech(model_dir, ".", "0")

logger = log.Logger()
clients = []


@app.route("/register", methods=["GET"])
def register() -> u.UUID:
    name = request.args.get("name")
    password = request.args.get("password")
    for client in clients:
        if client["key"]["name"] == name and client["key"]["password"] == password:
            logger.info("Client trying to re-register: " + str(client["values"]["id"]))
            return str(client["values"]["id"])
    new_id = u.uuid4()
    client = {
        "key": {
            "name": name,
            "password": password,
        },
        "values": {
            "id": new_id,
        },
    }
    logger.info("Creating client:")
    logger.info(client)
    clients.append(client)
    return str(new_id)


@app.route("/stream", methods=["POST"])
def stream():
    body = request.get_json()
    logger.info(body["text"])
    id = body["id"]
    text = "You are not registered. Please register first."
    for client in clients:
        if str(client["values"]["id"]) == id:
            text = body["text"]
    buffer = io.BytesIO()
    output = tts_instance.generate(text)
    sf.write(buffer, output, samplerate, format="WAV")
    buffer.seek(0)
    return Response(buffer.read(), mimetype="audio/wav")


def start():
    app.run(host="0.0.0.0", debug=True)
