def update(api, status_id, mention_user_screen_name, mention_id):
	from remove_urls import remove_urls
	from urlencode import url_encode
	
	
	tweet = api.get_status(status_id, tweet_mode='extended')
	tweet_text = remove_urls(tweet.full_text)
	tweet_date = tweet.created_at
	url = 'https://twitter.com/search?'
	date = ''
	for attr in [ 'year', 'month', 'day']:
		date += str(getattr(tweet_date, attr)) + " "
	date = date.split()
	date = date[0] + "-" + date[1] + "-" + str(int(date[2]) + 1)
	string = tweet_text + ' ' + 'until:' + date
	url += url_encode("q", string)
	reply_text = "@" + mention_user_screen_name + " " + url
	reply = api.update_status(reply_text, mention_id)
	print("Link replied to " + mention_user_screen_name + "\n")
	return tweet.full_text, reply.id, url
