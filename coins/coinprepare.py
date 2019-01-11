

from twitter.tweetcollector import TweetCollector
from twitter.tweetio import TweetIO
from coins.binance import BinanceApi
from twitter.sentiment import SentimentAnalyzer


PHASE = "rt"

class CoinPrepare:
    def do_prepare(self,coin,specific_hour,n_hours=48):

        # pd.set_option('display.max_rows', 99)
        # pd.set_option('precision', 10)
        # pd.set_option('display.width', 1000)
        #
        #

        #Getting Tweets from DB
        tweetio = TweetIO()
        df=tweetio.read_db_tweet_last_n_hour_by_specific_hour_by_coin(coin,specific_hour,n_hours)
        coin.tweets = df
        print("tweets from DB: ")
        print(len(df))

        #Filter and sort tweets
        #tapi = TwitterApi() we dont need twitter connection:
        tweetcollector = TweetCollector(None)
        df = tweetcollector.filter_tweets(coin.tweets)
        df = tweetio.sort_and_clip(df, coin.loadtime)
        coin.tweets = df
        print("tweets>: ")
        print(len(df))

        #Collect retweets, users
        rdf=tweetio.read_db_retweet_last_n_hour_by_specific_hour_by_coin(coin,specific_hour,n_hours)
        setattr(coin, 'retweets', rdf)

        print("retweets>: ")
        #print(rdf)
        udf=tweetio.read_db_referenced_users(coin)
        print("Users>: ")
        print(len(udf))

        #tweetcollecto
        # r.collect_all_users(coin, tapi, tmpdir=tmpd)

        ##PREPARE 1
        #df = tweetio.read_all_scraped_retweet(coin, tmpd)



        ## MERGING TWEET FOLLOWERS
        #tweetio.read_users_for_tweets(coin, tmpd)
        print("nr. of tweets before merge:")
        print(len(coin.tweets))
        coin.tweets=coin.tweets.merge(udf, left_on='user_history_row_id', right_on='user_row_id', how='inner')
        print("nr. of tweets after merge:")
        print(len(coin.tweets))

        sid = SentimentAnalyzer()
        #only with multicore CPU:
        #dfsents = sid.paralellanalyse(coin.tweets)
        #this with singlecore CPU:
        dfsents = sid.analysedf(coin.tweets)
        # print(dfsents.head())
        print("coin.tweets ready.")

        setattr(coin, 'tweets', dfsents)

        # PREPARE 2

        #df = tweetio.sort_and_clip(coin.tweets, coin.ico)
        #coin.tweets = df


        ## MULTIPLYING RETWEETS FOLLOWERS

        print("multiplying nr. of retweet followers by sentiments.")
        sentanalyzer = SentimentAnalyzer()
        sentanalyzer.merge_tweets_with_retweets(coin)
        sentanalyzer.sent_mul_tweet_followers(coin)
        sentanalyzer.sent_mul_retweet_followers(coin)

        print(len(coin.retweets))
        #print(coin.retweets.head())

        ## GROUPING RETWEETS BY HOUR

        print("grouping retweets by hour basis")
        sentanalyzer.group_retweet_by_hour(coin)
        #print(coin.grtdf.head())

        print("grouping tweets by hour basis")
        sentanalyzer.group_tweet_by_hour(coin)
        #print(coin.gtdf.head())


        print("RETWEET S")
        #print(coin.retweets)
        print(len(coin.retweets))

        print("TWEETS")
        #print(coin.tweets)
        print(len(coin.tweets))

        print("USERS")
        #print(udf)
        print(len(udf))

        ## Setting in prices:
        bapi=BinanceApi()
        coin_price = bapi.collect_coindata(coin,specific_hour)
        setattr(coin, 'pricehourly', coin_price)

        coin.save_to_storeage(PHASE, tmpdir='runtime/')

        return coin