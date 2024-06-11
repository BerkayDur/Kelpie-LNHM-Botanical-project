from extract import get_data, fetch_data
from unittest.mock import patch, MagicMock



@patch('extract.requests.get')
def test_get_data_success(mock_get):
    mock_response = MagicMock()
    expected_data = {'id': 1, 'name': 'Test Plant'}
    mock_response.json.return_value = expected_data
    mock_get.return_value = mock_response

    result = get_data(1)

    assert result == expected_data
    mock_get.assert_called_once_with(
        'https://data-eng-plants-api.herokuapp.com/plants/1', timeout=60)

