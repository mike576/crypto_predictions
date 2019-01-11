import os
import time
from datetime import datetime
from datetime import timedelta, date


class DateUtil:
    def __init__(self):
        print("init TweetIO")

    def parse_time_string(self,datestr):
        datetime_object = datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')
        return datetime_object

    def round_datetime_down(self,datetime_object):
        new_datetime_object = datetime_object.strftime("%Y-%m-%d %H:00:00")
        return new_datetime_object

    def round_datetime_up(self,datetime_object):
        datetime_object_plus_one=datetime_object+timedelta(hours=+1)
        new_datetime_object = datetime_object_plus_one.strftime("%Y-%m-%d %H:00:00")
        return new_datetime_object



    def unix_time_millis(self,dt):
        epoch = datetime.utcfromtimestamp(0)
        return (dt - epoch).total_seconds() * 1000.0

    def binance_datetime_int(self,datetime_object):
        return self.unix_time_millis(datetime_object)


    def last_round_hour(self):
        now = datetime.now()
        last_hour = now.strftime("%Y-%m-%d %H:00:00")
        tsto = last_hour
        return tsto

    def two_round_hours_ago(self):
        last_n_hour = datetime.now() + timedelta(hours=-1)
        tsfrom = str(last_n_hour.strftime("%Y-%m-%d %H:00:00"))
        return tsfrom

    def two_days_ago(self):
        last_n_hour = datetime.now() + timedelta(days=-2)
        tsfrom = str(last_n_hour.strftime("%Y-%m-%d %H:00:00"))
        return tsfrom
