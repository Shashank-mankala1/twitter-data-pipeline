import tweepy
import pandas as pd 
import json
from datetime import datetime
import s3fs 
from dotenv import load_dotenv
import os

def run_twitter_etl():

    load_dotenv()

    # Note: variable names kept to match the existing tweepy usage below.
    # OAuthHandler(access_key, access_secret) then set_access_token(consumer_key, consumer_secret)
    access_key = os.getenv("ACCESS_KEY")
    access_secret = os.getenv("ACCESS_SECRET")
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    if not all([access_key, access_secret, consumer_key, consumer_secret]):
        raise RuntimeError("Missing Twitter credentials in environment variables.")


    # Twitter authentication
    auth = tweepy.OAuthHandler(access_key, access_secret)   
    auth.set_access_token(consumer_key, consumer_secret) 

    # # # Creating an API object 
    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name='@elonmusk', 
                            # 200 is the maximum allowed count
                            count=20,
                            include_rts = False, # exclude retweets
                            # Necessary to keep full_text 
                            # otherwise only the first 140 words are extracted
                            tweet_mode = 'extended'
                            )
    print("Number of tweets extracted: {}.\n".format(len(tweets)))
    list = []
    for tweet in tweets:
        text = tweet._json["full_text"]

        refined_tweet = {"user": tweet.user.screen_name,
                        'text' : text,
                        'favorite_count' : tweet.favorite_count,
                        'retweet_count' : tweet.retweet_count,
                        'created_at' : tweet.created_at}
        
        list.append(refined_tweet)

    print("Tweets Fetched: {}".format(len(list)))
    df = pd.DataFrame(list)
    # print(df.head())
    # df.to_csv('s3://shash-airflow-bucket/refined_tweets.csv')
    df.to_csv('refined_tweets.csv')


run_twitter_etl()