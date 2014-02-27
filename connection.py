import request

class Connection:
	def __init__(self):
		self.url_base = 'https://api.predictious.com/v1/'
		api_key = 'rGTAtchx86jDxadDCOnKVQi8W8yKnnE708TIr1e9w/3Xs7M0mA6LKV0VgbtRN'
		self.headers = {'X-Predictious-Key': self.api_key}		

	def get(self, *kwargs):
		endpoint = self.api_key + '/'.join(kwargs)
		return request.get(endpoint, headers=self.headers)
		
		
