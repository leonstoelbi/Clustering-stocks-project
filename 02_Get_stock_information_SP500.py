##### Program 2: Getting the stock information (S&P 500) through webscraping

import pandas as pd
from lxml import html
import requests

## 1. Download website from Wikipedia

# Download Wikipedia page with list of current stocks in index
page_sp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

# Change format of downloaded pages so that we can use them
tree = html.fromstring(page_sp.content)

## 2. Extract table with relevant information, solution based on https://towardsdatascience.com/web-scraping-html-tables-with-python-c9baba21059

# Rows of the table are separated by "tr" so we parse the data between each of them
tr_elements = tree.xpath('//tr')


# Create an empty list
col = []
i = 0
# For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i += 1
    name = t.text_content()
    print('%d:"%s"' % (i, name))
    col.append((name, []))

# Since our first row is the header, data is stored on the second row onwards
for j in range(1, len(tr_elements)):
    # T is our j'th row
    T = tr_elements[j]

    # If row is not of size 10, the //tr data is not from our table
    if len(T) != 9:
        break

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
df_cols=df_index.columns.tolist()
df_index=df_index[['Symbol','Security','SEC filings','GICS Sector', 'GICS Sub Industry', 'Location', 'Date first added[3][4]','CIK', 'Founded\n']]

# Drop the last column since it is not required for the further process
df_index = df_index.iloc[:, :-1]

# Change the names of the columns for the further process
df_index.columns = ["Ticker", "Security", "SEC Filings", "GICS Sector", "GICS Sub Industry", "Address", "Date Added", "CIK"]

# Remove unnecessary symbols from tickers
ticker_list = []
for ticker in df_index["Ticker"].values:
    if "." in ticker:
        ticker = ticker.replace(".","")
        ticker = ticker.replace(":","")
        ticker = ticker.replace(";","")
    ticker_list.append(ticker)

# Add new tickers list to .csv file
df_index["Ticker"]=ticker_list

# Set tickers as index
df_index.set_index('Ticker', inplace = True)

# Save output as .csv file
df_index.to_csv("SP500_array.csv", encoding="UTF-8")