import connection

def get_total_funds(conn):
	wallet_data = conn.retrieve_wallet()
	return wallet_data[u'TotalFunds']

def get_available_funds(conn):
	wallet_data = conn.retrieve_wallet()
	return wallet_data[u'AvailableFunds']

def get_all_bitcoin_contracts(conn):
	contracts = {}
	all_contracts = conn.retrieve_current_contracts()
	for contract in all_contracts:
		if 'Bitcoin' in contract[u'Name']:
			contract_data = conn.retrieve_order_book(contract[u'Id'])
			contracts[contract[u'Name']] = contract_data
	return contracts

def get_current_contracts(conn):
	return conn.retrieve_open_orders()
			
if __name__ == '__main__':		
	conn = connection.Connection()
	print conn.get_bitcoin_volatility()
	print conn.get_bitcoin_price()
	#print get_total_funds(conn)
	#print get_available_funds(conn)
	#print get_current_bitcoin_contracts(conn)
	#print get_all_bitcoin_contracts(conn)
	#print conn.retrieve_recent_transactions()
	#print conn.retrieve_current_contracts()

