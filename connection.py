import requests

class Connection:
	def __init__(self):
		self.url_base = 'https://api.predictious.com/v1/'
		api_key_2 = '2umz/dm6lXWqB1Mn9OAE8tr2wAI93iv3QE08M/p7GrTBW41U5yc5+AkEcxQjKJfF7pXyPzP8T/+9tm6/YOmA/jPwLXJab6p0oLWDTVKrbrnXRxYTXVcTxt9nsZzglhtoABG4VYWLpNp/ABBFftUHNAkdHI8='
		self.headers = {'X-Predictious-Key': api_key_2}

	def get(self, *args):
		endpoint = self.url_base + '/'.join(args)
		return requests.get(endpoint, headers=self.headers, verify=False)
	
	def post(self, **kwargs):
		pass	
		
