from dia.model import Dia
from dotenv import load_dotenv
import os

load_dotenv()


clone_from_text = os.environ['VOICE_SOURCE_TEXT']
clone_from_audio = os.environ['VOICE_SOURCE_AUDIO']

text_to_generate_1 = "[S1] Once upon a time, in a land far away from mankind, lived a gorgeous little fox."
text_to_generate_2 = "[S1] Her name was foxy, and she loved dancing in the flower fields."
text_to_generate = [clone_from_text + text_to_generate_1, clone_from_text + text_to_generate_2]

index = 1

for text in text_to_generate:
    model = Dia.from_pretrained("nari-labs/Dia-1.6B-0626", compute_dtype="float16")

    output = model.generate(
        text,
        audio_prompt=clone_from_audio,
        use_torch_compile=True,
        verbose=False,
        cfg_scale=4.5,
        temperature=1.5,
        top_p=0.90,
        cfg_filter_top_k=50,
    )

    model.save_audio("voice_clone_" + str(index) + ".mp3", output)
    index = index + 1
    model = None