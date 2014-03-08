import requests

class Connection:
	def __init__(self):
		self.url_base = 'https://api.predictious.com/v1/'
		api_key_2 = '2umz/dm6lXWqB1Mn9OAE8tr2wAI93iv3QE08M/p7GrTBW41U5yc5+AkEcxQjKJfF7pXyPzP8T/+9tm6/YOmA/jPwLXJab6p0oLWDTVKrbrnXRxYTXVcTxt9nsZzglhtoABG4VYWLpNp/ABBFftUHNAkdHI8='
		self.headers = {'X-Predictious-Key': api_key_2}

	def get(self, *args):
		endpoint = self.url_base + '/'.join(args)
		return requests.get(endpoint, headers=self.headers, verify=False).json()
	
	def post(self, **kwargs):
		pass
		
	def retrieve_open_orders(self):
        	return self.get('orders')
  
  	def retrieve_wallet(self):
    		return self.get('wallet')
  
  	def retrieve_recent_transactions(self):
        	return self.get('transactions')
  
  	def retrieve_current_contracts(self):
        	return self.get('contracts')
  
  	def retrieve_order_book(self, contract_id):
        	return self.get('contractorders', contract_id)

	def get_bitcoin_volatility(self):
		return requests.get('http://btcvol.info/latest').json()[u'Volatility']

	def get_bitcoin_price(self):
		return requests.get('https://coinbase.com/api/v1/currencies/exchange_rates').json()[u'btc_to_usd']
