# pylint: disable=W0212

'''Gets the file from a local repo and writes '''

from os import path
from os import environ as CONFIG
from datetime import datetime
from dotenv import load_dotenv
import boto3
import botocore
import botocore.client
import botocore.exceptions
import mypy_boto3_s3.client as s3_client

def get_s3_client(config: dict) -> s3_client:
    '''Returns an s3 client'''
    access_key = config["ACCESS_KEY"]
    secret_access_key = config['SECRET_ACCESS_KEY']
    return boto3.client(
        's3',
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_access_key
    )


def is_s3(client: s3_client) -> bool:
    '''Return true if s3 bucket else return false.'''
    return (isinstance(client, botocore.client.BaseClient)
            and client._service_model.service_name == 's3')


def generate_unique_file_name(file_name: str) -> str:
    '''Generate a unique file name based on datetime.now()'''
    splt = file_name.split('.')
    return '.'.join(splt[:-1]) + str(datetime.now()) + '.' + splt[-1]


def is_bucket(client: s3_client, bucket_name: str) -> bool:
    '''Return true if bucket_name exists, else false.'''
    if not is_s3(client):
        raise TypeError('client must be a boto3 client for service S3.')
    try:
        client.head_bucket(Bucket=bucket_name)
        return True
    except botocore.exceptions.ClientError:
        return False


def write_file_to_bucket(client: s3_client, file_name: str, bucket_name: str, key: str) -> None:
    '''Write a file to bucket.'''
    if not is_s3(client):
        raise TypeError('client must be a boto3 client for service S3.')
    if not path.isfile(file_name):
        raise ValueError(f'file {file_name} does not exist!')
    if not is_bucket(client, bucket_name):
        raise ValueError(f'bucket {bucket_name} does not exist!')
    client.upload_file(file_name, bucket_name, key)


def load_to_s3(config: dict) -> None:
    '''load a file specified in the config to an s3 bucket.'''
    s3 = get_s3_client(config)
    file_name = generate_unique_file_name(config['FILE_NAME'])
    write_file_to_bucket(s3, config['FILE_NAME'], config['BUCKET'], file_name)


if __name__ == '__main__':
    load_dotenv()
    load_to_s3(CONFIG)
