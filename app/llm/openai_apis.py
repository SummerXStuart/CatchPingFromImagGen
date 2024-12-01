from openai import OpenAI
import os

# TODO key추가해서 관리하기
os.environ["OPENAI_API_KEY"] = ""

# 아래는 예제
client = OpenAI()


def generate_text(model, system_prompt, user_prompt, params, response_format):
    """Generate text using open ai API

    Args:
        model (_type_): _description_
        system_prompt (_type_): _description_
        user_prompt (_type_): _description_
        params (_type_): _description_
        response_format (_type_): _description_
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system", 
                "content": system_prompt
            },
            {
                "role": "user", 
                "content": user_prompt
            }
        ],
        response_format=response_format,
        **params
    )

    print(response)
    print(response.choices[0].message.content)
    return response