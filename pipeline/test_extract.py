from extract import get_data, fetch_data
from unittest.mock import patch, MagicMock


@patch('extract.requests.get')
def test_get_data_success(mock_get):
    expected_data = {'id': 1, 'name': 'Test Plant'}
    mock_get.return_value.json.return_value = expected_data

    result = get_data(1)

    assert mock_get.call_args[0][0] == 'https://data-eng-plants-api.herokuapp.com/plants/1'
    assert mock_get.call_args[1] == {'timeout': 60}
    assert mock_get.call_count == 1
    assert mock_get.return_value.json.call_count == 1
    assert result == expected_data


@patch('extract.get_data')
@patch('extract.Pool')
def test_fetch_data_success(mock_Pool, mock_get_data):
    fetch_data()
    assert mock_Pool.return_value.__enter__.return_value.imap.call_count == 1
    assert mock_Pool.return_value.__enter__.return_value.imap.call_args[0][1] == list(
        range(0, 51))
    assert mock_Pool.return_value.__enter__.return_value.imap.call_args[0][0] == mock_get_data


@patch('extract.fetch_data')
def test_main(mock_fetch_data):
    mock_fetch_data.assert_called_once
