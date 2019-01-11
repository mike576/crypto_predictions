from coins.coininfo import CoinInfo
from twitter.statistics import Statistics
from twitter.tweetcollector import TweetCollector
from twitter.tweepy import TwitterApi
from twitter.tweetio import TweetIO


# Következő coin tippek:
# EOS - már több mint egy hónapja hasít töretlenül, lehet hogy van még benne potenciál, de az is lehet hogy most egy masszívabb korrekció jön.
# ICON - Sokan  sokat várnak tőle, csak félek tőle hogy mivel gyakori szó, ezért felejtős a Twitteres követése
# NANO - korábbi XRB, szintén nagyon ígéretes volt pár hónapja, szintén gyakori szó a neve.
# Qlink (QLC) nagyon új coin, a tőzsdei bevezetése óta kezd "ICO reversal pattern"-t formálni (bármit is jelentsen 🙂 )  ami miatt a kedvenc youtube-erem egyik titkos várományosa.

print('Main starts')
cinfo=CoinInfo()
coinlist=cinfo.list_coins('./data/altcoin-1hour')

## choosing first one: xyz
coin=coinlist[9]
print(coin.name)

coin.ico="2017-07-1"
coin.hashtags=['eos']

tapi=TwitterApi()

tweetcollector=TweetCollector(tapi.get_api())
#do not scrape, just once
#tweetcollector.scrape_coin_tweets(coin)

tweetio=TweetIO()
df=tweetio.read_all_scraped_tweet(coin)
df=tweetio.sort_and_clip(df,coin.ico)
coin.tweets=df
setattr( coin, 'tweets', df )

print(coin.tweets.tail())

stat=Statistics()
stat.plot_tweet_stat(coin)

#tweetcollector.collect_all_retweets(coin,tapi,1,99000)
#tweetcollector.collect_all_users(coin,tapi)

