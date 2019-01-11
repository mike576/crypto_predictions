import requests
from datetime import datetime
from dateutil import relativedelta

from coins.dateutil import DateUtil
from datetime import timedelta, date
import pandas as pd

class BinanceApi:
    def __init__(self):
        self.apikey='nIOkas8asbaYvetstwgm2uNmMDcucSroDySCEJMxnEJ27uWDDSli9wChPlEDEL8l'
        self.secret='saved to last pass'

    #Depricated, the unclosed candle is also returned:
    # def get_last_n_hour_by_coin(self, coin,n_hours):
    #     coinname=coin.name
    #     coinnameupper=coinname.upper()
    #     apiurl='https://api.binance.com/api/v1/klines?symbol='+coinnameupper+'BTC&interval=1h&limit='+str(n_hours)
    #     print("calling: "+apiurl)
    #     response=requests.get(apiurl)
    #     return response.json()

    def get_nr_of_hour_distance_from_server(self):
        nowdt=datetime.now()
        dateutil=DateUtil()
        nowmillis=dateutil.unix_time_millis(nowdt)
        server_time = self.get_server_time()['serverTime']
        diff=(nowmillis-server_time)/1000/3600
        diff=round(diff)
        return diff


    def get_last_n_hour_by_specific_hour_by_coin(self, coin,specific_hour,n_hours):
        coinname=coin.name
        coinnameupper=coinname.upper()
        offset_from_server = self.get_nr_of_hour_distance_from_server()
        #once you have to substract the offset from server
        targethour=specific_hour+ timedelta(hours=-1*offset_from_server)

        #twice you have to substract because the server end time means until the next hour. >:)
        targethour=targethour+ timedelta(hours=-1)
        date_util = DateUtil()
        start_time= round(date_util.unix_time_millis(targethour))

        apiurl='https://api.binance.com/api/v1/klines?symbol='+coinnameupper+'BTC&endTime='+str(start_time)+\
               '&interval=1h&limit='+str(n_hours)

        print("calling: "+apiurl)
        response=requests.get(apiurl)
        return response.json()

    def get_server_time(self):

        apiurl='https://api.binance.com/api/v1/time'
        print("calling: "+apiurl)
        response=requests.get(apiurl)
        return response.json()

    def get_diff_since_loadtime_and_specific_hour(self,coin,specific_hour):
        date_1 = specific_hour
        date_2 = datetime.strptime(coin.loadtime, "%Y-%m-%d")
        return self.get_diff_in_hours(date_1, date_2)

    def get_diff_in_hours(self,date_1, date_2):
        difference = relativedelta.relativedelta(date_1, date_2)
        hours = difference.hours

        delta = date_1 - date_2
        days=delta.days

        totalhours = days * 24 + hours

        return totalhours

    def get_diff_since_loadtime(self,coin):
        date_1 = datetime.now()
        date_2 = datetime.strptime(coin.loadtime, "%Y-%m-%d")
        return self.get_diff_in_hours(date_1, date_2)


    def get_diff_since_ico(self,coin):
        date_1 = datetime.now()
        date_2 = datetime.strptime(coin.ico, "%Y-%m-%d")
        return self.get_diff_in_hours(date_1, date_2)



    def collect_coindata(self,coin,specific_hour):
        bapi = BinanceApi()
        pricehourly = pd.DataFrame(columns=['datetime'])

        n_hours = self.get_diff_since_loadtime(coin)
        #    for index, row in inputdf.iterrows():
        #        coin=Coin()
        #        coin.name=index
        jsonresponse = bapi.get_last_n_hour_by_specific_hour_by_coin(coin,specific_hour, n_hours + 1)
        i = 0
        for row in jsonresponse:
            #this is one second befor the close datetime
            ts_epoch = jsonresponse[i][6]
            ts = datetime.fromtimestamp((int(ts_epoch)+1000) / 1000).strftime('%Y-%m-%d %H:%M:%S')

            pricehourly.at[i, 'datetime'] = ts
            pricehourly.at[i, 'open'] = jsonresponse[i][1]
            pricehourly.at[i, 'high'] = jsonresponse[i][2]
            pricehourly.at[i, 'low'] = jsonresponse[i][3]
            pricehourly.at[i, 'close'] = jsonresponse[i][4]
            pricehourly.at[i, 'volumefrom'] = jsonresponse[i][9]
            pricehourly.at[i, 'volumeto'] = jsonresponse[i][10]
            i += 1

        for column in pricehourly:
            if column != 'datetime':
                pricehourly[column] = pricehourly[column].astype('float64')

        pricehourly['high_raised'] = pricehourly['high'] / pricehourly['open']
        pricehourly['low_raised'] = pricehourly['low'] / pricehourly['open']
        pricehourly['close_raised'] = pricehourly['close'] / pricehourly['open']

        return pricehourly

