import sys

import MySQLdb
from datetime import datetime
from datetime import timedelta
from train.prediction import Prediction
import yaml



class Database:


    def __init__(self):
        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)

        self.host=cfg['mysql']['host']
        self.db=cfg['mysql']['db']
        self.user=cfg['mysql']['user']
        self.password=cfg['mysql']['password']

        self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)

        self.connection.set_character_set('utf8')
        self.cursor = self.connection.cursor()
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except:
            print("exception")
            self.connection.rollback()

    def query(self, query):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)

        return cursor.fetchall()

    def __del__(self):
        self.connection.close()

    def n_round_hours_ago(self,n):
        last_n_hour = datetime.now() + timedelta(hours=-1*n)
        tsfrom = str(last_n_hour.strftime("%Y-%m-%d %H:00:00"))
        return tsfrom

    def check_prediction_in_db_last_hour(self,coin):
        tsfrom=self.n_round_hours_ago(1)
        tsto=self.n_round_hours_ago(0)
        return self.check_prediction_in_db(coin,tsfrom,tsto)


    def check_prediction_in_db(self,coin,tsfrom,tsto):

        currency_pair=coin.name.upper()+"BTC"
        select_query = """
        select * from prediction where period_from = '"""+tsfrom+"""' and period_to = '"""+tsto+"""' and currency_pair 
        like '%"""+currency_pair+"""%' ;
        """
        print(select_query)

        rows=dbconn.query(select_query)

        coinbinancename=''
        chance=''
        signal=''
        i=0
        for dbrow in rows:
            coinbinancename=dbrow['currency_pair']
            chance=dbrow['chance']
            signal=dbrow['predicted_signal']

            i+=1
        print("return",i,"lines: ",coinbinancename," chance:",chance,"signal",signal)
        if i==0:
            return None
        else:
            p=Prediction()
            pred=p.generate_prediction(coin,tsfrom,tsto,coinbinancename,chance,coin.treshold,signal)
            #{'currenctpair': coinbinancename, 'chance': str(chance), 'signal': signal}

            return pred


    def save_predictions(self,predictions):

        for p in predictions:
            print(p)

            query = '''INSERT INTO prediction ( currency_pair,chance,predicted_signal,period_from,period_to
                  )  VALUES (%s,%s,%s,%s,%s)'''

            print(query)

            try:
                self.cursor.execute(query, (p['currenctpair'],p['chance'],p['signal'],p['tsfrom'],p['tsto']))
                self.connection.commit()
            except MySQLdb.ProgrammingError as e:
                print("Error: {}".format(e))
                self.connection.rollback()
            except MySQLdb.DataError as e:
                print("Error: {}".format(e))
                self.connection.rollback()
            except MySQLdb.OperationalError as e:
                print("Error: {}".format(e))
                self.connection.rollback()
            except UnicodeEncodeError as e:
                print("Error: {}".format(e))
                self.connection.rollback()
            except:
                print("exception")
                print("Unexpected error:", sys.exc_info()[0])
                self.connection.rollback()



