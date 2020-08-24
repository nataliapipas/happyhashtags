from stream_listener import HappyHashtagsStreamListener
from unittest.mock import MagicMock

fake_batch = \
    {
        '#xbox':
            {
                'fake_hour': 1,
                'fake_hour_2': 2
            },
        '#switch':
            {
                'fake_hour': 3,
                'fake_hour_2': 4
            }
    }


def test_it_returns_correct_rows():
    listener = HappyHashtagsStreamListener(MagicMock(), MagicMock())
    listener.batch = fake_batch
    rows = listener.get_rows()
    assert list(rows) == [
        ('#xbox', 'fake_hour', 1),
        ('#xbox', 'fake_hour_2', 2),
        ('#switch', 'fake_hour', 3),
        ('#switch', 'fake_hour_2', 4)
    ]


def test_it_updates_batch_counts():
    # setup
    listener = HappyHashtagsStreamListener(MagicMock(), MagicMock())
    listener.batch = fake_batch
    tweet = MagicMock()
    tweet.created_at_hour = 'fake_hour'
    tweet.hashtags = ['#xbox', '#switch']

    # action
    listener.update_counts(tweet)

    # assert
    assert listener.batch == \
           {
               '#xbox':
                   {
                       'fake_hour': 1 + 1,
                       'fake_hour_2': 2
                   },
               '#switch':
                   {
                       'fake_hour': 3 + 1,
                       'fake_hour_2': 4
                   }
           }
