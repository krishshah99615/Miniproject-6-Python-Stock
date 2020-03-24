import pandas as pd 
from pandas_datareader import data 
import matplotlib.pyplot as plt 
import numpy as np
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

def alfaBeta(df,l,market):
    #df is whole stock data, l is list of company to find alfa beta value wrt to market
    for com in l:
        
        #calulate daily return
        x = dailyReturn(df[market]).dropna()
        y = dailyReturn(df[com]).dropna()
        
        #Calculate beta alfa values
        beta,alfa=np.polyfit(x,y,1)
        
        #Plot the values and line
        dailyReturn(df).plot(kind='scatter',x=market,y=com)
        plt.plot(x,beta*x+alfa,color='r')
        print(f"Alfa Value for {com} is {alfa}  wrt to {market}")
        print(f"Beta Value for {com} is {alfa}  wrt to {market}")
        
    print("Correlation between each value and market is \n")
    print(df.corr(method='pearson'))


def portfolio(loc,start,end,alloc):
    
    
    d = stock_data(start,end,loc) 
    
    norm_d=d/d.iloc[0]
    alloc_d=norm_d.mul(alloc,axis='columns')
    
    alloc_d.iloc[1:]= alloc_d.iloc[1:]*alloc_d.iloc[0]
    
    pos_d=alloc_d
    
    port_val = pos_d.sum(axis=1)
    
    
    
    return port_val
    
    
#Plotting all metrics
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
        
        
    
ticker = ['GOOGL','CSCO','MSFT','AAPL']
alloc=[0.4,0.4,0.1,0.1]
start='2010-01-25'
end='2010-12-25'  
    
a = stock_data(start,end,ticker)

plotting_whole(a,ticker) 

  
alfaBeta(a,ticker[1:],'GOOGL')



port_val = portfolio(ticker,start,end,alloc)
