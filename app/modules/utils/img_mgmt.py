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

