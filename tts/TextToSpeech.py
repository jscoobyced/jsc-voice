from dia.model import Dia
from dotenv import load_dotenv
import numpy as np
import os
import warnings

load_dotenv()

DEFAULT_SAMPLE_RATE = 44100


class TextToSpeech:
    _clone_from_text = os.environ["VOICE_SOURCE_TEXT"]
    _clone_from_audio = os.environ["VOICE_SOURCE_AUDIO"]
    _model_name = None
    _model = None

    def __init__(self, model_name="nari-labs/Dia-1.6B-0626"):
        self._model_name = model_name
        warnings.filterwarnings(action="ignore", category=FutureWarning)
        self._model = Dia.from_pretrained(
            self._model_name, device="cuda", compute_dtype="float16"
        )

    def split_text(self, text: str):
        split_text = []
        split_text.append("[S1] " + self._clone_from_text + " [S1] " + text)
        return split_text

    def generate(self, content: str) -> np.ndarray:
        text = "[S1] " + self._clone_from_text + "[S1] " + content

        output = self._model.generate(
            text,
            audio_prompt=self._clone_from_audio,
            use_torch_compile=True,
            verbose=False,
            cfg_scale=4.5,
            temperature=1.5,
            top_p=0.90,
            cfg_filter_top_k=50,
        )
        return output

    def save_audio(self, path: str, audio: np.ndarray):
        """Saves the generated audio waveform to a file.

        Uses the soundfile library to write the NumPy audio array to the specified
        path with the default sample rate.

        Args:
            path: The path where the audio file will be saved.
            audio: The audio waveform as a NumPy array.
        """
        import soundfile as sf

        sf.write(path, audio, DEFAULT_SAMPLE_RATE)
