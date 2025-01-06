
from app.modules.genImg.dalle_api import call_dalle_api
from app.modules.llm.openai_apis import generate_text
from app.modules.search.words import (
    get_full_target_words,
    get_single_play_set
)
from app.modules.utils.img_mgmt import (
    resize_base64_image
)
import yaml
import pandas as pd

with open("app/prompts/prompt.yaml") as _f:
    prompts = yaml.safe_load(_f)

def generate_hint_image(hint_word):
    """hint_word에 대한 이미지 만들기

    Args:
        hint_word (_type_): _description_
    """

# 미리 싱글 플레이를 위한 힌트 단어 및 이미지 만들어 놓기
def make_single_play_set():
    target_words = get_full_target_words()
    df = get_single_play_set()

    HINT_WORD_PROMPT = prompts["HINT_WORD_PROMPT"]
    HINT_WORD_TO_IMAGE_PROMPT = prompts["HINT_WORD_TO_IMAGE_PROMPT"]

    # 타겟 단어 가져와서 순서대로
    for i, _target in enumerate(target_words):
        if _target not in df["target"].unique():
            print(f"### target : {_target}")
            # 만들기
            hint_word_prompt = HINT_WORD_PROMPT[:]
            hint_word_prompt = hint_word_prompt.replace("[input]", _target)
            print(f"- hint_word_prompt: {hint_word_prompt}")

            # 힌트 단어 생성
            gen_results = generate_text(model="gpt-4o",
                                        user_prompt=hint_word_prompt,
                                        params={
                                            "temperature": 1.5,
                                            "max_tokens": 34
                                            },
                                        response_format=None
                                        )
            if gen_results:
                gen_results = gen_results.choices[0].message.content
            else:
                print("df 저장")
                df.to_csv("app/resources/single_mode_set.csv", index=False)

                break

            hint_words = gen_results.split(",")
            hint_words = [v.strip() for v in hint_words]

            print(f"\n- hint단어 생성!: {hint_words}\n")
            
            # 각 힌트 단어별 이미지 생성
            print("힌트별 이미지 프롬프트 생성")
            hint_img_prompts, hint_b64_imgs = [], []
            # hint_img_prompts, hint_img_urls = [], []
            for hint_word in hint_words:
                print(f"  - hint: {hint_word}")
                hint_word_to_img_prompt = HINT_WORD_TO_IMAGE_PROMPT[:]
                hint_word_to_img_prompt = hint_word_to_img_prompt.replace("[input]", hint_word)
                print(f"  - hint image prompt for gen image: {hint_word_to_img_prompt}\n\n")
                
                hint_image_prompt = generate_text(model="gpt-4o",
                                            user_prompt=hint_word_to_img_prompt,
                                            params={
                                                "temperature": 1.5,
                                                "max_tokens": 128
                                                },
                                            response_format=None
                                            )
                if hint_image_prompt:
                    hint_image_prompt = hint_image_prompt.choices[0].message.content
                else:
                    print("df 저장")
                    df.to_csv("app/resources/single_mode_set.csv", index=False)

                    break
                print(f"    - hint_image_prompt: {hint_image_prompt}")
                hint_img_prompts.append(hint_image_prompt)

                # hint_image_url = call_dalle_api(model="dall-e-3", prompt=hint_image_prompt)
                # hint_img_urls.append(hint_image_url)
                hint_b64_img = call_dalle_api(model="dall-e-3", prompt=hint_image_prompt, response_format="b64_json")
                resized_hint_b64_img = resize_base64_image(hint_b64_img, 300, 300)
                hint_b64_imgs.append(resized_hint_b64_img)
                
            df_tmp = pd.DataFrame({"target": [_target]*len(hint_b64_imgs),
                                   "hint": hint_words,
                                   "hint_image_prompt": hint_img_prompts,
                                   "hint_b64_img": hint_b64_imgs
                                   })
            df = pd.concat([df, df_tmp], ignore_index=True)

            if i > 10:
                break

    # df로 저장??
    print("df 저장")
    df.to_csv("app/resources/single_mode_set.csv", index=False)
    
