""""Extract script"""

from multiprocessing import Pool
import requests


API_URL = 'https://data-eng-plants-api.herokuapp.com/plants/'
NUMBER_OF_PLANTS = 52

def get_data(i: int) -> dict:
    """
    Fetches data from the API for a given index.
    """
    try:
        response = requests.get(f'{API_URL}{i}', timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        return {'error': "HTTPError"}
    except requests.exceptions.ReadTimeout:
        return {'error': "Timeout"}
    except requests.exceptions.ConnectionError:
        return {'error': "ConnectionError"}
    except requests.exceptions.RequestException:
        return {'error': "RequestException"}

    
def fetch_data(number_of_plants: int) -> list[dict]:
    """
    Fetches data for multiple indices concurrently using a pool of processes.
    """
    indices = list(range(0, number_of_plants))
    with Pool(processes=8) as pool:
        data = list(pool.imap(get_data, indices))
    return data


def extract_data(number_of_plants: int) -> list[dict]:
    """
    Main
    """
    return fetch_data(number_of_plants)

if __name__ == "__main__":
    extract_data(NUMBER_OF_PLANTS)
