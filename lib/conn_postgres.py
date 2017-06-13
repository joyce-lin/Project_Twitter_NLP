import psycopg2
import psycopg2.extras as pgex
import yaml
import re
import redis
import os,sys,inspect
import os,os.path
curfilePath = os.path.abspath(__file__)
curDir = os.path.abspath(os.path.join(curfilePath,os.pardir)) # this will return current directory in which python file resides.
parentDir = os.path.abspath(os.path.join(curDir,os.pardir)) # this will return parent directory.


file = parentDir+'/lib/credential_keys.yml'
try:
    open(file, 'r')
except:
    file = 'home/jovyan/work/DSI/capstone/lib/credential_keys.yml
        
def connect_to_postgres (location = 'postgres'):
    """ v 1.2 Open a psycopg2 connection and create a cursor based on a yaml credential file.
        The current expected name of the yaml file is "Database_credentials"; please customize this to your taste.
        The credentials file will look for a entry in the dictionary called 'remote' by default.  If the remote
        databse is unavailalbe, it will attempt to connect with the settings the 'local' key.  
        Please remember to close the cursor and connection when you are done using them.        
    """
#TO DO: make  'location' to a list and iterate through the list, rather than default to local db.
#TO DO: add credential file support as a param for the function call.

    with open(file, 'r') as f:
        credentials =  yaml.load(f) 
    
    #try:
    conn = psycopg2.connect(**credentials[location])
        #print "Connected to server {}.".format(credentials[location]['host'])
    return conn, conn.cursor(cursor_factory=pgex.RealDictCursor)
    #except:
    #    print ("Check Postgres Server Connection")
    #    pass
        #print 'FAILED to connect to server {}.  Trying local server.'.format(credentials[location]['host'])
        #try:
        #    connection = psycopg2.connect(**credentials['local'])
        #    print ("Conencted to localhost.")
        #    return conn, conn.cursor(cursor_factory=pgex.RealDictCursor)
        #except:
        #    print ("No Database is available")
        #    pass 
        
def connect_to_redis (location = 'redis'):        
    with open(file, 'r') as f:
        credentials =  yaml.load(f)
    try:
        r = redis.StrictRedis(**credentials[location])   
        return r
    except:
        print ("Check Redis Server Connection")
        pass