import pandas, json, numpy
from matplotlib import pyplot
import pandas_datareader
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

tesla = Stock('TSLA')

# print(tesla.getData())
# ([x], [y])
t = numpy.arange(0., 5., 0.2)
pyplot.plot(t, 'ro')
pyplot.show()
    


