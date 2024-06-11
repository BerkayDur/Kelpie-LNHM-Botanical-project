""""Extract script"""

from multiprocessing import Pool
import requests


API_URL = 'https://data-eng-plants-api.herokuapp.com/plants/'


def get_data(i: int) -> dict:
    """
    Fetches data from the API for a given index.
    """
    response = requests.get(f'{API_URL}{i}', timeout=60)
    return response.json()


def fetch_data() -> list[dict]:
    """
    Fetches data for multiple indices concurrently using a pool of processes.
    """
    indices = list(range(1,51))
    with Pool(processes=8) as pool:
        data = list(pool.imap(get_data, indices))
    return data


def main():
    """
    Main
    """
    return fetch_data()

if __name__ == "__main__":
    main()
