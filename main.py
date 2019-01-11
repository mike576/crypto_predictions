#!flask/bin/python
import time
from datetime import datetime
# import datetime
from datetime import timedelta, date

import pandas as pd

from flask import Flask, jsonify
from flask import request

from coins.coininfo import CoinInfo
from twitter.tweepy import TwitterApi
from twitter.tweetcollector import TweetCollector
from twitter.tweetio import TweetIO
from coins.binance import BinanceApi
from twitter.sentiment import SentimentAnalyzer

from coins.coin import Coin
from coins.dateutil import DateUtil
from train.cointrain import CoinTrain

from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import keras.backend as K
from db.mysqldb import dbconn
from train.prediction import Prediction


app = Flask(__name__)

coinlist = ['OMGBTC', 'GASBTC', 'NEOBTC']

predictions = []

PHASE = "rt"







COLS = ['hour', 'open', 'high', 'low', 'close', 'volumefrom', 'volumeto',
        'high_raised', 'low_raised', 'close_raised', 'retweeter_followers',
        'retweet_count', 'sum_posmulrfollower', 'sum_negmulrfollower',
        'sum_neumulrfollower', 'sum_compmulrfollower', 'follower_count',
        'tweet_count', 'sum_posmulfollower', 'sum_negmulfollower',
        'sum_neumulfollower', 'sum_compmulfollower', 'change1', 'change2',
        'change3', 'change6', 'change1_12', 'asia_market', 'eu_market',
        'us_market']
shouldbe_cols = ['high_raised', 'low_raised', 'close_raised', 'retweeter_followers',
                 'retweet_count', 'sum_posmulrfollower', 'sum_negmulrfollower',
                 'sum_neumulrfollower', 'sum_compmulrfollower', 'follower_count',
                 'tweet_count', 'sum_posmulfollower', 'sum_negmulfollower',
                 'sum_neumulfollower', 'sum_compmulfollower', '24 sd', 'boll_up-close',
                 'boll_down-close', 'boll_up_close_ratio', 'boll_down_close_ratio',
                 'boll_up_close_ratio_pow3', 'boll_down_close_ratio_pow3', 'rsi_12',
                 'rsi_6', 'c_o_change', 'h_o_change', 'l_o_change', 'c_o_change1',
                 'h_o_change1', 'l_o_change1', 'o_change1', 'o_change2', 'o_change3',
                 'o_change4', 'o_change5', 'o_change6', 'o_change1_3', 'o_change1_12',
                 'vf_change1', 'vt_change1', 'rsi_12_change1', 'rsi_12_change2',
                 'rsi_6_change1', 'rsi_6_change2', 'rsi_6_12_ratio']


def generate_coins(specific_hour):
    coins=[]

    #OMG
    coin = Coin()
    coin.name = 'omg'
    coin.treshold = 0.81
    one_day_before = specific_hour + timedelta(days=-1)
    coin.loadtime = one_day_before.strftime("%Y-%m-%d")
    coin.hashtags = ['omg', 'omisego']
    coin.target=1.7
    coin.stoploss=coin.target/(-0.5)
    coin.timelimit=3
    coin.modelfile='omg/found_omg_bsig34.0_prec0.7083333333333334_tre64_aimr1.7_decr-0' \
                   '.5_offs3_actmet_tanh_keras_model.h5'
    coin.scalerfile='omg/found_omg_bsig34.0_prec0.7083333333333334_tre64_aimr1.7_decr-0.5_offs3_actmet_tanh_scaler.pkl'
    coins.append(coin)

    #NEO
    coin = Coin()
    coin.name = 'neo'
    coin.treshold = 0.72
    one_day_before = specific_hour + timedelta(days=-1)
    coin.loadtime = one_day_before.strftime("%Y-%m-%d")
    coin.hashtags = ['neo']
    coin.target=1.7
    coin.stoploss=coin.target/(-0.667)
    coin.timelimit=3
    coin.modelfile='neo/found_neo_bsig18.0_prec0.782608695652174_tre72_aimr1.7_decr-0.667_offs4_actmet_relu_keras_model.h5'
    coin.scalerfile='neo/found_neo_bsig18.0_prec0.782608695652174_tre72_aimr1.7_decr-0.667_offs4_actmet_relu_scaler.pkl'
    coins.append(coin)

    #XVG
    coin = Coin()
    coin.name = 'xvg'
    coin.treshold = 0.99
    one_day_before = specific_hour + timedelta(days=-1)
    coin.loadtime = one_day_before.strftime("%Y-%m-%d")
    coin.hashtags = ['xvg','verge']
    #coins.append(coin)

    #LSK
    coin = Coin()
    coin.name = 'lsk'
    coin.treshold = 0.61
    one_day_before = specific_hour + timedelta(days=-1)
    coin.loadtime = one_day_before.strftime("%Y-%m-%d")
    coin.hashtags = ['lsk','lisk']
    #coins.append(coin)

    #ADA
    coin = Coin()
    coin.name = 'ada'
    coin.treshold = 0.56
    one_day_before = specific_hour + timedelta(days=-1)
    coin.loadtime = one_day_before.strftime("%Y-%m-%d")
    coin.hashtags = ['ada','cardano']
    #coins.append(coin)

    #GNT
    coin = Coin()
    coin.name = 'gnt'
    coin.treshold = 0.55  #buysig 3, at prec 1.0!
    one_day_before = specific_hour + timedelta(days=-1)
    coin.loadtime = one_day_before.strftime("%Y-%m-%d")
    coin.hashtags = ['gnt','golem']
    #coins.append(coin)

    return coins


