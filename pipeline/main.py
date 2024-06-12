import extract
import transform
import load

NUMBER_OF_PLANTS = 51


def run_pipeline(number_of_plants: int = NUMBER_OF_PLANTS):
    api_data = extract.extract_data(number_of_plants)
    _, _, transformed_data = transform.transform_data(api_data)
    load.load_data(transformed_data)


if __name__ == '__main__':
    run_pipeline(NUMBER_OF_PLANTS)
