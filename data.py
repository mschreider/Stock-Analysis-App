import pandas, json
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

    def inc_dec(self, c, o):
        if c > o:
            value = "Increase"
        elif c < o:
            value = "Decrease"
        else:
            value = "Equal"
        return value
    
    def getGraph(self, df):
        
        df["Status"] = [self.inc_dec(c, o) for c, o in zip(df.Close, df.Open)]
        df["Middle"] = (df.Open + df.Close) / 2
        df["Daily Change"] = abs(df.Close - df.Open)
        date = df.index.values
        openprice = df['Open']
        closeprice = df['Close']
        high = df['High']
        low = df['Low']

        ## Get data for candlestick_ochl() ##
        x = 0
        y = len(date)
        data = []
        while x < y:
            append_me = date[x], openprice[x], closeprice[x], high[x], low[x]
            data.append(append_me)
            x += 1
        
        ## Plot Candlesticks ##
        fig = pyplot.figure(figsize=(10, 7))
        ax1 = pyplot.subplot()
        candlestick_ochl(ax1, data, width=np.timedelta64(12, 'h'), colorup='green', colordown='red', alpha=0.75)
        # pyplot.plot(date, high, 'go', date, low, 'ro')
        pyplot.yticks(np.arange(min(closeprice)-(0.1*min(closeprice)), max(closeprice)+(0.1*max(closeprice)),  50))
        pyplot.ylabel('Price')
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d-%Y'))
        pyplot.xticks(rotation=45)
        pyplot.xlabel('Date')
        pyplot.show()
        
        
tesla = Stock('TSLA')
data = tesla.getData()
tesla.getGraph(data)
