import tweepy
from tweet import Tweet
import time
from collections import defaultdict


def get_clean_batch():
    return defaultdict(lambda: defaultdict(int))


class HappyHashtagsStreamListener(tweepy.StreamListener):

    def __init__(self, db_connector, logger, batch_size=10):
        super(HappyHashtagsStreamListener, self).__init__()
        self.batch_size = batch_size
        self.batch = get_clean_batch()
        self.db_connector = db_connector
        self.logger = logger

    def on_status(self, status):
        """
        Triggered on each new tweet that meets the filter criteria
        :param status: The object containing information to create a Tweet object
        :return:
        """
        tweet = Tweet(status)
        self.update_counts(tweet)

        if len(self.batch) > self.batch_size:
            self.db_connector.writeRows(rows=self.get_rows(), query="update_counts.sql")
            self.batch = get_clean_batch()

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
        """
        Triggered on an exception during the execution. Sleeps on error.
        :param status_code: The exception code
        :return:
        """
        self.logger.info(status_code)
        if status_code == 420:
            self.logger.info("420 error: sleeping for 15 min...")
            time.sleep(15 * 60)
        return True