@app.route('/signal/predictcoins/backfill', methods=['GET'])
def fill_past_signals():

    predictions = []
    coins=generate_coins(datetime.now())

    coininfo=CoinInfo()
    du=DateUtil()
    for coin in coins:

        earliest_date=dbconn.get_earliest_date_in_db(coin)
        print(coin.name,"earliest date",earliest_date)

        start_datetime=du.parse_time_string(du.round_datetime_down(earliest_date))
        last_round_hour=du.parse_time_string(du.last_round_hour())
        #adding 24 hours to have earlier data in the past for prediction
        curr_datetime=start_datetime + timedelta(hours=+24)
        while(curr_datetime<last_round_hour):
            coin.reset_data_frames()
            one_day_before = curr_datetime + timedelta(days=-1)
            coin.loadtime = one_day_before.strftime("%Y-%m-%d")

            curr_datetime = curr_datetime + timedelta(hours=+1)
            print("checking pred in DB for ",coin,"at",curr_datetime)

            tsfrom=(curr_datetime+timedelta(hours=-1)).strftime("%Y-%m-%d %H:00:00")
            tsto=curr_datetime.strftime("%Y-%m-%d %H:00:00")
            print(tsfrom,tsto)

            pred=dbconn.check_prediction_in_db(coin,tsfrom,tsto)
            print("pred:",pred)

            if pred is None:
                coininfo.do_prepare(coin,curr_datetime)
                predictions=do_predict(coin,predictions,curr_datetime)
            else:
                predictions.append(pred)

    return jsonify({'predictions': predictions})


@app.route('/signal/predictcoins/history', methods=['GET'])
def get_signal_history():

    dthour = request.args.get('datetime')
    du=DateUtil()
    specific_hour_dt=du.parse_time_string(dthour)
    predictions = []
    coins=generate_coins(specific_hour_dt)
    coininfo=CoinInfo()

    for coin in coins:

        earliest_date=dbconn.get_earliest_date_in_db(coin)
        print(coin.name,"earliest date",earliest_date)

        one_day_before = specific_hour_dt + timedelta(days=-1)
        coin.loadtime = one_day_before.strftime("%Y-%m-%d")
        print("checking pred in DB for ",coin,"at",specific_hour_dt)

        tsfrom=(specific_hour_dt+timedelta(hours=-1)).strftime("%Y-%m-%d %H:00:00")
        tsto=specific_hour_dt.strftime("%Y-%m-%d %H:00:00")
        print(tsfrom,tsto)

        pred=dbconn.check_prediction_in_db(coin,tsfrom,tsto)
        print("pred:",pred)

        if pred is None:
            coininfo.do_prepare(coin,specific_hour_dt)
            predictions=do_predict(coin,predictions,specific_hour_dt)
        else:
            predictions.append(pred)

    return jsonify({'predictions': predictions})

