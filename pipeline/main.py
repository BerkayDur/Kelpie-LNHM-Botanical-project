"""main"""

from os import environ as ENV
from dotenv import load_dotenv
import extract
import transform
import load

def run_pipeline(number_of_plants: int):
    """
    Runs complete ETL pipeline
    """
    api_data = extract.extract_data(number_of_plants)
    _, _, transformed_data = transform.transform_data(api_data)
    load.load_data(transformed_data)


if __name__ == '__main__':
    load_dotenv()
    num_plants = int(ENV["NUM_PLANTS"])
    run_pipeline(num_plants)
