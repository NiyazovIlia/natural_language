import config
import telebot
import movie
import reviews

bot = telebot.TeleBot(config.token)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Кино', 'Поболтать', 'Оставить отзыв')


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
        bot.send_message(message.chat.id, 'Отлично, но увы я еще не готов болтать с вами')
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

if __name__ == '__main__':
    bot.infinity_polling()
