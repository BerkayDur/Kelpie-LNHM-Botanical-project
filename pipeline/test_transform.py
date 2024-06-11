from transform import get_botanist_detail, get_origin_detail, get_scientific_name, get_origin_region, get_details, botanist_details, plant_details, plant_readings, group_data, convert_to_dataframe, main
import pytest
import pandas as pd
from unittest.mock import patch

@pytest.fixture
def example_valid_data():
    return {
        "botanist": {
            "email": "eliza.andrews@lnhm.co.uk",
            "name": "Eliza Andrews",
            "phone": "(846)669-6651x75948"
        },
        "images": {
            "license": 451,
            "license_name": "CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
            "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
            "medium_url": "https://perenual.com/storage/image/upgrade_access.jpg",
            "original_url": "https://perenual.com/storage/image/upgrade_access.jpg",
            "regular_url": "https://perenual.com/storage/image/upgrade_access.jpg",
            "small_url": "https://perenual.com/storage/image/upgrade_access.jpg",
            "thumbnail": "https://perenual.com/storage/image/upgrade_access.jpg"
        },
        "last_watered": "Mon, 10 Jun 2024 13:23:01 GMT",
        "name": "Bird of paradise",
        "origin_location": [
            "5.27247",
            "-3.59625",
            "Bonoua",
            "CI",
            "Africa/Abidjan"
        ],
        "plant_id": 8,
        "recording_taken": "2024-06-11 13:00:09",
        "scientific_name": [
            "Heliconia schiedeana 'Fire and Ice'"
        ],
        "soil_moisture": 15.478956774353875,
        "temperature": 11.483367104821191
    }


@pytest.fixture
def example_invalid_data():
    return {"error": "plant not found", "plant_id": 7}

@pytest.fixture
def example_expected_output():
    return ([{
        'plant_id': 8,
        'plant_name': 'Bird of paradise',
        'scientific_name': "Heliconia schiedeana 'Fire and Ice'",
        'origin_longitude': '-3.59625',
        'origin_latitude': '5.27247',
        'origin_town': 'Bonoua',
        'origin_country_code': 'CI',
        'origin_region': 'Africa'
    }],
        [{
            'name': 'Eliza Andrews',
            'email': 'eliza.andrews@lnhm.co.uk',
            'phone_no': '(846)669-6651x75948'}],
        [{
            'soil_moisture': 15.478956774353875,
            'temperature': 11.483367104821191,
            'last_watered': 'Mon, 10 Jun 2024 13:23:01 GMT',
            'recording_taken': '2024-06-11 13:00:09'
        }]
    )


def test_get_botanist_name(example_valid_data):
    assert get_botanist_detail(example_valid_data, 'name') == "Eliza Andrews"


def test_get_botanist_email(example_valid_data):
    assert get_botanist_detail(
        example_valid_data, 'email') == "eliza.andrews@lnhm.co.uk"


def test_get_botanist_phone(example_valid_data):
    assert get_botanist_detail(
        example_valid_data, 'phone') == "(846)669-6651x75948"


def test_get_botanist_missing_detail(example_invalid_data):
    assert get_botanist_detail(
        example_invalid_data, 'name') == None


def test_get_origin_latitude(example_valid_data):
    assert get_origin_detail(example_valid_data, 0) == "5.27247"

def test_get_origin_longitude(example_valid_data):
    assert get_origin_detail(example_valid_data, 1) == "-3.59625"


def test_get_origin_town(example_valid_data):
    assert get_origin_detail(example_valid_data, 2) == "Bonoua"

def test_get_origin_country_code(example_valid_data):
    assert get_origin_detail(example_valid_data, 3) == "CI"


def test_get_origin_missing_values(example_invalid_data):
    assert get_origin_detail(example_invalid_data, 3) == None


def test_get_scientific_name(example_valid_data):
    assert get_scientific_name(
        example_valid_data) == "Heliconia schiedeana 'Fire and Ice'"


def test_get_scientific_name_missing(example_invalid_data):
    assert get_scientific_name(example_invalid_data) == None


def test_get_origin_region(example_valid_data):
    assert get_origin_region(example_valid_data) == 'Africa'


def test_get_temperature(example_valid_data):
    assert get_details(example_valid_data,
                       'temperature') == 11.483367104821191


def test_get_soil_moisture(example_valid_data):
    assert get_details(example_valid_data,
                       'soil_moisture') == 15.478956774353875


def test_get_last_watered(example_valid_data):
    assert get_details(example_valid_data,
                       'last_watered') == 'Mon, 10 Jun 2024 13:23:01 GMT'


def test_get_recording_taken(example_valid_data):
    assert get_details(example_valid_data,
                       'recording_taken') == '2024-06-11 13:00:09'


def test_get_detail_missing(example_invalid_data):
    assert get_details(example_invalid_data,
                       'recording_taken') == None
    

def test_botanist_details(example_valid_data):
    assert botanist_details(example_valid_data) == {
        'name': 'Eliza Andrews',
        'email': 'eliza.andrews@lnhm.co.uk',
        'phone_no': '(846)669-6651x75948'
        }


def test_botanist_missing_details(example_invalid_data):
    assert botanist_details(example_invalid_data) == {
        'name': None,
        'email': None,
        'phone_no': None
        }


def test_plant_details(example_valid_data):
    assert plant_details(example_valid_data) == {
        'plant_id': 8,
        'plant_name': 'Bird of paradise',
        'scientific_name': "Heliconia schiedeana 'Fire and Ice'",
        'origin_longitude': '-3.59625',
        'origin_latitude': '5.27247',
        'origin_town': 'Bonoua',
        'origin_country_code': 'CI',
        'origin_region': 'Africa'
        }


def test_plant_details_missing(example_invalid_data):
    assert plant_details(example_invalid_data) == {
        'plant_id': 7,
        'plant_name': None,
        'scientific_name': None,
        'origin_longitude': None,
        'origin_latitude': None,
        'origin_town': None,
        'origin_country_code': None,
        'origin_region': None
        }


def test_plant_readings(example_valid_data):
    assert plant_readings(example_valid_data) == {
        'soil_moisture': 15.478956774353875,
        'temperature': 11.483367104821191,
        'last_watered': 'Mon, 10 Jun 2024 13:23:01 GMT',
        'recording_taken': '2024-06-11 13:00:09'
        }


def test_plant_readings_missing_details(example_invalid_data):
    assert plant_readings(example_invalid_data) == {
        'soil_moisture': None,
        'temperature': None,
        'last_watered': None,
        'recording_taken': None
    }


def test_group_data(example_valid_data, example_expected_output):
   assert group_data([example_valid_data]) == example_expected_output


def test_convert_to_dataframe():
    readings = [{
        'soil_moisture': 15.478956774353875,
        'temperature': 11.483367104821191,
        'last_watered': 'Mon, 10 Jun 2024 13:23:01 GMT',
        'recording_taken': '2024-06-11 13:00:09'
    }]
    actual_df = convert_to_dataframe(readings)

    assert isinstance(
        actual_df, pd.DataFrame)
    
    expected_columns = ['soil_moisture', 'temperature',
                        'last_watered', 'recording_taken']
    actual_columns = list(actual_df.columns)
    assert actual_columns == expected_columns

def test_main(example_valid_data):
    dim_plant, dim_botanist, fact_plant_reading = main([example_valid_data])

    assert isinstance(
            dim_plant, pd.DataFrame)
    assert isinstance(dim_botanist, pd.DataFrame)
    assert isinstance(fact_plant_reading, pd.DataFrame)