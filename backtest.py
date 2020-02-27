from alpha_vantage.timeseries import TimeSeries
import telegram
import pandas as pd
import time
import pytz
from datetime import datetime, timezone
from alpha_vantage.techindicators import TechIndicators
import pandas_ta as ta

#variables required
api_key = '4EWAGGPCYI53F188'
symbol = 'NSE:FEDERALBNK'
ts = TimeSeries(key=api_key,output_format='pandas')

def get_data():
 data,meta_data = ts.get_intraday(symbol=symbol,interval='1min',outputsize='compact')
 data = data.sort_index()
 return data,meta_data

def add_sma_crossover():
 data['LMA']=ta.sma(data['4. close'],21)
 data['SMA']=ta.sma(data['4. close'],9)
 data['psma']=data['SMA'].shift(1)
 data['plma']=data['LMA'].shift(1)
 #if (((data['SMA'][-1]>data['LMA'][-1])and(data['psma'][-1]<data['plma'][-1])) or ((data['SMA'][-1]<data['LMA'][-1])and(data['psma'][-1]>data['plma'][-1]))) or (((data['SMA'][-2]>data['LMA'][-2])and(data['psma'][-2]<data['plma'][-2])) or ((data['SMA'][-2]<data['LMA'][-2])and(data['psma'][-2]>data['plma'][-2]))) :
 data['buy']=(data['SMA']>data['LMA'])&(data['psma']<data['plma'])
 data['sell']=(data['SMA']<data['LMA'])&(data['psma']>data['plma'])
def add_mfi():
 data['MSI']=ta.mfi(data['2. high'],data['3. low'],data['4. close'],data['5. volume'])
def add_adx():
 df=ta.adx(data['2. high'],data['3. low'],data['4. close'])
 data['ADX']=df['ADX_14']
 data['DMP']=df['DMP_14']
 data['DMN']=df['DMN_14']
def add_rsi():
 data['RSI']=ta.rsi(data['4. close'])
def test(d):
 pb=-1
 investment = 15000
 balance = 15000
 profit = 0
 stocks=0
 price = 0
 print('----------------backtest started----------------------------')
 for i in range(0,len(d)):
  if d['buy'][i]:
   if balance>= d['4. close'][i]:
    stocks =stocks+(balance//d['4. close'][i])
    if stocks>=1:
     price = stocks*d['4. close'][i]
     if balance>=price:
      balance=balance-price
      pb=i
      print('=>buy:\n{3}\nquantity:{0} price:{1} balance:{2}------------------------'.format(stocks,price,balance,d.iloc[[i]]))
	  
  elif d['sell'][i]:
   if stocks>=1:# and d['4. close'][i]>d['4. close'][pb]
    price = stocks*d['4. close'][i]
    balance=balance+price-20
    print('=>sell:\n{3}\n-----------quantity:{0} price:{1} balance:{2}----------'.format(stocks,price,balance,d.iloc[[i]]))
    stocks=0
 profit = balance-investment
 print(len(d))
 return profit

#program starts
start_time = time.time()
print('program started')
#getting data
data,meta_data = get_data()
#add sma crossover datas
add_sma_crossover()
add_adx()
add_mfi()
add_rsi()
data.to_excel('out.xlsx')
  #if (((data['SMA'][-1]>data['LMA'][-1])and(data['psma'][-1]<data['plma'][-1])) or ((data['SMA'][-1]<data['LMA'][-1])and(data['psma'][-1]>data['plma'][-1]))) or (((data['SMA'][-2]>data['LMA'][-2])and(data['psma'][-2]<data['plma'][-2])) or ((data['SMA'][-2]<data['LMA'][-2])and(data['psma'][-2]>data['plma'][-2]))) :
print("-------------------------------------")
print(data.tail())
print('profit:'+str(test(data)))
data.to_excel('out.xlsx')
print("--- %s seconds ---" % (time.time() - start_time))

 

#help(ta.adx)


  


"""data['sma'] = data['4. close'].rolling(window=6).mean()
data['lma'] = data['4. close'].rolling(window=14).mean()
data.to_excel('out.xlsx')
fig,ax1 = plt.subplots() 
ax1.plot(data['4. close'][-360:],'b')
ax1.plot(data['LMA'][-360:],'r')
ax1.plot(data['SMA'][-360:],'g')
plt.show()"""
"""
data['LMA']=data['4. close'].rolling(window=21).mean()
data['SMA']=data['4. close'].rolling(window=5).mean()
data['psma']=data['SMA'].shift(1)
data['plma']=data['LMA'].shift(1)"""