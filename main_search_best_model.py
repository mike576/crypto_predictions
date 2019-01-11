from coins.coininfo import CoinInfo
from coins.coin import Coin
from train.cointrain import CoinTrain
from coins.coinprice import CoinPrice
from twitter.statistics import Statistics
from twitter.sentiment import SentimentAnalyzer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM,Conv1D,MaxPooling1D
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from sklearn.model_selection import train_test_split
import keras.backend as K
import math
import os
from datetime import datetime


print('Main starts searching for best model')

pd.set_option("display.max_rows",100)
pd.set_option("display.max_columns",100)

cinfo=CoinInfo()
#coinlist=cinfo.list_coins('./data/altcoin-1hour')

## choosing coin
coin=Coin()
#coin.path="./data/altcoin-1hour/neo.csv"
#coin.name="neo"
#coin.ico="2017-05-01"
coin.path="./data/altcoin-1hour/omg.csv"
coin.name="omg"
coin.ico="2017-09-01"

starttime=datetime.now()
print(str(starttime))



coin.read_from_storeage("prepare2")

print(coin.pricehourly.head())
possibleraise=[1.5,1.1]
possibledeclineratio=[-0.5,-0.667]
possibleoffset=[3,4]
countphase=0




for declineratio in possibledeclineratio:
    for raisei in possibleraise:
        for offseti in possibleoffset:
            progress=countphase/(len(possibleraise)*len(possibledeclineratio)*len(possibleoffset))*100

            print("STARTING raise: ",raisei," decline ratio: ",declineratio," offseti: ",offseti," progress: ",progress,"%")
            countphase+=1

            cointrain=CoinTrain()
            X=cointrain.create_buy_sig(coin,aimraise=raisei,declinelimit=raisei/(declineratio),offset=offseti)
            print("cant decide buy signals> ",str(len(X[X['buysig']==0])))
            X_gtdf=cointrain.increase_by_one_hour(coin.gtdf)
            X_grtdf=cointrain.increase_by_one_hour(coin.grtdf)

            Xdf,gXdf=cointrain.create_Xdf(X,X_grtdf,X_gtdf)

            ##adding extra features, removing cols, filling 0.

            # data=Xdf.copy()
            # data.reset_index(inplace=True)
            # data.fillna(0,inplace=True)

            from sklearn import preprocessing

            data=Xdf.copy()
            data.reset_index(inplace=True)
            data['buysig'].fillna(0,inplace=True)
            labels = data.pop('buysig')

            #data.fillna(method='ffill',inplace=True)

            data.fillna(0,inplace=True)

            cointrain.add_stock_features(data)

            cointrain.spreadtweeteffect(data)

            cointrain.add_change_columns(data)

            data.replace([np.inf, -np.inf], np.nan,inplace=True)
            data.fillna(0,inplace=True)

            data.drop(columns=['year','month','hour','open', 'high', 'low', 'close',
                               'volumefrom', 'volumeto',
                               #                   'vf_change1','vt_change1',
                               #                   'vfvt_ratio','vtvf_ratio',
                               #                    'c_o_change', 'h_o_change', 'l_o_change',
                               #        'c_o_change1', 'h_o_change1', 'l_o_change1', 'o_change1', 'o_change2',
                               #        'o_change3', 'o_change4', 'o_change5', 'o_change6', 'o_change1_3',
                               #        'o_change1_12'
                               #                    , 'asia_market', 'eu_market', 'us_market',
                               #                     'retweeter_followers',
                               #        'retweet_count', 'sum_posmulrfollower', 'sum_negmulrfollower',
                               #        'sum_neumulrfollower', 'sum_compmulrfollower', 'follower_count',
                               #        'tweet_count', 'sum_posmulfollower', 'sum_negmulfollower',
                               #        'sum_neumulfollower', 'sum_compmulfollower',
                               'asia_market', 'eu_market', 'us_market',
                               'day','max_datetime_x','max_datetime_y'],
                      inplace=True)

            #cointrain.add_log_columns(data,strCols=True)

            print(len(data))
            print('data.columns')
            print(data.columns)
            #print(data)
            coin.data_to_predict=data
            coin.save_to_storeage('train')


            #min_max_scaler = preprocessing.MinMaxScaler()
            #np_scaled = min_max_scaler.fit_transform(data)
            #data = pd.DataFrame(np_scaled)
            #coin.save_scaler(min_max_scaler)


            #cointrain.add_square_columns(data,strCols=False)

            def precision(y_true, y_pred):
                threshold=0.55
                mult=0.5/threshold
                true_positives = K.sum(K.round(K.clip(y_true * y_pred*mult, 0, 1)))
                predicted_positives = K.sum(K.round(K.clip(y_pred*mult, 0, 1)))
                precision = true_positives / (predicted_positives + K.epsilon())
                return precision

            def recall(y_true, y_pred):
                threshold=0.55
                mult=0.5/threshold
                true_positives = K.sum(K.round(K.clip(y_true * y_pred*mult, 0, 1)))
                possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
                recall = true_positives / (possible_positives + K.epsilon())
                return recall

            #SOME STATS
            print("some stats: ")
            print("cols of data",len(data.columns))
            print("rows of data",len(data))
            print("tweet rows",len(X_gtdf))
            print("retweet rows",len(X_grtdf))
            print("price data count",len(gXdf))
            print("buysig count: ",len(gXdf[gXdf['buysig']>0]))


            #PREPARE TRAINING DATA
            splitpoint=int(len(data)*0.7)
            print("shape data: ",data.shape)
            print("splitpoint: ",splitpoint)

            training_data = data[:splitpoint]
            training_label = labels[:splitpoint]
            eval_data = data[splitpoint:]
            eval_label = labels[splitpoint:]

            print("training_data shape: ",training_data.shape)
            print("training_label shape: ",training_label.shape)
            print("training_label, buysigs> ",training_label.sum())
            print()

            print("eval_data shape: ",eval_data.shape)
            print("eval_label shape: ",eval_label.shape)
            print("eval_label, buysigs> ",eval_label.sum())

            min_max_scaler = preprocessing.MinMaxScaler()
            np_scaled = min_max_scaler.fit_transform(training_data)
            training_data = pd.DataFrame(np_scaled)

            np_scaled_eval = min_max_scaler.transform(eval_data)
            eval_data = pd.DataFrame(np_scaled_eval)
            eval_label=eval_label.reset_index()
            eval_label.drop(columns=['index'],inplace=True)



            # STARTING TRAINING
            from keras.layers import Dense, Dropout

            #training_data, eval_data, training_label, eval_label = train_test_split(data, labels, test_size=0.3, random_state=42)


            model = Sequential()


            act_method=''

            act_methods=['tanh','relu']
            for act_method in act_methods:
                max_prec=0.55
                max_buysig=2
                best_tresh=0
                min_nr_bsig=15
                found_best_model=False
                max_prec_model=Sequential()
                best_act_method=''
                best_history=False
                for i in range(4):
                    ##MLP for binary classification:
                    featuresize=len(data.columns)
                    model = Sequential()

                    model.add(Dense(16, input_dim=featuresize, activation=act_method))
                    #model.add(Dense(feature_size, activation='relu'))
                    #   model.add(Dropout(0.2, noise_shape=None, seed=None))
                    #   model.add(Dense(16, activation='sigmoid'))
                    #model.add(Dense(64, activation='relu'))
                    #model.add(Dense(32, activation='relu'))
                    #model.add(Dropout(0.1, noise_shape=None, seed=None))
                    model.add(Dense(16, activation=act_method))
                    #model.add(Dropout(0.1, noise_shape=None, seed=None))
                    model.add(Dense(16, activation=act_method))
                    #model.add(Dropout(0.1, noise_shape=None, seed=None))
                    model.add(Dense(8, activation=act_method))
                    #model.add(Dropout(0.2, noise_shape=None, seed=None))
                    #   model.add(Dense(8, activation='sigmoid'))
                    #model.add(Dense(2, activation='relu'))
                    model.add(Dense(1, activation='sigmoid'))

                    model.compile(loss='binary_crossentropy',#loss='binary_crossentropy',#loss='mean_squared_error',
                                  optimizer='sgd',
                                  metrics=[precision,recall,'accuracy'])

                    batch=128
                    history=model.fit(training_data, training_label,
                                      epochs=1500,
                                      batch_size=batch,validation_split=0.3,verbose=0)
                    score = model.evaluate(eval_data, eval_label, batch_size=batch)
                    print(i,"SCORE: ")
                    print(score)
                    pred=model.predict(eval_data)

                    result=eval_data.copy()
                    result['label']=eval_label
                    result['pred']=pred

                    for thresh in range(5,100,1):
                        p=result[result['pred']>thresh/100]
                        nrbuysig=p['label'].sum()
                        prec=nrbuysig/len(p)
                        if(prec>=max_prec and (nrbuysig>=min_nr_bsig)):
                            max_prec=prec
                            max_buysig=nrbuysig
                            max_prec_model=model
                            best_tresh=thresh
                            print("max selected with buysig> ",max_buysig," with prec> ",max_prec," at treshold:",thresh)
                            found_best_model=True
                            best_history=history
                            best_act_method=act_method

                    if(score[1]>0.66 and score[2]>0.10):
                        print("Found one above expectation")
                        #break
                if(found_best_model):
                    filepath="./data/altcoin-storage/"+ coin.name+"/"
                    if not os.path.exists(filepath):
                        os.makedirs(filepath)
                    filename_chunk = "found_" + coin.name+"_bsig" + str(max_buysig) + "_prec" + str(max_prec) + \
                                     "_tre" + \
                                     str(
                        best_tresh) + "_aimr" + str(raisei) +"_decr" + str(declineratio) + "_offs" + str(
                        offseti) + "_actmet_" + best_act_method
                    max_prec_model.save(filepath+filename_chunk+ "_keras_model.h5")
                    coin.save_scaler_with_filename(min_max_scaler,filepath+filename_chunk+"_scaler.pkl")
                    fig = plt.figure(figsize=(10,6))
                    plt.plot(best_history.history['loss'])
                    plt.plot(best_history.history['val_loss'])
                    plt.plot(best_history.history['precision'])
                    plt.plot(best_history.history['val_precision'])

                    plt.title('model loss')
                    plt.ylabel('loss')
                    plt.xlabel('epoch')
                    plt.legend(['train', 'test','precision','val_precision'], loc='upper left')
                    plt.savefig(filepath+filename_chunk+"_history.png")
                    print("Best models files are written.")


endtime=datetime.now()
print(str(starttime))
print(str(endtime))
print("iterations: ",str(countphase))