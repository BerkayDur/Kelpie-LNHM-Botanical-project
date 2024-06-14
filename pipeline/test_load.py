import pandas as pd
from load import upload_plant_data
from unittest.mock import patch, MagicMock


@patch("load.get_cursor")
def test_upload_data(mock_get_cursor):
    mock_conn = MagicMock()
    data = [{'A': 'test',
             'C': 'test'}]
    df = pd.DataFrame(data)
    upload_plant_data(mock_conn, df)
    assert mock_get_cursor.return_value.executemany.call_count == 1
    assert mock_conn.commit.call_count == 1
