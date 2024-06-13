""""Extract script"""
from lambda_multiprocessing import Pool
import requests
from os import environ as ENV
from dotenv import load_dotenv

def get_data(api: str, i: int) -> dict:
    """
    Fetches data from the API for a given index.
    """
    try:
        response = requests.get(f'{api}{i}', timeout=60)
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
    with Pool(processes=51) as pool:
        data = list(pool.map(get_data, indices))
    return data


def extract_data(number_of_plants: int) -> list[dict]:
    """
    Main
    """
    load_dotenv()
    api_url = ENV["API_URL"]
    return fetch_data(api_url, number_of_plants)
