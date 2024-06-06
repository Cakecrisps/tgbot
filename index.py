import json
import base64
import requests
import random
import string
from bd import checkdate, gettokens

bannedLoras = ["<lora:gwen", "<lora:olyatb"]


def submit_post(url: str, data: dict):
    return requests.post(url, data=json.dumps(data))


def checkValid(prompt, id):
    for i in bannedLoras:
        if i in prompt and not checkdate(id) and gettokens(id)[2] < 10:
            return False
    return True


def save_encoded_image(b64_image: str, output_path: str):
    with open(output_path, "wb") as image_file:
        image_file.write(base64.b64decode(b64_image))


def generate_random_string(length):
    letters = string.ascii_uppercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


def createImg(prompt, scale, hires):
    if (scale == "vert"):
        height = 768
        width = 512
    elif (scale == "hor"):
        width = 768
        height = 512
    elif (scale == "sq"):
        width = 512
        height = 512
    txt2img_url = 'http://127.0.0.1:7860/sdapi/v1/txt2img'
    data = {'prompt': prompt,
            "height": height, "width": width, "negative_prompt": "easynegative bad_prompt, black and white,", "steps": 20}
    response = submit_post(txt2img_url, data)
    print(response)
    # print(response)
    namePick = generate_random_string(10)
    save_encoded_image(
        response.json()['images'][0], f'{namePick}.png')
    print(json.loads(response.json()['info'])['infotexts'])
    return namePick
