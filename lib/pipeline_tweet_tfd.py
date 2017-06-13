import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.pipeline import Pipeline

import pickle
import redis

import psycopg2 as pg2
import psycopg2.extras as pgex
from DataConnection import postgres, redis
ip= postgres['host']
usr= postgres['user']
pw= postgres['pw']
conn = pg2.connect(host = ip,user = usr,password = pw)


sql_select = '''select cleaned_tweet 
                from tweets where (date_time >= NOW() - '7 day'::INTERVAL) ;'''
cur = conn.cursor(cursor_factory=pgex.RealDictCursor)
cur.execute(sql_select)
rows = cur.fetchall()
conn.close()
df = pd.DataFrame(rows)
df.reset_index(inplace = True)

redis_ip = redis['host']
r = redis.StrictRedis(redis_ip)

tfd_svd_pipe = Pipeline([
    ('tfidf',TfidfVectorizer()),
    ('svd',TruncatedSVD(n_components=50))
])

tfd_svd_pipe.fit(df['cleaned_tweet'])

tfd_svd_pipe = pickle.dumps(tfd_svd_pipe)
r.set('tweets_tfd_svd_pipe', tfd_svd_pipe)
