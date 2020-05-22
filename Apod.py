import json
import time
import requests
import random
import urllib.request
import tweepy
import os


import cred
from nasapi import apodAPI

def twitter_api():
    auth = tweepy.OAuthHandler( cred.CONSUMER_KEY, cred.CONSUMER_SECRET)
    auth.set_access_token(cred.ACCESS_TOKEN, cred.ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

def photo_day():
    '''brings the HD image'''
    apod_url = apodAPI
    apod = requests.get(apod_url)
    apod_endpoint = apod.json()
    ph_url = apod_endpoint['url']
    return ph_url

def text_day():
    apod_url = apodAPI
    apod = requests.get(apod_url)
    apod_endpoint = apod.json()
    title = apod_endpoint['title']
    text = apod_endpoint['explanation'].split('.')[0] + '.'
    text = text.split('.')[0] + '.'
    return "Photo of the Day: \"{}\" - {}  credit:NASA".format(title,text)


def NASAImage():
    """Encompasses the main loop of the bot."""
    api = twitter_api()
    while True:
        t = int(time.strftime("%H", time.gmtime()))

        #if 18 <= t < 21:
        if t%1 ==0:
            url = photo_day()
            image = urllib.request.urlretrieve(url, "tempfile.jpg")
            filename = "tempfile.jpg"
            atod = text_day()
            try:
                api.update_with_media(filename, status= atod)
            except tweepy.error.TweepError:
                continue
            print(atod, end='\n')
            print('--'*5)
            print('Tweet sucessfully posted!')
            print('--'*5)
            print('Sleeping until the next read!')
            os.remove(filename)
            time.sleep(10800)
        else:
            print("sleeping until the next interval")
            time.sleep(10800)

if __name__=="__main__":
    NASAImage()
