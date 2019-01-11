import tweepy
from tweepy import OAuthHandler
 
consumer_key = 'r0vHGL20VO5YfXLhCoHimm4o5'
consumer_secret = '7VuzoBLEFZATkrYXj13fVZ53jnjcfT4cfL7SlHD6gF64udqRTN'
access_token = '3301731023-SExGOkbxz0emgWdmgI2QqPoEGsIfP2yCc00SSmp'
access_secret = 'vtbP2P3yyNQlz4IWIaDPVVs76XGr0wjkvWv2uKkmYoWms'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)


for status in tweepy.Cursor(api.home_timeline).items(2):
    # Process a single status
    print(status.text)



