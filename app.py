import tweepy
import config
import time
import requests
import random

#config.py holds the api keys and secrets
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_token_secret = config.access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

FILE_NAME = 'last_seen.txt'

def retrieve_last_seen_id(file_name):
    with open(file_name, 'r') as x:
        last_seen_id = x.readline()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    with open(file_name, 'w') as x:
        x.write(str(last_seen_id))
    return

#using the first mention id on my twitter account (541765679376908288) as a test
def run_bot():
    print("Reading Tweets...")
    last_seen_id = retrieve_last_seen_id('last_seen.txt')
    mentions = api.mentions_timeline(last_seen_id)
    
    #starts at the first mentioned tweet
    for mention in reversed(mentions):
        print(str(mention.id) + " - " + mention.text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if "#joke" in mention.text.lower():
            print("Found #joke!")
            print("Responding back...")
            joke = requests.get("https://sv443.net/jokeapi/v2/joke/Programming,Miscellaneous,Dark,Pun?blacklistFlags=nsfw,religious,political,racist,sexist&type=single").json()['joke']
            api.update_status('@' + mention.user.screen_name + " " + joke + " ", mention.id)
        if "#yesorno" in mention.text.lower():
            print("Found #yesorno!")
            print('Responding back...')
            api.update_status('@' + mention.user.name.screen_name + " " + random.choice(["Yes", "No"]), mention.id)


while True:
    run_bot()
    time.sleep(15)
