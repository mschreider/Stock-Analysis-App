import pandas, json
import numpy as np
from matplotlib import pyplot, axes
from mplfinance.original_flavor import candlestick_ochl
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
        df.index.to_pydatetime()
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
date = stockData.index.values
openprice = stockData['Open']
closeprice = stockData['Close']
high = stockData['High']
low = stockData['Low']

x = 0
y = len(date)
data = []
while x < y:
    append_me = date[x], openprice[x], closeprice[x], high[x], low[x]
    data.append(append_me)
    print(date[x])
    x += 1

myplot = pyplot.figure()
ax1 = pyplot.subplot()
# ([x], [y])
# t = numpy.arange(0., 5., 0.2)
candlestick_ochl(ax1, data, width=np.timedelta64(12, 'h'), colorup='green', colordown='red', alpha=0.75)
# pyplot.plot(date, high, 'g-', date, low, 'r-')
pyplot.yticks(np.arange(min(closeprice)-(0.1*min(closeprice)), max(closeprice)+(0.1*max(closeprice)),  50))
pyplot.xticks(rotation=45)
pyplot.xlabel('Date')
pyplot.ylabel('Price')
pyplot.show()



