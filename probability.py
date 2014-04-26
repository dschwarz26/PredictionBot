import random
import datetime

#Simulates the price of bitcoin. Assumes a Gaussian random process.
#Returns number of num_trials where the change is greater than the price
#difference.
def simulate_walk(num_trials, price_difference, num_days, std_dev):
	num_successes = 0
	for _ in range(num_trials):
		diff = 0
		for _ in range(num_days):
			change = random.gauss(0, std_dev)
			diff += change
		if diff > price_difference:
			num_successes += 1
	return num_successes

def get_option_value(date, price, strike_price, num_trials, std_dev):
	num_days = (date - datetime.datetime.utcnow()).days
	price_difference = price - strike_price
	num_successes = simulate_walk(num_trials, price_difference, num_days, std_dev)
	return 10 * float(num_successes) / float(num_trials)
