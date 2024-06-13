'''Lambda handler for extra_load from db to s3'''

from os import environ as CONFIG
from dotenv import load_dotenv

from load_to_s3 import load_to_s3
from extract_from_db import extract_and_delete_data

def handler(event=None, context=None):
    '''Lambda handler for reading/deleting data from
    database and writing to s3.'''
    try:
        load_dotenv(0)
        extract_and_delete_data()
        load_to_s3(CONFIG)
        return {
            'status' : 'success'
        }
    except Exception as e:
        return {
            'status' : 'error',
            "error" : str(e)
        }
