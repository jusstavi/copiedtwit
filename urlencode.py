def url_encode(q, string):
	from urllib.parse import urlencode
	
	params = {
		q : string,
	}
	
	return urlencode(params)
	