import mypy_boto3
import botocore
import boto3
import botocore.client
import botocore.exceptions
import mypy_boto3_s3.client as s3_client

def get_client(config: dict) -> boto3.client:
    '''Returns an s3 client
    '''
    access_key = config["ACCESS_KEY"]
    secret_access_key = config['SECRET_ACCESS_KEY']
    return boto3.client(
        's3',
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_access_key
    )

def is_s3_bucket(client: boto3.client) -> bool:
    return isinstance(client, botocore.client.BaseClient) and boto3.client('s3')._service_model.service_name == 's3'


def is_bucket(client: boto3.client, bucket_name: str) -> bool:
    '''Return true if client is a valid s3 bucket and '''
    try:
        client.head_bucket(Bucket=bucket_name)
        return True
    except botocore.exceptions.ClientError:
        return False

def write_file_to_bucket():
    ...


if __name__ == '__main__':
    print(boto3.client('s3')._service_model.service_name)
    # print(isinstance(boto3.client('s3'), botocore.client.BaseClient))
    # print(botocore.client.)
    # print(isinstance(boto3.client('s3'), botocore.client))