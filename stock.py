from alpha_vantage.timeseries import TimeSeries
import telegram
import pandas as pd
import time
import pytz
from datetime import datetime, timezone
from alpha_vantage.techindicators import TechIndicators



def notify():
 status = bot.send_message(chat_id="@smacrossoverchannel", text=msg)

def calculate():
 flag=1
 tz = pytz.timezone('Asia/Calcutta')
 ist = datetime.now(tz).strftime("%H:%M:%S")
 ist = datetime.strptime(ist,"%H:%M:%S")
 if ist>datetime.strptime('09:05:00',"%H:%M:%S") and ist<datetime.strptime('15:30:00',"%H:%M:%S"):
  flag=1
 else: 
  flag=0
 return flag

api_key = '4EWAGGPCYI53F188'
symbol = 'NSE:FEDERALBNK'
telegram_api = '1090803462:AAE5X2H-ojW3gxIji-1A7TaStbXKAavy_nM'
bot = telegram.Bot(token=telegram_api)
msg = 'cross over alert for symbol: {}'.format(symbol)

ts = TimeSeries(key=api_key,output_format='pandas')
ti = TechIndicators(key=api_key,output_format='pandas')


while True:
 if calculate():
  start_time = time.time()
  print('program started')
  data,meta_data = ts.get_intraday(symbol=symbol,interval='1min',outputsize='compact')
  data = data.sort_index()
  data['LMA']=data['4. close'].rolling(window=21).mean()
  data['SMA']=data['4. close'].rolling(window=9).mean()

  data['psma']=data['SMA'].shift(1)
  data['plma']=data['LMA'].shift(1)

  print(data.tail())
#loc=((data['SMA']>data['LMA'])&(data['psma']<data['plma'])|(data['SMA']<data['LMA'])&(data['psma']>data['plma']))

  if (((data['SMA'][-1]>data['LMA'][-1])and(data['psma'][-1]<data['plma'][-1])) or ((data['SMA'][-1]<data['LMA'][-1])and(data['psma'][-1]>data['plma'][-1]))) or (((data['SMA'][-2]>data['LMA'][-2])and(data['psma'][-2]<data['plma'][-2])) or ((data['SMA'][-2]<data['LMA'][-2])and(data['psma'][-2]>data['plma'][-2]))) :
   msg = msg + '\n\n{}'.format(data[-2:])
   notify()
   msg = 'cross over alert for symbol: {}'.format(symbol)
   print("--- %s seconds ---" % (time.time() - start_time))

 else:
  start_time = time.time()
  print('cannot start as stock market is closed')
  print("--- %s seconds ---" % (time.time() - start_time))
 time.sleep(60)
  
#data.to_excel('out.xlsx')

"""data['sma'] = data['4. close'].rolling(window=6).mean()
data['lma'] = data['4. close'].rolling(window=14).mean()
data.to_excel('out.xlsx')
fig,ax1 = plt.subplots() 
ax1.plot(data['4. close'][-360:],'b')
ax1.plot(data['LMA'][-360:],'r')
ax1.plot(data['SMA'][-360:],'g')
plt.show()"""
