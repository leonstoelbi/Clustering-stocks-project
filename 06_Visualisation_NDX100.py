##### Program 6: Display the results graphically

import pandas as pd
import matplotlib.pyplot as plt

## 1. Import .csv file for composition of groups

# Get the CSV file with the whole data set
# Since the pivot table got passed to a csv we have no headers and need to add them
result = pd.read_csv("Result_NDX100.csv",encoding="UTF-8", header=0, names=['Group', 'Industry', 'Number of companies'])
result.set_index('Group', inplace=True)
print('Composition of different Groups:\n', result)

# import dataset for visualization
final_stock_array = pd.read_csv("Final_stock_array_NDX100.csv",encoding="UTF-8")

## 2. Prepare data

# Get mean from data
dataset_mean = final_stock_array.groupby('Group').mean()
print(dataset_mean)

# Get Bar Chart to show influence of Indicators on different groups
dataset_mean.plot(kind='bar', by='Group')
plt.show()

# exclude Intercept and Index
# as in SPY500 we exclude Intercept and Index, since number of stocks is even
# smaller, the effect of the index will be even stronger
dataset_mean[["Gold","NatGas","Oil"]].plot(kind='bar', by='Group')
plt.show()

# Pie charts showing group association within industry
# Not very relevant for NDX100 since mostly technology firms
# Current data on industry is to narrow to appropriately group

# Try/Except loop due to some nan values in sector column

for x in final_stock_array["Sector"].unique():
    try:
        frame = final_stock_array[final_stock_array["Sector"]==x]
        frame["Group"].value_counts().plot(kind='pie',legend=True,title=x)
        plt.show()
    except: 
        print("An error occured with the industry: " + str(x))
        pass