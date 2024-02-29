


'''
Error code -999 or '-999' means there was an error when removing comma(s) from the stock ticker
Error code -1000 or '-1000' means the stock ticker information could not be accessed through HTML tags, 
either the stock does not exist or stock information could not be accessed.

Methods for the web scrapper, such as retrieving information.
stock_name_parser is beautifulsoup HTML parser for the designated stock 

'''

def get_closed_stock_price(stock_name_parser, stock_name):
	closed_price = stock_name_parser.find('fin-streamer', {'data-test':'qsp-price', 'data-field':'regularMarketPrice'})
	if closed_price:
		#handling error where text has comma for values over 1000
		try:
			return float(closed_price.text.replace(',', ''))
		except ValueError:
			return -999
	else:
		print(f"Error: could not load {stock_name} closed price.")
		return -1000

def get_open_stock_price(stock_name_parser, stock_name):
	open_price = stock_name_parser.find('td', {'data-test':'OPEN-value'})
	if open_price:
		#handling error where text has comma for values over 1000
		try:
			return float(open_price.text.replace(',', ''))
		except ValueError:
			return -999
	else:
		print(f"Error: could not load {stock_name} opened price.")
		return -1000

def get_previous_stock_price(stock_name_parser, stock_name):
	prev_stock_price = stock_name_parser.find('td', {'data-test':'PREV_CLOSE-value'})
	if prev_stock_price:
		#handling error where text has comma for values over 1000
		try:
			return float(prev_stock_price.text.replace(',', ''))
		except ValueError:
			return -999
	else:
		print(f'Error: could not load {stock_name} previous price.')
		return -1000
def get_ask_price(stock_name_parser, stock_name):
	ask = stock_name_parser.find('td', {'data-test':'ASK-value'})
	if ask:
		return ask.text
	else:
		print(f'Error: could not load {stock_name} ask')
		return '-1000'

def get_bid_price(stock_name_parser, stock_name):
	bid = stock_name_parser.find('td', {'data-test':'BID-value'})
	if bid:
		return bid.text
	else:
		print(f'Error: could not load {stock_name} bid')
		return '-1000'

def get_stock_market_cap(stock_name_parser, stock_name):
	stock_market_cap = stock_name_parser.find('td', {'data-test':'MARKET_CAP-value'})
	#market cap is String type
	if stock_market_cap:
		return stock_market_cap.text
	else:
		print(f'Error: could not load {stock_name} market cap')
		return '-1000'

def get_stock_volume(stock_name_parser, stock_name):
	stock_volume = stock_name_parser.find('fin-streamer', {'data-field': 'regularMarketVolume'})
	if stock_volume:
		#handling error where text has comma for values over 1000
		try:
			return float(stock_volume.text.replace(',', ''))
		except ValueError:
			return -999
	else:
		print(f"Error: could not load {stock_name} volume.")
		return -1000

def get_stock_pe_ratio(stock_name_parser, stock_name):
	stock_pe_r = stock_name_parser.find('td', {'data-test': 'PE_RATIO-value'})
	if stock_pe_r:
		#handling error where text has comma for values over 1000
		try:
			return float(stock_pe_r.text.replace(',', ''))
		except ValueError:
			return -999
	else:
		print(f"Error: could not load {stock_name} PE Ratio.")
		return -1000

def get_stock_eps(stock_name_parser, stock_name):
	stock_eps = stock_name_parser.find('td', {'data-test': 'EPS_RATIO-value'})
	if stock_eps:
		#handling error where text has comma for values over 1000
		try:
			return float(stock_eps.text.replace(',', ''))
		except ValueError:
			return -999
	else:
		print(f"Error: could not load {stock_name} EPS.")
		return -1000

def get_stock_earnings_date(stock_name_parser, stock_name):
	stock_ed = stock_name_parser.find('td', {'data-test': 'EARNINGS_DATE-value'})
	if stock_ed:
		return stock_ed.text
	else:
		print(f"Error: could not load {stock_name} Earnings Date.")
		return '-1000'

