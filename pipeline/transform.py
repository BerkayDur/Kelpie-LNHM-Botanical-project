"""Transform script"""

import extract
import pandas as pd

def get_botanist_detail(reading: dict, botanist_detail: str) -> str | None:
    """
    Fetches specific detail about the botanists
    """
    try:
        return reading['botanist'][botanist_detail]
    except KeyError:
        return None

def get_origin_detail(reading: dict, index: str) -> str | None:
    """
    Fetches specific detail about the plant's origin
    """
    try:
        return reading['origin_location'][index]
    except KeyError:
        return None


def get_scientific_name(reading: dict) -> str | None:
    """
    Fetches scientific name of the plant
    """
    try:
        return reading['scientific_name'][0]
    except KeyError:
        return None


def get_origin_region(reading: dict) -> str | None:
    """
    Fetches the region of where the plant originated from
    """
    try:
        return reading['origin_location'][4].split('/')[0]
    except KeyError:
        return None


def get_details(reading: dict, detail: str) -> str | None:
    """
    Fetches specific details by searching through the keys
    """
    try:
        return reading[detail]
    except KeyError:
        return None


def botanist_details(data: list[dict]) -> dict:
    """
    Returns a dataframe of botanist details
    """
    return {'name': get_botanist_detail(data, 'name'),
                             'email': get_botanist_detail(data, 'email'),
                             'phone_no': get_botanist_detail(data, 'phone')
                             }


def plant_details(data: list[dict]) -> dict:
    """
    Returns a dataframe of plant details
    """
    return {'plant_id': get_details(data, 'plant_id'),
                    'plant_name': get_details(data, 'name'),
                    'scientific_name': get_scientific_name(data),
                    'origin_longitude': get_origin_detail(data, 1),
                    'origin_latitude': get_origin_detail(data, 0),
                    'origin_town': get_origin_detail(data, 2),
                    'origin_country_code': get_origin_detail(data, 3),
                    'origin_region': get_origin_region(data)}


def plant_readings(data: list[dict]) -> dict:
    """
    Returns a dataframe of reading details
    """
    return {
            'soil_moisture': get_details(data, 'soil_moisture'),
            'temperature': get_details(data, 'temperature'),
            'last_watered': get_details(data, 'last_watered'),
            'recording_taken': get_details(data, 'recording_taken')
        }


def main():
    """
    Main
    """
    bigdata = extract.fetch_data()
    plant = []
    botanist = []
    plant_reading = []

    for data in bigdata:
        plant.append(plant_details(data))
        botanist.append(botanist_details(data))
        plant_reading.append(plant_readings(data))

    dim_plant = pd.DataFrame(plant)
    dim_botanist = pd.DataFrame(botanist)
    fact_plant_reading = pd.DataFrame(plant_reading)

    return dim_plant, dim_botanist, fact_plant_reading


if __name__ == "__main__":
    main()
