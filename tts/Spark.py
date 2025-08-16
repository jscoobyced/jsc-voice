import logging
import tts.model.SparkArgument as sa
import tts.model.SparkConfiguration as sc
import os
import torch
from datetime import datetime
import platform
import warnings

from sparktts.cli.SparkTTS import SparkTTS


class Spark:

    def __init__(self, configuration: sc.SparkConfiguration):
        self._configuration = configuration

    def generate(self, argument: sa.SparkArgument) -> torch.Tensor:
        """Perform TTS inference and save the generated audio."""
        logging.info(f"Using model from: {self._configuration.model_dir}")
        logging.info(f"Saving audio to: {self._configuration.save_dir}")

        # Ensure the save directory exists
        os.makedirs(self._configuration.save_dir, exist_ok=True)

        # Convert device argument to torch.device
        if platform.system() == "Darwin" and torch.backends.mps.is_available():
            # macOS with MPS support (Apple Silicon)
            device = torch.device(f"mps:{self._configuration.device}")
            logging.info(f"Using MPS device: {device}")
        elif torch.cuda.is_available():
            # System with CUDA support
            device = torch.device(f"cuda:{self._configuration.device}")
            logging.info(f"Using CUDA device: {device}")
        else:
            # Fall back to CPU
            device = torch.device("cpu")
            logging.info("GPU acceleration not available, using CPU")

        # Initialize the model
        warnings.filterwarnings(action="ignore", category=FutureWarning)
        model = SparkTTS(self._configuration.model_dir, device)

        # Generate unique filename using timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        logging.info("Starting inference...")

        # Perform inference and save the output audio
        with torch.no_grad():
            wav = model.inference(
                argument.text,
                self._configuration.prompt_speech_path,
                prompt_text=self._configuration.prompt_text,
                gender=argument.gender,
                pitch=argument.pitch,
                speed=argument.speed,
            )

        return wav
