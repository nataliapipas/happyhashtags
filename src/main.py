import tweepy
import time
from collections import defaultdict
import logging
import os
import psycopg2
from api import Api
from tweet import Tweet
from os_utils import read_query

logging.basicConfig(level=os.getenv('LOG_LEVEL', logging.INFO))
logger = logging.getLogger()

api = Api(os.getenv('API_CONSUMER_KEY'), os.getenv('API_CONSUMER_SECRET'), os.getenv('API_ACCESS_TOKEN'),
          os.getenv('API_ACCESS_TOKEN_SECRET')).connection


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, batch_size=10):
        super(MyStreamListener, self).__init__()
        self.batch_size = batch_size
        self.batch = self.get_clean_batch()

    def write_to_postgres(self, data):
        try:
            connection = psycopg2.connect(user="happy",
                                          password="hashtags",
                                          host="postgres",
                                          port="5432",
                                          database="happy_hashtags")

            cursor = connection.cursor()

            rows = []

            for hashtag, items in data.items():
                for hour, count in items.items():
                    rows.append((hashtag, hour, count))

            logger.info(rows)

            # Print PostgreSQL version
            cursor.executemany(read_query("update_counts.sql", logger), [(hashtag, hour, count) for hashtag, hour, count in rows])
            connection.commit()
            logger.info("Executed query")

        except Exception as error:
            logger.info("Error while connecting to PostgreSQL", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                logger.info("PostgreSQL connection is closed")

    def on_status(self, status):
        # check if text has been truncated
        tweet = Tweet(status)
        for hashtag in tweet.hashtags:
            self.batch[hashtag][tweet.created_at_hour] += 1

        if len(self.batch) > self.batch_size:
            logger.info("Batch:")
            logger.info(self.batch)
            self.write_to_postgres(self.batch)
            self.batch = self.get_clean_batch()

    def on_error(self, status_code):
        logger.info(status_code)
        if status_code == 420:
            logger.info("420 error: sleeping for 15 min...")
            time.sleep(15 * 60)
        return True

    def get_clean_batch(self):
        return defaultdict(lambda: defaultdict(int))


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

myStream.filter(track=[':)'])
