'''Extract the data from db and load into S3.'''

from os import environ as CONFIG

from dotenv import load_dotenv

from load_to_s3 import load_to_s3
from extract_from_db import extract_data

if __name__ == '__main__':
    load_dotenv('.env')
    extract_data(CONFIG['TIME_FRAME_HOURS'])
    load_to_s3(CONFIG)