@app.route('/signal/predictcoins/recalculate', methods=['GET'])
def update_signal_recalculate():

    dthour = request.args.get('datetime')
    du=DateUtil()
    specific_hour_dt=du.parse_time_string(dthour)
    predictions = []
    coins=generate_coins(specific_hour_dt)
    coininfo=CoinInfo()

    for coin in coins:

        earliest_date=dbconn.get_earliest_date_in_db(coin)
        print(coin.name,"earliest date",earliest_date)

        one_day_before = specific_hour_dt + timedelta(days=-1)
        coin.loadtime = one_day_before.strftime("%Y-%m-%d")
        print("checking pred in DB for ",coin,"at",specific_hour_dt)

        tsfrom=(specific_hour_dt+timedelta(hours=-1)).strftime("%Y-%m-%d %H:00:00")
        tsto=specific_hour_dt.strftime("%Y-%m-%d %H:00:00")
        print(tsfrom,tsto)

        coininfo.do_prepare(coin,specific_hour_dt)
        predictions=do_predict(coin,predictions,specific_hour_dt)


    return jsonify({'predictions': predictions})


@app.route('/signal/predictcoins', methods=['GET'])
def get_signal():
    predictions = []
    try:

        du=DateUtil()
        last_round_hour=du.parse_time_string(du.last_round_hour())

        coins=generate_coins(last_round_hour)
        coininfo=CoinInfo()

        for coin in coins:
            pred=dbconn.check_prediction_in_db_last_hour(coin)
            if pred is None:
                coininfo.do_prepare(coin,last_round_hour)
                predictions=do_predict(coin,predictions,last_round_hour)
            else:
                predictions.append(pred)
        return jsonify({'predictions': predictions})
    except Exception as e:
        print("Exception: ",e)
        return jsonify({'exception': predictions})


