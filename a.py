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
	return df1.dropna()

def ploting(df):
    #df = df/df.iloc[0,:]
    ax=df.plot(title='Stock Close Price')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    plt.show()   
    
def plot_rolling_mean(df,sym):
    com=a[sym]
    com_rm=com.rolling(20).mean()
    ax =com.plot(title=f"{sym} Sock Price")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    com_rm.plot()    



def daily_return(df):
    df=((df.shift(1)/df)-1)*100
    return df
def cumulative_return(df):
    df=((df/df.iloc[0,:])-1)*100
    return df

    
def global_stats(df):
    mean = df.mean()
    median = df.median()
    standard_d= df.std()
    
    print("Mean of the stocks \n"+ str(mean))
    
    print("Median of the stocks \n"+ str(median))
    
    print("Standard dev of the stocks \n"+ str(standard_d))
   

ticker = ['AAPL','MSFT','CSCO','GOOGL']
start='2010-01-22'
end='2010-05-22'  
    
a = get_stock_data(start,end,ticker)
ploting(a)
global_stats(a)
plot_rolling_mean(a,ticker[1])

b=daily_return(a)
ploting(b)

c=cumulative_return(a)
ploting(c)