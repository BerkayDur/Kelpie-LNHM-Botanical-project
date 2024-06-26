# pylint: disable=E0611

"""Transform script"""
from datetime import datetime
import re
from os import environ as ENV
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from pymssql import connect, Connection


LATITUDE_INDEX = 0
LONGITUDE_INDEX = 1
ORIGIN_TOWN_INDEX = 2
ORIGIN_COUNTRY_CODE_INDEX = 3
ORIGIN_REGION_INDEX = 4


def get_connection() -> Connection:
    """Function that creates a connection to the database."""
    conn = connect(
        host=ENV["DB_HOST"],
        port=int(ENV["DB_PORT"]),
        database=ENV["DB_NAME"],
        user=ENV["DB_USER"],
        password=ENV["DB_PASSWORD"]
    )
    return conn


def get_botanist_detail(reading: dict, botanist_detail: str) -> str | None:
    """
    Fetches specific detail about the botanists
    """
    if not isinstance(reading, dict):
        raise TypeError('entries into a DataFrame must be of type dict')
    if not isinstance(botanist_detail, str):
        raise TypeError('botanist_detail must be of type str')
    if 'botanist' in reading:
        return reading['botanist'].get(botanist_detail)
    return None



def get_origin_detail(reading: dict, index: int) -> str | None:
    """
    Fetches specific detail about the plant's origin
    """
    if not isinstance(reading, dict):
        raise TypeError('entries into a DataFrame must be of type dict')
    if not isinstance(index, int):
        raise TypeError('index must be of type int')
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
    if not isinstance(reading, dict):
        raise TypeError('entries into a DataFrame must be of type dict')
    if not isinstance(detail, str):
        raise TypeError('botanist_detail must be of type str')
    return reading.get(detail)


def identify_datetime_format(date_string: str) -> str:
    """
    Function to match the string date format to get the 
    desired datetime format
    """
    formats = {
        "%a, %d %b %Y %H:%M:%S %Z":
        r"^[A-Za-z]{3}, \d{2} [A-Za-z]{3} \d{4} \d{2}:\d{2}:\d{2} [A-Z]{3}$",
        "%Y-%m-%d %H:%M:%S":
        r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
    }
    for format_string, pattern in formats.items():
        if re.match(pattern, date_string):
            return format_string
    raise ValueError("Unknown datetime format")


def convert_to_datetime(date_string: str) -> None | datetime:
    """
    Converts a string into datetime
    """
    if not isinstance(date_string, str):
        return None
    format_string = identify_datetime_format(date_string)
    date_time_obj = datetime.strptime(date_string, format_string)
    return date_time_obj


def get_recent_readings(plant_id: int) -> list[tuple]:
    """
    Function that returns the last 5 readings for each plant id.
    """
    db_conn = get_connection()

    with db_conn.cursor() as cur:
        cur.execute("""
        WITH RankedData AS (
            SELECT
                plant_id,
                soil_moisture,
                temperature,
                taken_at,
                ROW_NUMBER() OVER (PARTITION BY plant_id ORDER BY taken_at DESC) AS rn
            FROM alpha.FACT_plant_reading
        )
        SELECT
            plant_id,
            temperature,
            taken_at
        FROM RankedData
        WHERE rn <= 5 AND plant_id = %s
        ORDER BY taken_at DESC;
        """, (plant_id,))
        return cur.fetchall()


def convert_recent_readings_to_dataframe(data: list) -> pd.DataFrame:
    """
    Converts the results from SQL query into a dataframe and double
    checks its sorted by most recent
    """
    columns = ['plant_id', 'temperature', 'taken_at']
    df = pd.DataFrame(data, columns=columns)
    df = df.sort_values(by='taken_at', ascending=False)
    return df


def calculate_average(readings: list[int]) -> int:
    """
    Calculates the average of 4 previous readings
    """
    return sum(readings) / len(readings)


def botanist_details(reading: dict) -> dict:
    """
    Returns a dataframe of botanist details
    """
    if not isinstance(reading, dict):
        raise TypeError('entries into a DataFrame must be of type dict')
    return {'name': get_botanist_detail(reading, 'name'),
            'email': get_botanist_detail(reading, 'email'),
            'phone_no': get_botanist_detail(reading, 'phone')
            }


def plant_details(reading: dict) -> dict:
    """
    Returns a dataframe of plant details
    """
    if not isinstance(reading, dict):
        raise TypeError('entries into a DataFrame must be of type dict')
    return {'plant_id': get_details(reading, 'plant_id'),
            'plant_name': get_details(reading, 'name'),
            'scientific_name': get_scientific_name(reading),
            'origin_longitude': get_origin_detail(reading, LONGITUDE_INDEX),
            'origin_latitude': get_origin_detail(reading, LATITUDE_INDEX),
            'origin_town': get_origin_detail(reading, ORIGIN_TOWN_INDEX),
            'origin_country_code': get_origin_detail(reading, ORIGIN_COUNTRY_CODE_INDEX),
            'origin_region': get_origin_region(reading)}


def check_valid_temperature(plant_id: int, latest_temp: int) -> int:
    """
    Function to check if the most recent reading is valid. If not, it will
    return previous reading
    """
    try:
        recent_readings = get_recent_readings(plant_id)
        readings_df = convert_recent_readings_to_dataframe(recent_readings)
        readings_dictionary = readings_df.to_dict('records') #returns a list of dictionaries
        temperatures = [reading['temperature'] for reading in readings_dictionary]
        if latest_temp > calculate_average(temperatures) + 40:
            return temperatures[0]
        return latest_temp
    except Exception:  # pylint: disable=W0718
        return None


def plant_readings(reading: dict) -> dict:
    """
    Returns a dataframe of reading details
    """
    plant_id = get_details(reading, 'plant_id')
    temperature = get_details(reading, 'temperature')
    if not isinstance(reading, dict):
        raise TypeError('entries into a DataFrame must be of type dict')
    return {
            'soil_moisture': check_soil_moisture(get_details(reading, 'soil_moisture')),
            'temperature': check_valid_temperature(plant_id, temperature),
            'last_watered': convert_to_datetime(get_details(reading, 'last_watered')),
            'recording_taken': convert_to_datetime(get_details(reading, 'recording_taken')),
            'plant_id': plant_id,
            'name': get_botanist_detail(reading, 'name')
        }



def group_data(readings: list[dict]) -> tuple[list, list, list]:
    """
    Iterates through the readings and organises different parameters
    into the relevant list
    """
    if not isinstance(readings, list):
        raise TypeError('entries into a DataFrame must be of type dict')
    if not all(isinstance(value, dict) for value in readings):
        raise TypeError('entries into a DataFrame must be of type dict')

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


def check_soil_moisture(moisture: int) -> int | None:
    """
    Checks if soil moisture is below 0, which would be invalid
    """
    if not moisture or moisture < 0:
        return None
    return moisture


def remove_nan(df: pd.DataFrame, threshold: int = 2) -> pd.DataFrame:
    """
    Drops all 
    """
    df = df.dropna(thresh=threshold)
    df = df.replace(np.nan, None)
    return df


def transform_data(readings: list[dict]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Main
    """
    load_dotenv()

    plant, botanist, plant_reading = group_data(readings)

    plant_table = remove_nan(convert_to_dataframe(plant))
    botanist_table = remove_nan(convert_to_dataframe(botanist))
    reading_table = remove_nan(convert_to_dataframe(plant_reading))

    return {
            "dim_plant": plant_table, 
            "dim_botanist": botanist_table, 
            "fact_plant_reading": reading_table
            }
