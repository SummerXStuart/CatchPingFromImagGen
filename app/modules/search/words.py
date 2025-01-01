import random

with open("app/resources/single_mode_target_words.txt", "r") as _f:
    data = _f.read()
    data = data.split("\n")

def get_random_word():
    return random.choice(data)