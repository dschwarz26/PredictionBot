import json
from google.appengine.api import urlfetch

class Connection:
  def __init__(self):
    self.url_base = 'https://api.predictious.com/v1/'
    api_key_2 = '2umz/dm6lXWqB1Mn9OAE8tr2wAI93iv3QE08M/p7GrTBW41U5yc5+AkEcxQjKJfF7pXyPzP8T/+9tm6/YOmA/jPwLXJab6p0oLWDTVKrbrnXRxYTXVcTxt9nsZzglhtoABG4VYWLpNp/ABBFftUHNAkdHI8='
    self.headers = {'X-Predictious-Key': api_key_2}

  def get(self, *args):
    url = self.url_base + '/'.join(args)
    return json.loads(urlfetch.fetch(url=url, headers=self.headers).content)
  
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
    return json.loads(urlfetch.fetch(url='http://btcvol.info/latest').content)[u'Volatility']

  def get_bitcoin_price(self):
    return json.loads(urlfetch.fetch(url='https://coinbase.com/api/v1/currencies/exchange_rates').content)[u'btc_to_usd']
