from dataclasses import dataclass


@dataclass
class SparkArgument:
    text: str
    gender: str = None
    pitch: str = None
    speed: str = None
