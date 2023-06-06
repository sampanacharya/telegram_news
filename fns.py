import feedparser
import ssl
import requests
from bs4 import BeautifulSoup
import hashlib

def etag_generator(data):
    return hashlib.md5(data.encode()).hexdigest()

def get_news():
    if hasattr(ssl, "_create_unverified_context"):
        ssl._create_default_https_context = ssl._create_unverified_context

    feeds = ['https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml','https://cointelegraph.com/rss',
             'https://cryptopotato.com/feed/','https://cryptonews.com/news/feed/',
             'https://www.fxempire.com/api/v1/en/articles/rss/news',
             ]

    content = []
    s = ""
    for i in range(5):
        feed = feedparser.parse(feeds[i])
        s += feed.entries[0].title
        
        news_dict = {
            "title" : feed.entries[i].title,
            "summary" : feed.entries[i].summary,
            "published_date" : feed.entries[i].published,
            "link" : feed.entries[i].link,
        }
        content.append(news_dict)
    
    etag = etag_generator(s)
    return content, etag

def rewrite(url):
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    content = soup.find('div')
    paragraphs = content.find_all('p')
    extracted_content = '\n'.join([p.get_text() for p in paragraphs])
    print(extracted_content)
    
# data, etag = get_news()
# print(data, etag)
