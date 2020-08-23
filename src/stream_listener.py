import tweepy
from tweet import Tweet
import time
from collections import defaultdict


class HappyHashtagsStreamListener(tweepy.StreamListener):

    def __init__(self, db_connector, logger, batch_size=10):
        super(HappyHashtagsStreamListener, self).__init__()
        self.batch_size = batch_size
        self.batch = self.get_clean_batch()
        self.db_connector = db_connector
        self.logger = logger

    def on_status(self, status):
        tweet = Tweet(status)
        self.update_counts(tweet)

        if len(self.batch) > self.batch_size:
            self.logger.info("Batch:")
            self.logger.info(self.batch)
            self.db_connector.writeRows(rows=self.get_rows(), query="update_counts.sql")
            self.batch = self.get_clean_batch()

    def get_rows(self):
        """
        :return: Rows for the current batch
        """
        for hashtag, items in self.batch.items():
            for hour, count in items.items():
                yield (hashtag, hour, count)

    def update_counts(self, tweet: Tweet):
        """
        Updates the counts of happy hashtags given a tweet
        :param tweet:
        :return:
        """
        for hashtag in tweet.hashtags:
            self.batch[hashtag][tweet.created_at_hour] += 1

    def on_error(self, status_code: int):
        self.logger.info(status_code)
        if status_code == 420:
            self.logger.info("420 error: sleeping for 15 min...")
            time.sleep(15 * 60)
        return True

    def get_clean_batch(self):
        return defaultdict(lambda: defaultdict(int))
