from coins.coininfo import CoinInfo
from coins.coin import Coin
from twitter.statistics import Statistics
from twitter.tweetio import TweetIO
from twitter.sentiment import SentimentAnalyzer
from twitter.tweepy import TwitterApi
from twitter.tweetcollector import TweetCollector

print('Main starts')
cinfo=CoinInfo()
coinlist=cinfo.list_coins('./data/altcoin-1hour')

## choosing first one: neo
coin=Coin()
coin.name="ada"
coin.ico="2017-10-01"
#coin.ico="2016-02-17"



tweetio=TweetIO()
print("read already scraped  retweets:")
df=tweetio.read_all_scraped_retweet(coin)
setattr( coin, 'retweets', df)
print("coin.retweets.head()")
print(coin.retweets.tail())
print("retweets done...")


tapi = TwitterApi()
tweetcollector = TweetCollector(tapi)
print("read already scraped tweets:")
df=tweetio.read_all_scraped_tweet(coin)
print("before filter: ",len(df.index))
df = tweetcollector.filter_tweets(df)
print("after filter: ",len(df.index))
print(df.columns)
df=df.rename(index=str, columns={"likes": "favorite_count","retweets": "retweet_count"})
df=tweetio.sort_and_clip(df,coin.ico)
print("after sort and clip: ",len(df.index))
print("DATA")
print(df)
coin.tweets=df
setattr( coin, 'tweets', df )
## MERGING TWEET FOLLOWERS
print("before read_users_for_tweets: ",len(coin.tweets.index))
tweetio.read_users_for_tweets(coin)
print("after read_users_for_tweets: ",len(coin.tweets.index))
sid=SentimentAnalyzer()
dfsents=sid.paralellanalyse(coin.tweets)

#print(dfsents.head())

setattr( coin, 'tweets', dfsents )
print("AFTER SETTING coin.tweets.head()")
print(coin.tweets.tail())


phase="prepare1"
coin.save_to_storeage(phase)




stat=Statistics()
#stat.plot_tweet_stat(coin)



