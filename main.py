#!/usr/bin/python

import connection
import probability
import datetime
import parse

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

def run(num_trials):
  conn = connection.Connection()
  rel_vol =  conn.get_bitcoin_volatility()
  curr_price = float(conn.get_bitcoin_price())
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
        num_trials,
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
  return curr_price, vol, option_data
  #print conn.retrieve_recent_transactions()
  #print conn.retrieve_current_contracts()

if __name__ == '__main__':
  run(num_trials = 1000)
