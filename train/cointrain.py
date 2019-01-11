import pandas as pd
import numpy as np
import math
import time
from datetime import datetime
from datetime import timedelta, date

from stockstats import StockDataFrame


class CoinTrain:
    def __init__(self):
        print('init CoinTrain')


    def create_buy_sig(self,coin,aimraise=10,declinelimit=-5,offset=12):
        #testing for some offset
        for o in range(offset,offset+1):
            print("At offset: ",o)
            X=coin.pricehourly.copy()
            #X['datetime'] = X['datetime'].map(mdates.num2date)
            X['raise']=(X.close-X.open)/X.open*100
            X['high_raise']=(X.high-X.open)/X.open*100
            X['cumraise']=0.0


            offset=o
            for i in X.index:
                isthereapointwhereaimraisereached=False
                isthereapointwheretrailingstopfires=False
                if i < len(X.index)-offset:
                    sumraise=0.0
                    startprice=X.at[i,'close']
                    trailing_stop_point=startprice*(1+declinelimit/100)
                    for j in range(1,offset):
                        if(sumraise+X.loc[i+j]['high_raise']>aimraise):
                            isthereapointwhereaimraisereached=True
                        sumraise+=X.loc[i+j]['raise']
                        if(sumraise>aimraise):
                            isthereapointwhereaimraisereached=True

                        if(X.loc[i+j]['low']<trailing_stop_point):
                            isthereapointwheretrailingstopfires=True
                        if(sumraise<declinelimit):
                            isthereapointwheretrailingstopfires=True
                        if(isthereapointwhereaimraisereached):
                            break

                    X.at[i,'cumraise']=sumraise
                    if(isthereapointwhereaimraisereached==True  and isthereapointwheretrailingstopfires==False):
                        X.at[i,'buysig']=1
                    if(isthereapointwhereaimraisereached==True  and isthereapointwheretrailingstopfires==True):
                        X.at[i,'buysig']=0


            #X.at[X['cumraise']>=10,'buysig']=1
            X.set_index(['datetime'],inplace=True)
            print("len data: ",len(X))
            print("buysig count",X['buysig'].count())
        return X

    def increase_by_one_hour(self,gtdf):
        #INCREASING HOUR BY 1
        X_gtdf=gtdf.copy()
        idx=X_gtdf.index
        X_gtdf.index=idx.set_names(['year', 'month','day','hour'])
        X_gtdf.reset_index(inplace=True)
        #X_gtdf['hour']=X_gtdf['hour'].map(lambda x: x+1)
        for i in X_gtdf.index:
            datetime_object = datetime.strptime(str(X_gtdf.at[i,'year'])+'-'+str(X_gtdf.at[i,'month'])+'-'+str(
                X_gtdf.at[i,'day'])+' '+str(X_gtdf.at[i,'hour']), '%Y-%m-%d %H')
            datetime_object_plus_one=datetime_object+timedelta(hours=+1)
            year=datetime_object_plus_one.strftime("%Y")
            month=datetime_object_plus_one.strftime("%m")
            day=datetime_object_plus_one.strftime("%d")
            hour=datetime_object_plus_one.strftime("%H")
            X_gtdf.at[i,'year']=year
            X_gtdf.at[i,'month']=month
            X_gtdf.at[i,'day']=day
            X_gtdf.at[i,'hour']=hour

        X_gtdf.set_index(['year', 'month','day','hour'],inplace=True)
        return X_gtdf

    def setreduction(self,dft,i,colname,reductionrate):
        dft.at[i,colname]=round(dft.at[i,colname]+dft.at[i-1,colname]/reductionrate)

    def spreadtweeteffect(self,data):
        reductionrate=2
        for i in data.index:
            if(i>0):
                self.setreduction(data,i,'follower_count',reductionrate)
                self.setreduction(data,i,'retweeter_followers',reductionrate)
                self.setreduction(data,i,'sum_posmulfollower',reductionrate)
                self.setreduction(data,i,'sum_negmulfollower',reductionrate)
                self.setreduction(data,i,'sum_neumulfollower',reductionrate)
                self.setreduction(data,i,'sum_compmulfollower',reductionrate)
                self.setreduction(data,i,'sum_posmulrfollower',reductionrate)
                self.setreduction(data,i,'sum_negmulrfollower',reductionrate)
                self.setreduction(data,i,'sum_neumulrfollower',reductionrate)
                self.setreduction(data,i,'sum_compmulrfollower',reductionrate)

    def add_stock_features(self,data):

        data['24 ma'] = pd.rolling_mean(data['close'],24)
        data['24 sd'] = pd.rolling_std(data['close'],24)
        data['Bollinger Upper Band'] = data['24 ma'] + (data['24 sd']*2)
        data['Bollinger Lower Band'] = data['24 ma'] - (data['24 sd']*2)
        data['boll_up-close']=(data['Bollinger Upper Band']-data['close'])/data['close']
        data['boll_down-close']=(data['close']-data['Bollinger Lower Band'])/data['close']
        data['boll_up_close_ratio']=(data['Bollinger Upper Band'])/data['close']
        data['boll_down_close_ratio']=(data['Bollinger Lower Band'])/data['close']
        data['boll_up_close_ratio_pow3']=data['boll_up_close_ratio'].map(lambda x: math.pow(x,3))
        data['boll_down_close_ratio_pow3']=data['boll_down_close_ratio'].map(lambda x: math.pow(x,3))

        data.drop(columns=['24 ma','Bollinger Upper Band','Bollinger Lower Band'],
                  inplace=True)


        prepare_stock=data[['open','high','low','close','volumeto']]
        prepare_stock=prepare_stock.rename(index=str, columns={"volumeto": "volume"})
        stock = StockDataFrame.retype(prepare_stock)
        data['rsi_12']=stock['rsi_12'].values
        data['rsi_6']=stock['rsi_6'].values






    def add_change_columns(self,data):
        data['eu_market']=0
        data['us_market']=0
        data['asia_market']=0


        for i in data.index:
            if(i>23):
                data.at[i,'c_o_change']=(data.at[i,'close']-data.at[i,'open'])/data.at[i,'open']
                data.at[i,'h_o_change']=(data.at[i,'high']-data.at[i,'open'])/data.at[i,'open']
                data.at[i,'l_o_change']=(data.at[i,'low']-data.at[i,'open'])/data.at[i,'open']
                data.at[i,'c_o_change1']=(data.at[i,'close']-data.at[i-1,'open'])/data.at[i-1,'open']
                data.at[i,'h_o_change1']=(data.at[i,'high']-data.at[i-1,'open'])/data.at[i-1,'open']
                data.at[i,'l_o_change1']=(data.at[i,'low']-data.at[i-1,'open'])/data.at[i-1,'open']
                data.at[i,'o_change1']=(data.at[i,'open']-data.at[i-1,'open'])/data.at[i-1,'open']
                data.at[i,'o_change2']=(data.at[i-1,'open']-data.at[i-2,'open'])/data.at[i-2,'open']
                data.at[i,'o_change3']=(data.at[i-2,'open']-data.at[i-3,'open'])/data.at[i-3,'open']
                data.at[i,'o_change4']=(data.at[i-3,'open']-data.at[i-4,'open'])/data.at[i-4,'open']
                data.at[i,'o_change5']=(data.at[i-4,'open']-data.at[i-5,'open'])/data.at[i-5,'open']
                data.at[i,'o_change6']=(data.at[i-5,'open']-data.at[i-6,'open'])/data.at[i-6,'open']
                data.at[i,'o_change1_3']=(data.at[i,'open']-data.at[i-3,'open'])/data.at[i-3,'open']
                data.at[i,'o_change1_12']=(data.at[i,'open']-data.at[i-12,'open'])/data.at[i-12,'open']
                data.at[i,'o_change1_12']=(data.at[i,'open']-data.at[i-24,'open'])/data.at[i-24,'open']
                data.at[i,'vf_change1']=(data.at[i,'volumefrom']-data.at[i-1,'volumefrom'])/data.at[i-1,'volumefrom']
                data.at[i,'vt_change1']=(data.at[i,'volumeto']-data.at[i-1,'volumeto'])/data.at[i-1,'volumeto']
                # data.at[i,'vtvf_ratio']=data.at[i,'volumeto']/data.at[i,'volumefrom']
                # data.at[i,'vfvt_ratio']=data.at[i,'volumefrom']/data.at[i,'volumeto']
                data.at[i,'rsi_12_change1']=(data.at[i,'rsi_12']-data.at[i-1,'rsi_12'])/data.at[i-1,'rsi_12']
                data.at[i,'rsi_12_change2']=(data.at[i,'rsi_12']-data.at[i-2,'rsi_12'])/data.at[i-2,'rsi_12']
                data.at[i,'rsi_6_change1']=(data.at[i,'rsi_6']-data.at[i-1,'rsi_6'])/data.at[i-1,'rsi_6']
                data.at[i,'rsi_6_change2']=(data.at[i,'rsi_6']-data.at[i-2,'rsi_6'])/data.at[i-2,'rsi_6']
                data.at[i,'rsi_6_12_ratio']=(data.at[i,'rsi_6'])/data.at[i,'rsi_12']

                if (data.at[i,'hour']>8 and data.at[i,'hour']<18):
                    data.at[i,'eu_market']=1
                if (data.at[i,'hour']>14 and data.at[i,'hour']<24):
                    data.at[i,'us_market']=1
                if (data.at[i,'hour']>2 and data.at[i,'hour']<12):
                    data.at[i,'asia_market']=1

    def add_squared_columns(self,data,strCols=True):
        orig_columns=data.columns.copy()
        for i in data.index:
            for col in orig_columns:
                if strCols==True:
                    data.at[i,col+'_squared']=data.at[i,col]*data.at[i,col]
                else:
                    data.at[i,col+len(orig_columns)]=data.at[i,col]*data.at[i,col]

    def do_log(self,value_for_log):
        if value_for_log>0:
            return math.log(value_for_log)
        else:
            return 0

    def add_log_columns(self,data,strCols=True):
        orig_columns=data.columns.copy()
        for i in data.index:
            for col in orig_columns:
                if strCols==True:
                    data.at[i,col+'_log']=self.do_log(data.at[i,col])
                else:
                    data.at[i,col+len(orig_columns)]=self.do_log(data.at[i,col])

    def create_Xdf(self,X,X_grtdf,X_gtdf):
        #global gXdf, gXdf
        # Converting X to the same multi index type
        times = pd.DatetimeIndex(X.index)

        # not really summing
        gX = X.groupby([times.year, times.month, times.day, times.hour]).open.sum()
        gXdf = pd.DataFrame(gX)
        # not really max just copy
        gXdf['buysig'] = X.groupby([times.year, times.month, times.day, times.hour])['buysig'].max()
        gXdf['high'] = X.groupby([times.year, times.month, times.day, times.hour])['high'].max()
        gXdf['low'] = X.groupby([times.year, times.month, times.day, times.hour])['low'].max()
        gXdf['close'] = X.groupby([times.year, times.month, times.day, times.hour])['close'].max()
        gXdf['volumefrom'] = X.groupby([times.year, times.month, times.day, times.hour])['volumefrom'].max()
        gXdf['volumeto'] = X.groupby([times.year, times.month, times.day, times.hour])['volumeto'].max()
        gXdf['high_raised'] = gXdf['high'] / gXdf['open']
        gXdf['low_raised'] = gXdf['low'] / gXdf['open']
        gXdf['close_raised'] = gXdf['close'] / gXdf['open']
        idx = gXdf.index
        gXdf.index = idx.set_names(['year', 'month', 'day', 'hour'])
        print("gXdf, head and tail:")
        # print(gXdf.head())
        # print(gXdf.tail())
        print("X_grtdf, head and tail:")
        # print(X_grtdf.head())
        # print(X_grtdf.tail())
        print("X_gtdf, head and tail:")
        # print(X_gtdf.head())
        # print(X_gtdf.tail())
        # MERGE:
        gXdf = gXdf.merge(X_grtdf, how='left', left_index=True, right_index=True)
        Xdf = gXdf.merge(X_gtdf, how='left', left_index=True, right_index=True)
        print("Xdf >")
        #print(Xdf)
        print("Len Xdf: ")
        print(len(Xdf))
        print("buysig NR: ")
        print(len(Xdf[Xdf['buysig']==1]))
        return Xdf,gXdf
