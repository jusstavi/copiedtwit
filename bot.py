import tweepy
import pandas as pd
import re
import time
import urllib.parse
from urllib.request import urlopen
from keys import *


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, retry_count=10, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


txt_file = 'last_seen_id.txt'
csv_file = 'bot_data.csv'
retry_count = 0
check = 1


def check_connection():
	try:
		urlopen("https://google.com/")
		return True
	except:
		return False
		pass
		
def save_data(csv_file, date_time, user_id, screen_name, tweet_text, reply_id, url):
	data = pd.read_csv(csv_file)
	
	col1 = data["Date & Time"].to_list()
	col2 = data["User ID"].to_list()
	col3 = data["Username"].to_list()
	col4 = data["Tweet Text"].to_list()
	col5 = data["Reply ID"].to_list()
	col6 = data["Replied URL"].to_list()
	
	col1.append(date_time)
	col2.append(user_id)
	col3.append(screen_name)
	col4.append(tweet_text)
	col5.append(reply_id)
	col6.append(url)
	
	dict = {
    	'Date & Time' : col1,
    	'User ID' : col2,
    	'Username' : col3,
    	'Tweet Text' : col4,
    	'Reply ID' : col5,
    	'Replied URL' : col6
	}
	
	dataframe = pd.DataFrame(dict)
	dataframe.to_csv(csv_file)
	print("Data Saved!")

def retrieve_last_seen_id(file_name):
	f_read = open(file_name, 'r')
	last_seen_id = int(f_read.read().strip())
	f_read.close()
	return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

    
def remove_urls(text):
    text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', text, flags=re.MULTILINE)
    return(text)
	
	
def reply_to_tweets():
    print(f'Retrieving and replying to tweets...({check})', flush=True)
    
    last_seen_id = retrieve_last_seen_id(txt_file)
    
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')
                        
    for mention in reversed(mentions):
    	print(str(mention.id) + ' - ' + mention.full_text, flush=True)
    	
    	last_seen_id = mention.id
    	store_last_seen_id(last_seen_id, file_name)
    	
    	if '@copiedtwit' in mention.full_text and reply_to_status_id != None and mention.user.screen_name != 'copiedtwit':
    		tweet = api.get_status(mention.in_reply_to_status_id, tweet_mode='extended')
    		tweet_text = remove_urls(tweet.full_text)
    		tweet_date = tweet.created_at
    		
    		url = 'https://twitter.com/search?'
    		
    		date = ''
    		
    		for attr in [ 'year', 'month', 'day']:
    			date += str(getattr(tweet_date, attr)) + " "
    			
    		date = date.split()
    		date = date[0] + "-" + date[1] + "-" + str(int(date[2]) + 1)
    		
    		string = tweet_text + ' ' + 'until:' + date
    		
    		params = {
    		"q" : string,
    		}
    		
    		url = url + urllib.parse.urlencode(params)
    		
    		reply = api.update_status("@" + mention.user.screen_name + " " + url, mention.id)
    		
    		print("Link replied to " + mention.user.screen_name)
    		
    		save_data(csv_file, mention.created_at, mention.user.id, mention.user.screen_name, tweet.full_text, reply.id, url)
    		
    	else:
    		print("No tweet to check!")


while True:
	check_connection()
	
	if check_connection() == True:
		print("Connection OK!")
		retry_count = 0
		
		try:
			reply_to_tweets()
			time.sleep(15)
			check += 1
			
		except tweepy.TweepError:
			pass
			
		except:
			pass
		
		
	else:
		print("No Connection!\n")
		retry_count += 1
		print("Retrying..." + str(retry_count))
		time.sleep(5)
		pass