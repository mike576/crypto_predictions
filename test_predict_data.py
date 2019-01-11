import unittest
from datetime import datetime
# import datetime
from datetime import timedelta, date

from coins.coin import Coin
from twitter.tweetio import TweetIO
import pandas as pd

class TestStringMethods(unittest.TestCase):
    def test_tweetio_read_predict(self):

        pd.set_option("display.max_rows",100)
        pd.set_option("display.max_columns",100)

        tio = TweetIO()
        coin = Coin()
        coin.name = 'omg'
        nowdt = datetime.now()
        argtime='2018-04-14_16-00-00'

        coin.read_from_storeage('rt','runtime/'+argtime+'/')
        print(coin.data_to_predict)

        print("test case finishes.")

    def test_range(self):
        for j in range(4,9,2):
            print(j)

    def test_tweetio_read_train(self):

        pd.set_option("display.max_rows",100)
        pd.set_option("display.max_columns",100)

        coin = Coin()
        coin.name = 'neo'

        coin.read_from_storeage('train')
        print(coin.data_to_predict)

        print("test case finishes.")


if __name__ == '__main__':
    unittest.main()
