def check():
	from urllib.request import urlopen
	
	try:
		urlopen("https://google.com/")
		return True
	except:
		return False
		pass