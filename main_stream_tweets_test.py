#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import the necessary methods from tweepy library
import tweepy
import time
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API
access_token = "3301731023-SExGOkbxz0emgWdmgI2QqPoEGsIfP2yCc00SSmp"
access_token_secret = "vtbP2P3yyNQlz4IWIaDPVVs76XGr0wjkvWv2uKkmYoWms"
consumer_key = "r0vHGL20VO5YfXLhCoHimm4o5"
consumer_secret = "7VuzoBLEFZATkrYXj13fVZ53jnjcfT4cfL7SlHD6gF64udqRTN"

start_time = time.time() #grabs the system time

#This is a basic listener that just prints received tweets to stdout.This class 'Listener' is inherited from the StreamLister class
class Listener(tweepy.StreamListener):

    def __init__(self, start_time, time_limit=60):

        self.time = start_time
        self.limit = time_limit

    #on_data method of a stream listener receives all messages and calls functions according to the message type
    #he on_data method of Tweepy’s StreamListener conveniently passes data from statuses to the on_status method
    def on_data(self, data):

        print(data)
        return True

    def on_status(self, status):
        print(status.text)

    # We can use on_error to catch 420 errors and disconnect our stream.
    def on_error(self, status):
        if status == 420:
            return False
        print (status)


if __name__ == '__main__':

    #create an object of the Listner class which was inherited from the StreamListener class
    myStreamListener = Listener("Ropa")

    #This handles Twitter authetification and the connection to Twitter Streaming API
    #create an OAuthHandler instance
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    #api = tweepy.API(auth)
    #create the stream object calles stream


    stream = tweepy.streaming.Stream(auth, myStreamListener)

    #Streams will not terminate unless the connection is closed, blocking the thread. Tweepy offers a convenient async parameter on filter so the stream will run on a new thread
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'], async = True)