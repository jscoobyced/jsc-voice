from dia.model import Dia
from dotenv import load_dotenv
import numpy as np
import os

load_dotenv()


class TextToSpeech:
    _clone_from_text = os.environ["VOICE_SOURCE_TEXT"]
    _clone_from_audio = os.environ["VOICE_SOURCE_AUDIO"]
    _model_name = None

    def __init__(self, model_name="nari-labs/Dia-1.6B-0626"):
        self._model_name = model_name

    def split_text(self, text: str):
        split_text = []
        split_text.append("[S1] " + self._clone_from_text + " [S1] " + text)
        # split_text.append(
        #     "[S1] "
        #     + self._clone_from_text
        #     + " [S1] "
        #     + "Her name was foxy, and she loved dancing in the flower fields."
        # )
        return split_text

    def generate(self, content: str):
        text = "[S1] " + self._clone_from_text + "[S1] " + content

        model = Dia.from_pretrained(
            self._model_name, device="cuda", compute_dtype="float16"
        )
        output = model.generate(
            text,
            audio_prompt=self._clone_from_audio,
            use_torch_compile=False,
            verbose=True,
            cfg_scale=4.5,
            temperature=1.5,
            top_p=0.90,
            cfg_filter_top_k=50,
        )
        model.save_audio("output.mp3", output)
