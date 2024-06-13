"""main"""

from os import environ as ENV
import logging
from dotenv import load_dotenv
import extract
import transform
import load


def run_pipeline(number_of_plants: int):
    """
    Runs complete ETL pipeline
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting ETL pipeline")

    api_data = extract.extract_data(number_of_plants)
    logging.info("Data extraction complete.")
    transformed_data = transform.transform_data(api_data)
    # print(transformed_data['dim_plant'])
    # print(transformed_data['dim_botanist'])
    # print(transformed_data['fact_plant_reading'])
    logging.info("Data transformation complete.")
    load.load_data(transformed_data['fact_plant_reading'])
    logging.info("Data loading complete.")


if __name__ == '__main__':
    load_dotenv()
    num_plants = int(ENV["NUM_PLANTS"])
    run_pipeline(num_plants)
