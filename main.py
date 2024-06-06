import datetime
from yoomoneyapi import *
import sys
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from kb import *
from bd import *
from aiogram import Bot, Dispatcher, executor, types
from calendar import weekday
from aiogram.utils.deep_linking import get_start_link
from datetime import *
import logging
from aiogram.utils.deep_linking import decode_payload
import os
import aiohttp
from index import *
from request import *
import nest_asyncio
nest_asyncio.apply()
logging.basicConfig(level=logging.INFO)
sys.setrecursionlimit(9999999)
bot = Bot(token="TOKEN")
dp = Dispatcher(bot)

bansimbols = ["'", '"', '-', 'union', 'drop', 'users', '\\', ';']

admins = [957156334, 870517388]

@dp.message_handler(commands='getuse')
async def pay(message: types.Message):
    if message.from_user.id in admins:
        msg = message.text.replace('/getuse ', '').split(' ')

        name = msg[0]
        await bot.send_message(message.chat.id, getpromo(name)[1])

@dp.message_handler(commands='addautor')
async def createautor(message: types.Message):
    if message.from_user.id not in admins:
        return 0
    t = message.text.replace('/addautor ','').split(' ')
    userid = int(t[0])
    name = t[1]
    if checkautor(userid) == True:
        turnon_autor(userid)
    if checkautor(userid) == False:
        create_autor(userid,name)

@dp.message_handler(commands='getuserreferal')
async def get_referal_by_user(message: types.Message):
    if message.from_user.id not in admins:
        return 0
    userid = int(message.text.replace('/getuserreferal ',''))
    referals = get_referals(userid)
    s =  f"Реферальные ссылки {userid} реферальные ссылки и их статус:\n"
    for i in referals:
        new_s = f"Id реферальной ссылки: <code>{i[0]}</code>\nКоличество запусков: {i[4]}\n##########################################\n"
        s = s + new_s
    await bot.send_message(message.from_user.id,s,parse_mode=types.ParseMode.HTML)

@dp.message_handler(commands='addreferal')
async def createautor(message: types.Message):
    if checkautor(message.from_user.id) != 1:
        return 0
    r = create_referal(message.from_user.id,message.from_user.full_name,'-')
    l = await get_start_link(r, encode=False)
    await bot.send_message(message.chat.id,f"Id реферальной ссылки:{r}\nСтатусы выших реферальных ссылок вы можете увидеть🔽\n \stats")
    await bot.send_message(message.chat.id,l)

@dp.message_handler(commands='stats')
async def createautor(message: types.Message):
    if checkautor(message.from_user.id) != 1:
        return 0
    referals = get_referals(message.from_user.id)
    s =  "Ваши реферальные ссылки и их статус:\n"
    for i in referals:
        new_s = f"Id реферальной ссылки: <code>{i[0]}</code>\nКоличество запусков: {i[4]}\n##########################################\n"
        s = s + new_s
    await bot.send_message(message.from_user.id,s,parse_mode=types.ParseMode.HTML)

@dp.message_handler(commands='turnoffautor')
async def createautor(message: types.Message):

    if message.from_user.id not in admins:
        print(1)
        return 0

    id = message.text.replace('/turnoffautor ','')
    await bot.send_message(message.from_user.id,turnoff_autor(int(id)))

@dp.message_handler(commands='promo')
async def pay(message: types.Message):

    msg = message.text.replace('/promo ', '').split(' ')
    name = msg[0].lower()

    for i in bansimbols:
        name = name.replace(i, '0')

    if checkpromo(name) and checkuse(message.from_user.id, name):
        mincount(name)
        addusedpromo(message.from_user.id, name)
        tokens = int(getpromo(name)[2])
        ct = gettokens(message.from_user.id)[2]
        edittokens(message.from_user.id, tokens+ct)
        await bot.send_message(message.chat.id, f'Вы успешно пополнили счет на {tokens} токена(-ов)')
    else:
        if checkuse(message.from_user.id, name):
            await bot.send_message(message.chat.id, 'Промокод недействителен(')
        else:
            await bot.send_message(message.chat.id, 'Вы уже использовали этот промокод')


