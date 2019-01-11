from coins.binance import BinanceApi
from coins.dateutil import DateUtil
from twitter.tweetio import TweetIO
import unittest
import time
from datetime import datetime
#import datetime
from datetime import timedelta, date
from coins.coin import Coin

class TestStringMethods(unittest.TestCase):

    def convert_unix_to_date(self,unix_epoch):
        return datetime.fromtimestamp(int(unix_epoch))

    def print_unix_as_date(self,unix_epoch_including_millisec):
        unix_epoch_including_millisec_str=str(unix_epoch_including_millisec)
        unix_epoch=unix_epoch_including_millisec_str[:-3]
        print(self.convert_unix_to_date(unix_epoch))

    def test_dateutil0(self):
        dateutil=DateUtil()

        self.print_unix_as_date("1523692799000")
        # print(
        #     datetime.fromtimestamp(
        #         int("1523692800000")
        #     ).strftime('%Y-%m-%d %H:%M:%S')
        # )

    def test_dateutil1(self):
        dateutil=DateUtil()
        ba=BinanceApi()
        print(ba.get_server_time())
        nowdt=datetime.now()
        nowdt=nowdt+ timedelta(hours=-2)
        binancedt_int=dateutil.binance_datetime_int(nowdt)
        print("binancedt_int ",binancedt_int)

    def test_date_time_binance_diff(self):
        bapi=BinanceApi()
        date_1 = datetime.strptime("2018-06-01 09:48:02","%Y-%m-%d %H:%M:%S")
        date_2 = datetime.strptime("2018-05-01", "%Y-%m-%d")


        diff=bapi.get_diff_in_hours(date_1, date_2)
        print('diff: ',diff)




    def test_date_time_binance1(self):
        bapi=BinanceApi()
        print(bapi.get_nr_of_hour_distance_from_server())

    def test_date_time_binance2(self):
        bapi=BinanceApi()
        coin = Coin()
        coin.name = 'OMG'
        spech=datetime.now()+ timedelta(hours=-1)


        print("spec_closed_hour: ")
        json_spec_hour=bapi.get_last_n_hour_by_specific_hour_by_coin(coin,spech,1)
        self.print_unix_as_date(json_spec_hour[0][0])
        self.print_unix_as_date(json_spec_hour[0][6])
        print(json_spec_hour)

    def test_date_time_binance3(self):
        bapi=BinanceApi()
        coin = Coin()
        coin.name = 'OMG'
        one_day_before=datetime.now()+ timedelta(days=-1)
        coin.loadtime = one_day_before.strftime("%Y-%m-%d")
        spech=datetime.now()+ timedelta(hours=-1)

        print("spec_closed_hour: ")
        pricehourly=bapi.collect_coindata(coin,spech)
        print(pricehourly)

if __name__ == '__main__':
    unittest.main()


