import whisper


class SpeechToText:
    def __init__(self, model_name="turbo"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_path: str, language="en"):
        audio = whisper.load_audio(audio_path)
        result = self.model.transcribe(audio, language=language)
        return result["text"]


if __name__ == "__main__":
    stt = SpeechToText(model_name="large")
    text = stt.transcribe("./audio/billy-willy.wav", language="en")
    print(text)
