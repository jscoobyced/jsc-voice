from dotenv import load_dotenv
import os
import torch

import tts.model.SparkArgument as sa
import tts.model.SparkConfiguration as sc

import tts.Spark as s


load_dotenv()


class TextToSpeech:
    _clone_from_text = os.environ["VOICE_SOURCE_TEXT"]
    _clone_from_audio = os.environ["VOICE_SOURCE_AUDIO"]
    _model = None

    def __init__(self, model_dir: str, save_dir: str, device: str):
        configuration = sc.SparkConfiguration(
            model_dir, save_dir, device, self._clone_from_text, self._clone_from_audio
        )
        self._model = s.Spark(configuration)

    def generate(self, content: str) -> torch.Tensor:
        argument = sa.SparkArgument(content, speed="moderate", pitch="moderate")

        return self._model.generate(argument)
