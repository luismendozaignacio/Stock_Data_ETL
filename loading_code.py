#methods for loading stock tickers, saving code to external txt or csv files

#loading stocks from stockNames.txt
def load_test_text_stocks():
	# Specify the txt file path
	txt_file_path = 'stockNames.txt'

	# Open the text file and read names into a list
	with open(txt_file_path, 'r') as txt_file:
	    # Use list comprehension to extract names from each row
	    stock_ticker = [row.strip() for row in txt_file]
	return stock_ticker


#saving stock errors
def save_errors(error_stocks):
	#Specify the file path
	txt_file_path = 'errors.txt'

	#'a' to append any errors that have occurred
	with open(txt_file_path, 'a') as txt_file:
	    for item in error_stocks:
	        txt_file.write(f"{item}\n")  # Add a newline character after each item

	print(f"The list has been saved to {txt_file_path}")


#loading the stock errors from stockErrors.txt
def load_stock_errors():
	txt_file_path = 'stockErrors.txt'

	# Open the file in read mode
	with open(txt_file_path, 'r') as txt_file:
	    load_errors = [item.strip() for item in txt_file]
	    return load_errors

