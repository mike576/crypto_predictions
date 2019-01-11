import simplejson as json
import tweepy
from tweepy import OAuthHandler


class TwitterApi:
    def __init__(self):

        self.apilist=[]
        self.index=0

        print("TwitterApi: connecting to twitter")
        '''

        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        '''

        #aiwebtesting
        cons_key = 'yyy'
        cons_sec = 'sss'
        access_token = 'ttt'
        access_secret = 'xxx'
        auth_aiwebtesting = tweepy.OAuthHandler(cons_key, cons_sec)
        auth_aiwebtesting.set_access_token(access_token, access_secret)


        #miklostoth

        #czegledit

        self.apilist=[tweepy.API(auth_czegledi),tweepy.API(auth_attila),tweepy.API(auth_rago),tweepy.API(
            auth_fajt_peti)]

        self.api = tweepy.API(auth_miklostoth)

        self.auth = auth_aiwebtesting

    def get_auth(self):
        return self.auth

    def get_api(self):
        return self.api

    def get_apilist(self):
        return self.apilist

    def set_index(self,ind):
        self.index=ind

    def get_index(self):
        self.index

    def get_nextapi(self):
        ret=self.apilist[self.index]
        self.index+=1
        if (self.index >=len(self.apilist)):
            self.index=0
        return ret

    def get_listsize(self):
        return len(self.apilist)
