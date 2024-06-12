from dotenv import load_dotenv
from os import environ as ENV
import main

def handler(event=None, context=None):
    try:     
        load_dotenv()
        num_plants = int(ENV["NUM_PLANTS"])
        main.run_pipeline(num_plants)

        return {
            'status': 'Success!!!!!!!!!'
        }
    except Exception as e:
        return {
            'status': 'failed :(',
            'reason': str(e)
        }
    
if __name__ == "__main__":
    print(handler())