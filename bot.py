def reply_to_tweets():
	import tweepy
	from my_tweepy import auth
	from database import save_to_csv, retrieve_last_seen_id, store_last_seen_id
	from status_update import update
	
	
	txt_file = 'last_seen_id.txt'
	csv_file = 'bot_data.csv'
	
	
	api = auth()
	
	
	print('Retrieving and replying to tweets...\n', flush=True)
	
	last_seen_id = retrieve_last_seen_id(txt_file)
	
	mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')
	
	for mention in reversed(mentions):
		print(str(mention.id) + ' - ' + mention.full_text + '\n', flush=True)
		
		last_seen_id = mention.id
		store_last_seen_id(last_seen_id, txt_file)
		
		print(mention.full_text.split()[-1])
		
		if '@copiedtwit' in mention.full_text.split()[-1] and mention.in_reply_to_status_id != None and mention.user.screen_name != 'copiedtwit':
		
			try:
				tweet_full_text, reply_id, url = update(api, mention.in_reply_to_status_id, mention.user.screen_name, mention.id)
				
				save_to_csv(csv_file, mention.created_at, mention.user.id, mention.user.screen_name, tweet_full_text, reply_id, url)
			
			except:
				print("Can't reply!")
		
		else:
			print("No tweet to check!")