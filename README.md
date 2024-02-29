# Stock_Data_ETL
Python Script that scrapes data from finance.yahoo.com with the selected stock tickers specified. Then uploads it to local PostgreSQL server for storage and/or further analysis. This is considered an ETL (Extract, Transform, Load) pipeline but in a small scale. 

Initially the project was to scrape data for Fortune 500 Companies. I used https://www.50pros.com/fortune500 to compile the list of Fortune 500 Companies found in 'stockNames.txt'. Unfortunately only 429 tickers work on finance.yahoo.com. Feel free to add/remove any stock tickers. 

# How to get started
The main file you will run is called 'web_scrapper.py'. It contains the code to read the stock tickers stored in 'stockNames.txt' and connects to your PostgreSQL.

Before you run 'web_scrapper.py', make sure to add your PostgreSQL credentials to 'database.ini'. Change the following only: host, database, user, password, port. 
Next, make sure to run 'requirements.py' (you only need to do this once) to download the required libraries used such as beautifulsoup4, requests, & psycopg2.

Lastly run 'web_scrapper.py' and change any stock tickers you want to have data in 'stockNames.txt', enjoy!

# Other resources
PostgreSQL setup: https://www.postgresqltutorial.com/postgresql-getting-started/install-postgresql/

BeautifulSoup: https://beautiful-soup-4.readthedocs.io/en/latest/#

psycopg2: https://www.psycopg.org/docs/
