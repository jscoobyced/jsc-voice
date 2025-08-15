import tts.TextToSpeech as tts
import numpy as np

text_to_generate_1 = (
    "Once upon a time, in a land far away from mankind, lived a gorgeous little fox."
)
text_to_generate_2 = "Her name was foxy, and she loved dancing in the flower fields."
list_of_text = [text_to_generate_1, text_to_generate_2]

tts_instance = tts.TextToSpeech()
outputs = list()
for text in list_of_text:
    output = tts_instance.generate(text)
    outputs.append(output)

full_output = np.concatenate(outputs)
tts_instance.save_audio("output.mp3", full_output)
