# - * - coding: utf - 8 -*-

import io
import re

import telebot

import config

bot = telebot.TeleBot(config.token)

print(bot.get_me())
isAdmin = False
isStudent = False
Whitelist = config.Whitelist
Masterkey = config.Masterkey
Students = config.Students


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    with io.open(Whitelist, 'r', encoding='utf-8') as file:
        for line in file:
            if message.from_user.username in line:
                global isAdmin
                isAdmin = True
                user_markup.row = ('Все вопросы студентов')
                user_markup.row = ('Новые вопросы студентов')
                user_markup.row = ('Старые вопросы студентов')
                bot.send_message(message.chat.id, 'Добро пожаловать, ' + line[line.find(':') + 1:],
                                 reply_markup=user_markup)
    if not isAdmin:
        with io.open(Students, 'r', encoding='utf-8') as file:
            for line in file:
                if message.from_user.username in line:
                    global isStudent
                    isStudent = True
                    user_markup.row = ('Задать вопрос деканату')
                    user_markup.row = ('Узнать расписание')
                    user_markup.row = ('Проверить посещаемость')
                    bot.send_message(message.chat.id, 'Добро пожаловать, ' + line.split(':')[1],
                                     reply_markup=user_markup)
    if not isStudent:
        user_markup.row('Зарегистрироваться как студент')
        user_markup.row('Зарегистрироваться как сотрудник деканата')
        bot.send_message(message.chat.id, 'Пожалуйста, зарегистрируйтесь', reply_markup=user_markup)


@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text == 'Меню' or message.text == 'Главная страница':
        if isStudent:
            studentmenu(message)
        elif isAdmin:
            adminmenu(message)
    else:
        registration(message)


def registration(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    if message.text == 'Зарегистрироваться как студент':
        bot.send_message(message.chat.id, 'Введите ваше имя, фамилию и номер группы')
    elif message.text == 'Зарегистрироваться как сотрудник деканата':
        bot.send_message(message.chat.id, 'Введите уникальный пароль деканата')
    elif re.match('[А-я ]+-[0-9]{4}', message.text):
        with io.open(Students, 'a', encoding='utf-8') as file:
            lines = message.text.split(' ')
            line = message.from_user.username + ':' + lines[0] + ' ' + lines[1] + ':' + lines[2] + '\n'
            file.write(line)
            line = 'Вы успешно зарегистрировались как ' + lines[0] + ' ' + lines[1]
            user_markup.row = 'Главная страница'
            bot.send_message(message.chat.id, line)
    elif re.match('[0-9a-z]{5}', message.text):
        with io.open(Whitelist, 'a', encoding='utf-8') as file:
            if message.text == Masterkey:
                file.write(message.from_user.username + '\n')
                user_markup.row = 'Главная страница'
                bot.send_message(message.chat.id, 'Вы успешно зарегистрировались как сотрудник деканата',
                                 reply_markup=user_markup)
            else:
                bot.send_message(message.chat.id, 'Введённый пароль не подходит')


def studentmenu(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row = ('Задать вопрос деканату')
    user_markup.row = ('Узнать расписание')
    user_markup.row = ('Проверить посещаемость')
    bot.send_message(message.chat.id, 'Меню:', reply_markup=user_markup)


def adminmenu(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row = ('Все вопросы студентов')
    user_markup.row = ('Новые вопросы студентов')
    user_markup.row = ('Старые вопросы студентов')
    bot.send_message(message.chat.id, 'Меню:', reply_markup=user_markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
