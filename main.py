def main():
	import connection
	import time
	from bot import reply_to_tweets
	
	
	check = 0
	retry_count = 0
	
	while True:
		connection.check()
		if connection.check() == True:
			print("Connection OK!\n")
			check += 1
			retry_count = 0
			print("Check " + str(check))
			
			try:
				reply_to_tweets()
					
			except:
				print("Can't retrieve at the moment!")
				pass
			
			time.sleep(15)
		else:
			print("No Connection!\n")
			retry_count += 1
			print("Retrying..." + str(retry_count) + "\n")
			time.sleep(10)
			pass
					
			
if __name__ == "__main__":
	main()