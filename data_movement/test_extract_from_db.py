from extract_from_db import get_the_time, load_into_parquet
from unittest.mock import patch
import pytest

@pytest.mark.parametrize('inp', [-1, -5, -110, '5', '2', 'cheese'])
@patch('extract_from_db.DEFAULT_TIME_FRAME_HOURS')
@patch('extract_from_db.timedelta')
@patch('extract_from_db.datetime')
def test_get_the_time_default_time(mock_datetime, mock_timedelta, mock_default_time_frame_hours, inp):
    get_the_time(-5)
    assert mock_timedelta.call_args[1]['hours'] == mock_default_time_frame_hours


@patch('extract_from_db.DEFAULT_TIME_FRAME_HOURS')
@patch('extract_from_db.timedelta')
@patch('extract_from_db.datetime')
def test_get_the_time_valid(mock_datetime, mock_timedelta, mock_default_time_frame_hours):
    get_the_time(24)
    assert mock_datetime.now.call_count == 1
    assert mock_timedelta.call_count == 1
    assert mock_timedelta.call_args[1]['hours'] == 24


@pytest.mark.parametrize('fake_data', [(1,), {'hi':1}, {2,4,522,3,3}, 'adb', 234, 23.0])
def test_load_into_parquet_invalid_data(fake_data):
    with pytest.raises(TypeError):
        load_into_parquet(fake_data, ['test', '2'])

@pytest.mark.parametrize('fake_cols', [(1,), {'hi':1}, {2,4,522,3,3}, 'adb', 234, 23.0])
def test_load_into_parquet_invalid_cols_type(fake_cols):
    with pytest.raises(TypeError):
        load_into_parquet(['1', 2], fake_cols)

@pytest.mark.parametrize('fake_cols', [['a', 2], ['a', 'b', 'c', 234.30], ['a', []]])
def test_load_into_parquet_invalid_cols_item_type(fake_cols):
    with pytest.raises(TypeError):
        load_into_parquet(['1', 2], fake_cols)