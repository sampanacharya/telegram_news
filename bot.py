import os
import telebot 
from fns import get_news

bot = telebot.TeleBot("6274653807:AAFLp2bltMY5DysTK_2XfsyeWWO9VG-4HA4")

flag = False
etag = ""
res = ""
@bot.message_handler(commands = ['start'])
def start(message):
    bot.reply_to(message, "Hi User, I am a bot/n Type /news to recieve all the latest updates")

@bot.message_handler(commands=['news'])
def send_news(message):
    global etag, res, flag
    flag = True
    while(flag):
        news, et = get_news()
        if (not etag and not res) or et != etag:
            res = ""
            etag = et
            for ele in news:
                res += ele['title'] + "\n " + ele['link'] + "\n" + ele['published_date'] + "\n"
                res += "\n"
            bot.reply_to(message, res)
    
@bot.message_handler(commands=['stop'])
def stop(message):
    global flag 
    flag = False
    bot.send_message(message.chat.id, 'bye')

bot.infinity_polling()