##### Program 2: Getting the stock information (S&P 500) through webscraping

import pandas as pd
from lxml import html
import requests

## 1. Download website from Wikipedia

# Download Wikipedia page with list of current stocks in index
# Use DE page since stocks tickers are listed in table, ENG tickers are embedded as regular text
page_sp = requests.get('https://de.wikipedia.org/wiki/NASDAQ-100')

# Change format of downloaded pages so that we can use them
tree = html.fromstring(page_sp.content)

## 2. Extract table with relevant information, solution based on https://towardsdatascience.com/web-scraping-html-tables-with-python-c9baba21059
# Table with tickers is the 5th table on the website

tr_elements = tree.xpath('//table[5]//tr')

# Create an empty list
col = []
i = 0
# For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i += 1
    name = t.text_content()
    #print('%d:"%s"' % (i, name))
    col.append((name, []))


# Since our first row is the header, data is stored on the second row onwards
for j in range(1, len(tr_elements)):
    # T is our j'th row
    T = tr_elements[j]

    # i is the index of our column
    i = 0

    # Iterate through each element of the row
    for t in T.iterchildren():
        data = t.text_content()
        # Check if row is empty
        if i > 0:
            # Convert any numerical value to integers
            try:
                data = int(data)
            except:
                pass
        # Append the data to the empty list of the i'th column
        col[i][1].append(data)
        # Increment i for the next column
        i += 1

## 3. Transform information into a dictionary

Dict = {title: column for (title, column) in col}

## 4. Transform dictionary into a dataframe and store it locally as a .csv file

df_index = pd.DataFrame(Dict)

# Reorder columns since we experienced problems, on some computer columns were automatically arranged alphabetically

df_index.reindex(sorted(df_index.columns), axis=1)

# To see current order and name of columns for reordering
# df_cols = df_index.columns.tolist()

df_index=df_index[['Symbol\n','Name (A-Z)\n','Firmensitz\n','Branche\n']]

# Change the names of the columns for the further process

df_index.columns = ['Ticker', 'Security', 'HQ Location', 'Sector']
df_index.set_index('Ticker', inplace = True)

# The Nasdaq-100 is comprised of 100 companies but 103 securities (e.g Alphabet has class A and C shares - GOOG and GOOGL)
# in the dataset they are listed under the same ticker and we hence need to separate them

for index, row in df_index.iterrows():
    if "," in index:
        # Add new line at bottom of DF and set name to second security
        to_be_added = row
        to_be_added.name = index.split(',')[1][1:]
        df_index = df_index.append(to_be_added)

        # Change index name of current row to first security
        df_index.rename(index={index:index.split(',')[0]}, inplace=True)

# Check to if changes successful
#print(df_index.loc[['GOOG','GOOGL','LBTYA','LBTYK','FOX','FOXA']])

# Sort by index alphabetically
df_index.sort_index(inplace=True)

## 5. Exchange indsutries with classification from NASDAQ website

# Access and save url where stock classification of all NASDAQ stocks are stored
url = 'https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download'
r = requests.get(url, allow_redirects=True)
open('NASDAQ_stock_info_all.csv', 'wb').write(r.content)

# Import the csv file with all NASDAQ stocks
stock_info = pd.read_csv("NASDAQ_stock_info_all.csv",encoding="UTF-8")

# Set ticker as index
stock_info.set_index('Symbol', inplace = True)

# Remove all columns except the sector information
stock_info = stock_info["Sector"]

# Remove current sector column from NDX100 df
del df_index['Sector']

# Append new sector classification
df_index = pd.concat([df_index, stock_info], axis=1, join_axes=[df_index.index])

print(df_index)

# Save the dataframe in a .csv file
df_index.to_csv("NDX100_array.csv", encoding="UTF-8")