def do_predict(coin,predictions,specific_hour):

    ##print(coin.gtdf.head())
    data = coin.pricehourly.copy()

    convert_hour_col(data)
    times = pd.DatetimeIndex(data['datetime'])

    cointrain = CoinTrain()
    X_gtdf = cointrain.increase_by_one_hour(coin.gtdf)
    X_grtdf = cointrain.increase_by_one_hour(coin.grtdf)
    X = data

    # not really summing
    gX = X.groupby([times.year, times.month, times.day, times.hour]).open.sum()
    gXdf = pd.DataFrame(gX)
    # not really max just copy
    gXdf['high'] = X.groupby([times.year, times.month, times.day, times.hour])['high'].max()
    gXdf['low'] = X.groupby([times.year, times.month, times.day, times.hour])['low'].max()
    gXdf['close'] = X.groupby([times.year, times.month, times.day, times.hour])['close'].max()
    gXdf['volumefrom'] = X.groupby([times.year, times.month, times.day, times.hour])['volumefrom'].max()
    gXdf['volumeto'] = X.groupby([times.year, times.month, times.day, times.hour])['volumeto'].max()
    gXdf['high_raised'] = gXdf['high'] / gXdf['open']
    gXdf['low_raised'] = gXdf['low'] / gXdf['open']
    gXdf['close_raised'] = gXdf['close'] / gXdf['open']

    print("X_grtdf")
    #print(X_grtdf)
    print("X_gtdf")
    #print(X_gtdf)
    #type(data)
    # gXdf['retweeter_followers']=coin.grtdf['retweeter_followers']
    # gXdf['retweet_count']=coin.grtdf['retweet_count']
    # data[]=coin.grtdf[]

    print("renaming cols")
    idx = gXdf.index
    gXdf.index = idx.rename(['year', 'month', 'day', 'hour'])

    print("merging data")
    gXdf = gXdf.merge(X_grtdf, how='left', left_index=True, right_index=True)
    Xdf = gXdf.merge(X_gtdf, how='left', left_index=True, right_index=True)



    data = Xdf

    data.reset_index(inplace=True)
    print("add stock features")
    cointrain.add_stock_features(data)
    print("spreadtweeteffect")
    cointrain.spreadtweeteffect(data)
    print("add_change_columns")
    cointrain.add_change_columns(data)

    print("data.fillna 0")
    data.fillna(0, inplace=True)
    print("data.drop columns ")
    data.drop(columns=['year','month','hour','open', 'high', 'low', 'close',
                   'volumefrom', 'volumeto',
                   #                   'vf_change1','vt_change1',
                   #                   'vfvt_ratio','vtvf_ratio',
                   #                    'c_o_change', 'h_o_change', 'l_o_change',
                   #        'c_o_change1', 'h_o_change1', 'l_o_change1', 'o_change1', 'o_change2',
                   #        'o_change3', 'o_change4', 'o_change5', 'o_change6', 'o_change1_3',
                   #        'o_change1_12',
                   #                     'retweeter_followers',
                   #        'retweet_count',
                   #        'sum_posmulrfollower', 'sum_negmulrfollower',
                   #        'sum_neumulrfollower', 'sum_compmulrfollower', 'follower_count',
                   #        'tweet_count',
                   #        'sum_posmulfollower', 'sum_negmulfollower',
                   #        'sum_neumulfollower', 'sum_compmulfollower',
                   'asia_market', 'eu_market', 'us_market',
                   'day','max_datetime_x','max_datetime_y'],
          inplace=True)

    #data = data[COLS]
    coin.data_to_predict=data
    print(data.tail())
    print("Checking columns:")
    print(data.columns)

    import collections
    compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

    condition=compare(data.columns,shouldbe_cols)

    #if(len(condition[condition==True])>0):#data.columns!=shouldbe_cols):
    if(condition!=True):
        print("Columns/Features are not the same as in the model, exiting")
        print("which col not equal: ",shouldbe_cols)
        print("which col not equal: ",data.columns)
        print("shouldbe_cols ")
        print(shouldbe_cols)
        print('data.columns')
        print(data.columns)
        return predictions

    print("saving to storeage... ")
    spec_hour_str = str(specific_hour.strftime("%Y-%m-%d_%H-%M-%S"))
    coin.save_to_storeage(PHASE,tmpdir='runtime/'+spec_hour_str+'/')
    print("saving is done.")

    print("doin min max scaling")
    min_max_scaler=coin.read_scaler()
    scaled_data=min_max_scaler.transform(data)
    data=pd.DataFrame(scaled_data)
    print(data.tail())

    # load json and create model
    def precision(y_true, y_pred):
        threshold=0.3
        mult=0.5/threshold
        true_positives = K.sum(K.round(K.clip(y_true * y_pred*mult, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred*mult, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision

    def recall(y_true, y_pred):
        threshold=0.3
        mult=0.5/threshold
        true_positives = K.sum(K.round(K.clip(y_true * y_pred*mult, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall
    #metrics=[precision,recall,'accuracy']
    metrics={"precision":precision,'recall':recall}
    print("loading model for coin:"+coin.name)
    #model = load_model("./data/altcoin-storage/"+coin.name+"_keras_model.h5",custom_objects=metrics)
    #loading once>
    p=Prediction()
    model =p.load_model(coin,metrics)

    print("doing predictions.")
    pred=model.predict(data)
    print("predictions are ready.")


    coinbinancename=coin.name.upper()+"BTC"
    chance=pred[len(pred)-1][0]

    signal=0
    treshold=coin.treshold
    if chance>treshold:
        signal=1


    #generating prediction
    print("generating prediction")
    du=DateUtil()
    specific_hour_minus_one=specific_hour+timedelta(hours=-1)
    pred=p.generate_prediction(coin,specific_hour_minus_one,specific_hour,coinbinancename,chance,treshold,signal)
    dbconn.save_predictions([pred])
    predictions.append(pred)

    return predictions


@app.route('/signal/test', methods=['GET'])
def get_tasks():
    i = 0
    predictions = []
    for coin in coinlist:
        predictions.append({'currenctpair': coinlist[i], 'chance': 0.12345678, 'signal': 0})
        i += 1
    #print(predictions)
    print("Sending test/fake predictions")
    return jsonify({'predictions': predictions})






def current_timestamp():
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
    return st


def convert_hour_col(datadf):
    datadf['hour'] = pd.to_datetime(datadf['datetime'], format='%Y-%m-%d %H:%M:%S')
    datadf['hour'] = datadf['hour'].dt.strftime(date_format='%H')


def collect_hour(inputdf):
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%H')
    inputdf['hour'] = st
    return inputdf




def collect_tweets(coin, tweetcollector):
    tweets = tweetcollector.collect_todays_tweets(coin)
    tweets = tweets.drop_duplicates('id')
    print("collected tweets: " + str(tweets['id'].count()))
    tweets.reset_index(inplace=True)
    coin.tweets = tweets
    return tweets


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
