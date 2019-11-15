def auth():
	import tweepy
	import keys

	auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
	auth.set_access_token(keys.ACCESS_KEY, keys.ACCESS_SECRET)
	return tweepy.API(auth, retry_count=10, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
	
