import pytest
from unittest.mock import patch, MagicMock
import boto3

from load_to_s3 import is_s3, is_bucket, generate_unique_file_name, write_file_to_bucket

def test_is_s3_valid():
    client = boto3.client('s3', region_name='eu-west-2')
    assert is_s3(client)

@pytest.mark.parametrize('inp', [boto3.client('sns', region_name='eu-west-2'), boto3.client('ec2', region_name='eu-west-2'), 'None', 's3', 23])
def test_is_s3_invalid(inp):
    assert not is_s3(inp)

@pytest.mark.parametrize('client', [boto3.client('sns', region_name='eu-west-2'), boto3.client('ec2', region_name='eu-west-2'), 'None', 's3', 23])
def test_is_bucket_invalid_client_error(client):
    with pytest.raises(TypeError):
        is_bucket(client, 'name')

@patch('load_to_s3.is_s3')
def test_is_bucket_true(mock_is_s3):
    mock_is_s3.return_value = True
    mock_client = MagicMock()
    assert is_bucket(mock_client, 'test')

@pytest.mark.parametrize('in_out', [['test.csv', 'test2024-06-12 17:56:36.093352.csv'],
                                    ['test.file.parquet', 'test.file2024-06-12 17:56:36.093352.parquet'],
                                    ['test.file.2.file-extension', 'test.file.22024-06-12 17:56:36.093352.file-extension'],])
@patch('load_to_s3.datetime')
def test_generate_unique_file_name(mock_datetime, in_out):
    mock_datetime.now.return_value.__str__.return_value = '2024-06-12 17:56:36.093352'
    assert in_out[1] == generate_unique_file_name(in_out[0])