import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Get stock symbol from command line parameter use command line parser
import argparse

# Get stock symbol from command line parameter
parser = argparse.ArgumentParser()
parser.add_argument("symbol", help="Stock symbol")
parser.add_argument("-p", "--plot", help="Plot the data", action="store_true")
args = parser.parse_args()

symbol = args.symbol

ticker = yf.Ticker(symbol)

# Get historical market data
hist = ticker.history(period="max")

start_date = hist.index[0]
end_date = hist.index[-1]
# output the start and end date the date part

# resample the data to monthly
monthly_hist = hist.resample('ME').last()

# calculate the monthly return
monthly_returns = monthly_hist['Close'].pct_change().dropna()
monthly_returns.name = 'Return'

#calculate the average monthly return of all positive returns
positive_returns = monthly_returns[monthly_returns > 0]
average_positive_return = positive_returns.mean()
max_positive_return = positive_returns.max()

# calculate the return distribution of the monthly returns
# return_distribution = monthly_returns.describe()

bins = pd.IntervalIndex.from_tuples([
    (-float('inf'), -0.1), 
    (-0.1, -0.09), 
    (-0.09, -0.08),
    (-0.08, -0.07),
    (-0.07, -0.06),
    (-0.06, -0.05),
    (-0.05, -0.04),
    (-0.04, -0.03),
    (-0.03, -0.02),
    (-0.02, -0.01),
    (-0.01, 0), 
    (0, 0.01),
    (0.01, 0.02),
    (0.02, 0.03),
    (0.03, 0.04),
    (0.04, 0.05),
    (0.05, 0.06),
    (0.06, 0.07),
    (0.07, 0.08),
    (0.08, 0.09),
    (0.09, 0.1), 
    (0.1, 0.2), 
    (0.2, float('inf'))])  
return_distribution_bycount = monthly_returns.groupby(pd.cut(monthly_returns, bins)).count()

return_distribution = pd.cut(monthly_returns, bins).value_counts(normalize=True).sort_index() * 100


print(f"Symbol: {symbol}")
#print the start and end date and show the date difference between the two  dates
print(f"From:{start_date.date()} To:{end_date.date()}")
# print the average positive return as percentage
print(f"Average positive monthly return: {average_positive_return:.2%}")
print(f"Max positive monthly return: {max_positive_return:.2%}")



print(return_distribution)

if args.plot:
    # plot the monthly returns
    monthly_returns.plot(kind='hist', bins=30, title=f'{symbol} Monthly Return Distribution', color='skyblue', edgecolor='black')
    plt.show()
