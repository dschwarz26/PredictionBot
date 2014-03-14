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
				<li><font color='%s'>%s</font></li>
		""" % (option['color'], option['data'])
	content += """\
			</body>
		</html>
		"""
	print content
	msg = MIMEText(content, 'html')
	from_email = 'DanielSchwarz27@gmail.com'
	to_email = 'DanielSchwarz26@gmail.com'
	password = open('password.txt', 'rf').readline()[:-1]
	msg['Subject'] = 'PredictiousBot Data for %s' % datetime.datetime.utcnow().strftime('%Y-%m-%d')
	msg['From'] = from_email
	msg['To'] = to_email
	server = smtplib.SMTP('smtpcorp.com', 2525)
	server.ehlo()
	server.starttls()
	server.login(from_email, password)
	server.sendmail(from_email, to_email, msg.as_string())
	server.close()
	
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
	for key, val in sorted(contracts.iteritems(), key = lambda x: x):
		name_data = parse.parse_contract_name(key)
		if name_data:
			option_value = probability.get_option_value(
				name_data['date'],
				name_data['strike_price'],
				curr_price,
				vol
			)
			highest_bid, lowest_ask = get_buy_and_sell_points(val)
			data = 'Contract %s has value %.3f. Highest bid: %.2f. Lowest ask: %.2f' % (
				key, option_value, highest_bid, lowest_ask)
			color = ''
			if option_value > lowest_ask:
				if option_value < highest_bid:
					color = 'purple'
				else:
					color = 'green'
			elif option_value < highest_bid:
				color = 'red'
			option_data.append({'data': data, 'color': color})

	print 'Got option data'
	send_email(option_data)
	print 'Sent email'
	#print conn.retrieve_recent_transactions()
	#print conn.retrieve_current_contracts()
