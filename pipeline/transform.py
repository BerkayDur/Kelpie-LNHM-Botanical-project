"""Transform script"""
import pandas as pd
import extract 
from datetime import datetime

LATITUDE_INDEX = 0
LONGITUDE_INDEX = 1
ORIGIN_TOWN_INDEX = 2
ORIGIN_COUNTRY_CODE_INDEX = 3
ORIGIN_REGION_INDEX = 4




def get_botanist_detail(reading: dict, botanist_detail: str) -> str | None:
    """
    Fetches specific detail about the botanists
    """
    if not isinstance(reading, dict) or not isinstance(botanist_detail, str):
        raise TypeError('entries into a DataFrame must be of type dict')
    if 'botanist' in reading:
        return reading['botanist'].get(botanist_detail)

def get_origin_detail(reading: dict, index: int) -> str | None:
    """
    Fetches specific detail about the plant's origin
    """
    if not isinstance(reading, dict) or not isinstance(index, int):
        raise TypeError('entries into a DataFrame must be of type dict')
    try:
        return reading['origin_location'][index]
    except KeyError:
        return None


def get_scientific_name(reading: dict) -> str | None:
    """
    Fetches scientific name of the plant
    """
    if not isinstance(reading, dict):
        raise TypeError('entries into a DataFrame must be of type dict')
    try:
        return reading['scientific_name'][0]
    except KeyError:
        return None


def get_origin_region(reading: dict) -> str | None:
    """
    Fetches the region of where the plant originated from
    """
    if not isinstance(reading, dict):
        raise TypeError('entries into a DataFrame must be of type dict')
    try:
        return reading['origin_location'][ORIGIN_REGION_INDEX].split('/')[0]
    except KeyError:
        return None


def get_details(reading: dict, detail: str) -> str | int | None:
    """
    Fetches specific details by searching through the keys
    """
    return reading.get(detail)

def botanist_details(reading: list[dict]) -> dict:
    """
    Returns a dataframe of botanist details
    """
    return {'name': get_botanist_detail(reading, 'name'),
            'email': get_botanist_detail(reading, 'email'),
            'phone_no': get_botanist_detail(reading, 'phone')
            }


def plant_details(reading: list[dict]) -> dict:
    """
    Returns a dataframe of plant details
    """
    return {'plant_id': get_details(reading, 'plant_id'),
            'plant_name': get_details(reading, 'name'),
            'scientific_name': get_scientific_name(reading),
            'origin_longitude': get_origin_detail(reading, LONGITUDE_INDEX),
            'origin_latitude': get_origin_detail(reading, LATITUDE_INDEX),
            'origin_town': get_origin_detail(reading, ORIGIN_TOWN_INDEX),
            'origin_country_code': get_origin_detail(reading, ORIGIN_COUNTRY_CODE_INDEX),
            'origin_region': get_origin_region(reading)}


def convert_last_watered_to_datetime(date_string):
    if not isinstance(date_string, str):
        return None
    format_string = "%a, %d %b %Y %H:%M:%S %Z"
    date_time_obj = datetime.strptime(date_string, format_string)
    return date_time_obj


def convert_recording_time_to_datetime(date_string):
    if not isinstance(date_string, str):
        return None
    format_string = "%Y-%m-%d %H:%M:%S"
    date_time_obj = datetime.strptime(date_string, format_string)
    return date_time_obj

def plant_readings(reading: list[dict]) -> dict:
    """
    Returns a dataframe of reading details
    """
    return {
            'soil_moisture': get_details(reading, 'soil_moisture'),
            'temperature': get_details(reading, 'temperature'),
            'last_watered': convert_last_watered_to_datetime(get_details(reading, 'last_watered')),
            'recording_taken': convert_recording_time_to_datetime(get_details(reading, 'recording_taken')),
            'name': get_botanist_detail(reading, 'name'),
            'plant_name': get_details(reading, 'name')
        }

def group_data(readings: list[dict]) -> tuple[list, list, list]:
    """
    Iterates through the readings and organises different parameters
    into the relevant list
    """
    plant = []
    botanist = []
    plant_reading = []

    for reading in readings:
        plant.append(plant_details(reading))
        botanist.append(botanist_details(reading))
        plant_reading.append(plant_readings(reading))

    return plant, botanist, plant_reading


def convert_to_dataframe(readings: list[dict]) -> pd.DataFrame:
    """
    Converts a list into a dataframe
    """
    if not isinstance(readings, list):
        raise TypeError('readings must be of type list')
    if not all(isinstance(value, dict) for value in readings):
        raise TypeError('entries into a DataFrame must be of type dict')
    return pd.DataFrame(readings)


def clean_data(df: pd.DataFrame, threshold: int = 2) -> pd.DataFrame:
    """
    Drops all 
    """
    df = df.dropna(thresh=threshold)
    return df

def transform_data(readings) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Main
    """
    plant, botanist, plant_reading = group_data(readings)

    dim_plant = convert_to_dataframe(plant)
    dim_botanist = convert_to_dataframe(botanist)
    fact_plant_reading = convert_to_dataframe(plant_reading)

    return clean_data(dim_plant), clean_data(dim_botanist), clean_data(fact_plant_reading)

if __name__ == "__main__":
    plant, botanist, plant_reading = transform_data(extract.extract_data(51))
    print(plant, botanist, plant_reading)
