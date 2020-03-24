import pandas as pd 
from pandas_datareader import data 
import matplotlib.pyplot as plt 

#Download all the stock data
def stock_data(start,end,loc): 

	date_index = pd.date_range(start,end)
	df1=pd.DataFrame(index=date_index)
	for sym in loc:
		df=data.DataReader(sym,'yahoo',start,end)
		df1=df1.join(df['Close'])
		df1.rename(columns={'Close':f'{sym}'},inplace=True)
	return df1.dropna()

#Calculate Rolling Mean
def rollingMean(df):
    
    return df.rolling(20).mean() 
#Calculate Rolling Standard deviation
def rollingStd(df):
    
    return df.rolling(20).std()
      
#Calculate Daily return
    
def dailyReturn(df):
    df=((df/df.shift(1))-1)*100
   
    return df

#Calculate Cumulative Return

def cumulativeReturn(df):
    df=((df/df.iloc[0])-1)*100
    
    return df

#Calculating bollinger bands
def bolingerBand(df):
    
    x = df
   #Calculate upper band
    upper_rolling=rollingMean(x)+(rollingStd(x)*2)
    
    #Calculate lower band
    lower_rolling=rollingMean(x)-(rollingStd(x)*2)
    
    
    return upper_rolling,lower_rolling

def plotting_whole(df,l):
    for com in l:
        x= df[com]
        u,l=bolingerBand(x)
        dr = dailyReturn(x)
        
        fig,ax = plt.subplots(6,figsize=(20,20))
    
        
        #Plot stock close price
        ax[0].plot(x.index,x.values)
        ax[0].set_xlabel("Date")
        ax[0].set_ylabel("Price")
        ax[0].set_title(f"Stock Price {com}")
        
        
        
        #Plot rolling mean
        ax[1].plot(rollingMean(x).index,rollingMean(x).values)
        ax[1].set_xlabel("Date")
        ax[1].set_ylabel("Price")
        ax[1].set_title(f"Rolling Mean {com}")
        
        
        #Plot daily return
        ax[2].plot(dailyReturn(x).index,dailyReturn(x).values)
        ax[2].set_xlabel("Date")
        ax[2].set_ylabel("Percentage")
        ax[2].set_title(f"Daily Return {com}")
        
        #Plot cumulative return
        ax[3].plot(cumulativeReturn(x).index,cumulativeReturn(x).values)
        ax[3].set_xlabel("Date")
        ax[3].set_ylabel("Percentage")
        ax[3].set_title(f"Cumulative Return {com}")
        
        #Plot Bollinger band
        ax[4].plot(rollingMean(x).index,rollingMean(x).values)
        ax[4].plot(u.index,u.values)
        ax[4].plot(l.index,l.values)
        ax[4].set_xlabel("Date")
        ax[4].set_ylabel("Price")
        ax[4].set_title(f"Bollinger Bands  {com}")
        
        #Plot histogram of daily return
        ax[5] = dr.hist(bins=20)
        ax[5].axvline(dr.mean(),color='w',linestyle='dashed',linewidth=2)
        ax[5].axvline(dr.std(),color='r',linestyle='dashed',linewidth=2)
        ax[5].axvline(-dr.std(),color='r',linestyle='dashed',linewidth=2)
        
        plt.show()
        
        plt.savefig(f'{com}.png')
    
ticker = ['CSCO','GOOGL']

start='2010-01-25'
end='2010-12-25'  
    
a = stock_data(start,end,ticker)

plotting_whole(a,ticker)
        
       
        