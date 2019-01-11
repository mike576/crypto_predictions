import pandas as pd
import numpy as np
import os
from sklearn.externals import joblib

BASE_STOREAGE='./data/altcoin-storage/'

class Coin:
    def __init__(self):
        self.name='<altcoin>'
        self.hashtags=['']
        self.ico='unknown'
        self.loadtime='unknown'
        self.path=''
        self.treshold=0.8
        self.tweets=pd.DataFrame()
        self.retweets=pd.DataFrame()
        self.grtdf=pd.DataFrame()
        self.gtdf=pd.DataFrame()
        self.pricehourly=pd.DataFrame()
        self.currenttimestamp='<current_timestamp>'
        self.data_to_predict=pd.DataFrame()
        self.target=1.0
        self.stoploss=-1.0
        self.timelimit=3
        self.modelfile=None
        self.scalerfile=None


    def reset_data_frames(self):
        self.tweets=pd.DataFrame()
        self.retweets=pd.DataFrame()
        self.grtdf=pd.DataFrame()
        self.gtdf=pd.DataFrame()
        self.pricehourly=pd.DataFrame()
        self.data_to_predict=pd.DataFrame()


    def save_to_storeage(self,phase,tmpdir=''):
        directory='./data/'+tmpdir+'altcoin-storage/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        print("saveing to dir: "+directory)
        self.tweets.to_pickle( directory + self.name + '_tweets_'+phase+'.pkl')
        self.retweets.to_pickle('./data/'+tmpdir+'altcoin-storage/' + self.name + '_retweets_'+phase+'.pkl')
        self.grtdf.to_pickle('./data/'+tmpdir+'altcoin-storage/' + self.name + '_grtdf_'+phase+'.pkl')
        self.gtdf.to_pickle('./data/'+tmpdir+'altcoin-storage/' + self.name + '_gtdf_'+phase+'.pkl')
        self.pricehourly.to_pickle('./data/'+tmpdir+'altcoin-storage/' + self.name + '_pricehourly_'+phase+'.pkl')
        self.data_to_predict.to_pickle('./data/'+tmpdir+'altcoin-storage/' + self.name +
                                       '_data_to_predict_'+phase+'.pkl')

    def read_from_storeage(self,phase,tmpdir=''):
        print("Reading coin from storage: ",self.name)

        # filepath='./data/altcoin-storage/' + self.name + '_tweets_'+phase+'.json'
        # print("reading ",filepath)
        # df=pd.read_json(filepath)
        # self.tweets=df
        #
        # filepath='./data/altcoin-storage/' + self.name + '_retweets_'+phase+'.json'
        # print("reading ",filepath)
        # df=pd.read_json(filepath)
        # self.retweets=df
        #
        # filepath='./data/altcoin-storage/' + self.name + '_grtdf_'+phase+'.json'
        # print("reading ",filepath)
        # df=pd.read_json(filepath)
        # self.grtdf=df
        #
        # filepath='./data/altcoin-storage/' + self.name + '_gtdf_'+phase+'.json'
        # print("reading ",filepath)
        # df=pd.read_json(filepath)
        # self.gtdf=df
        #
        # filepath='./data/altcoin-storage/' + self.name + '_pricehourly_'+phase+'.json'
        # print("reading ",filepath)
        # df=pd.read_json(filepath)
        # self.pricehourly=df



        filepath='./data/'+tmpdir+'altcoin-storage/' + self.name + '_tweets_'+phase+'.pkl'
        print("reading ",filepath)
        df=pd.read_pickle(filepath)
        self.tweets=df

        filepath='./data/'+tmpdir+'altcoin-storage/' + self.name + '_retweets_'+phase+'.pkl'
        print("reading ",filepath)
        df=pd.read_pickle(filepath)
        self.retweets=df

        filepath='./data/'+tmpdir+'altcoin-storage/' + self.name + '_grtdf_'+phase+'.pkl'
        print("reading ",filepath)
        df=pd.read_pickle(filepath)
        self.grtdf=df

        filepath='./data/'+tmpdir+'altcoin-storage/' + self.name + '_gtdf_'+phase+'.pkl'
        print("reading ",filepath)
        df=pd.read_pickle(filepath)
        self.gtdf=df

        filepath='./data/'+tmpdir+'altcoin-storage/' + self.name + '_pricehourly_'+phase+'.pkl'
        print("reading ",filepath)
        df=pd.read_pickle(filepath)
        self.pricehourly=df

        filepath='./data/'+tmpdir+'altcoin-storage/' + self.name + '_data_to_predict_'+phase+'.pkl'
        if (os.path.exists(filepath)):
            print("reading ",filepath)
            df=pd.read_pickle(filepath)
            self.data_to_predict=df


    def save_scaler_with_filename(self,min_max_scaler,filename):
        joblib.dump(min_max_scaler, filename)

    def save_scaler(self,min_max_scaler):
        joblib.dump(min_max_scaler, self.get_scaler_path())

    def get_scaler_path(self):
        self.scaler_filename = BASE_STOREAGE + self.name + "_minmaxscaler.pkl"
        return self.scaler_filename

    def read_scaler(self):
        print('loading scaler:')
        if (self.scalerfile):
            print(BASE_STOREAGE + self.scalerfile)
            scaler = joblib.load(BASE_STOREAGE + self.scalerfile)
            return scaler
        else:
            print(self.get_scaler_path())
            scaler = joblib.load(self.get_scaler_path())
            return scaler

    def __str__(self):
        return str(self.name)+" size of tweets: "+str(len(self.tweets))

    __repr__ = __str__