import tweepy
import config
import time
import requests
import random

#API keys and secrets used to log into the bot
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_token_secret = config.access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

FILE_NAME = 'last_seen.txt'

def retrieve_last_seen_id(file_name):
    with open(file_name, 'r') as x:
        last_seen_id = x.readline()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    with open(file_name, 'w') as x:
        x.write(str(last_seen_id))
    return

#using the first mention id (541765679376908288) to test
def run_bot():
    user = api.me()

    #following everyone that follows this bot account
    #print('Checking for new followers...')
    #for follower in tweepy.Cursor(api.followers).items():
    #    try:
    #        follower.follow()
    #    except:
    #        continue
    #print("Followed everyone that is following " + user.name)

    #Replying to everyone who mentioned the bot with a #keyword
    print("Reading Tweets...")
    last_seen_id = retrieve_last_seen_id('last_seen.txt')
    mentions = api.mentions_timeline(last_seen_id)
    for mention in reversed(mentions):
        print(str(mention.id) + " - " + mention.text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if "#joke" in mention.text.lower():
            print("Found #joke!")
            print("Responding back...")
            joke = requests.get("https://sv443.net/jokeapi/v2/joke/Miscellaneous,Dark,Pun?blacklistFlags=nsfw,religious,political,racist,sexist&type=single").json()['joke']
            api.update_status('@' + str(mention.user.screen_name) + " " + joke + " ", mention.id)
        elif "#yesorno" in mention.text.lower():
            answer = random.choice(['Yes', 'No'])
            print("Found #yesorno!")
            print('Responding back...')
            api.update_status('@' + str(mention.user.screen_name) + " " + answer, mention.id)

while True:
    run_bot()
    time.sleep(15)
