import os
from coins.coin import Coin
from coins.coininfo import CoinInfo
from datetime import timedelta,datetime,date
import simplejson as json
import pandas as pd
import numpy as np
import time
from twitter.tweepy import TwitterApi
from db.mysqldb import dbconn
import time
from datetime import datetime
# import datetime
from datetime import timedelta, date
from coins.dateutil import DateUtil


class TweetIO:
    def __init__(self):
        print("init TweetIO")
        self.dateutil=DateUtil()


    def read_db_tweet_last_n_hour_by_specific_hour_by_coin(self, coin,specific_hour,n_hours=48):

        df=pd.DataFrame(columns=['id','text','user_id','user_history_row_id','user_name','retweet_count','favorite_count',
                                 'timestamp','lang'])

        tsto=self.dateutil.round_datetime_down(specific_hour)

        tsfrom=self.dateutil.round_datetime_down(specific_hour+timedelta(hours=-1*n_hours))

        for tag in coin.hashtags:
            print("getting ",tag," from: ",tsfrom," to: ",tsto)
            df=self.read_db_tweet(tsfrom,tsto,tag,df)
        return df



    def read_db_tweet_last_n_hour_by_coin(self, coin):

        df=pd.DataFrame(columns=['id','text','user_id','user_history_row_id','user_name','retweet_count','favorite_count',
                                 'timestamp','lang'])

        tsfrom = self.dateutil.two_days_ago()

        tsto = self.dateutil.last_round_hour()

        for tag in coin.hashtags:
            print("getting ",tag," from: ",tsfrom," to: ",tsto)
            df=self.read_db_tweet(tsfrom,tsto,tag,df)
        return df



    def read_db_tweet(self,tsfrom,tsto,searchtext,df=pd.DataFrame(columns=['id','text','user_id','user_history_row_id',
                                                                           'user_name','retweet_count','favorite_count',
                                                                           'timestamp','lang'])):

        select_query = """
        select * from tweet where created_at > '"""+tsfrom+"""' and created_at < '"""+tsto+"""' and text like 
        '%"""+searchtext+"""%' and lang like 'en';
        """
        print(select_query)

        rows=dbconn.query(select_query)

        i=len(df)
        print("len rows",len(rows))
        print("i from ",i)

        for dbrow in rows:
            df.at[i,'id']=dbrow['id']
            df.at[i,'text']=dbrow['text']
            df.at[i,'user_id']=dbrow['user_id_str']
            df.at[i,'user_history_row_id']=dbrow['user_history_row_id']
            df.at[i,'user_name']=dbrow['user_name']
            df.at[i,'retweet_count']=dbrow['retweet_count']
            df.at[i,'favorite_count']=dbrow['favorite_count']
            df.at[i,'timestamp']=dbrow['created_at']
            df.at[i,'lang']=dbrow['lang']
            i+=1
        print("i until ",i)
        print("len(df)",len(df))
        return df


    def read_db_retweet_last_n_hour_by_specific_hour_by_coin(self, coin,specific_hour,n_hours=48):

        df=pd.DataFrame(columns=['retweet_id','orig_tweet_id',
                                 'retweeter_followers','retweet_created_at',
                                 'user_history_row_id','user_id_str'])

        tsto=self.dateutil.round_datetime_down(specific_hour)

        tsfrom=self.dateutil.round_datetime_down(specific_hour+timedelta(hours=-1*n_hours))

        for tag in coin.hashtags:
            print("getting ",tag," from: ",tsfrom," to: ",tsto)
            df=self.read_db_retweet(tsfrom,tsto,tag,df)
        return df


    def read_db_retweet_last_n_hour_by_coin(self, coin):

        df=pd.DataFrame(columns=['retweet_id','orig_tweet_id',
                                 'retweeter_followers','retweet_created_at',
                                 'user_history_row_id','user_id_str'])

        tsfrom=self.dateutil.two_days_ago()

        tsto=self.dateutil.last_round_hour()

        for tag in coin.hashtags:
            print("getting ",tag," from: ",tsfrom," to: ",tsto)
            df=self.read_db_retweet(tsfrom,tsto,tag,df)
        return df


    def read_db_retweet(self,tsfrom,tsto,searchtext,df=pd.DataFrame(columns=['retweet_id','orig_tweet_id',
                                                                             'retweeter_followers','retweet_created_at',
                                                                             'user_history_row_id','user_id_str'])):

        select_query = """
        select * from retweet where retweet_created_at > '"""+tsfrom+"""' and retweet_created_at < '"""+tsto+"""' and
         orig_tweet_id in (select id from tweet where text like '%"""+searchtext+"""%'  and lang like 'en');
        """
        print(select_query)

        rows=dbconn.query(select_query)

        i=len(df)
        for dbrow in rows:
            df.at[i,'retweet_id']=dbrow['retweet_id']
            df.at[i,'orig_tweet_id']=dbrow['orig_tweet_id']
            df.at[i,'retweeter_followers']=dbrow['retweeter_followers']
            df.at[i,'retweet_created_at']=dbrow['retweet_created_at']
            df.at[i,'user_history_row_id']=dbrow['user_history_row_id']
            df.at[i,'user_id_str']=dbrow['user_id_str']
            i+=1
        return df

    def read_db_referenced_users(self,coin):
        tdf=coin.tweets
        rtdf=coin.retweets
        referenced_user_ids=[]
        for index,row in tdf.iterrows():
            referenced_user_ids.append(row['user_history_row_id'])
        for index,row in rtdf.iterrows():
            referenced_user_ids.append(row['user_history_row_id'])

        return self.read_db_users(referenced_user_ids)

    def read_db_users(self,referenced_user_ids):
        df=pd.DataFrame(columns=['user_row_id','twitter_user_id','user_name',
                                 'follower_count','friends_count','listed_count',
                                 'favourites_count','statuses_count','user_created_at'])
        ruids=str(referenced_user_ids)
        ruids=ruids[1:]
        ruids=ruids[:-1]
        select_query = """
        select * from tweet_user_history where id in ("""+ruids+""");
        """
        print(select_query)
        rows=dbconn.query(select_query)

        i=len(df)
        for dbrow in rows:
            df.at[i,'user_row_id']=dbrow['id']
            df.at[i,'twitter_user_id']=dbrow['user_id']
            df.at[i,'user_name']=dbrow['user_name']
            df.at[i,'follower_count']=dbrow['followers_count']
            df.at[i,'friends_count']=dbrow['friends_count']
            df.at[i,'listed_count']=dbrow['listed_count']
            df.at[i,'favourites_count']=dbrow['favourites_count']
            df.at[i,'statuses_count']=dbrow['statuses_count']
            df.at[i,'user_created_at']=dbrow['user_created_at']
            i+=1
        return df


    def read_all_scraped_tweet(self,coin,tmpdir=''):
        coin_name = coin.name
        dir = './data/'+tmpdir+'altcoin-tweets/' + coin_name + '/'
        print("reading tweet files from: "+dir)
        ci=CoinInfo()
        dflist=[]
        list=ci.list_tweetfiles(dir)
        for tweetfile in list:
            print("reading in: "+tweetfile)

            df=pd.read_json(path_or_buf=tweetfile)
            dflist.append(df)
        df=pd.concat(dflist)
        print("collected tweets: " + str(df['id'].count()))
        print("dropping duplicate tweets: ")
        df=df.drop_duplicates('id')
        print("collected tweets: " +str(df['id'].count()))
        df.reset_index(inplace=True)
        return df

    def read_all_scraped_retweet(self,coin,tmpdir=''):
        coin_name = coin.name
        dir = './data/'+tmpdir+'altcoin-tweets/' + coin_name + '/'
        print("reading RETWEET files from: "+dir)
        ci=CoinInfo()
        dflist=[]
        list=ci.list_retweetfiles(dir)
        for retweetfile in list:
            print("reading in: "+retweetfile)
            df=pd.read_csv(retweetfile)
            dflist.append(df)
        df=pd.concat(dflist)
        print("collected retweets: " + str(df['retweet_id'].count()))
        print("dropping duplicate tweets: ")
        df=df.drop_duplicates('retweet_id')
        print("collected tweets: " +str(df['retweet_id'].count()))
        df.reset_index(inplace=True)
        return df

    def read_users_for_tweets(self,coin,tmpdir=''):
        cname=coin.name
        userdf=pd.read_csv('./data/'+tmpdir+'altcoin-tweets/'+cname+'/users_of_'+cname+'.csv')
        print("before merge: coin.tweets", len(coin.tweets.index))
        print("before merge: userdf", len(userdf.index))
        #print(coin.tweets.head())
        coin.tweets=coin.tweets.merge(userdf, left_on='user', right_on='t_userid', how='inner')

    def sort_and_clip(self,df,date):
        df['tstamp']=pd.to_datetime(df["timestamp"])
        df['t_int']=pd.to_numeric(df['tstamp'])
        df=df.sort_values('t_int')
        df=df[df['t_int']>self.date_to_int(date)]


        #df['score']=(1+df['likes']*1+df['replies']*1)*1#+df['replies']

        df['count']=1
        df['# Tweets Cumulative']=df['count'].cumsum()
        #df['Likes, Replies, Retweets']=df['score']*1
        return df

    def date_to_int(self,strclipdate):
        t=pd.to_datetime(strclipdate)
        s=pd.Series([t])
        ti=pd.to_numeric(s)
        return ti.at[0]



