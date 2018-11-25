##### Program 4: Running a regression on the S&P 500 data set to see what drives S&P 500 stock prices

import pandas as pd
import statsmodels.formula.api as sm

## 1. Import .csv file with dataset

# Get the CSV file with the whole data set 
dataset = pd.read_csv("Dataset_complete_SP500.csv", encoding="UTF-8")

## 2. Create function with regression model

def regress(ticker):
    # Creating model and determining dependent variable/independent variables
    # Does not include Nasdaq Index in regression
    reg_model = sm.ols(formula=ticker+" ~ SPY_Index + Oil + Gold + NatGas", data=dataset).fit()
    
    # Following line does the following:
    # 1. Check whether p-Value is smaller than 5%, index the results 
    # 2. Return parameters if p-Value < 0.05
    # 3. Stores parameters for each given ticker/stock in a dataframe
    return pd.DataFrame(reg_model.params[reg_model.pvalues<.05], columns=[ticker])

## Test regression
#def regress_test(ticker):
#    result = sm.ols(formula=ticker+" ~ SPY_Index + Oil + Gold + NatGas", data=dataset).fit()
#    print(result.pvalues<.05)
#    print(result.params)

## 3. Run regression function for every stock/ticker

# Using for loop for this
reg_matrix = pd.DataFrame()

# Do not include last 5 columns with indices and commodity prices and 1st column with index name
for ticker in dataset.columns[1:-5]:

    # Perform regression for stock and save parameters in reg_stock
    reg_stock = regress(ticker)

    # Append parameter of stock´s regression to the dataframe
    reg_matrix = pd.concat([reg_matrix,reg_stock], axis=1, sort=True)

# Assign name to Index
reg_matrix.index.name = 'Indicators'
print(reg_matrix.head())

## 4. Store regression matrix as a .csv file

reg_matrix.to_csv("Reg_Matrix_SP500.csv",encoding="UTF-8")