# Data Insert into the table
    def save_tweet(self, tw,user_row_id):

        if user_row_id == 0:
            print("Something went wrong, user is not saved, no returned id, skipping tweet... ")
            return

        query = '''INSERT INTO tweet (id, text,user_history_row_id,user_id_str,user_name,retweet_count,
        favorite_count,hashtags,
        created_at,lang)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

        # query = """
        # INSERT INTO tweet
        # (`id`, `text`,`user_id`,`user_name`,`retweet_count`,`favorite_count`,`hashtags`,`created_at`,`lang`)
        # VALUES
        # """
        # query+="( "+str(tweetattr.id)+",'"+str(tweetattr.text)+"','"+str(tweetattr.user_id)+"'," \
        #                                   "'"+str(tweetattr.user_name)+"',"+str(
        #  tweetattr.retweet_count)+","+str(tweetattr.favorite_count)+",'"+str(tweetattr.hashtags)+"'," \
        #                             "'"+str(tweetattr.created_at)+"','"+str(tweetattr.lang)+"' )"

        try:
            self.cursor.execute(query, (tw.id, tw.text,user_row_id, tw.user_id_str, tw.user_name, tw.retweet_count,
                                        tw.favorite_count,
                                        tw.hashtags, tw.created_at, tw.lang))
            self.connection.commit()
        except MySQLdb.ProgrammingError as e:
            print("Error: {}".format(e))
            self.connection.rollback()
        except MySQLdb.DataError as e:
            print("Error: {}".format(e))
            self.connection.rollback()
        except MySQLdb.OperationalError as e:
            print("Error: {}".format(e))
            self.connection.rollback()
        except UnicodeEncodeError as e:
            print("Error: {}".format(e))
            self.connection.rollback()
        except:
            print("exception")
            print("Unexpected error:", sys.exc_info()[0])
            self.connection.rollback()


            # print(query)
            # self.insert(query)

    # Retweet Data Insert into the table
    def save_retweet(self, tw,user_row_id):

        query = '''INSERT INTO retweet (retweet_id, orig_tweet_id,retweeter_followers,retweet_created_at,
        user_history_row_id,user_id_str)  VALUES (%s,%s,%s,%s,%s,%s)'''


        try:
            self.cursor.execute(query, (tw.id, tw.orig_tweet_id, tw.retweeter_followers, tw.retweet_created_at,
                                        user_row_id,tw.user_id_str))
            self.connection.commit()
        except MySQLdb.ProgrammingError as e:
            print("Error: {}".format(e))
            self.connection.rollback()
        except MySQLdb.DataError as e:
            print("Error: {}".format(e))
            self.connection.rollback()
        except MySQLdb.OperationalError as e:
            print("Error: {}".format(e))
            self.connection.rollback()
        except UnicodeEncodeError as e:
            print("Error: {}".format(e))
            self.connection.rollback()
        except:
            print("exception")
            print("Unexpected error:", sys.exc_info()[0])
            self.connection.rollback()

    # Retweet Data Insert into the table
    def save_user_current_status(self, tweetuser):

        query = '''INSERT INTO tweet_user_history (user_id, user_name,followers_count,friends_count,listed_count,
        favourites_count,statuses_count,user_created_at)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'''


        try:
            self.cursor.execute(query, (tweetuser.user_id,tweetuser.user_name,tweetuser.followers_count,tweetuser.friends_count,
                                        tweetuser.listed_count,tweetuser.favourites_count,tweetuser.statuses_count,
                                        tweetuser.user_created_at))
            id = self.cursor.lastrowid
            self.connection.commit()
            return id
        except MySQLdb.ProgrammingError as e:
            print("Error: {}".format(e))
            self.connection.rollback()
        except MySQLdb.DataError as e:
            print("Error: {}".format(e))
            self.connection.rollback()
        except MySQLdb.OperationalError as e:
            print("Error: {}".format(e))
            self.connection.rollback()
        except UnicodeEncodeError as e:
            print("Error: {}".format(e))
            self.connection.rollback()
        except:
            print("exception")
            print("Unexpected error:", sys.exc_info()[0])
            self.connection.rollback()
        return 0
    # print(query)
    # self.insert(query)

    def get_earliest_date_in_db(self,coin):

        first_hashtag=coin.hashtags[0]
        select_query = """
        SELECT * FROM tweet where text like '%"""+first_hashtag+"""%' order by created_at asc limit 1;
        """
        print(select_query)

        rows=dbconn.query(select_query)
        created_at=''
        i=0
        for dbrow in rows:
            created_at=dbrow['created_at']
            i+=1
        print("earliest date:",created_at)
        return created_at


dbconn = Database()

if __name__ == "__main__":
    db = Database()

    # CleanUp Operation
    # del_query = "DELETE FROM basic_python_database"
    # db.insert(del_query)

    # Data Insert into the table
    query = """
        INSERT INTO tweet
        (`tweet_id`, `text`,`user_id`,`hashtags`,`creation_date`)
        VALUES
        ( 22,'userid test','hash hash','2018-02-28 14:12:15')
        """

    # db.query(query)
    db.insert(query)

    print('done')
    # Data retrieved from the table
    # select_query = """
    #    SELECT * FROM basic_python_database
    #    WHERE age = 21
    #    """

    # people = db.query(select_query)

    # for person in people:
    #    print "Found %s " % person['name']
