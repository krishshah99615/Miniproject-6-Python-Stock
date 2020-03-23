import pandas as pd 
from pandas_datareader import data 
import matplotlib.pyplot as plt 


def get_stock_data(start,end,loc): 

	date_index = pd.date_range(start,end)
	df1=pd.DataFrame(index=date_index)
	for sym in loc:
		df=data.DataReader(sym,'yahoo',start,end)
		df1=df1.join(df['Close'])
		df1.rename(columns={'Close':f'{sym}'},inplace=True)
	return df1
def ploting(df):
    df = df/df.iloc[0,:]
    ax=df.plot(title='Stock Close Price')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    plt.show()    


ticker = ['AAPL','MSFT','CSCO','GOOGL']
start='2010-01-22'
end='2015-01-22'  
    
a = get_stock_data(start,end,ticker)
ploting(a)