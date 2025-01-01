import openai 
import webbrowser
import os
from time import time
# Replace YOUR_API_KEY with your OpenAI API key
openai_api_key = None

client = openai.OpenAI(api_key = openai_api_key)

# Call the API
def call_dalle_api(model, prompt, size:str="1024x1024", quality:str="standard", n:int=1):
    # 1장 생성 시 0.03$ 
    start = time()
    response = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        quality=quality,
        n=n,
    )
    elapsed_time = time() - start

    url = response.data[0].url
    print(f"url: {url}")
    print(f"elapsed_time: {elapsed_time}")

if __name__ == "__main__":
    model_name = "dall-e-3"
    # prompt = "A dynamic and energetic marathon race scene, with a diverse group of runners in athletic gear, sprinting through a bustling city street. The runners are determined and focused, with sweat glistening on their faces, and the crowd cheering from the sidelines. Tall skyscrapers line the background, and the sky is bright with the energy of the event. The runners are diverse in age, gender, and ethnicity, capturing the inclusive and challenging nature of a marathon race."
    prompt = 'A detailed sketch of a traditional Korean turtle ship ("Geobukseon") from the Joseon dynasty, featuring its armored shell-like roof covered with spikes, a dragon-shaped head at the bow emitting smoke, and sailors actively engaged on the deck, set against the backdrop of a calm sea with mountains in the distance. The style is intricate and monochromatic, evoking historical and cultural significance.'
    """
    https://oaidalleapiprodscus.blob.core.windows.net/private/org-AzrspxicrlUwmwfkL0uonb8p/user-ktNL6obxumeplHBAVmmFrjZu/img-v9MxnSCTGnKE6QbFa3lLqWke.png?st=2025-01-01T10%3A06%3A12Z&se=2025-01-01T12%3A06%3A12Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-12-31T22%3A41%3A27Z&ske=2025-01-01T22%3A41%3A27Z&sks=b&skv=2024-08-04&sig=DsH5E0JK4EU2%2BbfRn4aXPk8OFx0NbY6i/sdWRCSVMRM%3D
    """
    call_dalle_api(model_name, prompt)
