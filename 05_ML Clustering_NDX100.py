##### Program 5: Use machine learning algorythms for clustering the stocks

import pandas as pd
from sklearn.cluster import KMeans

## 1. Import .csv file with dataset

# Get the CSV file with the betas/regression results

reg_matrix = pd.read_csv('Reg_Matrix_NDX100.csv',encoding='UTF-8')

# Set NaN values as 0
reg_matrix = reg_matrix.fillna(0)
reg_matrix.set_index('Indicators', inplace=True)

## 2. Transpose dataframe so that beta indicators are the columns

reg_matrix = reg_matrix.transpose()


## 3. Calculate the z-value to determine whether the value of the indicator is far from the mean

# Create dataframe for z values
reg_matrix_z = pd.DataFrame()

# Use a for loop to run this operation for every indicator and put it in dataframe for z-values
for indicator in reg_matrix.columns:
    # z-value = value of the indicator minus the mean, divided by the column´s standard deviation
    reg_matrix_z[indicator] = (reg_matrix[indicator] - reg_matrix[indicator].mean())/reg_matrix[indicator].std(ddof=0)

## 4. Apply kmeans to cluster stocks based on number of groups as an input

# Get the number of Groups as an input
print('How many clusters would you like to create? (We recommend 5 to 10) - Please enter an integer:')

try:
    num_clusters = int(input())
except:
    print('You did not enter a valid value. You can only enter an integer. Please restart the program.')


# Set number of clusters to n (=input)
algo = KMeans(n_clusters=num_clusters)

# Create n groups where stocks are as similar as possible to each other within group
# but as different as possible compared to stocks in other groups
algo = algo.fit(reg_matrix)

# Create new column that contains the group of each stock
reg_matrix['Group'] = algo.labels_

## 5. Get industry information (previously parsed from wiki with stock tickers)

# Import .csv file with stock info
stock_info = pd.read_csv('NDX100_array.csv', encoding='UTF-8')

# Set tickers as index
stock_info.set_index('Ticker', inplace=True)

# Concat Regression matrix and stock info array
stock_info = pd.concat([stock_info,reg_matrix],axis=1,join='inner')
stock_info.index.name = 'Ticker'

print(stock_info.head())

## 6. Get industry information from wiki

# Group by the number of companies per group   
result = pd.DataFrame()
result = stock_info
result = result.groupby('Group')['Sector'].value_counts()
# print(result)

## 6. Save the final result locally as a .csv file

result.to_csv('Result_NDX100.csv',encoding='UTF-8')

stock_info.to_csv('Final_stock_array_NDX100.csv',encoding='UTF-8')