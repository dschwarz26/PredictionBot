import datetime
import calendar

def parse_contract_name(name):
	if name.startswith('Price of Bitcoin end'):
		pass
	elif name.startswith('Price of Bitcoin'):
		return parse_bitcoin_option_contract(name)
	elif name.startswith('Next Bitcoin network difficulty'):
		pass
	elif name.startswith('Bitcoin network difficult'):
		pass
	elif name.startswith('Bitcoin price to reach'):
		pass
	else:
		print('Unknown bitcoin contract name: %s' % name)

def parse_bitcoin_option_contract(name):
	tokens = name.split(' ')
	month = 0
	for i, month_name in enumerate(calendar.month_name):
		if tokens[3] == month_name:
			month = i
	try:
		day = int(tokens[4][:2])
	except ValueError:
		day = int(tokens[4][0])
	date = datetime.datetime(2014, month, day)
	strike_price = float(tokens[9][1:])
	data = {'date': date, 'strike_price': strike_price}
	return data
