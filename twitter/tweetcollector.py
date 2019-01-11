import os
import pytz
from coins.coin import Coin
from coins.coininfo import CoinInfo
from datetime import timedelta,datetime,date
import simplejson as json
import pandas as pd
import numpy as np
import time
from twitter.tweepy import TwitterApi
import tweepy
from pytz import utc, timezone, all_timezones
pd.set_option('display.max_rows', 99)
pd.set_option('precision', 10)
pd.set_option('display.width', 1000)


class TweetCollector:
    def __init__(self,tapi):
        print("init")
        self.twapi=tapi
        self.counter = 0
        self.size = 0


    def scrape_coin_tweets(self, coin,tmpdir=''):
        print("Collecting tweets for coin: ",coin)
        icodate=coin.ico
        print("ico: ",icodate)

        i=0
        hashtags = coin.hashtags

        for hashtag in hashtags:
            #today=date.today()
            tomorrow=date.today() + timedelta(days=1)

            #TODO implement #p not to be
            for numproc in range(10,40,2):
                ##+ ' -ed '+str(today)
                command='twitterscraper "#' + hashtag + '" -bd ' + icodate + ' -ed '+str(tomorrow) +' -p '+str(
                    numproc)+' ' \
                                                                                                                  '--lang en -o '
                dir = './data/'+tmpdir+'altcoin-tweets/' + coin.name + '/'
                if not os.path.exists(dir):
                    os.makedirs(dir)
                outputfile=dir+'tweets_' + hashtag + '-' + icodate + '-now'+str(i)+'.json'
                while(os.path.exists(outputfile)):
                    i+=1
                    outputfile= dir + 'tweets_' + hashtag + '-' + icodate + '-now' + str(i) +'.json'

                print("running command : "+command+outputfile)

                p = os.popen(command+outputfile,"r")
                while 1:
                    line = p.readline()
                    if not line: break
                    print(line)

    def collect_users_followers(self,userid,userdf,tapi):
        try:
            print(self.counter,"/",self.size,"using api index:",tapi.get_index()," getting user:",userid)
            self.counter+=1
            result=tapi.get_nextapi().get_user(userid)
            followcount=result.followers_count
            print("followcount:",followcount)
            userdf.at[userid,'follower_count']=followcount
        except Exception as e:
            print(e)
        numapis=tapi.get_listsize()
        #dividing by numapis and substracting network lag.
        waiting=1.0/numapis-0.15
        print("waiting the rate limit sec:",waiting)
        time.sleep(waiting)
        return userid

    def collect_all_users(self,coin,tapi,tmpdir=''):
        self.counter=0
        print("collecting users for tweets of:",coin.name)
        df=coin.tweets
        user_series=df.groupby([df.user]).user.count()
        userdf=pd.DataFrame({'userid':user_series.index, 'tweetabout':user_series.values})
        userdf['follower_count']=0
        userdf=userdf.set_index('userid')
        userdf['t_userid']=userdf.index
        self.size=len(userdf)
        print("getting users followers ",len(userdf)," times")
        userdf['t_userid'].map(lambda x: self.collect_users_followers(x,userdf,tapi))
        name = coin.name
        directory='./data/'+tmpdir+'altcoin-tweets/' + name + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        userdf.to_csv(directory+'users_of_' + name + '.csv')



    def collect_retweets(self,dft, orig_tweet_id,numretweeted,tapi):
        try:

            self.counter+=1
            print(self.counter,"/",numretweeted,"Getting retweets trough API orig tweet id: ",orig_tweet_id)
            api = tapi.get_nextapi()
            results = api.retweets(orig_tweet_id)
            for retweet in results:
                retweet_created_at=retweet.created_at
                retweeter_followers=retweet.user.followers_count
                #dft=dft.append({'orig_tweet_id': orig_tweet_id,'retweet_id': retweet}, ignore_index=True)
                dft.loc[retweet.id] = [orig_tweet_id,retweet.id,retweeter_followers,retweet_created_at]
                #print(tweet.id)
                #print(json.dumps(tweet._json, indent=3))
                #print(" ")
        except Exception as e:
            print(e)
        numapis=tapi.get_listsize()
        #dividing by numapis and substracting network lag.
        waiting=3.0/numapis-0.11
        #print("waiting sec:",waiting)
        time.sleep(waiting)

        return orig_tweet_id


    def collect_all_retweets(self,coin,tapi, fromind=0, toind=99999999,tmpdir=''):
        df=coin.tweets.copy()
        df=df[df['retweets']>0]

        trange=''+str(fromind)+'-'+str(toind)
        if toind<len(df) or fromind!=0:
            print("reducing data size (",str(len(df)),")")
            df=df[df.index<toind]
            df=df[df.index>=fromind]
            print("reduced size",str(len(df)))

        dfrt=pd.DataFrame(columns=list(['orig_tweet_id','retweet_id','retweeter_followers','retweet_created_at']))
        numretweeted=len(df)
        df['id'].map(lambda x: self.collect_retweets(dfrt,x,numretweeted,tapi))
        print("writing to datafile: ")
        name = coin.name

        directory='./data/'+tmpdir+'altcoin-tweets/' + name + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        csvdatafile = directory+'retweets_of_' + name + trange + '.csv'
        print(csvdatafile)
        dfrt.to_csv(csvdatafile)


    def find_timezone(self,name):
        """ Find an appropriate Timezone only by capital name..."""
        for timezone_name in all_timezones:
            if name in timezone_name:
                return timezone_name

    def filter_tweets(self,tweets):
        searchfor = ['btc', 'coin','currency','currencies','hodl','eth','blockchain','digital','crypt'
                     'BTC', 'COIN','CURRENCY','CURRENCIES','HODL','ETH','BLOCKCHAIN','DIGITAL','CRYPT'
                     'Btc', 'Coin','Currency','Currencies','Hodl','Eth','Blockchain','Digital','Crypt']

        print("do filtering, on ", len(tweets), "tweets")
        #tweets=tweets[tweets['text'].str.contains('|'.join(searchfor))]
        #tweets=tweets[]
        #print(any(word in tweets['text'] for word in searchfor))
        #tweets=tweets[tweets['text'] in searchfor]
        print('|'.join(searchfor))
        mask = tweets['text'].str.contains('|'.join(searchfor),regex=True)
        #tweets=tweets[tweets['text'].str.contains('|'.join(searchfor))]
        tweets=tweets[mask]
        print("after filtering nr. of left", len(tweets))
        return tweets

    def collect_todays_tweets(self, coin):
        api=self.twapi.get_api()

        gmtplusone = pytz.timezone('Europe/Budapest')
        tweets=pd.DataFrame()
        i=0
        for hashtag in coin.hashtags:
            ## TODO today date:
            for status in tweepy.Cursor(api.search,
                                     q="#"+hashtag,
                                     since=coin.loadtime,
                                     count=100,
                                     result_type='recent',
                                     include_entities=True,
                                     monitor_rate_limit=True,
                                     wait_on_rate_limit=True,
                                     lang="en").items():
                #print(status)
                print(status)

                tweets.at[i,'id']=status.id
                tweets.at[i,'text']=status.text
                tweets.at[i,'timestamp']=status.created_at
                tweets.at[i,'fullname']=status.user.name
                tweets.at[i,'user']=status.user.screen_name
                tweets.at[i,'retweet']=1

                i+=1
        print('todays queries count: '+str(i))
        tweets=self.filter_tweets(tweets)
        print('After filter todays queries count: '+str(len(tweets)))
        print(tweets.head())
        return tweets