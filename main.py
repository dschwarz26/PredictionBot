import connection

def get_total_funds(conn):
	wallet_data = conn.retrieve_wallet().json()
	return wallet_data[u'TotalFunds']

def get_available_funds(conn):
	wallet_data = conn.retrieve_wallet().json()
	return wallet_data[u'AvailableFunds']

def get_all_bitcoin_contracts(conn):
	contracts = {}
	all_contracts = conn.retrieve_current_contracts().json()
	for contract in all_contracts:
		if 'Bitcoin' in contract[u'Name']:
			contract_data = conn.retrieve_order_book(contract[u'Id']).json()
			contracts[contract[u'Name']] = contract_data
	return contracts

def get_current_bitcoin_contracts(conn):
	contracts = []
	orders = conn.retrieve_open_orders().json()
	for contract in orders:
		if 'Bitcoin' in contract[u'Name']:
			contract_data = conn.retrieve_order_book(contract[u'Id']).json()
			contracts.append(contract_data)
	return contracts
			
if __name__ == '__main__':
		
	conn = connection.Connection()
	#print get_total_funds(conn)
	#print get_available_funds(conn)
	#print get_current_bitcoin_contracts(conn)
	print get_all_bitcoin_contracts(conn)
	#print conn.retrieve_recent_transactions().json()
	#print conn.retrieve_current_contracts().json()

