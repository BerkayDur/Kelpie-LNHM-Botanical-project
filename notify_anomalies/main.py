#pylint: skip-file

'''Lambda handler for anomly detection''' 
from os import environ as CONFIG
from dotenv import load_dotenv

from calculate_anomalies import calculate_anomalies
from sns_alert import publish_to_topic

def handler(event = None, context = None) -> dict: 
    '''Handler for lambda.'''
    try:
        load_dotenv()
        message = calculate_anomalies()
        if message != "No anomalies have been detected!":
            publish_to_topic(CONFIG, Message=message)
        return {
            'status' : 'Success!!!!!!!!!'
        }
    except Exception as e:
        return {
            'status' : 'failed :(',
            'reason' : str(e)
        }
    
if __name__ == '__main__':
    load_dotenv()
    msg = calculate_anomalies()
    if msg != "No anomalies have been detected!":
        publish_to_topic(CONFIG, Message=msg)