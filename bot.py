import telebot
import time 

from fns import feed_fetcher, article_rewrite,etag_gen
from ds import RSS_FEEDS

bot = telebot.TeleBot("6299208799:AAG73EfJfTJKaTdMQcSN4DYnFjVjaiIPNTE")
flag = True

@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, "Hi User, I am a bot/n Type /news to see what's going on in the crypto world and to receive ehnanced news feed type /updates")

@bot.message_handler(commands = ['news'])
def news(message):
    news_update = ""
    for feed in RSS_FEEDS:
        news_dict = feed_fetcher(feed)
        news_update += news_dict['title'] + "\n"
        news_update += news_dict['link'] + '\n' + news_dict['published'] + '\n\n'

    bot.send_message(message.chat.id, news_update)


@bot.message_handler(commands=['updates'])
def updateMe(message):
    global flag
    flag = True
    news_set = []
    idx = 0
    while(flag):
        if(idx == len(RSS_FEEDS)):
            idx = 0
            continue
        
        if(len(news_set) == 10):
            news_set = []
            continue

        try:
            news_dict = feed_fetcher(RSS_FEEDS[idx])
            etag = etag_gen(news_dict['title'])
            print(etag, news_set)
            if(etag not in news_set):
                
                rewritten_Dict = article_rewrite(news_dict)
                
                news_set.append(etag)

                reply = rewritten_Dict['title'] + '\n' + '\n' + "----------------------" + "\n"
                reply += rewritten_Dict['paragraph'] + '\n'
                reply += 'Source: ' + news_dict['link'] + '\n\n'
                reply += 'Published On: ' + news_dict['published'] + '\n'
                
                bot.send_message(message.chat.id, reply)
        except:
            pass 

        idx += 1
        

@bot.message_handler(commands = ['stop'])
def stop(message):
    global flag
    flag = False 
    bot.send_message(message.chat.id, "I'll be stopping now 😔")

bot.infinity_polling()
