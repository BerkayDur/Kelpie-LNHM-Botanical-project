'''SNS client.'''

from os import environ as CONFIG
from dotenv import load_dotenv
import boto3

def get_sns_client(config: dict) -> object:
    '''returns sns client'''
    access_key = config['ACCESS_KEY']
    secret_access_key = config['SECRET_ACCESS_KEY']
    return boto3.client(
        'sns',
        region_name='eu-west-2',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key
    )

def publish_to_topic(config:dict, **kwargs) -> None:
    '''Publish message to an SNS topic.'''
    sns = get_sns_client(config)
    sns.publish(
        TopicArn=config['SNS_ARN'],
        **kwargs
    )

if __name__ == '__main__':
    load_dotenv()
    publish_to_topic(CONFIG, Message="Hello")
