from flask import Flask, request
import os
import telebot


app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)


with open('courses.txt') as file:
    courses = [item.split(',') for item in file]

with open('schedule.txt') as file:
    courses_plan = {
        'start': [],
        'pro': [],
        'other': []
    }
    for item in file:
        if 'start' in item.lower():
            courses_plan['start'].append(item)
        elif 'pro' in item.lower():
            courses_plan['pro'].append(item)
        else:
            courses_plan['other'].append(item)


@bot.message_handler(commands=['start'])
def message_start(message):
    bot.send_message(message.chat.id, 'Hello, user!')


@bot.message_handler(commands=['help'])
def message_help(message):
    bot.send_message(message.chat.id, '/courses - показывает все доступные курсы\n'
                                      '/schedule - показывает текущее расписание')


@bot.message_handler(commands=['courses'])
def list_of_courses(message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)

    for name, link in courses:
        url_button = telebot.types.InlineKeyboardButton(text=name.strip(), url=link.strip(' \n'))
        keyboard.add(url_button)

    bot.send_message(message.chat.id, 'A list of courses:', reply_markup=keyboard)


@bot.message_handler(commands=['schedule'])
def list_of_schedule(message):
    res = ''
    for category in courses_plan:
        for item in courses_plan[category]:
            title, date = item.split(',')
            res += f'<b>{title}</b>: <code>{date}</code>'
        res += '\n'*2

    bot.send_message(message.chat.id, text=res, parse_mode='HTML')


@bot.message_handler(func=lambda x: x.text.startswith('info'))
def get_course_info(message):
    text_from_user = message.json['text']
    if 'python' in text_from_user.lower():
        res = ''
        for category in courses_plan:
            for item in courses_plan[category]:
                title, date = item.split(',')
                if 'python' in title.lower():
                    res += f'<b>{title}</b>: <code>{date}</code>'

        bot.send_message(message.chat.id, text=res, parse_mode='HTML')
    if 'java' in text_from_user.lower():
        res = ''
        for category in courses_plan:
            for item in courses_plan[category]:
                title, date = item.split(',')
                if 'java' in title.lower():
                    res += f'<b>{title}</b>: <code>{date}</code>'

        bot.send_message(message.chat.id, text=res, parse_mode='HTML')
    if 'qa' in text_from_user.lower():
        res = ''
        for category in courses_plan:
            for item in courses_plan[category]:
                title, date = item.split(',')
                if 'qa' in title.lower():
                    res += f'<b>{title}</b>: <code>{date}</code>'

        bot.send_message(message.chat.id, text=res, parse_mode='HTML')
    if 'web design' in text_from_user.lower():
        res = ''
        for category in courses_plan:
            for item in courses_plan[category]:
                title, date = item.split(',')
                if 'web design' in title.lower():
                    res += f'<b>{title}</b>: <code>{date}</code>'

        bot.send_message(message.chat.id, text=res, parse_mode='HTML')
    if 'front-end' in text_from_user.lower():
        res = ''
        for category in courses_plan:
            for item in courses_plan[category]:
                title, date = item.split(',')
                if 'front-end' in title.lower():
                    res += f'<b>{title}</b>: <code>{date}</code>'

        bot.send_message(message.chat.id, text=res, parse_mode='HTML')


@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "Python Telegram Bot 24-11-2021", 200


@app.route('/')
def main():
    bot.remove_webhook()
    bot.set_webhook(url='https://jurbbot.herokuapp.com/' + TOKEN)
    return "Python Telegram Bot", 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
