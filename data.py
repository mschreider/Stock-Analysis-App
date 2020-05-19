import pandas, json
import numpy as np
from matplotlib import pyplot
from mpl_finance import candlestick_ochl
import pandas_datareader.data as data
import datetime

class Stock():
    def __init__(self, ticker):
        self.ticker = ticker
    
    def getData(self):
        start = datetime.date.today() - datetime.timedelta(days=90)
        end = datetime.date.today()
            
        # dataframe object
        df = data.DataReader(name=self.ticker, data_source="yahoo",start=start,end=end) 
        return df

def inc_dec(c, o):
        if c > o:
            value = "Increase"
        elif c < o:
            value = "Decrease"
        else:
            value = "Equal"
        return value

tesla = Stock('TSLA')
stockData = tesla.getData()
stockData["Status"] = [inc_dec(c, o) for c, o in zip(stockData.Close, stockData.Open)]
stockData["Middle"] = (stockData.Open + stockData.Close) / 2
stockData["Daily Change"] = abs(stockData.Close - stockData.Open)
print(stockData)
date = stockData.index.values
open = stockData['Open']
close = stockData['Close']
high = stockData['High']
low = stockData['Low']


# ([x], [y])
# t = numpy.arange(0., 5., 0.2)
candlestick_ochl(pyplot, date, open, close, high, low, width=0.6, colorup='green', colordown='red', alpha=0.75)
# pyplot.plot(date, high, 'g-', date, low, 'r-')
# pyplot.yticks(np.arange(min(close)-(0.1*min(close)), max(close)+(0.1*max(close)),  50))
# pyplot.xticks(rotation=45)
# pyplot.xlabel('Date')
# pyplot.ylabel('Price')
pyplot.show()



