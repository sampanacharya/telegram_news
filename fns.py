import feedparser 
import ssl 
import requests 
import hashlib
from bs4 import BeautifulSoup
import json
from tabulate import tabulate
from ds import *

###### OPENAI API FUNCTIONS ######

key="YOUR_OPENAI_API_KEY" # openai api key
# API URL DECLARATION
url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {key}",
}

# Rewriting the articles
def rewrite(para):
    payload = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "rewrite this article: " + para}],
     }
    response = requests.post(url, headers = headers, json=payload).json()
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

##### RSS FEEDS ######

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


##### INFERENCE API FUNCTIONS #########
MODEL_ID = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

hf_token = "YOUR_HF_TOKEN" # hugginf_face_api_token
hf_headers = {
    "Authorization" : f"Bearer {hf_token}",
}

def sentiment_inference(payload):
    data = json.dumps(payload)
    response_hf = requests.request("POST", API_URL, headers=hf_headers, data=data)
    data = json.loads(response_hf.content.decode('utf-8'))
    
    keys = data[0][0].keys()
    values = [list(d.values()) for d in data[0]]
    table_string = tabulate(values, keys, tablefmt = "grid")
    return table_string

