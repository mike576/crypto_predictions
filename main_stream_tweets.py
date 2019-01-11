from tweepy.streaming import StreamListener
from twitter.tweet import Tweet
from twitter.tweet import TweetUser
from db.mysqldb import Database
from tweepy import OAuthHandler
from tweepy import Stream
from twitter.tweepy import TwitterApi
import json
import time



def save_user_and_tweet_to_db(tweetuser,tweet):
    db=Database()
    user_row_id=db.save_user_current_status(tweetuser)
    db.save_tweet(tweet,user_row_id)

def save_user_and_retweet_to_db(tweetuser,retweet):
    db=Database()
    user_row_id=db.save_user_current_status(tweetuser)
    db.save_retweet(retweet,user_row_id)

def create_coin_tags():
    coin_tags=['Ardor','ARDR',
               'Ark',
               'Augur','REP',
               'Cardano','ADA',
               'Dash','DASH',
               'Decred','DCR',
               'Digibyte','DGB',
               'dogecoin',#'doge',
               'Eos','EOS'
               'Ethreum','ETH',
               #'gas',
               'Golem','GNT',
               #'ICON',
                'ICX',
               'IOTA','MIOTA',
               'Lisk','LSK',
               'Litecoin','LTC',
               'Maker','MKR',
               'Monero','XMR',
               'Neblio','NEBL',
               'NEM','XEM',
               'Neo',#'NEO',
               'OmiseGo','OMG',
               'Qash','QASH',
               'Qtum','QTUM',
               'Raiblocks','XRB',
               'Ripple','XRP',
               'Siacoin','SC',
               #'steem','STEEM',
               'Stellar','XLM',
               'Stratis','STRAT',
               'Tron','TRX',
               'Ubiq','UBQ',
               'Verge','xvg',
               'Vertcoin','VTC',
               'Zcash','ZEC',
               '0x','ZRX',
               'Bitcoin','BTC',
               'BitcoinCash','BCH',
               'Theter','USDT',
               'VeChain','VEN',
               'Binance','BNB',
               'EthereumClassic','ETC',
               'Bytecoin','BCN',
               'Ontology','ONT',
               'Zilliqa','ZIL',
               'BitcoinGold','BTG',
               'Aeternity','AE',
               'Decred','DCR',
               'Bytom','BTM',
               'Nano','NANO',
               'BitShares','BTS',
               'Wanchain','WAN',
               'RChain','RHOC',
               'BitcoinPrivate','BTCP',
               'Populous',#'#PPT',

               # 'BitcoinDiamond','BCD',
               # 'Waves','WAVES',
               # 'IOST',
               # 'WaykiChain','WICC',
               # #'Status',
               # 'SNC',
               # 'Waltonchain','WTC',
               # 'Mixin','XIN',
               # 'Aion','AION',
               # 'Hshare','HSR',
               # 'Nebulas','NAS',
               # 'Loopring','LRC',
               # 'BasicAttention','BAT',
               # 'DigixDAO','DGD',
               # 'Komodo','KMD',
               # 'aelf','ELF',
               # 'CyberMiles','CMT',
               # 'HuobiToken','HT',
               # 'PIVX','PIVX',
               # 'LoomNetwork','LOOM',
               # 'MaidSafeCoin','MAID',
               # #'Gas','GAS',
               # 'Polymath','POLY',
               # 'Cortex','CTXC',
               # 'Dentacoin','DCN',
               # 'Bancor','BNT',
               # 'Cryptonex','CNX',
               # 'MonaCoin','MONA',
               # 'Ethos','ETHOS',
               # 'Elastos','ELA',
               # 'GXChain','GXS',
               # 'Mithril','MITH',
               # 'Syscoin','SYS',
               # 'ReddCoin','RDD',
               # 'Skycoin','SKY',
               # 'KyberNetwork','KNC',
               # 'Veritaseum','VERI',
               # 'Fusion','FSN',
               # 'QASH','QASH',
               # #'FunFair','FUN',
               # 'Nuls','NULS',
               # 'Substratum','SUB',
               # 'MyBitToken','MYB',
               # 'Centrality','CENNZ',
               # 'AllSports','SOC',
               # 'Electroneum','ETN',
               # 'ThetaToken','THETA',
               # 'Dragonchain','DRGN',
               # 'Enigma','ENG',
               # 'ZCoin','XZC',
               # 'Nexus','NXS',
               # 'Kin','KIN',
               # 'Storm','STORM'

               ]

    #track=['#xvg', '#verge','#neo','#omg','#omisego','#lsk','#lisk','#gnt','#golem',
    #       '$xvg', '$verge','$neo','$omg','$omisego','$lsk','$lisk','$gnt','$golem']
    track=[]
    for tag in coin_tags:
        track.append('#'+tag)
        track.append('$'+tag)
        track.append('#'+tag.lower())
        track.append('$'+tag.lower())

    print('Streaming the following searchterms:')
    print(track)
    print(len(track))

    return track


#Basic listener which parses the json, creates a tweet, and sends it to parseTweet
class TweetListener(StreamListener):

    def on_data(self, data):

        try:
            jsonData = json.loads(data)

            if 'retweeted_status' in jsonData:

                tweetuser = TweetUser(jsonData)
                tweet = Tweet(jsonData,is_reweet=True)
                save_user_and_retweet_to_db(tweetuser,tweet)

            else:
                #normal tweet
                tweetuser = TweetUser(jsonData)
                tweet = Tweet(jsonData)

                #Insert Tweet to DB
                save_user_and_tweet_to_db(tweetuser,tweet)

            #print(str())
            global parsedTweets
            parsedTweets+=1
            if parsedTweets % 100 ==0:
                print("parsedTweets: ", parsedTweets)
        except Exception as e:
            print("exception:")
            print(e)



        return True

        # We can use on_error to catch 420 errors and disconnect our stream.
    def on_error(self, status):
        print (status)
        if status == 420:
            print("waiting 5 sec")
            time.sleep(5)
            #TODO EMAIL TO WARN STOPPED SERVICE
            return False





if __name__ == '__main__':
    parsedTweets = 0
    listener = TweetListener()
    tapi=TwitterApi()
    auth = tapi.get_auth()
    stream = Stream(auth, listener)
    while True:
        try:
            stream.filter(track=create_coin_tags())
        except Exception as e:
            print("Exception: "+str(e))


