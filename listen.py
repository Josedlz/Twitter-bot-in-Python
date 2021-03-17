import sys
import psycopg2
import load_configs
import tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

from google_trans_new import google_translator  
from nltk.sentiment import SentimentIntensityAnalyzer

import json
import re
from textblob import TextBlob
import string
import preprocessor as p
import os
import time

#credentials for twitter
consumer_key    = "HIm9ix6N5dH3KCVsuvEJnaPog"
consumer_secret = "NAQRuy3BEVfUTeRwcRNHQ2sqIO4F0kwAGhQTe24tnIyKoL1oAt"
access_key      = "1368074971449339905-LG6o5LWP69Ga3kyHAZDr3eul4qdIor"
access_secret   = "INEfgAibmHLgt81QVEliaiLxdG6dYpXr9ywt5i6zkmuHa"

#initilization of the twitter api
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

#objects for sentiment analysis
translator = google_translator()  
sia = SentimentIntensityAnalyzer()

class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # if "retweeted_status" attribute exists, flag this tweet as a retweet.
        is_retweet = hasattr(status, "retweeted_status")

        # check if text has been truncated
        if hasattr(status, "extended_tweet"):
            text = status.extended_tweet["full_text"]
        else:
            text = status.text

        # check if thload_configse tweet.
        is_quote = hasattr(status, "quoted_status")
        quoted_text = ""
        if is_quote:
            # check if quoted tweet's text has been truncated before recording it
            if hasattr(status.quoted_status,"extended_tweet"):
                quoted_text = status.quoted_status.extended_tweet["full_text"]
            else:
                quoted_text = status.quoted_status.text

        # remove characters that might cause problems with csv encoding
        remove_characters = [",","\n"]
        for c in remove_characters:
            text.replace(c," ")
            quoted_text.replace(c, " ")
         
        tid       = status.id
        username  = status.user.screen_name
        time.sleep(20)
        content   = translator.translate(status.text)
        retcount  = status.retweet_count
        score     = sia.polarity_scores(content)
        location  = status.user.location
        latitude  = 0
        longitude = 0
        if status.coordinates is not None:
            latitude  = status.coordinates['coordinates'][1]
        is_negative = (score['neg'] > score['neu']) and (score['neg'] > score['pos'])
        
        #sends message to the user if the post is uninformed/negative
        if is_negative : 
            post = 'Por favor, te recomiendo que te informes en https//:www.consideramos.pe '
            api.update_status(post + '@' + username)
            #api.send_direct_message(status.user.id_str, post)
        try:
            # read connection parameters
            params = load_configs.config()

            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
            cur = conn.cursor()

            print('Saving tweet into the database...')
            query = """INSERT INTO listener_output(twitter_id, username, retcount, location, lat, long, positive, neutral, negative, is_negative) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            record = (tid, username, retcount, location, latitude, longitude, score['pos'], score['neu'], score['neg'], is_negative)
            cur.execute(query, record)
            conn.commit()

            print('Closing connection...')
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
         
    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()
