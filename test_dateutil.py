from coins.binance import BinanceApi
from coins.dateutil import DateUtil
from twitter.tweetio import TweetIO
import unittest
import time
from datetime import datetime
#import datetime
from datetime import timedelta, date
from coins.coin import Coin
from train.cointrain import CoinTrain
import pandas as pd

class TestStringMethods(unittest.TestCase):


    def test_increase_one_hour(self):
        cointrain=CoinTrain()
        #df=pd.DataFrame(index=['year', 'month','day','hour'],columns=[i],data=)
        coin=Coin()
        coin.path="./data/altcoin-1hour/neo.csv"
        coin.name="neo"
        coin.ico="2017-12-31"


        coin.read_from_storeage("prepare2")

        gtdf=coin.gtdf
        idx=gtdf.index
        gtdf.index=idx.set_names(['year', 'month','day','hour'])
        print(gtdf['sum_neumulfollower'].tail(27))
        gtdf=cointrain.increase_by_one_hour(gtdf)

        print(gtdf['sum_neumulfollower'].tail(27))





    def test_dateutil0(self):
        dateutil=DateUtil()

        print(
            datetime.fromtimestamp(
                int("1523689200")
            ).strftime('%Y-%m-%d %H:%M:%S')
        )

    def test_dateutil1(self):
        dateutil=DateUtil()
        ba=BinanceApi()
        print(ba.get_server_time())
        nowdt=datetime.now()
        nowdt=nowdt+ timedelta(hours=-2)
        binancedt_int=dateutil.binance_datetime_int(nowdt)
        print("binancedt_int ",binancedt_int)





    def test_isupper(self):
        self.assertEqual('foo'.upper(), 'FOO')

        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()


