
from app.modules.genImg.dalle_api import call_dalle_api
from app.modules.llm.openai_apis import generate_text
from app.modules.search.words import (
    get_full_target_words,
    get_single_play_set
)
import yaml

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


    # 타겟 단어 가져와서 순서대로
    for i, _target in enumerate(target_words):
        print(f"### target : {_target}")
        if _target not in df["target"]:
            # 만들기
            hint_word_prompt = prompts["HINT_WORD_PROMPT"]
            hint_word_prompt = hint_word_prompt.replace("[input]", _target)
            print(f"- hint_word_prompt: {hint_word_prompt}")

            # 힌트 단어 생성
            gen_results = generate_text(model="gpt-4o",
                                        user_prompt=hint_word_prompt,
                                        params={
                                            "temperature": 1.5,
                                            },
                                        response_format=None
                                        )
            if gen_results:
                gen_results = gen_results.choices[0].message.content
            else:
                # TODO 여기까지라도 저장하기
                break

            hint_words = gen_results.split(",")
            hint_words = [v.strip() for v in hint_words]

            print(f"\n- hint단어 생성!: {hint_words}\n")
            
            # 각 힌트 단어별 이미지 생성
            # print("힌트별 이미지 프롬프트 생성")
            # for hint_word in hint_words:
            #     print(f"  - hint: {hint_word}")
            #     HINT_WORD_TO_IMAGE_PROMPT = prompts["HINT_WORD_TO_IMAGE_PROMPT"]
            #     HINT_WORD_TO_IMAGE_PROMPT = HINT_WORD_TO_IMAGE_PROMPT.replace("[input]", hint_word)
            #     print(f"  - hint image prompt: {HINT_WORD_TO_IMAGE_PROMPT}\n\n")

            # # 이미지 생성
            # print("이미지 생성")

            # # 생성된 이미지 링크를 shorten
            # print("shorten url")
            if i > 0:
                break

            

    # df로 저장??
    print("df 저장")
    # target word, hint word, hint image shorten url

    # 저장

