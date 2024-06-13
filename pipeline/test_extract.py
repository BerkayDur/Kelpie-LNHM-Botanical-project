from extract import get_data, fetch_data, extract_data
from unittest.mock import patch, MagicMock
import requests
import pytest

@pytest.fixture
def example_url():
    return 'www.api.com'

@patch('extract.requests.get')
def test_get_data_success(mock_get, example_url):
    expected_data = {'id': 1, 'name': 'Test Plant'}
    mock_get.return_value.json.return_value = expected_data

    result = get_data(example_url, 1)

    assert mock_get.call_args[1] == {'timeout': 60}
    assert mock_get.call_count == 1
    assert mock_get.return_value.json.call_count == 1
    assert result == expected_data


@patch('extract.requests.get')
def test_http_error(mock_get, example_url):
    mock_get.side_effect = requests.exceptions.HTTPError
    result = get_data(example_url, 1)
    assert result == {'error': "HTTPError"}


@patch('extract.requests.get')
def test_timeout_error(mock_get, example_url):
    mock_get.side_effect = requests.exceptions.ReadTimeout
    result = get_data(example_url, 1)
    assert result == {'error': "Timeout"}


@patch('extract.requests.get')
def test_connection_error(mock_get, example_url):
    mock_get.side_effect = requests.exceptions.ConnectionError
    result = get_data(example_url, 1)
    assert result == {'error': "ConnectionError"}


@patch('extract.requests.get')
def test_request_exception(mock_get, example_url):
    mock_get.side_effect = requests.exceptions.RequestException
    result = get_data(example_url, 1)
    assert result == {'error': "RequestException"}


@patch('extract.get_data')
@patch('extract.Pool')
def test_fetch_data_success(mock_Pool, mock_get_data):
    fetch_data(51)
    assert mock_Pool.return_value.__enter__.return_value.map.call_count == 1
    assert mock_Pool.return_value.__enter__.return_value.map.call_args[0][1] == list(
        range(0, 51))
    assert mock_Pool.return_value.__enter__.return_value.map.call_args[0][0] == mock_get_data


@patch('extract.fetch_data')
@patch('extract.get_env_values')
def test_main(mock_get_env_values, mock_fetch_data, example_url):
    mock_get_env_values.return_value = example_url
    extract_data(51)
    mock_fetch_data.assert_called_once()
