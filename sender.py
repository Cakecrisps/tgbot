from flask import Flask, jsonify, request
from index import *
from kb import *
from bd import *
from aiogram import Bot, Dispatcher
import os
from index import *
import nest_asyncio
from waitress import serve
nest_asyncio.apply()
app = Flask(__name__)
bot = Bot(token="TOKEN")
from bd import gettokens, edittokens

@app.route("/", methods=["POST"])
async def st():
    js = request.get_json()
    print(js)
    call = js['body']
    size = js['size']
    scale = js['scale']
    chatId = js['chatid']
    userId = js['userid']
    current_tokens = gettokens(userId)[2]
    checkValidValue = checkValid(call, userId)
    if (checkValidValue):
        nameImg = createImg(call, size, scale)
        with open(f"{nameImg}.png", "rb") as f:
            await bot.send_photo(chatId, f, call)
            os.remove(f"{nameImg}.png")
        return 'ok'
    else:
        await bot.send_message(chatId, 'К сожалению, одна из ваших выбранных Lora доступна только по подписке или при условии, что у вас 10 или более токенов :(. Ознакомиться с тарифами - /buy')
        edittokens(userId, current_tokens+1)

if __name__ == "__main__":
    serve(app, host="127.0.0.1", port=5000)
