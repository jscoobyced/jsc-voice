import tts.TextToSpeech as tts

text_to_generate_1 = (
    "Once upon a time, in a land far away from mankind, lived a gorgeous little fox."
)
text_to_generate_2 = "Her name was foxy, and she loved dancing in the flower fields."

tts_instance = tts.TextToSpeech()
tts_instance.generate(text_to_generate_1)
