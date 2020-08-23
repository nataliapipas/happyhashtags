import tweepy
import time
from collections import defaultdict
import logging
import os
import psycopg2
from api import Api

logging.basicConfig(level=os.getenv('LOG_LEVEL', logging.INFO))
logger = logging.getLogger(__name__)

api = Api(os.getenv('API_CONSUMER_KEY'), os.getenv('API_CONSUMER_SECRET'), os.getenv('API_ACCESS_TOKEN'),
          os.getenv('API_ACCESS_TOKEN_SECRET')).connection


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, batch_size=10):
        super(MyStreamListener, self).__init__()
        self.batch_size = batch_size
        self.batch = defaultdict(lambda: defaultdict(int))

    def get_hour(self, tweet_datetime):
        """
        Truncates the minutes and seconds attributes from a datetime object.
        :param tweet_datetime: The datetime to be truncated
        :return:
        """
        return str(tweet_datetime)[:13] + ":00:00"

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
            cursor.executemany("""
            insert into hourly_counts (hashtag, hour, count)
values (%s,%s,%s)
on conflict (hashtag, hour)
do
    update set count = EXCLUDED.count + hourly_counts.count;
""", [(hashtag, self.get_hour(hour), count) for hashtag, hour, count in rows])
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
        if hasattr(status, "extended_tweet"):
            text = status.extended_tweet["full_text"]
        else:
            text = status.text
        hashtags = [word for word in text.split() if word[0] == '#']
        for hashtag in hashtags:
            self.batch[hashtag][status.created_at] += 1

        if len(self.batch) > self.batch_size:
            logger.info("Batch:")
            logger.info(self.batch)
            self.write_to_postgres(self.batch)
            self.batch = defaultdict(lambda: defaultdict(int))

    def on_error(self, status_code):
        logger.info(status_code)
        if status_code == 420:
            logger.info("420 error: sleeping for 15 min...")
            time.sleep(15 * 60)
        return True


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

myStream.filter(track=[':)'])
