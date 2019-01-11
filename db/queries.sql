

mysql> select * from retweet limit 1;
+--------------------+--------------------+---------------------+---------------------+---------------------+--------------------+
| retweet_id         | orig_tweet_id      | retweeter_followers | retweet_created_at  | user_history_row_id | user_id_str        |
+--------------------+--------------------+---------------------+---------------------+---------------------+--------------------+
| 982006383687151616 | 981841347890982912 |                 105 | 2018-04-05 23:25:41 |                   4 | 900710369416687616 |
+--------------------+--------------------+---------------------+---------------------+---------------------+--------------------+
1 row in set (0.00 sec)

mysql> select * from tweet limit 1;
+--------------------+--------------------------------------------------------------------------------------------------------------------------------------+---------------------+--------------------+----------------+---------------+----------------+-----------------------------------------------------------------------------------------------------------------------------------------+---------------------+------+
| id                 | text                                                                                                                                 | user_history_row_id | user_id_str        | user_name      | retweet_count | favorite_count | hashtags                                                                                                                                | created_at          | lang |
+--------------------+--------------------------------------------------------------------------------------------------------------------------------------+---------------------+--------------------+----------------+---------------+----------------+-----------------------------------------------------------------------------------------------------------------------------------------+---------------------+------+
| 982001200282423296 | 1 OmiseGO = 9.1148 USD. OMG has changed by -0.0249 USD in 30 mins. Live price: https://t.co/72qHUrkz4r #omisego #omg #cryptocurrency |                   1 | 902850250276261889 | OmiseGO Market |             0 |              0 | [{'text': 'omisego', 'indices': [103, 111]}, {'text': 'omg', 'indices': [112, 116]}, {'text': 'cryptocurrency', 'indices': [117, 132]}] | 2018-04-05 23:05:05 | en   |
+--------------------+--------------------------------------------------------------------------------------------------------------------------------------+---------------------+--------------------+----------------+---------------+----------------+-----------------------------------------------------------------------------------------------------------------------------------------+---------------------+------+
1 row in set (0.00 sec)

mysql> select * from tweet_user_history limit 1;
+----+--------------------+----------------+-----------------+---------------+--------------+------------------+----------------+---------------------+---------------------+
| id | user_id            | user_name      | followers_count | friends_count | listed_count | favourites_count | statuses_count | status_at_now       | user_created_at     |
+----+--------------------+----------------+-----------------+---------------+--------------+------------------+----------------+---------------------+---------------------+
|  1 | 902850250276261889 | OmiseGO Market |             323 |            73 |            3 |                0 |          10442 | 2018-04-05 23:05:05 | 2017-08-30 13:07:28 |
+----+--------------------+----------------+-----------------+---------------+--------------+------------------+----------------+---------------------+---------------------+
1 row in set (0.00 sec)

m

select * from tweet limit 1;

SELECT count(tweet.id) FROM tweet inner join retweet on retweet.orig_tweet_id = tweet.id
WHERE tweet.created_at > DATE_ADD(NOW(),INTERVAL -3 HOUR);

select count(retweet_id) from retweet where orig_tweet_id in (SELECT id FROM tweet
WHERE tweet.created_at > DATE_ADD(NOW(),INTERVAL -3 HOUR));

SELECT count(tweet.id) FROM tweet inner join retweet on retweet.orig_tweet_id = tweet.id
      left join tweet_user_history on tweet.user_history_row_id = tweet_user_history.id
WHERE tweet.created_at > DATE_ADD(NOW(),INTERVAL -3 HOUR);

SELECT * FROM tweet inner join retweet on retweet.orig_tweet_id = tweet.id
      left join tweet_user_history on tweet.user_history_row_id = tweet_user_history.id
WHERE tweet.created_at > DATE_ADD(NOW(),INTERVAL -1 HOUR) limit 5;


+---------------------+-------------------------------------------------------------------------------------------------------------------------------------------------+---------------------+--------------------+-----------------+---------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------+------+---------------------+---------------------+---------------------+---------------------+---------------------+--------------------+----------+--------------------+-----------------+-----------------+---------------+--------------+------------------+----------------+---------------------+---------------------+
| id                  | text                                                                                                                                            | user_history_row_id | user_id_str        | user_name       | retweet_count | favorite_count | hashtags                                                                                                                                                                                                                                                                                          | created_at          | lang | retweet_id          | orig_tweet_id       | retweeter_followers | retweet_created_at  | user_history_row_id | user_id_str        | id       | user_id            | user_name       | followers_count | friends_count | listed_count | favourites_count | statuses_count | status_at_now       | user_created_at     |
+---------------------+-------------------------------------------------------------------------------------------------------------------------------------------------+---------------------+--------------------+-----------------+---------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------+------+---------------------+---------------------+---------------------+---------------------+---------------------+--------------------+----------+--------------------+-----------------+-----------------+---------------+--------------+------------------+----------------+---------------------+---------------------+
| 1003846222560530432 | • INFO • #BTS #JIN # # # # #

 Park Seo Joon en su cuenta de Instagram:

"Muchas gracias a éste chico… https://t.co/abc32GOmJ6                  |            17046904 | 942304379960471552 | Seokjin México  |             0 |              0 | [{'text': 'BTS', 'indices': [9, 13]}, {'text': 'JIN', 'indices': [14, 18]}, {'text': '진', 'indices': [19, 21]}, {'text': '김석진', 'indices': [22, 26]}, {'text': '뷔', 'indices': [27, 29]}, {'text': '김태형', 'indices': [30, 34]}, {'text': '방탄소년단', 'indices': [35, 41]}]              | 2018-06-05 05:49:24 | es   | 1003846429138354176 | 1003846222560530432 |                  52 | 2018-06-05 05:50:13 |            17047459 | 1688932308         | 17046904 | 942304379960471552 | Seokjin México  |            5996 |           300 |           11 |             2788 |           3759 | 2018-06-05 05:49:25 | 2017-12-17 09:04:06 |
| 1003846222560530432 | • INFO • #BTS #JIN # # # # #

 Park Seo Joon en su cuenta de Instagram:

