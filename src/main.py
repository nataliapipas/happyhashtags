import tweepy
import logging
from api import Api
from os_utils import read_variable
from db_connector import DbConnector
from stream_listener import HappyHashtagsStreamListener

logging.basicConfig(level=read_variable('LOG_LEVEL', logging.INFO))
logger = logging.getLogger()

HAPPY_HASHTAGS = [':)']


def get_api_connection():
    """
    Reads variables to configure and create an API object
    :return: The API connection
    """
    consumer_key = read_variable('API_CONSUMER_KEY')
    consumer_secret = read_variable('API_CONSUMER_SECRET')
    access_token = read_variable('API_ACCESS_TOKEN')
    access_token_secret = read_variable('API_ACCESS_TOKEN_SECRET')
    return Api(consumer_key, consumer_secret, access_token, access_token_secret).connection


def get_db_connector():
    user = read_variable('POSTGRES_USER')
    password = read_variable('POSTGRES_PASSWORD')
    database = read_variable('POSTGRES_DB')
    host = read_variable('POSTGRES_HOST')
    return DbConnector(user=user, password=password,
                       database=database, host=host,
                       logger=logger)


def get_stream_listener(db_connector):
    return HappyHashtagsStreamListener(db_connector=db_connector, logger=logger)


def start_stream(api_connection, listener):
    stream = tweepy.Stream(auth=api_connection.auth, listener=listener)
    stream.filter(track=HAPPY_HASHTAGS)


def main():
    api_connection = get_api_connection()
    db_connector = get_db_connector()
    stream_listener = get_stream_listener(db_connector)
    start_stream(api_connection, stream_listener)


if __name__ == "__main__":
    main()
