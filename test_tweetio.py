import unittest
from datetime import datetime
# import datetime
from datetime import timedelta, date

from coins.coin import Coin
from twitter.tweetio import TweetIO


class TestStringMethods(unittest.TestCase):
    def test_tweetio_read_db0(self):
        tio = TweetIO()
        coin = Coin()
        coin.name = 'neo'
        nowdt = datetime.now()

        dfnow1 = tio.read_db_tweet_last_n_hour_by_specific_hour_by_coin(coin, nowdt)
        dfnow2 = tio.read_db_tweet_last_n_hour_by_coin(coin)
        print("dfnow1:")
        print(dfnow1)
        print("dfnow2:")
        print(dfnow2)

        print("equality check: ", dfnow1.equals(dfnow2))
        self.assertTrue(dfnow1.equals(dfnow2))

        print("test case finishes.")

    def test_tweetio_read_db1(self):
        tio = TweetIO()
        coin = Coin()
        coin.name = 'neo'
        nowdt = datetime.now()

        dfnow1 = tio.read_db_retweet_last_n_hour_by_specific_hour_by_coin(coin, nowdt)
        dfnow2 = tio.read_db_retweet_last_n_hour_by_coin(coin)
        print("dfnow1:")
        print(dfnow1)
        print("dfnow2:")
        print(dfnow2)

        print("equality check: ")
        self.assertTrue(dfnow1.equals(dfnow2))

        print("test case finishes.")

    def test_tweetio_read_db3(self):
        tio = TweetIO()
        coin = Coin()
        coin.name = 'neo'
        nowdt = datetime.now()

        dfnow1 = tio.read_db_tweet_last_n_hour_by_specific_hour_by_coin(coin, nowdt + timedelta(hours=-1))

        print("dfnow1:")
        print(dfnow1)

        print("test case finishes.")

    def test_tweetio_read_db2(self):
        coin = Coin()

        coin.name = 'omg'
        yesterday = date.today() + timedelta(days=-1)
        coin.loadtime = yesterday.strftime("%Y-%m-%d")
        coin.hashtags = ['omg', 'omisego']

        tio = TweetIO()
        df = tio.read_db_tweet_last_n_hour_by_coin(coin)
        print(df)

    def test_isupper(self):
        self.assertEqual('foo'.upper(), 'FOO')

        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_filter(self):
        searchfor = ['btc', 'coin', 'currency', 'currencies', 'hodl', 'eth', 'blockchain', 'digital', 'crypt'
                                                                                                      'BTC', 'COIN',
                     'CURRENCY', 'CURRENCIES', 'HODL', 'ETH', 'BLOCKCHAIN', 'DIGITAL', 'CRYPT'
                                                                                       'Btc', 'Coin', 'Currency',
                     'Currencies', 'Hodl', 'Eth', 'Blockchain', 'Digital', 'Crypt']
        s = '1 OmiseGO = 9.743 USD. OMG has changed by -0.0511 USD in 30 mins. Live price: https://t.co/72qHUrkz4r #omisego #omg #'
        #print(str(s).contains('|'.join(searchfor)))

        print()


if __name__ == '__main__':
    unittest.main()