"Muchas gracias a éste chico… https://t.co/abc32GOmJ6                  |            17046904 | 942304379960471552 | Seokjin México  |             0 |              0 | [{'text': 'BTS', 'indices': [9, 13]}, {'text': 'JIN', 'indices': [14, 18]}, {'text': '진', 'indices': [19, 21]}, {'text': '김석진', 'indices': [22, 26]}, {'text': '뷔', 'indices': [27, 29]}, {'text': '김태형', 'indices': [30, 34]}, {'text': '방탄소년단', 'indices': [35, 41]}]              | 2018-06-05 05:49:24 | es   | 1003846475879677953 | 1003846222560530432 |                  59 | 2018-06-05 05:50:25 |            17047574 | 992571426602409984 | 17046904 | 942304379960471552 | Seokjin México  |            5996 |           300 |           11 |             2788 |           3759 | 2018-06-05 05:49:25 | 2017-12-17 09:04:06 |
| 1003846259612868608 | [INFO] 2017 #BTS Live Trilogy Episode Ⅲ The Wings Tour in Japan Special Edition~ at Kyocera Dome will have 4 versi… https://t.co/lXF0LZ1zPb     |            17047016 | 731207181018652672 | JIMIN BASE      |             0 |              0 | [{'text': 'BTS', 'indices': [12, 16]}]                                                                                                                                                                                                                                                            | 2018-06-05 05:49:33 | en   | 1003846531961610240 | 1003846259612868608 |                 157 | 2018-06-05 05:50:38 |            17047717 | 921635056992493569 | 17047016 | 731207181018652672 | JIMIN BASE      |           47871 |            41 |          364 |             2562 |          33156 | 2018-06-05 05:49:34 | 2016-05-13 21:39:11 |
| 1003846564480086016 | [!!!] MBC music akan menyiarkan program khusus #BTS, 7 jam, untuk ulang tahun ke 5 mereka pada 13 Juni nanti pada p… https://t.co/8PjoCs1rNu    |            17047811 | 1108908174         | BTS—ARMYTEAM    |             0 |              0 | [{'text': 'BTS', 'indices': [47, 51]}]                                                                                                                                                                                                                                                            | 2018-06-05 05:50:46 | in   | 1003846647149817856 | 1003846564480086016 |                 111 | 2018-06-05 05:51:05 |            17048052 | 868854632692432896 | 17047811 |         1108908174 | BTS—ARMYTEAM    |           51272 |          6724 |          242 |              109 |         273697 | 2018-06-05 05:50:46 | 2013-01-21 13:35:39 |
| 1003846564480086016 | [!!!] MBC music akan menyiarkan program khusus #BTS, 7 jam, untuk ulang tahun ke 5 mereka pada 13 Juni nanti pada p… https://t.co/8PjoCs1rNu    |            17047811 | 1108908174         | BTS—ARMYTEAM    |             0 |              0 | [{'text': 'BTS', 'indices': [47, 51]}]                                                                                                                                                                                                                                                            | 2018-06-05 05:50:46 | in   | 1003846648752033792 | 1003846564480086016 |                   1 | 2018-06-05 05:51:06 |            17048057 | 968044505285902337 | 17047811 |         1108908174 | BTS—ARMYTEAM    |           51272 |          6724 |          242 |              109 |         273697 | 2018-06-05 05:50:46 | 2013-01-21 13:35:39 |
+---------------------+-------------------------------------------------------------------------------------------------------------------------------------------------+---------------------+--------------------+-----------------+---------------+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------+------+---------------------+---------------------+---------------------+---------------------+---------------------+--------------------+----------+--------------------+-----------------+-----------------+---------------+--------------+------------------+----------------+---------------------+---------------------+


SELECT count(retweet_id),sum(retweeter_followers),sum(followers_count)
  FROM tweet inner join retweet on retweet.orig_tweet_id = tweet.id
  left join tweet_user_history on tweet.user_history_row_id = tweet_user_history.id
  WHERE tweet.created_at > DATE_ADD(NOW(),INTERVAL -1 HOUR)
  GROUP BY tweet.id
  limit 5;

SELECT count(retweet_id),sum(retweeter_followers),sum(followers_count),sum(retweeter_followers)+sum(followers_count)
  FROM tweet inner join retweet on retweet.orig_tweet_id = tweet.id
  left join tweet_user_history on tweet.user_history_row_id = tweet_user_history.id
  WHERE tweet.created_at > DATE_ADD(NOW(),INTERVAL -1 HOUR)
  GROUP BY tweet.id
  ;


select * from (
SELECT tweet.id,count(retweet_id) as retweetnr,sum(retweeter_followers),max(followers_count),sum(retweeter_followers)
+max(followers_count) as affected_users
  FROM tweet inner join retweet on retweet.orig_tweet_id = tweet.id
  left join tweet_user_history on tweet.user_history_row_id = tweet_user_history.id
  WHERE tweet.created_at > DATE_ADD(NOW(),INTERVAL -1 HOUR)
  GROUP BY tweet.id
) as gtweets order by affected_users desc
  limit 10
;

