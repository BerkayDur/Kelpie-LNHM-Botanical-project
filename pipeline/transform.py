"""Transform script"""
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


def get_details(reading: dict, detail: str) -> str | int | None:
    """
    Fetches specific details by searching through the keys
    """
    try:
        return reading[detail]
    except KeyError:
        return None


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
                    'origin_longitude': get_origin_detail(reading, 1),
                    'origin_latitude': get_origin_detail(reading, 0),
                    'origin_town': get_origin_detail(reading, 2),
                    'origin_country_code': get_origin_detail(reading, 3),
                    'origin_region': get_origin_region(reading)}


def plant_readings(reading: list[dict]) -> dict:
    """
    Returns a dataframe of reading details
    """
    return {
            'soil_moisture': get_details(reading, 'soil_moisture'),
            'temperature': get_details(reading, 'temperature'),
            'last_watered': get_details(reading, 'last_watered'),
            'recording_taken': get_details(reading, 'recording_taken')
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
    return pd.DataFrame(readings)


def clean_data(df: pd.DataFrame, threshold: int = 2) -> pd.DataFrame:
    """
    Drops all 
    """
    df = df.dropna(thresh=threshold)
    return df

def main(readings) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Main
    """
    plant, botanist, plant_reading = group_data(readings)

    dim_plant = convert_to_dataframe(plant)
    dim_botanist = convert_to_dataframe(botanist)
    fact_plant_reading = convert_to_dataframe(plant_reading)

    return clean_data(dim_plant), clean_data(dim_botanist), clean_data(fact_plant_reading)
