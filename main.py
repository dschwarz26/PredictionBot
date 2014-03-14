import connection
import probability
import datetime
import parse
import smtplib

from email.mime.text import MIMEText

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

def get_buy_and_sell_points(bids_and_asks):
	highest_bid = 0
	lowest_ask = 1000000
	for bid in bids_and_asks['Bids']:
		if bid['Price'] > highest_bid:
			highest_bid = bid['Price']
	for ask in bids_and_asks['Asks']:
		if ask['Price'] < lowest_ask:
			lowest_ask = ask['Price']
	return float(highest_bid) / 100000, float(lowest_ask) / 100000

def send_email(option_data):
	content = """\
		<html>
			<head></head>
		  	<body>
		"""
	for option in option_data:
		content += """\
				<li>%s</li>
		""" % option
	content += """\
			</body>
		</html>
		"""
	print content
	msg = MIMEText(content, 'html')
	msg['Subject'] = 'PredictiousBot Data for %s' % datetime.datetime.utcnow().strftime('%Y-%m-%d')
	msg['From'] = 'DanielSchwarz26@gmail.com'
	msg['To'] = 'DanielSchwarz26@gmail.com'
	s = smtplib.SMTP('localhost')
	s.sendmail(msg['From'], msg['To'], msg.as_string())
	s.quit()
	
if __name__ == '__main__':		
	conn = connection.Connection()
	rel_vol =  conn.get_bitcoin_volatility()
	print 'Got volatility'
	curr_price = float(conn.get_bitcoin_price())
	print 'Got price'
	vol = rel_vol * curr_price / 100
	#print get_total_funds(conn)
	#print get_available_funds(conn)
	contracts = get_all_bitcoin_contracts(conn)
	option_data = []
	for key, val in contracts.iteritems():
		name_data = parse.parse_contract_name(key)
		if name_data:
			option_value = probability.get_option_value(
				name_data['date'],
				name_data['strike_price'],
				curr_price,
				vol
			)
			highest_bid, lowest_ask = get_buy_and_sell_points(val)
			option_data.append('Contract %s has value %.3f. Highest bid: %.2f. Lowest ask: %.2f' % (
				key, option_value, highest_bid, lowest_ask))
	print 'Got option data'
	send_email(option_data)
	print 'Sent email'
	#print conn.retrieve_recent_transactions()
	#print conn.retrieve_current_contracts()
