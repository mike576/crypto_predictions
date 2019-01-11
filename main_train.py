from coins.coininfo import CoinInfo
from coins.coin import Coin
from train.cointrain import CoinTrain
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
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM,Conv1D,MaxPooling1D
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from sklearn.model_selection import train_test_split
import keras.backend as K



print('Main starts plotting')

pd.set_option("display.max_rows",100)
pd.set_option("display.max_columns",100)

cinfo=CoinInfo()
#coinlist=cinfo.list_coins('./data/altcoin-1hour')

## choosing coin
coin=Coin()
coin.path="./data/altcoin-1hour/neo.csv"
coin.name="neo"
coin.ico="2017-05-01"



tweetio=TweetIO()
coin.read_from_storeage("prepare2")

#print(coin.pricehourly.head())


cointrain=CoinTrain()
X=cointrain.create_buy_sig(coin,aimraise=10,declinelimit=-5,offset=12)
X_gtdf=cointrain.increase_by_one_hour(coin.gtdf)
X_grtdf=cointrain.increase_by_one_hour(coin.grtdf)


#Converting X to the same multi index type
times = pd.DatetimeIndex(X.index)

# not really summing
gX=X.groupby([times.year, times.month, times.day,times.hour]).open.sum()
gXdf=pd.DataFrame(gX)
# not really max just copy
gXdf['buysig']=X.groupby([times.year, times.month, times.day,times.hour])['buysig'].max()
gXdf['high']=X.groupby([times.year, times.month, times.day,times.hour])['high'].max()
gXdf['low']=X.groupby([times.year, times.month, times.day,times.hour])['low'].max()
gXdf['close']=X.groupby([times.year, times.month, times.day,times.hour])['close'].max()
gXdf['volumefrom']=X.groupby([times.year, times.month, times.day,times.hour])['volumefrom'].max()
gXdf['volumeto']=X.groupby([times.year, times.month, times.day,times.hour])['volumeto'].max()
gXdf['high_raised']=gXdf['high']/gXdf['open']
gXdf['low_raised']=gXdf['low']/gXdf['open']
gXdf['close_raised']=gXdf['close']/gXdf['open']
idx=gXdf.index
gXdf.index=idx.set_names(['year', 'month','day','hour'])

#print(len(gXdf))
#print("buysig NR: ")
#print(len(gXdf[gXdf['buysig']==1]))

print("gXdf, head and tail:")
#print(gXdf.head())
print(gXdf.tail())

print("X_grtdf, head and tail:")
#print(X_grtdf.head())
print(X_grtdf.tail())


print("X_gtdf, head and tail:")
#print(X_gtdf.head())
print(X_gtdf.tail())

#MERGE:

gXdf=gXdf.merge(X_grtdf,how='inner',left_index=True,right_index=True)
#print("gXdf >")
#print(gXdf)
Xdf=gXdf.merge(X_gtdf,how='inner',left_index=True,right_index=True)
print("Xdf >")
print(Xdf)

print("Len Xdf: ")
#print(len(Xdf))
print("buysig NR: ")
print(len(Xdf[Xdf['buysig']==1]))



data=Xdf.copy()
data.reset_index(inplace=True)
data.fillna(0,inplace=True)



from sklearn import preprocessing


data=Xdf.copy()
data.reset_index(inplace=True)
data['buysig'].fillna(0,inplace=True)
labels = data.pop('buysig')

#data.fillna(method='ffill',inplace=True)
data.fillna(0,inplace=True)

cointrain.spreadtweeteffect(data)

cointrain.add_change_columns(data)

data.fillna(0,inplace=True)
data.drop(columns=['year','month','open', 'high', 'low',
          'close','day','max_datetime_x','max_datetime_y'],
inplace=True)


print(len(data))
print('data.columns')
print(data.columns)
print(data)
coin.data_to_predict=data
coin.save_to_storeage('train')

#exit(1)

min_max_scaler = preprocessing.MinMaxScaler()
np_scaled = min_max_scaler.fit_transform(data)
data = pd.DataFrame(np_scaled)

coin.save_scaler(min_max_scaler)

