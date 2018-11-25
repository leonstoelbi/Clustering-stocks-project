##### Program 6: Display the results graphically

import pandas as pd
import matplotlib.pyplot as plt

## 1. Import .csv file for composition of groups

# Get the CSV file with the whole data set
# Since the pivot table got passed to a csv we have no headers and need to add them
result = pd.read_csv("Result_SP500.csv",encoding="UTF-8", header=0, names=['Group', 'Industry', 'Number of companies'])
result.set_index('Group', inplace=True)
print('Composition of different Groups:\n', result)

# import dataset for visualization
final_stock_array = pd.read_csv("Final_stock_array_SP500.csv",encoding="UTF-8")

## 2. Prepare data

# Delete the CIK column, not needed
del final_stock_array['CIK']

# Get mean from data
dataset_mean = final_stock_array.groupby('Group').mean()
print(dataset_mean)

# Get Bar Chart to show influence of Indicators on different groups
dataset_mean.plot(kind='bar', by='Group')
plt.show()

# exclude Intercept and Index
# since stocks in SPY500 are weighted according to their market cap
# betas of large companies are expected to be extraordinarily high
dataset_mean[["Gold","NatGas","Oil"]].plot(kind='bar', by='Group')
plt.show()

# Pie charts showing group association within industry
for x in final_stock_array["GICS Sector"].unique():
    frame = final_stock_array[final_stock_array["GICS Sector"]==x]
    frame["Group"].value_counts().plot(kind='pie',legend=True,title=x)
    plt.show()