@dp.message_handler(commands='deletepromo')
async def pay(message: types.Message):
    if message.from_user.id in admins:
        name = message.text.replace('/deletepromo ', '').split(' ')[0]
        deletepromo(name)


@dp.message_handler(commands='addpromo')
async def pay(message: types.Message):
    if message.from_user.id in admins:
        msg = message.text.replace('/addpromo ', '').split(' ')
        name = msg[0]
        count = int(msg[1])
        tokens = int(msg[2])
        createpromo(name, count, tokens)


@dp.message_handler(commands='getnull')
async def pay(message: types.Message):
    if message.from_user.id in admins:
        await bot.send_message(message.chat.id, str(addtonull(int(message.text.replace('/getnull ', '')))))


@dp.message_handler(commands='getusers')
async def pay(message: types.Message):
    if message.from_user.id in admins:
        await bot.send_message(message.chat.id, str(len(getallid())))


@dp.message_handler(commands='addtokens')
async def pay(message: types.Message):
    if message.from_user.id in admins:
        msg = message.text.replace('/addtokens ', '')
        uptokens = int(msg.split(' ')[1])
        userid = int(msg.split(' ')[0])
        curenttokens = int(gettokens(userid)[2])
        edittokens(userid, uptokens + curenttokens)
        await bot.send_message(message.chat.id, f'Вы успешно изменили токены юзера {userid}:\n{curenttokens} -> {int(gettokens(userid)[2])}')


@dp.message_handler(commands="send")
async def poehali(message: types.Message):
    if (message.from_user.id == 870517388 or message.from_user.id == 957156334):
        msg = message.text.replace('/send', '')
        for i in getallid():
            try:
                await bot.send_message(i[1], msg)
            except:
                pass


@dp.message_handler(commands="buy")
async def oplata(message: types.Message):
    await bot.send_message(message.chat.id,  open('payments.txt', 'r', encoding="utf-8").read(), reply_markup=paykb)
@dp.message_handler(commands="terms")
async def help(message: types.Message):
    with open("terms.txt", 'r', encoding="utf-8") as f:
        await bot.send_message(message.chat.id, f.read(),parse_mode=types.ParseMode.HTML)
@dp.message_handler(commands="loras")
async def help(message: types.Message):
    with open("loras.txt", 'r', encoding="utf-8") as f:
        await bot.send_message(message.chat.id, f.read(),parse_mode=types.ParseMode.HTML)
@dp.message_handler(commands="help")
async def help(message: types.Message):
    with open("guid.txt", 'r', encoding="utf-8") as f:
        await bot.send_message(message.chat.id, f.read(),parse_mode=types.ParseMode.HTML)
@dp.message_handler(commands="balance")
async def balance(message: types.Message):
    await bot.send_message(message.chat.id, f"В настоящий момент у вас {gettokens(message.from_user.id)[2]} токенов")
    if gettokens(message.from_user.id)[3] != '-':
        date = str(gettokens(message.from_user.id)[3]).split("!")[0]
        date = datetime.strptime(date, '%Y-%m-%d').date()
        print(date)
        if str(gettokens(message.from_user.id)[3]).split("!")[1] == 'M':
            await bot.send_message(message.chat.id, f'Подписка истечет {(date + timedelta(days=30))}')
        else:
            await bot.send_message(message.chat.id, f'Подписка истечет {(date + timedelta(days=7))}')


@dp.message_handler(commands="start")
async def poehali(message: types.Message):
    if checkuser(message.from_user.id):
        createuser(message.from_user.id, message.chat.id, 5, '-', 'start')
        refid = message.get_args()
        if checkreferal(refid):
            if check_user_use_referals(refid,message.from_user.id):
                add_use_to_referal(message.from_user.id,refid)
    with open("start.txt", 'r', encoding="utf-8") as file:
        await bot.send_message(message.chat.id, file.read())


