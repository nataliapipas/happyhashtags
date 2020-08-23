import pytest
from os_utils import read_query, read_variable
from unittest.mock import MagicMock


def test_read_query_raises_the_expected_exception():
    with pytest.raises(FileNotFoundError):
        read_query('not_to_be_found.txt', MagicMock())


def test_read_variable_uses_default_value():
    assert read_variable('not_to_be_found', default='default') == 'default'
