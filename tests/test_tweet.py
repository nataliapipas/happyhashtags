from tweet import Tweet
from unittest.mock import MagicMock, Mock
import datetime

fake_datetime = datetime.datetime(2020, 1, 1, 10, 10, 10)


def test_it_truncates_hour():
    # setup
    status = MagicMock()
    status.created_at = fake_datetime
    tweet = Tweet(status)

    # action
    hour = tweet.get_hour()

    # assert
    assert hour == '2020-01-01 10:00:00'


def test_it_retrieves_text():
    # setup
    status = type('', (), {})()  # mock object
    status.text = 'magical tweet'
    status.created_at = fake_datetime
    tweet = Tweet(status)

    # action
    text = tweet.get_text()

    # assert
    assert text == 'magical tweet'


def test_it_retrieves_extended_tweet_when_available():
    # setup
    status = type('', (), {})()  # mock object
    status.text = 'text'
    status.extended_tweet = {'full_text': 'extended_tweet'}
    status.created_at = fake_datetime
    tweet = Tweet(status)

    # action
    text = tweet.get_text()

    # assert
    assert text == 'extended_tweet'
