import nltk
import multiprocessing as mp
import pandas as pd

from nltk.sentiment.vader import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    def __init__(self):
        nltk.download('vader_lexicon')
        self.sid = SentimentIntensityAnalyzer()

    def analysedf(self,df):
        print("Sentiment analyzing df's text column.")
        dfsent=df
        print("len(dfsent)",len(dfsent))

        dfsent['sent_pos']=dfsent['text'].map(lambda x: self.sid.polarity_scores(x)['pos'])
        dfsent['sent_neg']=dfsent['text'].map(lambda x: self.sid.polarity_scores(x)['neg'])
        dfsent['sent_neu']=dfsent['text'].map(lambda x: self.sid.polarity_scores(x)['neu'])
        dfsent['sent_compound']=dfsent['text'].map(lambda x: self.sid.polarity_scores(x)['compound'])

        print("analysedf finished")
        return dfsent

    def analyse_worker(self,args):
        print("Sentiment analyzing df's text column.")
        df,newcolname,feature=args
        dfsent=df
        print("len(dfsent)",len(dfsent))

        dfsent[newcolname]=dfsent['text'].map(lambda x: self.sid.polarity_scores(x)[feature])
        return dfsent


    def paralellanalyse(self,df):
        print(__name__)
        print("analyzing coin")
        data=([df,'sent_pos','pos'],[df,'sent_neg','neg'],[df,'sent_neu','neu'],[df,'sent_compound','compound'])
        if __name__ == 'twitter.sentiment':
            with mp.Pool() as pool:
                dfsent = pool.map(self.analyse_worker, data)

        i=0
        for d in data:
            #print(dfsent[i][d[1]])
            df[d[1]]=dfsent[i][d[1]]
            i+=1
        return df

    def merge_tweets_with_retweets(self,coin):
        coin_retweet_sent=coin.retweets.merge(coin.tweets,how='left',left_on='orig_tweet_id',right_on='id')
        #print((coin_retweet_sent[coin_retweet_sent["sent_neg"]-0.2>coin_retweet_sent['sent_pos']]['text']))
        setattr( coin, 'retweets', coin_retweet_sent)


    def sent_mul_retweet_followers(self,coin):
        coin_retweet_sent=coin.retweets
        f = lambda x, y : x*y
        coin_retweet_sent['posmulrfollower'] = coin_retweet_sent[['sent_pos','retweeter_followers']].apply(lambda x: f(*x), axis=1)
        coin_retweet_sent['negmulrfollower'] = coin_retweet_sent[['sent_neg','retweeter_followers']].apply(lambda x: f(*x), axis=1)
        coin_retweet_sent['neumulrfollower'] = coin_retweet_sent[['sent_neu','retweeter_followers']].apply(lambda x: f(*x), axis=1)
        coin_retweet_sent['compmulrfollower'] = coin_retweet_sent[['sent_compound','retweeter_followers']].apply(lambda x: f(*x), axis=1)

    def sent_mul_tweet_followers(self,coin):
        f = lambda x, y : x*y
        coin_tweet=coin.tweets
        coin_tweet['follower_count']=coin_tweet['follower_count'].astype(float)
        #print(coin_tweet.head())
        print(len(coin_tweet))
        if(len(coin_tweet) >0):
            coin_tweet['posmulfollower'] = coin_tweet[['sent_pos','follower_count']].apply(lambda x: f(*x), axis=1)
            coin_tweet['negmulfollower'] = coin_tweet[['sent_neg','follower_count']].apply(lambda x: f(*x), axis=1)
            coin_tweet['neumulfollower'] = coin_tweet[['sent_neu','follower_count']].apply(lambda x: f(*x), axis=1)
            coin_tweet['compmulfollower'] = coin_tweet[['sent_compound','follower_count']].apply(lambda x: f(*x), axis=1)
        else:
            coin_tweet['posmulfollower']=0
            coin_tweet['negmulfollower']=0
            coin_tweet['neumulfollower']=0
            coin_tweet['compmulfollower']=0



    def group_retweet_by_hour(self,coin):
        coin_retweet_sent=coin.retweets
        coin_retweet_sent['datetime']=pd.to_datetime(coin_retweet_sent['retweet_created_at'],format='%Y-%m-%d %X')
        times = pd.DatetimeIndex(coin_retweet_sent.datetime)
        grt=coin_retweet_sent.groupby([times.year, times.month, times.day,times.hour]).retweeter_followers.sum()
        grtdf=pd.DataFrame(grt)
        grtdf['max_datetime']=coin_retweet_sent.groupby([times.year, times.month, times.day,times.hour]).datetime.max()
        grtdf['retweet_count']=coin_retweet_sent.groupby([times.year, times.month, times.day,times.hour]).retweeter_followers.count()
        if(len(coin_retweet_sent) >0):
            grtdf['sum_posmulrfollower']=coin_retweet_sent.groupby([times.year, times.month, times.day,times.hour]).posmulrfollower.sum()
            grtdf['sum_negmulrfollower']=coin_retweet_sent.groupby([times.year, times.month, times.day,times.hour]).negmulrfollower.sum()
            grtdf['sum_neumulrfollower']=coin_retweet_sent.groupby([times.year, times.month, times.day,times.hour]).neumulrfollower.sum()
            grtdf['sum_compmulrfollower']=coin_retweet_sent.groupby([times.year, times.month, times.day,times.hour]).compmulrfollower.sum()
        else:
            grtdf['sum_posmulrfollower']=0
            grtdf['sum_negmulrfollower']=0
            grtdf['sum_neumulrfollower']=0
            grtdf['sum_compmulrfollower']=0
        setattr( coin, 'grtdf', grtdf)

    def group_tweet_by_hour(self,coin):
        coin_tweet=coin.tweets
        times = pd.DatetimeIndex(coin_tweet.tstamp)
        gt=coin_tweet.groupby([times.year, times.month, times.day,times.hour]).follower_count.sum()
        gtdf=pd.DataFrame(gt)
        gtdf['max_datetime']=coin_tweet.groupby([times.year, times.month, times.day,times.hour]).tstamp.max()
        gtdf['tweet_count']=coin_tweet.groupby([times.year, times.month, times.day,times.hour]).follower_count.count()
        if(len(coin_tweet) >0):
            gtdf['sum_posmulfollower']=coin_tweet.groupby([times.year, times.month, times.day,times.hour]).posmulfollower.sum()
            gtdf['sum_negmulfollower']=coin_tweet.groupby([times.year, times.month, times.day,times.hour]).negmulfollower.sum()
            gtdf['sum_neumulfollower']=coin_tweet.groupby([times.year, times.month, times.day,times.hour]).neumulfollower.sum()
            gtdf['sum_compmulfollower']=coin_tweet.groupby([times.year, times.month, times.day,times.hour]).compmulfollower.sum()
        else:
            gtdf['sum_posmulfollower']=0
            gtdf['sum_negmulfollower']=0
            gtdf['sum_neumulfollower']=0
            gtdf['sum_compmulfollower']=0
        setattr( coin, 'gtdf', gtdf)
