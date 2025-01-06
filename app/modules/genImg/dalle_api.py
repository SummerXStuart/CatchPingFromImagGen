import openai 
import os
from time import time
# from app.modules.utils.link_shortener import shorten
import traceback

openai_api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key = openai_api_key)

# Call the API
def call_dalle_api(model, prompt, size:str="1024x1024", quality:str="standard", n:int=1, response_format="url"):
    # 1장 생성 시 0.03$ 
    start = time()
    try:
        response = client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality,
            n=n,
            response_format=response_format
        )
    except:
        print(traceback.format_exc())
        return None
        
    elapsed_time = time() - start

    # url = response.data[0].url
    # short_url = shorten(url)
    print(f"elapsed_time: {elapsed_time}")
    
    # return url
    return response.data[0].b64_json


import requests
from io import BytesIO
from PIL import Image
import base64

def resize_image(image_url, target_width, target_height):
    # 이미지 다운로드
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    # 이미지 크기 변경
    resized_img = img.resize((target_width, target_height))

    # 변경된 이미지 반환
    return resized_img

def img_to_base64(img):
    # 이미지를 BytesIO로 변환
    buffered = BytesIO()
    img.save(buffered, format="PNG")

    # base64로 인코딩
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return img_base64

def img_file_to_base64(img_file_path):
    img = Image.open(img_file_path)
    
    # 이미지를 BytesIO로 변환
    buffered = BytesIO()
    img.save(buffered, format="PNG")

    # base64로 인코딩
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return img_base64


def save_base64_image(base64_str, file_path):
    # base64 문자열을 바이트로 디코딩
    img_data = base64.b64decode(base64_str)
    
    # 디코딩된 바이트 데이터를 파일로 저장
    with open(file_path, 'wb') as f:
        f.write(img_data)
    print(f"save {file_path}")
        
def resize_base64_image(base64_str, target_width, target_height):
    # base64 문자열을 바이트로 디코딩
    img_data = base64.b64decode(base64_str)
    
    # 바이트 데이터를 이미지로 변환
    img = Image.open(BytesIO(img_data))
    
    # 이미지 크기 변경
    resized_img = img.resize((target_width, target_height))
    
    # 이미지를 BytesIO로 변환
    buffered = BytesIO()
    resized_img.save(buffered, format="PNG")

    # base64로 인코딩
    resized_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return resized_base64

if __name__ == "__main__":
    model_name = "dall-e-3"
    # prompt = "A dynamic and energetic marathon race scene, with a diverse group of runners in athletic gear, sprinting through a bustling city street. The runners are determined and focused, with sweat glistening on their faces, and the crowd cheering from the sidelines. Tall skyscrapers line the background, and the sky is bright with the energy of the event. The runners are diverse in age, gender, and ethnicity, capturing the inclusive and challenging nature of a marathon race."
    prompt = 'A detailed sketch of a traditional Korean turtle ship ("Geobukseon") from the Joseon dynasty, featuring its armored shell-like roof covered with spikes, a dragon-shaped head at the bow emitting smoke, and sailors actively engaged on the deck, set against the backdrop of a calm sea with mountains in the distance. The style is intricate and monochromatic, evoking historical and cultural significance.'
    """
    https://oaidalleapiprodscus.blob.core.windows.net/private/org-AzrspxicrlUwmwfkL0uonb8p/user-ktNL6obxumeplHBAVmmFrjZu/img-v9MxnSCTGnKE6QbFa3lLqWke.png?st=2025-01-01T10%3A06%3A12Z&se=2025-01-01T12%3A06%3A12Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-12-31T22%3A41%3A27Z&ske=2025-01-01T22%3A41%3A27Z&sks=b&skv=2024-08-04&sig=DsH5E0JK4EU2%2BbfRn4aXPk8OFx0NbY6i/sdWRCSVMRM%3D
    """
    # url = call_dalle_api(model_name, prompt)
    # print(f"url: {url}")
    # original_b64 = call_dalle_api(model_name, prompt)
    # save_base64_image(original_b64, "original_turtleship.png")
    
    # resized_b64_img = resize_base64_image(original_b64, 300, 300)
    # save_base64_image(resized_b64_img, "resize_300_300_turtleship.png")
    
    # resized_img = resize_image(url, 300, 300)
    # b64_img = img_to_base64(resized_img)
    # print(f"base64 image\n{b64_img}")
    
    b64_img = img_file_to_base64("resize_300_300_turtleship.png")
    print(len(b64_img))