def precision(y_true, y_pred):
    threshold=0.4
    mult=0.5/threshold
    true_positives = K.sum(K.round(K.clip(y_true * y_pred*mult, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred*mult, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def recall(y_true, y_pred):
    threshold=0.4
    mult=0.5/threshold
    true_positives = K.sum(K.round(K.clip(y_true * y_pred*mult, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

featuresize=len(data.columns)
# model = Sequential()
# model.add(Dense(120, activation='relu', input_dim=featuresize))
# model.add(Dense(120, activation='relu'))
# model.add(Dense(120, activation='relu'))
# model.add(Dense(1, activation='sigmoid'))
# model.compile(optimizer='rmsprop',
#               loss='binary_crossentropy',
#               metrics=[precision,recall,'accuracy'])
#
# #model.compile(loss='categorical_crossentropy',
# #              optimizer='adadelta',
# #              metrics=['accuracy', 'f1score', 'precision', 'recall'])
#
# # Train the model, iterating on the data in batches of 32 samples
# model.fit(data, labels, epochs=10, batch_size=32)


print("some stats: ")
print("tweet count",len(X_gtdf))
print("retweet count",len(X_grtdf))
print("price data count",len(gXdf))
print("buysig count: ",len(gXdf[gXdf['buysig']>0]))


from keras.layers import Dense, Dropout


splitpoint=int(len(data)*0.8)
print("splitpoint: ",splitpoint)
training_data = data[:splitpoint]
training_label = labels[:splitpoint]
eval_data = data[splitpoint:]
eval_label = labels[splitpoint:]

#training_data, eval_data, training_label, eval_label = train_test_split(data, labels, test_size=0.3, random_state=42)


##MLP for binary classification:

model = Sequential()
model.add(Dense(64, input_dim=featuresize, activation='relu'))
#model.add(Dense(128, activation='relu'))
#model.add(Dense(128, activation='relu'))
#model.add(Dense(64, activation='relu'))
#model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))
#model.add(Dense(8, activation='relu'))
#model.add(Dense(4, activation='relu'))
#model.add(Dense(2, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=[precision,recall,'accuracy'])

batch=8
model.fit(training_data, training_label,
          epochs=50,
          batch_size=batch)
score = model.evaluate(eval_data, eval_label, batch_size=batch)
print("SCORE: ")
print(score)

model.save("./data/altcoin-storage/"+coin.name+"_keras_model.h5")


pred=model.predict(eval_data)
result=eval_data.copy()
result['label']=eval_label
result['pred']=pred

for thresh in range(10,99,2):
    p=result[result['pred']>thresh/100]
    prec=p['label'].sum()/len(p)
    print("thresh:",thresh/100,'  precision:',prec)

p=result[result['pred']>0.7]
#p
datat=Xdf.copy()
datat=datat.reset_index()
datat.head()
buysig=datat.iloc[p.index]





df_ohlc= coin.pricehourly.copy()
df_ohlc=df_ohlc[['datetime','open','high','low','close']]
#df_ohlc=df_ohlc.drop(['time1','volumefrom','volumeto'],axis=1)
fromperiod='2017-12-01'
toperiod='2018-02-18'
df_ohlc=df_ohlc[(df_ohlc['datetime'] >= fromperiod) & (df_ohlc['datetime'] < toperiod)]

#Please check if it was needed:
print("Please check if it was NEEDED:")
#coin.gtdf['max_datetime']
#coin.gtdf['max_datetime_epoch']=coin.gtdf['max_datetime']
#coin.gtdf['max_datetime']=pd.to_datetime(coin.gtdf['max_datetime'].astype('int')*int(1e6))
#coin.grtdf['max_datetime_epoch']=coin.grtdf['max_datetime']
#coin.grtdf['max_datetime']=pd.to_datetime(coin.grtdf['max_datetime'].astype('int')*int(1e6))


gcoin_tweet_tmp=coin.gtdf.copy()
gcoin_tweet_tmp=gcoin_tweet_tmp[(gcoin_tweet_tmp['max_datetime'] > fromperiod) & (gcoin_tweet_tmp['max_datetime'] < toperiod)]

grtdf_tmp=coin.grtdf.copy()
grtdf_tmp=grtdf_tmp[(grtdf_tmp['max_datetime'] > fromperiod) & (grtdf_tmp['max_datetime'] < toperiod)]
buysig_tmp=buysig.copy()
buysig_tmp=buysig_tmp[(buysig_tmp['max_datetime_y'] > fromperiod) & (buysig_tmp['max_datetime_y'] < toperiod)]

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

print(buysig_tmp.columns)
print(buysig_tmp)
#ax2.plot(coin_tweet_tmp['timestamp'],coin_tweet_tmp['score'], 'o',alpha=0.5)
if(len(buysig_tmp)>0):
    ax2.bar(buysig_tmp['max_datetime_y'],10000, width=0.1, align='center',alpha=0.5,color='g')
ax3 = ax1.twinx()
ax3.bar(gcoin_tweet_tmp['max_datetime'], gcoin_tweet_tmp['follower_count'], width=0.01, align='center',alpha=0.5)
ax3.bar(grtdf_tmp['max_datetime'], grtdf_tmp['retweeter_followers'], width=0.01, align='center',alpha=0.5)

print("gcoin_tweet_tmp.head()")
print(gcoin_tweet_tmp.head())
print("grtdf_tmp.head()")
print(grtdf_tmp.head())

#plt.ylim(ymax=1000)
plt.ylabel("nr. of followers could see")


plt.title(coin.name+" 1 hour candles")
#plt.legend(['buysignal','orig tweets\' followers #OmiseGo','retweets\' followers #OmiseGo'])

fig.subplots_adjust(bottom=0.2)
plt.savefig(coin.name+'-'+fromperiod)
plt.show()