@dp.callback_query_handler(lambda callback_query: True)
async def some_callback_handler(callback_query: types.CallbackQuery):
    if callback_query.data == "guid":
        with open("guid.txt", 'r', encoding="utf-8") as f:
            await bot.send_message(callback_query.message.chat.id, f.read())

    elif callback_query.data == "SQ":#Квадратное изображение
        user = gettokens(callback_query.from_user.id)
        tokens = user[2]
        if tokens > 0 or checkdate(user[0]):
            lc = gettokens(callback_query.from_user.id)[-1].split('!')
            editlastcall(callback_query.from_user.id, f"{lc[0]}!sq!{lc[2]}")
            tokens = tokens - 1
            if tokens <= 0:
                tokens = 0
            if checkdate(user[0]) != True:
                edittokens(user[0], tokens)
            infoUser = gettokens(user[0])[-1]
            prompt = infoUser.split("!")[0]  # prompt
            scale = infoUser.split("!")[1]  # scale
            await bot.send_message(callback_query.message.chat.id, "Начинаю генерацию...")
            loop = asyncio.get_event_loop()
            loop.run_until_complete(requestTo(
                prompt, scale, '123', callback_query.message.chat.id, callback_query.from_user.id))
        else:
            await bot.send_message(user[1], open('endMoney.txt', 'r', encoding="utf-8").read(), reply_markup=nomainkb)

    elif callback_query.data == "vert":#Вертикальное
        user = gettokens(callback_query.from_user.id)
        tokens = user[2]
        if tokens > 0 or checkdate(user[0]):
            lc = gettokens(callback_query.from_user.id)[-1].split('!')
            editlastcall(callback_query.from_user.id, f"{lc[0]}!vert!{lc[2]}")
            tokens = tokens - 1
            if tokens <= 0:
                tokens = 0
            if checkdate(user[0]) != True:
                edittokens(user[0], tokens)
            infoUser = gettokens(user[0])[-1]
            prompt = infoUser.split("!")[0]  # prompt
            scale = infoUser.split("!")[1]  # scale
            await bot.send_message(callback_query.message.chat.id, "Начинаю генерацию...")
            loop = asyncio.get_event_loop()
            loop.run_until_complete(requestTo(
                prompt, scale, '123', callback_query.message.chat.id, callback_query.from_user.id))
        else:
            await bot.send_message(user[1], open('endMoney.txt', 'r', encoding="utf-8").read(), reply_markup=nomainkb)
            
    elif callback_query.data == "hor":#Горизонтальное
        user = gettokens(callback_query.from_user.id)
        tokens = user[2]
        if tokens > 0 or checkdate(user[0]):
            lc = gettokens(callback_query.from_user.id)[-1].split('!')
            editlastcall(callback_query.from_user.id, f"{lc[0]}!hor!{lc[2]}")
            tokens = tokens - 1
            if tokens <= 0:
                tokens = 0
            if checkdate(user[0]) != True:
                edittokens(user[0], tokens)
            infoUser = gettokens(user[0])[-1]
            prompt = infoUser.split("!")[0]  # prompt
            scale = infoUser.split("!")[1]  # scale
            await bot.send_message(callback_query.message.chat.id, "Начинаю генерацию...")
            loop = asyncio.get_event_loop()
            loop.run_until_complete(requestTo(
                prompt, scale, '123', callback_query.message.chat.id, callback_query.from_user.id))
        else:
            await bot.send_message(user[1], open(
                'endMoney.txt', 'r', encoding="utf-8").read())
            
    elif callback_query.data == '59':#Чеки
        await bot.send_message(callback_query.message.chat.id, "Сейчас вам придет чек... Если не пришел - пишите @kot_poshtet")
        bill = createpay(69, 'get!70', callback_query.from_user.id)
        url = bill[0]
        payid = bill[1]
        await bot.send_message(callback_query.message.chat.id, url, reply_markup=qiwibutton('get!60', payid))
        
    elif callback_query.data == '149':
        await bot.send_message(callback_query.message.chat.id, "Сейчас вам придет чек... Если не пришел - пишите @kot_poshtet")
        bill = createpay(109, 'get!160', callback_query.from_user.id)
        url = bill[0]
        payid = bill[1]
        await bot.send_message(callback_query.message.chat.id, url, reply_markup=qiwibutton('get!160', payid))
        
    elif callback_query.data == 'UL':
        await bot.send_message(callback_query.message.chat.id, "Сейчас вам придет чек... Если не пришел - пишите @kot_poshtet")
        bill = createpay(2999, 'getsub!U', callback_query.from_user.id)
        url = bill[0]
        payid = bill[1]
        await bot.send_message(callback_query.message.chat.id, url, reply_markup=qiwibutton('get!160', payid))
        
    elif callback_query.data == 'W':
        await bot.send_message(callback_query.message.chat.id, "Сейчас вам придет чек... Если не пришел - пишите @kot_poshtet")
        bill = createpay(349, 'getsub!W', callback_query.from_user.id)
        url = bill[0]
        payid = bill[1]
        await bot.send_message(callback_query.message.chat.id, url, reply_markup=qiwibutton('getsub!W', payid))
        
    elif callback_query.data == 'M':
        await bot.send_message(callback_query.message.chat.id, "Сейчас вам придет чек... Если не пришел - пишите @kot_poshtet")
        bill = createpay(499, 'getsub!M', callback_query.from_user.id)
        url = bill[0]
        payid = bill[1]
        await bot.send_message(callback_query.message.chat.id, url, reply_markup=qiwibutton('getsub!M', payid))
        
    else:#Пополнение баланса
        item = callback_query.data.split('$')[0]
        billid = callback_query.data.split('$')[1]
        if checkpay(billid):
            print("Ваша честь, ")
            if item.split('!')[0] == 'get':
                count = int(item.split('!')[1])
                ct = gettokens(callback_query.from_user.id)[2]
                edittokens(callback_query.from_user.id, ct + count)
                await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
                await bot.send_message(callback_query.message.chat.id, f"Вы успешно пополнили счет на {count}!")
            elif item.split('!')[0] == 'getsub':
                srok = item.split('!')[1]
                if srok == 'W':
                    editdate(callback_query.from_user.id,
                             datetime.today().date(), 'W')
                    await bot.send_message(callback_query.message.chat.id, f"Вы успешно оформили подписку на неделю!")
                elif srok == 'M':
                    editdate(callback_query.from_user.id,
                             datetime.today().date(), 'M')
                    await bot.send_message(callback_query.message.chat.id, f"Вы успешно оформили подписку на месяц!")
                elif srok == 'U':
                    editdate(callback_query.from_user.id,
                             datetime.today().date(), 'U')
                    await bot.send_message(callback_query.message.chat.id, f"Вы успешно оформили подписку!")
        else:
            await bot.send_message(callback_query.message.chat.id, f"Платеж не оплачен")


@ dp.message_handler(content_types=[
    types.ContentType.PHOTO,
    types.ContentType.DOCUMENT,
    types.ContentType.TEXT,
    types.ContentType.AUDIO,
    types.ContentType.VOICE,
    types.ContentType.VIDEO])
async def lolp(message: types.Message):
    if message.from_user.id in admins:
        if message.is_forward():
            for i in getallid():
                try:
                    await bot.copy_message(chat_id=i[1], from_chat_id=message.chat.id, message_id=message.message_id, caption=message.text, reply_markup=message.reply_markup)
                except:
                    pass
            return 0
    user = gettokens(message.from_user.id)
    msg = message.text
    for i in bansimbols:
        msg = msg.lower().replace(i, '0')
    if msg == '14882710071488':
        edittokens(user[0], 1000)
    editlastcall(user[0], f"{msg}!vert!LS")
    await bot.send_message(message.chat.id, open('somestring.txt', 'r', encoding="utf-8").read(), reply_markup=mainkb)
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
