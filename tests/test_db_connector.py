from db_connector import DbConnector
from unittest.mock import patch
import pytest


@patch('psycopg2.connect')
def test_it_does_a_rollback_on_error(connect_mock):
    connector = DbConnector('', '', '', '', '')
    with pytest.raises(Exception):
        connector.writeRows(rows=[], query='')
    assert "().rollback" in [call[0] for call in connect_mock.mock_calls]
