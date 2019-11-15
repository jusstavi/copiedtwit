def save_to_csv(csv_file, date_time, user_id, screen_name, tweet_text, reply_id, url):
	import pandas as pd
	
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