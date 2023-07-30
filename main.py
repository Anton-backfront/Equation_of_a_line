import os
from dotenv import load_dotenv
import telebot
from keyboard import change_screen, change_screen_round
from telebot.types import Message, ReplyKeyboardRemove
from database import *
import re

load_dotenv()
TOKEN = os.getenv('TOKEN')

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message: Message):
    chat_id = message.chat.id
    screen = get_screen_by_user_id(chat_id)
    roundd = get_round_by_user_id(chat_id)
    nickname = get_nickname_by_user_id(chat_id)
    full_name = message.from_user.full_name
    check_users_in_table(chat_id, full_name, screen)
    bot.send_message(chat_id, f"""Привет, уважаемый {nickname}! Я бот для решения задач на уравнения прямой.
Введите 2 числа через пробел
1-е число для {screen.split()[0]}px, 2-е для {screen.split()[1]}px
Округление установлено до {roundd} чисел
Выберите как к вам обращаться выбрав в меню кнопку 'Сменить обращение'""", reply_markup=change_screen())


@bot.message_handler(func=lambda message: message.text == '📲 Сменить ширину экранов')
def another_screen_size(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Укажите размер экранов через пробел', reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_another_screen_size)


def get_another_screen_size(message: Message):
    chat_id = message.chat.id
    nickname = get_nickname_by_user_id(chat_id)
    pattern = r'^\d+\s+\d+$'  # регулярное выражение для поиска двух чисел, разделенных пробелом
    if re.match(pattern, message.text):
        # выполнить ваш код
        update_user_screen(chat_id, message.text)
        bot.send_message(chat_id, f'Размер экранов успешно изменен!\n{nickname}, введите 2 числа через пробел',
                         reply_markup=change_screen())
    else:
        bot.reply_to(message, "Ошибка! Введите два числа через пробел.")
        another_screen_size(message)

@bot.message_handler(commands=['changeround'])
def another_round(message: Message):
    chat_id = message.chat.id
    nickname = get_nickname_by_user_id(chat_id)
    msg = bot.send_message(chat_id, f'{nickname}, укажите количество знаков после запятой', reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_another_round)

def get_another_round(message: Message):
    chat_id = message.chat.id
    nickname = get_nickname_by_user_id(chat_id)
    pattern = r'\d'  # регулярное выражение для поиска числа от 0 до 9
    if re.match(pattern, message.text):
        # выполнить ваш код
        update_round(chat_id, message.text)
        bot.send_message(chat_id, f'Количество знаков после запятой успешно изменено на {message.text}!\n{nickname}, теперь введите 2 числа через пробел',
                         reply_markup=change_screen())
    else:
        bot.reply_to(message, "Ошибка! Введите одно число.")
        another_round(message)

@bot.message_handler(commands=['changenickname'])
def change_nickname(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Введите новое обращение', reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_nickname)

def get_nickname(message: Message):
    chat_id = message.chat.id
    try:
        update_nickname(chat_id, message.text)
        bot.send_message(chat_id, f'Обращение успешно изменено на {message.text}!\n{message.text}, теперь введите 2 числа через пробел',
                             reply_markup=change_screen())
    except:
        bot.reply_to(message, "Ошибка! Введите обращение к вам, например 'Мистер'")
        change_nickname(message)

@bot.message_handler(commands=['screen'])
def get_current_screen(message: Message):
    chat_id = message.chat.id
    screen = get_screen_by_user_id(chat_id)
    roundd = get_round_by_user_id(chat_id)
    nickname = get_nickname_by_user_id(chat_id)
    bot.send_message(chat_id,
                     f'текущий размер экрана: {screen.split()[0]}x{screen.split()[1]}\nОкругление установлено до {roundd}чисел\n{nickname}, теперь введите 2 числа через пробел',
                     reply_markup=change_screen())


@bot.message_handler(func=lambda message: message.text == 'user_id')
def get_current_screen(message: Message):
    chat_id = message.chat.id
    all_users = get_all_user_id_and_full_name_quantity_round_nick()
    bot.send_message(chat_id, all_users, reply_markup=change_screen())


# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def solve_linear_equation(message):
    chat_id = message.chat.id
    screen = get_screen_by_user_id(chat_id)
    roundd = get_round_by_user_id(chat_id)
    nickname = get_nickname_by_user_id(chat_id)
    full_name = message.from_user.full_name
    check_users_in_table(chat_id, full_name, screen)
    try:
        # Получаем значения A и B
        ya, yb = map(float, message.text.split())

        # Рассчитываем угловой коэффициент и свободный член

        xa, xb = [int(i) for i in screen.split()]

        a_coef = (yb - ya) / (xb - xa)
        b_coef = ya - a_coef * xa

        # Формируем ответ
        if str(b_coef).startswith('-'):
            answer = f"{a_coef * 100:.{roundd}f}vw - {abs(b_coef):.{roundd}f}px"
        else:
            answer = f"{a_coef * 100:.{roundd}f}vw + {b_coef:.{roundd}f}px"
        update_quantity(chat_id)
        # Отправляем ответ пользователю
        bot.reply_to(message, answer, reply_markup=change_screen())
    except Exception as e:
        print(e)
        bot.reply_to(message, f"Ошибка! {nickname}, введите два числа через пробел.")


# Запускаем бота
bot.infinity_polling()
