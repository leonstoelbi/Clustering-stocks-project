#This project is supposed to cluster stocks accoding to their riskiness/dependencies on independent factors. 
#The project will get daily return data, and use that to create regressions against daily commodity returns. 
#The betas from these regressions will then be used in our machine learning model.

#### Program 1: Getting the indicators

import datetime
import pandas as pd
import pandas_datareader as pddr

## 1. Set parameters

# Set start and end date of the considered period 
start_Date = datetime.datetime(2010, 1, 1)
end_Date = datetime.datetime(2017, 12, 31)


## 2. Get the data

# Get the index price data for SPY and NDX from Yahoo Finance
# Yahoo Finance API connection might be unstable, therefore, we use a try/except loop
try:
    index_spy = pddr.get_data_yahoo('SPY', start_Date, end_Date)
    index_ndx = pddr.get_data_yahoo('^NDX', start_Date, end_Date)
except:
    # Display message and end program if Yahoo API does not work
    print('\n'
          'It seems, that the Yahoo Finance API or your network connection is unstable \n'
          'Please try to launch the program again')
    exit()

# Get the oil price data from the federal reserve database 
oil_prices = pddr.fred.FredReader('DCOILWTICO', start_Date, end_Date).read()
# Get the gold price data from the federal reserve database
gold_prices = pddr.fred.FredReader('GOLDAMGBD228NLBM', start_Date, end_Date).read()
# Get the natural gas price data from the federal reserve database
naturalGas_prices = pddr.fred.FredReader('DHHNGSP', start_Date, end_Date).read()


## 3. Structure the data

# Transform DFs from absolute prices to percentage changes
index_ndx_chg = index_ndx['Adj Close'].pct_change()
index_ndx_chg.name = 'NDX_Index'
index_spy_chg = index_spy['Adj Close'].pct_change()
index_spy_chg.name = 'SPY_Index'
oil_chg = oil_prices.pct_change()
gold_chg = gold_prices.pct_change()
naturalGas_chg = naturalGas_prices.pct_change()

# Merge the DFs
df = pd.concat([index_ndx_chg, index_spy_chg, oil_chg, gold_chg, naturalGas_chg], axis=1)

# Rename columns and index for easier handling later
df.rename(columns={'DCOILWTICO':'Oil', 'GOLDAMGBD228NLBM':'Gold', 'DHHNGSP':'NatGas'}, inplace=True)
df.index.name ='DATE'

# Drop NaNs
df.dropna(inplace=True)

## 4. Check result and store data locally as a csv file

print(df.head())
print(df.tail())

df.to_csv('Variables.csv', encoding='UTF-8')