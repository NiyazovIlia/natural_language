import config
import telebot
import movie
import reviews
import blabla

bot = telebot.TeleBot(config.token)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Кино', 'Поболтать', 'Оставить отзыв')
keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.row('стоп болталка')


# При старте знакомство
@bot.message_handler(commands=['start'])
def start_message(message):
    s = 'CAACAgIAAxkBAAJYZV6n4sDP-9Ks-I3vMvX1Xd1EwCkvAAJfAgADOKAKRbnf8hWOy-kZBA'
    bot.send_sticker(message.chat.id, s)
    bot.send_message(
        message.chat.id,
        'Привет {}, добро пожаловать. \nВыбери один из вариантов'.format(
            message.from_user.first_name), reply_markup=keyboard1)


# Если ввести сообщение идет проверка на числа и ответ
@bot.message_handler(content_types=['text'])
def askAge(message):
    if message.text.lower() == 'кино':
        msg = bot.send_message(message.chat.id, 'Отлично, напишите сюда небольшое описание фильма')
        bot.register_next_step_handler(msg, movie_name)
    elif message.text.lower() == 'поболтать':
        msg = bot.send_message(message.chat.id, 'Отлично, давай болтать', reply_markup=keyboard2)
        bot.register_next_step_handler(msg, blabla_name)
    elif message.text.lower() == 'оставить отзыв':
        msg = bot.send_message(message.chat.id, 'Отлично, напишите сюда ваш отзыв')
        bot.register_next_step_handler(msg, reviews_name)
    else:
        msg = bot.send_message(message.chat.id, 'Увы, такого варианта нету, попробуйте еще раз')
        bot.register_next_step_handler(msg, askAge)


@bot.message_handler(content_types=['text'])
def movie_name(message):
    movie_five = movie.main(message.text)
    for i in movie_five:
        bot.send_message(message.chat.id, f'Вот ваш фильм: {i}')


@bot.message_handler(content_types=['text'])
def reviews_name(message):
    answer_reviews = reviews.main(message.text)
    bot.send_message(message.chat.id, f'{answer_reviews}')


@bot.message_handler(content_types=['text'])
def blabla_name(message):
    if message.text == 'стоп болталка':
        msg = bot.send_message(message.chat.id, 'Хорошо, возвращаемся назад', reply_markup=keyboard1)
        bot.register_next_step_handler(msg, askAge)
    else:
        answer_reviews = blabla.main(message.text)
        answer_reviews_finish = replace(answer_reviews)
        msg = bot.send_message(message.chat.id, f'{answer_reviews_finish}', reply_markup=keyboard2)
        bot.register_next_step_handler(msg, blabla_name)

def replace(text):
    for i in ['[', ']', "'"]:
        text.replace(i, '')
    return text

if __name__ == '__main__':
    bot.infinity_polling()
