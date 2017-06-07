import pandas as pd
import re
from spacy.en import English
nlp = English()

def c(text):
    text = re.sub("'","''", text)
    text = re.sub("{","\{",text)
    text = re.sub("}","\}",text)
    return text

from tqdm import tqdm
import psycopg2 as pg2
import psycopg2.extras as pgex
this_host='54.69.228.16'
this_user='postgres'
this_password='postgres'
conn = pg2.connect(host = this_host, 
                        user = this_user,
                        password = this_password)
conn2 = pg2.connect(host = this_host, 
                        user = this_user,
                        password = this_password)
from sklearn.feature_extraction.text import CountVectorizer
cv= CountVectorizer(stop_words='english')
count = 0
while count < 65363: 
    sql_select = '''
    select * from tweets_demo where lang = 'en' limit 1000 offset {}
    '''.format(count)
    count += 1000
    print(count)
    cur = conn.cursor(cursor_factory=pgex.RealDictCursor)
    cur.execute(sql_select)
    rows = cur.fetchall()
    df = pd.DataFrame(rows)
    for j in range(1000):
        v = nlp(c(df['tweet_content'][j]))
        cur_vec = conn2.cursor()
        sql_update = '''
        update tweets_demo
        set vector = '{}'
        where tweet_content = '{}';
        commit;
        '''.format(v.vector,v)
        #print(v.vector[0],v)
        cur_vec.execute(sql_update)
        conn2.commit()
conn2.close()  
conn.close()    
print('done') 
