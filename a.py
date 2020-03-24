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


    
def rolling_mean(df):
    
    com_rm=df.rolling(20).mean()
    return com_rm  
def rolling_std(df):
    
    com_rstd=df.rolling(20).std()
    return com_rstd 



def daily_return(df):
    df=((df.shift(1)/df)-1)*100
   
    return df
def cumulative_return(df):
    df=((df/df.iloc[0])-1)*100
    
    return df

    
def global_stats(df):
    mean = df.mean()
    median = df.median()
    standard_d= df.std()
    
    print("Mean of the stocks \n"+ str(mean))
    
    print("Median of the stocks \n"+ str(median))
    
    print("Standard dev of the stocks \n"+ str(standard_d))
   



        
def plotting_whole(df,l):
    for com in l:
        x= df[com]
        
        fig,ax = plt.subplots(2,2)
        
        #Plot stock close price
        ax[0,0].plot(x.index,x.values)
        ax[0,0].set_xlabel("Date")
        ax[0,0].set_ylabel("Price")
        ax[0,0].set_title(f"Stock Price {com}")
        
        
        
        #Plot rolling mean
        ax[0,1].plot(rolling_mean(x).index,rolling_mean(x).values)
        ax[0,1].set_xlabel("Date")
        ax[0,1].set_ylabel("Price")
        ax[0,1].set_title(f"Rolling Mean {com}")
        
        
        #Plot daily return
        ax[1,0].plot(daily_return(x).index,daily_return(x).values)
        ax[1,0].set_xlabel("Date")
        ax[1,0].set_ylabel("Percentage")
        ax[1,0].set_title(f"Daily Return {com}")
        
        #Plot cumulative return
        ax[1,1].plot(cumulative_return(x).index,cumulative_return(x).values)
        ax[1,1].set_xlabel("Date")
        ax[1,1].set_ylabel("Percentage")
        ax[1,1].set_title(f"Cumulative Return {com}")
        plt.show()
        
        plt.savefig(f'{com}.png')
    
        #Plot Bolinger Bands
        bolinger_band(x)
        
        #PLot daily return histogram
        p = daily_return(x)
        h=p.hist(bins=20)
        h.axvline(p.mean(),color='w',linestyle='dashed',linewidth=2)
        h.axvline(p.std(),color='r',linestyle='dashed',linewidth=2)
        h.axvline(-p.std(),color='r',linestyle='dashed',linewidth=2)
        plt.show()
        

        
def bolinger_band(df):
    
    x = df
   
    upper_rolling=rolling_mean(x)+(rolling_std(x)*2)
    lower_rolling=rolling_mean(x)-(rolling_std(x)*2)
    
    x.plot()
    rolling_mean(x).plot()
    upper_rolling.plot()
    lower_rolling.plot()
    plt.show()


ticker = ['CSCO','GOOGL']

start='2010-01-25'
end='2010-12-25'  
    
a = get_stock_data(start,end,ticker)

plotting_whole(a,ticker)

plt.scatter(daily_return(a['GOOGL']),daily_return(a['CSCO']))
plt.show()


