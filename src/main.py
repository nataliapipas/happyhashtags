import tweepy
import time
from collections import defaultdict
import logging
import os
from api import Api
from tweet import Tweet
from os_utils import read_variable
from db_connector import DbConnector

logging.basicConfig(level=os.getenv('LOG_LEVEL', logging.INFO))
logger = logging.getLogger()

api = Api(read_variable('API_CONSUMER_KEY'), read_variable('API_CONSUMER_SECRET'), read_variable('API_ACCESS_TOKEN'),
          read_variable('API_ACCESS_TOKEN_SECRET')).connection


class HappyHashtagsStreamListener(tweepy.StreamListener):

    def __init__(self, db_connector, batch_size=10):
        super(HappyHashtagsStreamListener, self).__init__()
        self.batch_size = batch_size
        self.batch = self.get_clean_batch()
        self.db_connector = db_connector

    def on_status(self, status):
        tweet = Tweet(status)
        self.update_counts(tweet)

        if len(self.batch) > self.batch_size:
            logger.info("Batch:")
            logger.info(self.batch)
            self.db_connector.writeRows(rows=self.get_rows(), query="update_counts.sql")
            self.batch = self.get_clean_batch()

    def get_rows(self):
        """
        :return: Rows for the current batch
        """
        for hashtag, items in self.batch.items():
            for hour, count in items.items():
                yield (hashtag, hour, count)

    def update_counts(self, tweet):
        """
        Updates the counts of happy hashtags given a tweet
        :param tweet:
        :return:
        """
        for hashtag in tweet.hashtags:
            self.batch[hashtag][tweet.created_at_hour] += 1

    def on_error(self, status_code):
        logger.info(status_code)
        if status_code == 420:
            logger.info("420 error: sleeping for 15 min...")
            time.sleep(15 * 60)
        return True

    def get_clean_batch(self):
        return defaultdict(lambda: defaultdict(int))


myStreamListener = HappyHashtagsStreamListener(
    DbConnector(user=read_variable('POSTGRES_USER'), password=read_variable('POSTGRES_PASSWORD'),
                database=read_variable('POSTGRES_DB'), host=read_variable('POSTGRES_HOST'), logger=logger))
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

myStream.filter(track=[':)'])
