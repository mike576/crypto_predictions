from coins.coininfo import CoinInfo
from coins.coinprice import CoinPrice
from twitter.statistics import Statistics
from twitter.tweetio import TweetIO
from twitter.sentiment import SentimentAnalyzer
from coins.coin import Coin
import pandas as pd

print('Main starts')
#cinfo=CoinInfo()
#coinlist=cinfo.list_coins('./data/altcoin-1hour')

## choosing first one: neo
#coin=coinlist[19]
coin=Coin()
coin.path="./data/altcoin-1hour/ada.csv"
coin.name="ada"
coin.ico="2017-10-01"
#coin.ico="2016-02-17"





tweetio=TweetIO()
coin.read_from_storeage("prepare1")
print(coin.tweets.columns)
print(coin.retweets.columns)
df=tweetio.sort_and_clip(coin.tweets,coin.ico)
coin.tweets=df


## MULTIPLYING RETWEETS FOLLOWERS

print("multiplying nr. of retweet followers by sentiments.")
sentanalyzer=SentimentAnalyzer()
sentanalyzer.merge_tweets_with_retweets(coin)
#print(coin.tweets)
sentanalyzer.sent_mul_tweet_followers(coin)
sentanalyzer.sent_mul_retweet_followers(coin)

print(len(coin.retweets))
print(coin.retweets.tail())

## GROUPING RETWEETS BY HOUR

print("grouping retweets by hour basis")
sentanalyzer.group_retweet_by_hour(coin)
print(coin.grtdf.head())

print("grouping tweets by hour basis")
sentanalyzer.group_tweet_by_hour(coin)
print(coin.gtdf.tail())


## COIN PRICE
coinprice=CoinPrice()
coinprice.read_and_sort_price(coin)

print(coin.pricehourly.tail())

phase="prepare2"
coin.save_to_storeage(phase)

