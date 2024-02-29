import requests 
from bs4 import BeautifulSoup
from configparser import ConfigParser
import psycopg2
from datetime import date
from loading_code import *
from ws_methods import *

#Fortune 500 Companies for 2024
#https://www.50pros.com/fortune500
#some of these companies have been excluded due to 
#not being able to access the stock in finance.yahoo.com


def scrapping_stocks(stock_tickers):
	'''
	BeautifulSoup is used along with request to obtain data from finance.yahoo.com

	Each method is stored in ws_methods.py

	Data is saved in a temp dictionary array

	returns dictionary array of stored data and an array of stock tickers whose data had errors.
	'''
	error_stocks = []
	data_storage = [] 
	for stock in stock_tickers:

		#connecting to Yahoo.com with stock name 
		url = f'https://finance.yahoo.com/quote/{stock}?p={stock}'
		print(f'Accessing: {url}')
		page = requests.get(url)
		

		#create Soup HTML parser
		soup = BeautifulSoup(page.content, 'html.parser')

		#closed price
		close_price = get_closed_stock_price(soup, stock)
		print(f'{stock} Closed price:{close_price}')

		#opened price
		open_price = get_open_stock_price(soup, stock)
		print(f'{stock} Open price:{open_price}')

		#previous price
		prev_price = get_previous_stock_price(soup, stock)
		print(f'{stock} Previous price:{prev_price}')

		#ask price 
		ask_price = get_ask_price(soup, stock)
		print(f'{stock} Ask price:{ask_price}')

		#bid price
		bid_price = get_bid_price(soup, stock)
		print(f'{stock} Bid price:{bid_price}')

		#market cap
		market_cap = get_stock_market_cap(soup, stock)
		print(f'{stock} Market cap:{market_cap}')

		#volume
		volume = get_stock_volume(soup, stock)
		print(f'{stock} Volume:{volume}')

		#PE Ratio
		pe_ratio = get_stock_pe_ratio(soup, stock)
		print(f'{stock} PE Ratio:{pe_ratio}')

		#EPS 
		eps = get_stock_eps(soup, stock)
		print(f'{stock} EPS:{eps}')

		#Earnings Date
		e_date = get_stock_earnings_date(soup, stock)
		print(f'{stock} Earnings Date:{e_date}')

		#Change of day (percentage)
		price_change_percentage = round((((close_price - open_price) / open_price) * 100), 2)
		print(f'{stock} Price change:{price_change_percentage}%')

		#Date stock data was accessed
		day_date = date.today()


		#Checks to see if close, open, prev prices could be accessed. 
		#If all three have no error codes (-999 or -1000) than they pass. Does not matter if the other info do not show
		if close_price != -1000 and close_price != -999 and open_price != -1000 and open_price != -999 and prev_price != -1000 and prev_price != -999:
			print('	-------NO ERRORS WITH STOCK-------')
			#save and append data
			stock_data = {
			'stock_name': stock,
			'close_price': close_price,
			'open_price': open_price,
			'previous_price': prev_price,
			'ask_rice': ask_price,
			'bid_price': bid_price,
			'market_cap': market_cap,
			'volume': volume,
			'pe_ratio': pe_ratio,
			'eps': eps,
			'e_date': e_date,
			'price_change': price_change_percentage,
			'date_': day_date
			}
			data_storage.append(stock_data)

		else:
			#stocks with main errors get appended to error_stocks and their data isn't included
			error_stocks.append(stock)
			print(f'ERRORS WITH {stock}')
		print('-------------------------------------------')


	return error_stocks, data_storage

def saving_data_to_SQL_server(stock_data, cur, conn):

	'''
	Data is parsed and inserted to relation specified after "INSERT INTO"

	returns nothing
	'''
	#prints dictionary array of data that will be parsed and sent to the server
	#print(f'------------------------------')
	#print(f'Current data: {stock_data}')

	try:
		#start parsing through dictionary of data.
		for stock in stock_data:
			print('--------------------------------')
			print(stock)
			print('--------------------------------')

			#following line is written in PostgreSQL 
			sql="""
					INSERT INTO fortunefivehundstocks(stock_name, 
					close_price, open_price, previous_price, 
					ask_price, bid_price, market_price, volume, 
					pe_ratio, eps, e_date, price_change_percentage,date_)
					VALUES(%(stock_name)s, 
						%(close_price)s,
						%(open_price)s,
						%(previous_price)s,     
						%(ask_rice)s,
						%(bid_price)s,
						%(market_cap)s,
						%(volume)s,
						%(pe_ratio)s,
						%(eps)s,
						%(e_date)s,
						%(price_change)s,
						%(date_)s)
				"""
			#send data for that stock to the server
			cur.execute(sql, stock)

			#commit the transaction
			conn.commit()


	except Exception as error:
		print(f'Error: {error}')
	
 
def config(filename='database.ini', section='postgresql'):
	'''
	returns credentials for server as config
	'''
	parser = ConfigParser()
	parser.read(filename)


	#get section
	config = {}
	if parser.has_section(section):
		params = parser.items(section)
		for param in params:
			config[param[0]] = param[1]
	else:
		raise Exception(f'Section {section} not found in the {filename} file')
	return config 

def connect():
	'''
	returns connection as conn and cursor as cur
	'''

	"""Connecting to the PostgreSQL database server"""

	conn = None
	try:
		#Read connection parameters
		params = config()

		#Connect to the PostgreSQL server 
		print('Connecting to the PostgreSQL database...')
		conn = psycopg2.connect(**params)

		#create cursor
		cur = conn.cursor()

		#sample query
		#.execute is used to execute the SQL command 
		cur.execute('SELECT version()')

		#PostgreSQL database server version  
		#fetchone(), gets the out put of the query from above
		db_version = cur.fetchone()
		print(f'PostgreSQL database version: {db_version}')

		#return connection and cursor
		return conn, cur
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		return None, None

def close_connection(conn, cur):
	'''
	returns nothing
	'''

	"""Closes the connection to the database"""

	try:
		cur.close()
		conn.close()
		print('Connection closed.')
	except psycopg2.Error:
		print('Error closing database connection:')





if __name__ == '__main__':
	#The following 2 lines of code are for testing purposes. Feel free to delete if not required
	#main_tester = ['WMT', 'CBRE', 'AAPL', 'XOM', 'UNH', 'CVS']
	#small_tester = ['WMT']
	
	#stock_ticker is the array of stocks you will use.
	#Make sure ALL STOCK TICKERS ARE CAPITALIZED
	stock_ticker = load_test_text_stocks()


	#initiate empty list for temp stock info storage before SQL Database
	stock_data_list = None

	#list of stocks that cannot be accessed
	error_stocks = None

	while True:
		#calls the scrapping function 
		error_stocks,stock_data_list = scrapping_stocks(stock_ticker)

		#if errors within the stocks then it saves the errors and moves on to sending data to server
		if error_stocks:
			print(f'There were some errors for {error_stocks} tickers.')
			save_errors(error_stocks) #saves errors to a txt file specified in save_errors()
			break
		else:
			print(f'Successful: No errors, proceeding to saving data to server')
			break

	#Connection to database and transfer of data
	print('----------------------------')
	print('Beginning of Data Transfer to database')

	#connecting to database
	conn, cur = connect()

	#saving stock data to PostgreSQL server
	saving_data_to_SQL_server(stock_data_list, cur, conn)


	#closing database connection
	#DO NOT DELETE, VERY IMPORTANT CONNECTION IS CLOSED
	close_connection(conn, cur)