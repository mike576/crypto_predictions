from datetime import datetime
import MySQLdb
import re
import pytz


def removeEmoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  ## emoticons
                               u"\U0001F170-\U0001F251"  # symbols & pictographs
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F600-\U0001F6FF"  ## transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"  ##
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def convert_tw_datetime(twdatetime):
    #example 'Thu Mar 29 10:19:48 +0000 2018'
    datetime_object = datetime.strptime(twdatetime, '%a %b %d %H:%M:%S %z %Y')
    local_tz = pytz.timezone('Europe/Budapest')
    datetime_object = datetime_object.astimezone(local_tz)
    # example: 2018-02-28 14:12:15
    dt = datetime_object.strftime('%Y-%m-%d %H:%M:%S')
    return dt

#Tweet class with all the information we need for this program (Hashtags and the actual tweet text)
class Tweet:
    text = str()
    hashtags = []

    def __init__(self, json,is_reweet=False):

        self.id = json["id"]
        self.text = removeEmoji(str(json["text"]))
        self.user_id_str = json["user"]["id"]
        self.user_name = removeEmoji(str(json["user"]["name"]))
        self.retweet_count = json["retweet_count"]
        self.favorite_count = json["favorite_count"]
        self.hashtags = str(json["entities"]["hashtags"])



        dt = convert_tw_datetime(json["created_at"])
        self.created_at = dt

        self.lang = json["lang"]

        self.is_retweet = is_reweet
        if is_reweet==True:
            self.orig_tweet_id = json["retweeted_status"]['id']
            self.retweet_created_at = self.created_at
            self.retweeter_followers = json["user"]["followers_count"]

    def __str__(self):
        return "text: \""+str(self.text)+"\"  hashtags: "+str(self.hashtags)

    __repr__ = __str__

class TweetUser:

    def __init__(self, json):
        self.user_id = json["user"]["id"]
        self.user_name = removeEmoji(str(json["user"]["name"]))
        self.followers_count = json["user"]["followers_count"]
        self.friends_count = json["user"]["friends_count"]
        self.listed_count = json["user"]["listed_count"]
        self.favourites_count = json["user"]["favourites_count"]
        self.statuses_count = json["user"]["statuses_count"]

        dt = convert_tw_datetime(json["user"]["created_at"])
        self.user_created_at = dt

        datetime_object = datetime.now()
        nowstr = datetime_object.strftime('%Y-%m-%d %H:%M:%S')
        self.status_at = nowstr


    def __str__(self):
        return "userid: \""+str(self.id)+"\"  name: "+str(self.user_name)

    __repr__ = __str__
