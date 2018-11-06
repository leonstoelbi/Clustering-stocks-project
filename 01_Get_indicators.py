#This project is supposed to cluster stocks accoding to riskiness. 
#The project will get daily return data, and use that to create regressions against daily commodity returns. 
#The betas from these regressions will then be used in our machine learning model.

#### Program 1: Getting the indicators

import datetime
import pandas as pd
import pandas_datareader as pddr

## 1. Set parameters

# Set start and end date of the considered period 
startDate = datetime.datetime(2010, 1, 1)
endDate = datetime.datetime(2017, 12, 31)


## 2. Get the data

# Get the index price data for SPY and NDX from Yahoo Finance
# Yahoo Finance API connection might be unstable
try:
    index_spy = pddr.get_data_yahoo('SPY', startDate, endDate)
    index_ndx = pddr.get_data_yahoo('^NDX', startDate, endDate)
except:
    # Display message and end program if Yahoo API does not work
    print('\n'
          'It seems, that the Yahoo Finance API or your network connection is unstable \n'
          'Please try to launch the program again')
    exit()

# Get the commodity price data from the federal reserve database 
oil = pddr.fred.FredReader('DCOILWTICO', startDate, endDate).read()
gold = pddr.fred.FredReader('GOLDAMGBD228NLBM', startDate, endDate).read()
natGas = pddr.fred.FredReader('DHHNGSP', startDate, endDate).read()


## 3. Structure the data

# Transform DFs from absolute prices to percentage changes
index_ndx_chg = index_ndx['Adj Close'].pct_change()
index_ndx_chg.name = 'NDX_Index'
index_spy_chg = index_spy['Adj Close'].pct_change()
index_spy_chg.name = 'SPY_Index'
oil_chg = oil.pct_change()
gold_chg = gold.pct_change()
natGas_chg = natGas.pct_change()

# Merge the DFs
df = pd.concat([index_ndx_chg, index_spy_chg, oil_chg, gold_chg, natGas_chg], axis=1)

# Rename columns and index for easier handling later
df.rename(columns={'DCOILWTICO':'Oil', 'GOLDAMGBD228NLBM':'Gold', 'DHHNGSP':'NatGas'}, inplace=True)
df.index.name ='DATE'

# Drop NaNs
df.dropna(inplace=True)

## 4. Store data locally as a csv file

print(df.head())
print(df.tail())

df.to_csv('Variables.csv', encoding='UTF-8')