import telebot
from transformers import pipeline

from fns import feed_fetcher, article_rewrite,etag_gen
from ds import RSS_FEEDS

bot = telebot.TeleBot("6274653807:AAFLp2bltMY5DysTK_2XfsyeWWO9VG-4HA4")
flag = True

model_pipeline = pipeline("sentiment-analysis",model="siebert/sentiment-roberta-large-english")

@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message("@cryptoNarad", "Hi User, I am a bot/n Type /news to see what's going on in the crypto world and to receive ehnanced news feed type /updates")

@bot.message_handler(commands = ['news'])
def news(message):
    news_update = ""
    for feed in RSS_FEEDS:
        news_dict = feed_fetcher(feed)
        news_update += news_dict['title'] + "\n"
        news_update += news_dict['link'] + '\n' + news_dict['published'] + '\n\n'

    bot.send_message("@cryptoNarad", news_update)


@bot.message_handler(commands=['updates'])
def updateMe(message):
    global flag
    flag = True
    news_set = []

    data = []
    idx = 0
    while(flag):
        if(idx == len(RSS_FEEDS)):
            idx = 0
            continue
        
        if(len(news_set) == 10):
            news_set = []
            continue

        news_dict = feed_fetcher(RSS_FEEDS[idx])
        etag = etag_gen(news_dict['title'])
        #print(etag, news_set)
        if(etag not in news_set):
            
            rewritten_Dict = article_rewrite(news_dict)
            
            news_set.append(etag)
            data.append(rewritten_Dict['title'])

            reply = rewritten_Dict['title'] + '\n' + '\n' + "----------------------" + "\n"
            reply += rewritten_Dict['paragraph'] + '\n'
            reply += 'Source: ' + news_dict['link'] + '\n\n'
            reply += 'Published On: ' + news_dict['published'] + '\n'

            if("cointelegraph" in news_dict['link']):
                print(rewritten_Dict['paragraph'] + "\n\n")
                sent = model_pipeline(rewritten_Dict['paragraph'])
            else:
                sent = model_pipeline(rewritten_Dict['title'])
            reply += '\n Sentiment Rating: Label - ' + str(sent[0]['label']) +' Score: '  + str(sent[0]['score']) + '\n' 

            bot.send_message("@cryptoNarad", reply)
        idx += 1
        

@bot.message_handler(commands = ['stop'])
def stop(message):
    global flag
    flag = False 
    bot.send_message(message.chat.id, "I'll be stopping now 😔")

bot.infinity_polling()
