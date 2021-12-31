import numpy as np 
import pandas as pd
from matplotlib import pyplot as plt
from IPython.display import display
import datetime as dt
import matplotlib.dates as mdates

#read in BTC Unique Wallets data and clean
btc_data = pd.read_csv('/Users/broderickbonelli/Desktop/BTCUniqueWallets.csv')
btc_data.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6'], axis=1, inplace=True)
btc_data.columns = ['Date', 'Wallets']
btc_data.drop([0], axis=0, inplace=True)
btc_data['Wallets'] = pd.to_numeric(btc_data['Wallets'])

#set index and convert to datetime object; group data by month, taking the mean # of wallets per month
btc_data.set_index(btc_data['Date'], drop=True)
btc_data['Date'] = pd.to_datetime(btc_data['Date'], format='%Y-%m-%d  %H:%M:%S')
btc_data = btc_data['Wallets'].groupby(btc_data['Date'].dt.to_period('m')).mean()

#create pandas DataFrame
df = pd.DataFrame(btc_data)

#calculate % change of wallet addresses over the prior 12 months
df['Pct Change'] = df['Wallets'].pct_change(periods=12)
df['Pct Change'] = [each * 100 for each in df['Pct Change'].round(2)]

#read in BTC price data, groupby month and calculate average monthly price
price_data = pd.read_csv('/Users/broderickbonelli/Desktop/BTCUSD_price.csv')
price_data.set_index(price_data['Date'], drop=True)
price_data['Date'] = pd.to_datetime(price_data['Date'], format='%Y-%m-%d')
price_data = price_data['Closing Price (USD)'].groupby(price_data['Date'].dt.to_period('m')).mean()
df2 = pd.DataFrame(price_data)

#reset indexes to merge dataframes
df.reset_index(inplace=True)
df2.reset_index(inplace=True)

#merge dataframes
df3 = pd.merge(df, df2)

#resize chart paramaters
plt.rcParams['figure.figsize'] = [15, 7.5]

#conform date format so x axis charts correctly; chart % change in wallets
date_fmt = '%Y-%m'
dt_x = [dt.datetime.strptime(str(i), date_fmt) for i in df3['Date']]
x = [mdates.date2num(i) for i in dt_x]
plt.plot_date(x, df3['Pct Change'], linestyle='solid')
plt.ylim(-60, 200)
plt.title('1y % Change in # of Avg Monthly Unique BTC Wallets')
plt.xlabel('Date')
plt.ylabel('% Change')
plt.axhline(0, color='black')
plt.show()

#chart change in BTC price
plt.plot_date(x, df3['Closing Price (USD)'], linestyle='solid', color='black')
plt.title('BTC Price')
plt.show()

#create figure to plot % Change in wallets and vertical grid lines
fig, ax=plt.subplots()
ax.plot_date(x, df3['Pct Change'], linestyle='solid')
ax.set_ylabel('1y Pct Change in Average Monthly Unique Addresses')
ax.xaxis.grid()


#highlight divergences on chart
ax.axvspan(*mdates.datestr2num(['2018-11', '2019-03']), color='lightgreen', alpha=0.5)
ax.axvspan(*mdates.datestr2num(['2019-05', '2019-07']), color='lightcoral', alpha=0.5)
ax.axvspan(*mdates.datestr2num(['2020-04', '2020-07']), color='lightgreen', alpha=0.5)
ax.axvspan(*mdates.datestr2num(['2021-02', '2021-03']), color='lightcoral', alpha=0.5)

#plot BTC Closing price on dual y-axis
ax2 = ax.twinx()
ax2.plot_date(x, df3['Closing Price (USD)'], color='black', linestyle='solid')
ax2.set_ylabel('BTC Price')
ax2.set_title('1y % Change in Avg Monthly Unique Addresses & BTC Price Divergence')

plt.show()

