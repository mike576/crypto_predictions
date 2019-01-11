import pandas as pd
import numpy as np


class CoinPrice:
    def __init__(self):
        print("init price")

    def colswap(df,col1,col2):
        # get a list of the columns
        col_list = list(df)
        # use this handy way to swap the elements
        col_list[col1], col_list[col2] = col_list[col2], col_list[col1]
        # assign back, the order will now be swapped
        df.columns = col_list

    def read_and_sort_price(self,coin):
        coin_price=pd.read_csv(coin.path,sep=';')

        coin_price['datetime']=pd.to_datetime(coin_price['time'],format='%Y.%m.%d %X')
        coin_price['time']=coin_price['datetime']
        coin_price=coin_price.rename(columns={'datetime':'time1','time':'datetime'})
        #colswap(coin_price,2,4)
        #colswap(coin_price,2,3)
        coin_price=coin_price[['datetime','open','high','low','close','volumefrom','volumeto']]


        coin_price['open']=coin_price['open'].map(lambda x: float(x.replace(',','.')))
        coin_price['high']=coin_price['high'].map(lambda x: float(x.replace(',','.')))
        coin_price['low']=coin_price['low'].map(lambda x: float(x.replace(',','.')))
        coin_price['close']=coin_price['close'].map(lambda x: float(x.replace(',','.')))
        coin_price['volumefrom']=coin_price['volumefrom'].map(lambda x: float(x.replace(',','.')))
        coin_price['volumeto']=coin_price['volumeto'].map(lambda x: float(x.replace(',','.')))
        ## TODO is this really true volumefrom+volumeto = volume? answer I think not.
        #coin_price['volume']=coin_price['volumefrom']+coin_price['volumeto']

        coin_price=coin_price[['datetime','open','high','low','close','volumefrom','volumeto']]

        setattr( coin, 'pricehourly', coin_price)
