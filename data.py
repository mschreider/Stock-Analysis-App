import pandas as pd
import numpy as np
from matplotlib import pyplot, axes
from matplotlib import dates as mdates
from mplfinance.original_flavor import candlestick_ochl
import pandas_datareader.data as data
import datetime

class Stock():
    def __init__(self, ticker):
        self.ticker = ticker
    
    def getData(self):
        start = datetime.date.today() - datetime.timedelta(days=120)
        end = datetime.date.today()
            
        # dataframe object
        df = data.DataReader(name=self.ticker, data_source="yahoo",start=start,end=end)
        df.index.to_pydatetime()
        return df
    
    def getSMA(self):
        df = self.getData()
        closeprice = df['Close']
        time_period = 20    
        """
        numbers_series = pd.Series(closeprice)
        windows = numbers_series.rolling(time_period)
        moving_averages = windows.mean()
        moving_averages_list = moving_averages.tolist()
        df['20-day SMA'] = moving_averages_list
        """
        df['20-day SMA'] = df['Close'].rolling(time_period).mean()

        return df
    
    def getBollBand(self, df):
        sma = df['20-day SMA'].tolist()
        time_period = 20
        df['Lower Band'] = df['20-day SMA'] - df['Close'].rolling(time_period).std() * 2
        df['Upper Band'] = df['20-day SMA'] + df['Close'].rolling(time_period).std() * 2
        return df
        """
        numbers_series = pd.Series(sma)
        std_dev = numbers_series.rolling(time_period).std()  
        std_dev_list = std_dev.tolist()
        df['20-Day Standard Deviation'] = std_dev_list
        
        lower = sma - df['Close'].rolling(time_period).std() * 2
        df['lowerband'] = lower
        print(lower)
        """

    def inc_dec(self, c, o):
        if c > o:
            value = "Increase"
        elif c < o:
            value = "Decrease"
        else:
            value = "Equal"
        return value

class SnapToCursor(object):
    def __init__(self, ax, x, y):
        self.ax = ax
        self.lx = ax.axvline(color='k') # The horizontal Line
        self.ly = ax.axvline(color='k') # The Vertcal Line
        self.x = x
        self.y = y
        # Text location in axes coords
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)
    
    def mouse_move(self, event):
        if not event.inaxes:
            return
        
        x, y = event.xdata, event.ydata
        indx = min(np.searchsorted(self.x, x), len(self.x) -1)
        x = self.x[indx]
        y = self.y[indx]
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        print('x=%1.2f, y=%1.2f' % (x, y))
        self.ax.figure.canvas.draw()

    
## Initialize Stock() Class ##
tesla = Stock('TSLA')
data = tesla.getSMA()
df = tesla.getBollBand(data)

## Extract data from tesla dataframe ##
#df["Status"] = [tesla.inc_dec(c, o) for c, o in zip(df.Close, df.Open)]
#df["Middle"] = (df.Open + df.Close) / 2
df["Daily Change"] = abs(df.Close - df.Open)
date = df.index.values
openprice = df['Open']
closeprice = df['Close']
high = df['High']
low = df['Low']

## Get data for candlestick_ochl() and append to a list ##
x = 0
y = len(date)
data = []
while x < y:
    append_me = date[x], openprice[x], closeprice[x], high[x], low[x]
    data.append(append_me)
    x += 1
print(type(date[1]))
## Plot Candlesticks ##
fig, ax1 = pyplot.subplots()
candlestick_ochl(ax1, data, width=np.timedelta64(12, 'h'), colorup='green', colordown='red', alpha=0.75)
## Plot 20-Day SMA overlapping Candlestick plot ##
ax1.plot(df['20-day SMA'], color='#26baee', linestyle='--')  

## Plot Upper Bands ##
ax1.plot(df['Upper Band'], color='#783eff', linestyle='-')

## Plot Lower Bands ##
ax1.plot(df['Lower Band'], color='#783eff', linestyle='-')

## Snap to Cursor ##
#snap_cursor = SnapToCursor(ax1, date, closeprice)
#fig.canvas.mpl_connect('motion_notify_event', snap_cursor.mouse_move)

## Set Plot properties ##
fig.suptitle('Bollinger Bands of TESLA')
pyplot.yticks(np.arange(min(closeprice)-(0.1*min(closeprice)), max(closeprice)+(0.1*max(closeprice)),  50))
pyplot.ylabel('Price')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d-%Y'))
fig.autofmt_xdate()
pyplot.xticks(rotation=45)
pyplot.xlabel('Date')
pyplot.show()
