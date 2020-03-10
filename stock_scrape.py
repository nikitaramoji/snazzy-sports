from bs4 import BeautifulSoup
import requests
import sqlite3
import datetime
import time
import calendar
import json

### IEX TRADING API METHODS ###

WIKIPEDIA_SP_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

stock_list_page = requests.get(WIKIPEDIA_SP_URL)

### YAHOO FINANCE SCRAPING
YAHOO_STOCKS_URL = "https://finance.yahoo.com/quote/"


# TODO: Use BeautifulSoup and requests to collect data required for the assignment.
soup = BeautifulSoup(stock_list_page.text, 'html.parser')
main_stock_rows = soup.find("table", {"id":"constituents"}).find_all("tr")
old_stock_rows = soup.find("table", {"id":"changes"}).find_all("tr")

def fix_price(price):
	return float(price.replace(',','').replace('-',''))

all_data = []


for row in main_stock_rows:
	#print(row)
	row_data = row.find_all("td")
	fixed_data = {}
	if len(row_data) > 0:
		fixed_data["symbol"] = row_data[0].find("a").text
		fixed_data["name"] = row_data[1].find("a").text
		all_data.append(fixed_data)

cutoff_date = datetime.datetime(2012, 1, 1, 0, 0)

for row in old_stock_rows:
	#print(row)
	row_data = row.find_all("td")
	fixed_data = {}
	if len(row_data) > 0:
		date_string = row_data[0].text
		date_removed = datetime.datetime.strptime(date_string, "%B %d, %Y")
		if date_removed > cutoff_date:
			fixed_data["symbol"] = row_data[3].text
			if fixed_data["symbol"] != "":
				fixed_data["name"] = row_data[4].find("a").text
				all_data.append(fixed_data)

time_ranges= [
		("November 1, 2012", "November 15, 2012"),
		("November 1, 2014", "November 15, 2014"),
		("November 1, 2016", "November 15, 2016"),
		("November 1, 2018", "November 15, 2018")
	]

#time_ranges= [("November 1, 2012", "November 15, 2012")]

stock_num = 0

for stock in all_data:
	print(stock_num)
	print(stock["symbol"])
	stock["stock_data"] = []
	for (start_date, end_date) in time_ranges:
		s_t = time.strptime(start_date, "%B %d, %Y")
		e_t = time.strptime(end_date, "%B %d, %Y")
		s_epoch = calendar.timegm(s_t)
		e_epoch = calendar.timegm(e_t)
		new_url = YAHOO_STOCKS_URL + stock["symbol"] + "/history?period1=" + str(s_epoch) + "&period2=" + str(e_epoch) + "&interval=1d&filter=history&frequency=1d"
		price_page = requests.get(new_url)
		price_soup = BeautifulSoup(price_page.text, 'html.parser')
		price_table = price_soup.find("table", {"data-test":"historical-prices"})
		if price_table != None:
			price_rows = price_table.find_all("tr")
			price_data = []
			for row in price_rows:
				row_data = row.find_all("td")
				# Check if a given row has all entries
				if len(row_data) == 7:
					day_data = {}
					if row_data[1].text != '-':
						day_data["Date"] = row_data[0].text
						day_data["Open"] = fix_price(row_data[1].text)
						day_data["High"] = fix_price(row_data[2].text)
						day_data["Low"] = fix_price(row_data[3].text)
						day_data["Close"] = fix_price(row_data[4].text)
						day_data["Adj. Close"] = fix_price(row_data[5].text)
						price_data.append(day_data)
			stock["stock_data"].append(price_data)
		else:
			print("TABLE NOT FOUND")
	stock_num = stock_num + 1
#print(len(all_data))

# TODO: Save data below.

json_data = json.dumps(all_data)
f = open("stock_data.json","w")
f.write(json_data)
f.close()
