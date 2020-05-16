import random
import time
import urllib.parse
from lxml.html import fromstring

import nltk

import requests
from twitter import OAuth, Twitter
from bs4 import BeautifulSoup

import string


import cred

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

oauth = OAuth(
        cred.ACCESS_TOKEN,
        cred.ACCESS_SECRET,
        cred.CONSUMER_KEY,
        cred.CONSUMER_SECRET
    )
t = Twitter(auth=oauth)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)'
                ' AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}



def wp_tag(page):
    '''takes page content and returns tags'''
    soup = BeautifulSoup(page.content,'html.parser')
    tags = soup.find_all('meta', property = 'article:tag')
    wptags = []
    for tag in tags:
       wptags.append(tag.get('content'))
    new1 = []
    for tag in wptags:
        new1.append(tag.replace(" ",""))
    new2 = []
    for tag in new1:
        new2.append(tag.replace("-",""))
    if len(new2) > 1:
        return random.sample(new2, k=2)
    elif len(new2) == 1:
        new2.append('space')
        return new2
    else:
        return ['space','science']


def extract_paratext(paras):
    """Extracts text from <p> elements and returns a clean, tokenized random
    paragraph."""

    paras = [para.text_content() for para in paras if para.text_content()]
    para = random.choice(paras)
    return tokenizer.tokenize(para)

def extract_text(para):
    """Returns a sufficiently-large random text from a tokenized paragraph,
    if such text exists. Otherwise, returns None."""

    for i in range(0,len(para)):
        text = random.choice(para)
        if text and 60 < len(text) < 210:
            return text
        else:
            return None

def choose_url():
    '''chooses a random category'''
    category = ['ancestors', 'arts', 'business', 'cosmos', 'life',
                'machine', 'society', 'worlds', 'starter-kits', 'sustaining-place']
    kon = random.choice(category)
    return kon


def scrap_blog():
    ''' Scraps FS content'''
    while True:
        konu = choose_url()
        i = random.randint(1,10)
        url = 'https://filling-space.com/category/{}/page/{}'.format(konu,i)
        try:
            r = requests.get(url , headers=HEADERS)
        except Exception as e:
            continue

        tree = fromstring(r.content)
        links = tree.xpath('//div[@class="entry-content"]/a/@href')
        del tree
        if len(links) < 1:
            continue
        while True:
            print('Reading' + ' ' + str(len(links)) +' articles for the most appropriate Tweet!' )
            print('Please Wait...')
            rng = len(links) - 1
            ind = random.randint(0,rng)
            print('...')
            r = requests.get(links[ind], headers=HEADERS)
            wptags = wp_tag(r)
            blog_tree = fromstring(r.content)
            paras = blog_tree.xpath('//div[@class="entry-content"]/p')
            para = extract_paratext(paras)
            print(len(para))
            text1 = str(extract_text(para))
            text = text1.replace('\n',' ')
            if text == "None":
                continue
            elif '–' in text:
                continue
            elif ')' in text:
                continue
            elif '(' in text:
                continue
            else:
                break
        break

    print('The most appropriate Tweet is....:')
    print('--'*5)
    try:
        link = links[ind]
    except Exception as e:
        print(e)
        link = links[ind]
    if text[0].isupper == False:
        text = text.capitalize()
    if '"' in text:
        text = text.replace('"',"'")
    text = text.strip()
    tags1 = '#' + wptags[0] + ' '+ '#' + wptags[1]
    return ' "{}" {} {} '.format(text,tags1,link)


def main():
    """Encompasses the main loop of the bot."""
    print('I am the Filling Space Twitter Bot.')
    while True:
        print('--'*5)

        try:
            tweet = scrap_blog()
        except Exception as e:
            continue
        try:
            t.statuses.update(status=tweet)
        except Exception as e:
            continue
        print(tweet, end='\n')
        print('--'*5)
        print('Tweet sucessfully posted!')
        print('--'*5)
        print('Sleeping 20 minutes until the next read!')
        time.sleep(20*60)

if __name__ == '__main__':
    main()
