import random
import pandas as pd

with open("app/resources/single_mode_target_words.txt", "r") as _f:
    data = _f.read()
    data = data.split("\n")

try:
    df_single_play = pd.read_csv("app/resources/single_mode_set.csv", encoding="utf-8")
except:
    # df_single_play = pd.DataFrame({"target": [], "hint": [], "hint_image_prompt": [], "hint_url": []})
    df_single_play = pd.DataFrame({"target": [], "hint": [], "hint_image_prompt": [], "hint_b64_img": []})

def get_random_word():
    return random.choice(data)

def get_full_target_words():
    return data

def get_single_play_set():
    return df_single_play
