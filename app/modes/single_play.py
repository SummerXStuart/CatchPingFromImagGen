
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
from make_img_file import save_base64_image

with open("app/prompts/prompt.yaml") as _f:
    prompts = yaml.safe_load(_f)

def generate_hint_image(hint_word):
    """hint_word에 대한 이미지 만들기

    Args:
        hint_word (_type_): _description_
    """


# 미리 싱글 플레이를 위한 힌트 단어 및 이미지 만들어 놓기
def make_single_play_set(start_num, last_num, save_file=False):
    target_words = get_full_target_words()
    df = get_single_play_set()

    HINT_WORD_PROMPT = prompts["HINT_WORD_PROMPT"]
    HINT_WORD_TO_IMAGE_PROMPT = prompts["HINT_WORD_TO_IMAGE_PROMPT"]
    
    normal = True
    
    # 타겟 단어 가져와서 순서대로
    # for i, _target in enumerate(target_words, start=51):
    for i in range(start_num, min(len(target_words), last_num+1), 1):
        _target = target_words[i]
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
                                            "temperature": 1.1,
                                            "max_tokens": 64
                                            },
                                        response_format=None
                                        )
            if gen_results:
                gen_results = gen_results.choices[0].message.content
            else:
                print("df 저장")
                df.to_csv("app/resources/single_mode_set.csv", index=False)
                normal = False

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
                                                "temperature": 1.1,
                                                "max_tokens": 64
                                                },
                                            response_format=None
                                            )
                if hint_image_prompt:
                    hint_image_prompt = hint_image_prompt.choices[0].message.content
                else:
                    print("df 저장")
                    df.to_csv("app/resources/single_mode_set.csv", index=False)
                    normal = False

                    break
                print(f"    - hint_image_prompt: {hint_image_prompt}")
                hint_img_prompts.append(hint_image_prompt)

                # hint_image_url = call_dalle_api(model="dall-e-3", prompt=hint_image_prompt)
                # hint_img_urls.append(hint_image_url)
                hint_b64_img = call_dalle_api(model="dall-e-3", prompt=hint_image_prompt, response_format="b64_json")
                if hint_b64_img is None:
                    print("df 저장")
                    df.to_csv("app/resources/single_mode_set.csv", index=False)
                    normal = False

                    break
                    
                resized_hint_b64_img = resize_base64_image(hint_b64_img, 300, 300)
                hint_b64_imgs.append(resized_hint_b64_img)
                
                if save_file:
                    if len(hint_word) > 40:
                        _path = f"app/resources/ex/{_target}_{hint_word[:30]}.png"
                    else:
                        _path = f"app/resources/ex/{_target}_{hint_word}.png"
                    save_base64_image(resized_hint_b64_img, _path)
                
            
            if normal:
                df_tmp = pd.DataFrame({"target": [_target]*len(hint_b64_imgs),
                                    "hint": hint_words,
                                    "hint_image_prompt": hint_img_prompts,
                                    "hint_b64_img": hint_b64_imgs
                                    })
                df = pd.concat([df, df_tmp], ignore_index=True)

            if i > last_num:
                break
        else:
            # target 있는 행의 정보 알아내기
            df_cur_target = df[df["target"]==_target]
            
            # target만 있을 때, 힌트 생성 -> 이미지 프롬프트 생성 -> 이미지 생성
            # print(f"hint 유무: {df_cur_target['hint'].isna().sum()}")

            # 힌트만 있을 때 -> 이미지 프롬프트 생성 -> 이미지 생성
            
            if df_cur_target['hint_b64_img'].isna().sum() > 0:
                print(f"\ntarget: {_target}")
                print(f"hint_b64_img: {df_cur_target['hint_b64_img'].isna().sum()}")

                for idx, img_absence in zip(df_cur_target['hint_b64_img'].isna().index, df_cur_target['hint_b64_img'].isna()):
                    if img_absence:
                        hint_word = df.iloc[idx, 1]
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
                            normal = False

                            break
                        print(f"    - hint_image_prompt: {hint_image_prompt}")
                        

                        # hint_image_url = call_dalle_api(model="dall-e-3", prompt=hint_image_prompt)
                        # hint_img_urls.append(hint_image_url)
                        hint_b64_img = call_dalle_api(model="dall-e-3", prompt=hint_image_prompt, response_format="b64_json")
                        
                        if hint_b64_img is None:
                            print("df 저장")
                            df.to_csv("app/resources/single_mode_set.csv", index=False)
                            normal = False

                            break
                            
                        
                        resized_hint_b64_img = resize_base64_image(hint_b64_img, 300, 300)
                        
                        df.loc[idx, "hint_image_prompt"] = hint_image_prompt
                        df.loc[idx, "hint_b64_img"] = resized_hint_b64_img
                        
                        if save_file:
                            if len(hint_word) > 40:
                                _path = f"app/resources/ex/{_target}_{hint_word[:30]}.png"
                            else:
                                _path = f"app/resources/ex/{_target}_{hint_word}.png"
                            save_base64_image(resized_hint_b64_img, _path)


            print("============")

            if i > last_num:
                break

    # df로 저장??
    print("df 저장")
    df.to_csv("app/resources/single_mode_set.csv", index=False)
    
def make_the_hints(_target):
    print(f"### target : {_target}")
    # 만들기
    HINT_WORD_PROMPT = prompts["HINT_WORD_PROMPT"]
    hint_word_prompt = HINT_WORD_PROMPT[:]
    hint_word_prompt = hint_word_prompt.replace("[input]", _target)
    # print(f"- hint_word_prompt: {hint_word_prompt}")

    # 힌트 단어 생성
    gen_results = generate_text(model="gpt-4o",
                                user_prompt=hint_word_prompt,
                                params={
                                    "temperature": 1.1,
                                    "max_tokens": 64
                                    },
                                response_format=None
                                )
    if gen_results:
        gen_results = gen_results.choices[0].message.content
    else:
        print("error")
        return []
    
    hint_words = gen_results.split(",")
    hint_words = [v.strip() for v in hint_words]

    for hint in hint_words:
        print(f"- hint: {hint}")