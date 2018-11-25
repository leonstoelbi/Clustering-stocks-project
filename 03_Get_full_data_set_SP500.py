##### Program 3: Get stock prices of SPY500 and merge data with index/commodity prices

import pandas as pd
import quandl
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pickle

# Set Quandl API key
quandl.ApiConfig.api_key = "GsT-jhY8mPatmzkh9yz8"

## 1. Import .csv file with indicators

# Get the CSV file from earlier with the index/commodity prices
variables = pd.read_csv("Variables.csv", encoding="UTF-8")

# Set Date as the index
variables = variables.set_index(["DATE"])

## 2. Import .csv file with indicators

# Get the CSV file with the stocks array
stocks = pd.read_csv("SP500_array.csv", encoding="UTF-8")
tickers = stocks['Ticker'].tolist()

## 3. Download stock prices from Quandl

# quandle.get_table can only download a limited number of data point per request
# Therefore we download the data yearwise and add it progressively to one large DataFrame

# Set Start/end date of entire dataset
abs_start = "2010-01-01"
abs_end = "2017-12-31"
# Following line would set today as end date
# abs_end = datetime.strftime(datetime.today(),"%Y-%m-%d")

# Get number of years between the dates and add additional period for unfinished year
periods = relativedelta(datetime.strptime(abs_end,"%Y-%m-%d"), datetime.strptime(abs_start,"%Y-%m-%d")).years + 1

# Create DataFrame to gather yearly data in loop
df = pd.DataFrame(columns=['adj_close', 'date', 'ticker'])

 ## UNCOMMENT ABOVE IF NOT USING PICKLE (for testing, to not download entire dataset from Quandl again)

# Loop through years and get data for every year
for year in range(periods):
    # set start date within every loop
    start = datetime.strptime(abs_start, "%Y-%m-%d") + relativedelta(years=year)
    start = datetime.strftime(start, "%Y-%m-%d")

    # set end date within every loop

    # check if timespan is larger than 1 year and fetch data for year
    if relativedelta(datetime.strptime(start, "%Y-%m-%d"), datetime.strptime(abs_end, "%Y-%m-%d")).years < 0:
        end = datetime.strptime(abs_start, "%Y-%m-%d") + relativedelta(years=year + 1) - timedelta(days=1)
        end = datetime.strftime(end, "%Y-%m-%d")
        print("Fetching data for time period " + str(start) + " - " + str(end) + " ...")

    # get remaining data
    else:
        end = datetime.strptime(abs_end, "%Y-%m-%d")
        print("Fetching data for time period " + str(start) + " - " + str(abs_end) + " ...")

    # get data in two dataframes due to limit in requests using above set 1 year ranges
    df1 = quandl.get_table('WIKI/PRICES', date={'gte': start, 'lte': end}, ticker=tickers[:250], paginate=True,
                           qopts={"columns": ["adj_close", "date", "ticker"]})
    df2 = quandl.get_table('WIKI/PRICES', date={'gte': start, 'lte': end}, ticker=tickers[250:], paginate=True,
                           qopts={"columns": ["adj_close", "date", "ticker"]})

    # merge above dataframes
    df3 = pd.concat([df1, df2])

    # add current data to base dataframe
    df = pd.concat([df, df3])

# convert to pivot table to get date unique observations (-> otherwise output would be unique for ticker and dates)
df = df.pivot_table(index="date", columns="ticker")

# Date as index
df.index.names = ['DATE']

# drop aditional column level
df.columns = df.columns.droplevel()

# drop empty columns
df.columns = df.columns.dropna(how='all')

# get relative returns per trading day per ticker
df = df.pct_change()

# Save dataframe locally as pickle to avoid downloading again while working on code
with open('SPY500_prices.pickle', 'wb') as f:
    pickle.dump(df, f)

## UNCOMMENT ABOVE IF NOT USING PICKLE

with open('SPY500_prices.pickle', 'rb') as f:
    stock_prices = pickle.load(f)

# Drop first row of stock_prices since it has this one observation more than variables
stock_prices = stock_prices.iloc[1:]

# print('Number of observations/trading days:', len(stock_prices.index), '\n')
# print('Number of observations/trading days:', len(variables.index)), '\n')

## 4. Merge dataframe containing the stock prices with dataframe containing the indicators

dataset = pd.merge(stock_prices, variables, how='left', right_index=True, left_index=True)

## 5. Get the tickers of the missing stocks

# Since the Quandl API cannot get the values of some stocks, we would like to find out which stocks are missing
missing_stocks = []
for stock in tickers:
    if stock not in stock_prices.columns.values:
        missing_stocks.append(stock)
print('\nThe following', len(missing_stocks), 'stocks are missing due to Quandl API:\n', missing_stocks)

# Store dataframe locally as csv file
dataset.to_csv('Dataset_complete_SP500.csv', encoding='UTF-8')