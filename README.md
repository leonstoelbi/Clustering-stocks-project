# Clustering-stocks-project
Comparison of the prices of the NASDAQ 100 and the SP 500 stocks according to their dependency on the market, oil, gold and natural gas. 

Please read the README file before running the program.

This program is doing the following for NASDAQ 100 and the SP 500 stocks seperately to compare the results:
1. Get historical prices for the index, oil, gold and natural gas
2. Get the stock information including ticker and sector via webscraping and downloading a .csv file from a url
3. Get the prices for each stock and merge the dataframes to get one dataframe conatining all the information required
4. Run a regression on the stock data set to see what drives stock prices
5. Use machine learning algorythms for clustering the stocks in groups based on their dependencies
6. Visualizes the results with pie charts for every industry showing the number stocks per group. 


Before you run the program please consider the following before you run the program:
1. Since every part creates necessary files for the following steps, you have to run the individual programs in the correct order (01 to 06)
2. NASDAQ clustering and SP 500 culstering are seperated, therefore run both programs and compare results afterwards

To understand the single lines in the code please read through the comments. If you have questions, do not hesitate to contact leon.stoelben@student.unisg.ch or florian.balmer@student.unisg.ch

Disclaimer:

The program worked fine with Spyder and Python 3.6 on the 7th of November 2018. Running the code with other versions of Python or programs may cause errors. Further, the website links and the available data on these websites may have changed meanwhile. 

