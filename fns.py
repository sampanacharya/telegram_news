import feedparser 
import ssl 
import requests 
import hashlib
from bs4 import BeautifulSoup

from ds import *

# API URL DECLARATION
url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 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",
}

# Fetching the updates from feed
def feed_fetcher(feed):
    if hasattr(ssl, "_create_unverified_context"):
        ssl._create_default_https_context = ssl._create_unverified_context
    
    feed = feedparser.parse(feed)
    return {
        'title': feed.entries[0].title,
        'summary': feed.entries[0].summary,
        'link' : feed.entries[0].link,
        'published': feed.entries[0].published,
    }

# Etag Generation
def etag_gen(string):
    return hashlib.md5(string.encode()).hexdigest()

# Rewriting the articles
def rewrite(para):
    payload = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "rewrite this article: " + para}],
     }
    response = requests.post(url, headers = headers, json=payload).json()
    print(response)
    return response['choices'][0]['message']['content']

def article_rewrite(news_dict):
    response = requests.get(news_dict['link'])

    title = news_dict['title']
    paragraphs = ""
    if(response.status_code == 200):
        soup = BeautifulSoup(response.content, 'html.parser')
        p = "".join([p.text.strip() for p in soup.find_all('p')])
        paragraphs += rewrite(p)

    return {
        'title': title,
        'paragraph' : paragraphs,
    }

article_rewrite(feed_fetcher(RSS_FEEDS[2]))