from dataclasses import dataclass


@dataclass
class SparkConfiguration:
    model_dir: str
    save_dir: str
    device: str
    prompt_text: str
    prompt_speech_path: str
