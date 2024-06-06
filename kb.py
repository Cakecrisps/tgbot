from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
guide_button = InlineKeyboardButton("Обучение", callback_data="guid")
obr60 = InlineKeyboardButton("70 Токенов", callback_data="59")
obr150 = InlineKeyboardButton("160 Токенов", callback_data="149")
UnLimitW = InlineKeyboardButton("Недельная подписка", callback_data="W")
UnLimitM = InlineKeyboardButton("Месячная подписка", callback_data="M")
UnLimit = InlineKeyboardButton("Безлимит навсегда", callback_data="UL")
paykb = InlineKeyboardMarkup().row(obr60, obr150).row(UnLimitW, UnLimitM).row(UnLimit)
vert = InlineKeyboardButton("Вертикальная фотография", callback_data="vert")
guid_kb = InlineKeyboardMarkup().add(guide_button)
hight_rb = InlineKeyboardButton("Квадрат", callback_data="SQ")
buytb = InlineKeyboardButton("Купить токены", callback_data="buy")
gorizontalartb = InlineKeyboardButton(
    "Горизонтальная фотография", callback_data="hor")
mainkb = InlineKeyboardMarkup().add(hight_rb).add(gorizontalartb).add(vert)
nomainkb = InlineKeyboardMarkup().add(buytb)
low = InlineKeyboardButton('Низкое разрешение', callback_data='low')
nohs = InlineKeyboardMarkup().add(low).add(buytb)
omainkb = InlineKeyboardMarkup().add(hight_rb).add(vert).add(buytb)
novert = InlineKeyboardMarkup().add(hight_rb).add(gorizontalartb).add(buytb)
buy = KeyboardButton('/buy')
help = KeyboardButton('/help')
balance = KeyboardButton('/balance')
mainmenu = ReplyKeyboardMarkup().add(buy).add(help).add(balance)


def qiwibutton(item, billid):
    return InlineKeyboardMarkup().add(InlineKeyboardButton('Проверить оплату', callback_data=f"{item}${billid}"))
