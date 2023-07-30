from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def change_screen():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text='📲 Сменить ширину экранов')

    markup.add(btn)
    return markup

def change_screen_round():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton(text='📲 Сменить ширину экранов')
    btn2 = KeyboardButton(text='🔄 Сменить кол-во знаков после запятой')

    markup.row(btn1, btn2)
    return markup

