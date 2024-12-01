# https://platform.stability.ai/pricing
# https://platform.stability.ai/docs/api-reference
# 가장 싸고 빠른 모델 API 사용하기

from io import BytesIO
import IPython
import json
import os
from PIL import Image
import requests
import time

import base64
import os
import requests

engine_id = "stable-diffusion-v1-6"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = os.getenv("STABILITY_API_KEY")

if api_key is None:
    raise Exception("Missing Stability API key.")

def call_sdxl_1_0_api(image_prompt: str, save_path: str):
    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": image_prompt
                }
            ],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    for i, image in enumerate(data["artifacts"]):
        with open(save_path, "wb") as f:
            f.write(base64.b64decode(image["base64"]))
