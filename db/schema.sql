

DROP SCHEMA `cryptopred`;
CREATE SCHEMA `cryptopred` DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;
ALTER DATABASE cryptopred CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;


use cryptopred;

drop table if EXISTS coin;
drop table if EXISTS retweet;
drop table if EXISTS tweet;
drop table if EXISTS tweet_user_history;
drop table if EXISTS prediction;

create table tweet_user_history(
   id BIGINT NOT NULL AUTO_INCREMENT,
   user_id BIGINT NOT NULL,
   user_name VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci  NOT NULL,
   followers_count INT DEFAULT 0,
   friends_count INT DEFAULT 0,
   listed_count INT DEFAULT 0,
   favourites_count INT DEFAULT 0,
   statuses_count INT DEFAULT 0,
   status_at_now TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   user_created_at DATETIME,
   PRIMARY KEY ( id )
);


create table tweet(
   id BIGINT NOT NULL,
   text VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
   user_history_row_id BIGINT NOT NULL,
   user_id_str VARCHAR(255),
   user_name VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci  NOT NULL,
   retweet_count INT DEFAULT 0,
   favorite_count INT DEFAULT 0,
   hashtags VARCHAR(2048) CHARACTER SET utf8 COLLATE utf8_unicode_ci ,
   created_at DATETIME,
   lang VARCHAR(20),
   PRIMARY KEY ( id ),
   FOREIGN KEY (user_history_row_id) REFERENCES tweet_user_history(id)
);


create table retweet(
   retweet_id BIGINT NOT NULL,
   orig_tweet_id BIGINT NOT NULL,
   retweeter_followers INT DEFAULT 0,
   retweet_created_at DATETIME,
   user_history_row_id BIGINT NOT NULL,
   user_id_str VARCHAR(255),
   PRIMARY KEY ( retweet_id ),
   FOREIGN KEY (user_history_row_id) REFERENCES tweet_user_history(id)
);

create table coin(
   id BIGINT NOT NULL AUTO_INCREMENT,
   abbrev VARCHAR(15) NOT NULL,
   name VARCHAR(255) NOT NULL,
   hashtags VARCHAR(255),
   ico DATE,
   PRIMARY KEY ( id )
);

drop table if EXISTS prediction;
create table prediction(
   id BIGINT NOT NULL AUTO_INCREMENT,
   coin_id BIGINT,
   currency_pair VARCHAR(15),
   chance DOUBLE NOT NULL,
   predicted_signal INT NOT NULL,
   period_from DATETIME,
   period_to DATETIME,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (id),
   FOREIGN KEY (coin_id) REFERENCES coin(id)
);



ALTER TABLE tweet CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE tweet CHANGE text text VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE tweet CHANGE user_name user_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE tweet_user_history CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE tweet_user_history CHANGE user_name user_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


#ALTER TABLE tweet_user_history MODIFY user_created_at DATETIME;
#ALTER TABLE tweet MODIFY created_at DATETIME;
#ALTER TABLE retweet MODIFY retweet_created_at DATETIME;

SHOW VARIABLES WHERE Variable_name LIKE 'character\_set\_%' OR Variable_name LIKE 'collation%';

CREATE INDEX i_tw_created_at ON tweet(created_at);
CREATE INDEX i_rtw_created_at ON retweet(retweet_created_at);
CREATE INDEX i_twuserhist_id ON tweet_user_history(id);
CREATE INDEX i_rtw_orig_tw_id ON retweet(orig_tweet_id);

-- if you need it:
--GRANT ALL PRIVILEGES ON *.* TO root@B020CA19.dsl.pool.netfone.hu IDENTIFIED BY 'Q584p7r2Dd78' WITH GRANT OPTION;




