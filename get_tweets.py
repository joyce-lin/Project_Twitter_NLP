import requests
import numpy as np
import pandas as pd
import json
from IPython.display import display
import re
#import os,sys,inspect
#currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#parentdir = os.path.dirname(currentdir)
#sys.path.insert(0,parentdir)

from lib.twitter_keys import keys
import json
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream


CONSUMER_KEY = keys['CONSUMER_KEY']
CONSUMER_SECRET = keys['CONSUMER_SECRET']
ACCESS_TOKEN = keys['ACCESS_TOKEN']
ACCESS_SECRET = keys['ACCESS_SECRET']

### -----------------------------------------------------------------------------------####
### geo bounding for tweet location----------------------------------------------------####

los_angeles_bb = "-118.6681759,33.5883113449,-117.5042724609,34.3373061"
Santa_Monica = "-118.514757,33.980857,-118.417253,34.065264"
Dallas = "-96.904907,32.761906,-96.684917,33.080035"
Midland_Odessa = "-103.1575,31.4849,-101.5178,32.3591"
Sacramento_east = "-121.8658,38.445,-120.2618,39.3598"
SFO = "-122.5319,37.5751,-122.3438,37.824"

### -----------------------------------------------------------------------------------####
### connect to postgres----------------------------------------------------------------####

import psycopg2 as pg2
import psycopg2.extras as pgex
this_host='54.69.228.16'
this_user='postgres'
this_password='postgres'


### -----------------------------------------------------------------------------------####
### cleaing text ----------------------------------------------------------------------####

def cleaner(text):
    #text = text.lower()
    text = re.sub("'","''", text)
    text = re.sub("{","\{",text)
    text = re.sub("}","\}",text)
    #text = re.sub(":","\:",text)
    return text
### -----------------------------------------------------------------------------------####
### Collecting tweets------------------------------------------------------------------####



oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_stream = TwitterStream(auth=oauth)
iterator = twitter_stream.statuses.filter(locations=Santa_Monica+','+\
                                          Midland_Odessa+','+Dallas+','+\
                                          Sacramento_east+','+SFO)
tweet_count = 300000

conn = pg2.connect(host = this_host, 
                        user = this_user,
                        password = this_password)

#tweets = []
cur = conn.cursor()
for tweet in iterator:
    tweet_count -= 1  
    #tweets.append(tweet)
   
    id_str = str(tweet['id_str'])
    screen_name = tweet['user']['screen_name']
    tweet_content = cleaner(tweet['text'])
    #tweet_content = tweet["text"]
    #tweet_content = tweet_content.encode('ascii', 'replace')
    
    try:
        hashtags = cleaner(tweet['entities']['hashtags']['text'])
    except:
        hashtags = None
    screen_name = tweet['user']['screen_name']
    retweeted = tweet['retweeted']
    retweet_count = tweet['retweet_count']
    created_at = tweet['created_at']
    
    try:
        location =  cleaner(tweet['place']['full_name'])
    except:
        location = None
    try:
        country = tweet['place']['country']
    except:
        country = None
    try:
        place_type = tweet['place']['place_type']
    except:
        place_type = None
    try:
        latitude = tweet["geo"]["coordinates"][0]
        longitude = tweet["geo"]["coordinates"][1]
    except:
        latitude = 0.0 
        longitude = 0.0  
    usr= tweet['user']
    lang = tweet['lang']
    try:
        time_zone = cleaner(tweet['user']['time_zone'])
    except:
        time_zone = None    
    sql_insert = '''insert into tweets 
                        (
                            id,
                            screen_name,
                            tweet_content,
                            created_at,
                            retweeted,
                            retweet_count,
                            hashtags,
                            location,
                            country,
                            place_type,
                            latitude,
                            longitude, 
                            time_zone,
                            lang
                        )
                    values
                        ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');
                 '''.format(id_str,
                            screen_name,
                            tweet_content,
                            created_at,
                            retweeted,
                            retweet_count,
                            hashtags,
                            location,
                            country,
                            place_type,
                            latitude,
                            longitude,
                            time_zone,
                            lang
                           )
    print(str(tweet_count)+' '+ screen_name+ ':  '+ tweet_content)
    #print(latitude,longitude)
    cur.execute(sql_insert)
    conn.commit()    
    if tweet_count <= 0:
        break

conn.close()
