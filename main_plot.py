from coins.coininfo import CoinInfo
from coins.coinprice import CoinPrice
from twitter.statistics import Statistics
from twitter.tweetio import TweetIO
from twitter.sentiment import SentimentAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import datetime as dt



print('Main starts plotting')
cinfo=CoinInfo()
coinlist=cinfo.list_coins('./data/altcoin-1hour')

## choosing first one: neo
coin=coinlist[18]
coin.ico="2016-05-01"

tweetio=TweetIO()
coin.read_from_storeage("prepare2")





df_ohlc= coin.pricehourly.copy()
df_ohlc=df_ohlc[['datetime','open','high','low','close']]
#df_ohlc=df_ohlc.drop(['time1','volumefrom','volumeto'],axis=1)
fromperiod='2017-08-01'
toperiod='2017-08-25'
df_ohlc=df_ohlc[(df_ohlc['datetime'] >= fromperiod) & (df_ohlc['datetime'] < toperiod)]

coin.gtdf['max_datetime_epoch']=coin.gtdf['max_datetime']
coin.gtdf['max_datetime']=pd.to_datetime(coin.gtdf['max_datetime'].astype('int')*int(1e6))
coin.grtdf['max_datetime_epoch']=coin.grtdf['max_datetime']
coin.grtdf['max_datetime']=pd.to_datetime(coin.grtdf['max_datetime'].astype('int')*int(1e6))


gcoin_tweet_tmp=coin.gtdf.copy()
gcoin_tweet_tmp=gcoin_tweet_tmp[(gcoin_tweet_tmp['max_datetime'] > fromperiod) & (gcoin_tweet_tmp['max_datetime'] < toperiod)]

grtdf_tmp=coin.grtdf.copy()
grtdf_tmp=grtdf_tmp[(grtdf_tmp['max_datetime'] > fromperiod) & (grtdf_tmp['max_datetime'] < toperiod)]
#buysig_tmp=buysig.copy()
#buysig_tmp=buysig_tmp[(buysig_tmp['max_datetime_y'] > fromperiod) & (buysig_tmp['max_datetime_y'] < toperiod)]

#Reset the index to remove Date column from index
#df_ohlc = df_ohlc.reset_index()

#Naming columns
#df_ohlc.columns = ["Date","Open","High",'Low',"Close"]

#Converting dates column to float values
df_ohlc['datetime'] = df_ohlc['datetime'].map(mdates.date2num)

#Making plot
fig = plt.figure(figsize=(10,6))
#ax1 = plt.subplot2grid((9,1), (0,0), rowspan=6, colspan=1)

ax1 = plt.subplot()

#Converts raw mdate numbers to dates
ax1.xaxis_date()
plt.xlabel("Date")
plt.ylabel("Price BTC")
#print(df_ohlc)

#Making candlestick plot
candlewidth=0.04
(lines, patches)=candlestick_ohlc(ax1,df_ohlc.values,width=candlewidth, colorup='g', colordown='k',alpha=0.75)
#plt.xticks(rotation=90)


for pat in patches:
    pat.xy=(pat.xy[0]+candlewidth/2,pat.xy[1])
for line in lines:
    line.set_xdata((line.get_xdata()[0]+candlewidth/2,line.get_xdata()[1]+candlewidth/2))
    #pat.x=(pat.xy[0]+candlewidth/2,pat.xy[1])

ax2 = ax1.twinx()

#ax2.plot(coin_tweet_tmp['timestamp'],coin_tweet_tmp['score'], 'o',alpha=0.5)
ax2.bar(gcoin_tweet_tmp['max_datetime'], gcoin_tweet_tmp['follower_count'], width=0.01, align='center',alpha=0.5)
ax2.bar(grtdf_tmp['max_datetime'], grtdf_tmp['retweeter_followers'], width=0.01, align='center',alpha=0.5)
#ax2.bar(buysig_tmp['max_datetime_y'],100000, width=0.1, align='center',alpha=0.5,color='g')

#plt.ylim(ymax=1000)
plt.ylabel("nr. of followers could see")


plt.title(coin.name+" 1 hour candles")
#plt.legend(['buysignal','orig tweets\' followers #OmiseGo','retweets\' followers #OmiseGo'])

fig.subplots_adjust(bottom=0.2)
plt.show()

