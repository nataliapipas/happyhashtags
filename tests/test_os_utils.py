import pytest
from os_utils import read_query, read_variable, read_variables
from unittest.mock import MagicMock
from unittest.mock import patch


def test_read_query_raises_the_expected_exception():
    with pytest.raises(FileNotFoundError):
        read_query('not_to_be_found.txt', MagicMock())


def test_read_variable_uses_default_value():
    assert read_variable('not_to_be_found', default='default') == 'default'


@patch('os.getenv', lambda x: "fake_" + x)
def test_it_reads_multiple_variables():
    var1, var2, var3 = read_variables('a', 'b', 'c')
    assert [var1, var2, var3] == ['fake_a', 'fake_b', 'fake_c']
