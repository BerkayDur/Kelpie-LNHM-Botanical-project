from transform import get_botanist_detail, get_origin_detail, get_scientific_name, get_origin_region, get_details, botanist_details, plant_details, plant_readings, group_data, convert_to_dataframe, transform_data, remove_nan, convert_to_datetime, identify_datetime_format
import pytest
import datetime
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
        [{'soil_moisture': 15.478956774353875, 'temperature': 11.483367104821191, 'last_watered': datetime.datetime(
            2024, 6, 10, 13, 23, 1), 'recording_taken': datetime.datetime(2024, 6, 11, 13, 0, 9), 'plant_id': 8, 'name': 'Eliza Andrews'}]
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


def test_get_botanist_detail_invalid_type_dict():
    with pytest.raises(TypeError):
        get_botanist_detail(['test', 'test'], 'name')


def test_get_botanist_detail_invalid_type_str(example_valid_data):
    with pytest.raises(TypeError):
        get_botanist_detail(example_valid_data, ['name'])


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


def test_get_origin_detail_invalid_type_int(example_valid_data):
    with pytest.raises(TypeError):
        get_origin_detail(example_valid_data, 'name')


def test_get_origin_detail_invalid_type_dict(example_valid_data):
    with pytest.raises(TypeError):
        get_origin_detail([example_valid_data], 3)


def test_get_scientific_name(example_valid_data):
    assert get_scientific_name(
        example_valid_data) == "Heliconia schiedeana 'Fire and Ice'"


def test_get_scientific_name_missing(example_invalid_data):
    assert get_scientific_name(example_invalid_data) == None


def test_get_scientific_name_invalid_type_dict(example_valid_data):
    with pytest.raises(TypeError):
        get_scientific_name([example_valid_data])

def test_get_origin_region(example_valid_data):
    assert get_origin_region(example_valid_data) == 'Africa'


def test_get_origin_region_invalid_type_dict(example_valid_data):
    with pytest.raises(TypeError):
        get_origin_region([example_valid_data])


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
 

def test_get_details_invalid_type_dict(example_valid_data):
    with pytest.raises(TypeError):
        get_details([example_valid_data], 'name')


def test_get_details_invalid_type_str(example_valid_data):
    with pytest.raises(TypeError):
        get_details(example_valid_data, ['name'])


def test_identify_datetime_format():
    assert identify_datetime_format(
        "2024-06-12 15:45:30") == "%Y-%m-%d %H:%M:%S"


def test_identify_datetime_format_unknown_format():
    with pytest.raises(ValueError):
        identify_datetime_format("12/06/2024 15:45:30")


def test_convert_to_datetime_valid_format_1():
    assert convert_to_datetime(
        "Wed, 12 Jun 2024 15:45:30 GMT") == datetime.datetime(2024, 6, 12, 15, 45, 30)


def test_convert_to_datetime_invalid_format():
    with pytest.raises(ValueError):
        convert_to_datetime("12/06/2024 15:45:30") == None


def test_convert_to_datetime_non_string_input():
    assert convert_to_datetime(20240612) == None


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


def test_botanist_details_invalid_type_dict(example_valid_data):
    with pytest.raises(TypeError):
        botanist_details([example_valid_data])


def test_plant_details_invalid_type_dict(example_valid_data):
    with pytest.raises(TypeError):
        plant_details([example_valid_data])


def test_plant_readings_invalid_type_dict(example_valid_data):
    with pytest.raises(TypeError):
        plant_readings([example_valid_data])


def test_group_data_invalid_type_list():
    with pytest.raises(TypeError):
        plant_readings(['test', 1])


def test_group_data_invalid_type_contents():
    with pytest.raises(TypeError):
        plant_readings([1, 2, 4])

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
    assert plant_readings(example_valid_data) == {'soil_moisture': 15.478956774353875, 'temperature': 11.483367104821191, 'last_watered': datetime.datetime(
            2024, 6, 10, 13, 23, 1), 'recording_taken': datetime.datetime(2024, 6, 11, 13, 0, 9), 'plant_id': 8, 'name': 'Eliza Andrews'}
        


def test_plant_readings_missing_details(example_invalid_data):
    assert plant_readings(example_invalid_data) == {
        'soil_moisture': None, 'temperature': None, 'last_watered': None, 'recording_taken': None, 'plant_id': 7, 'name': None}


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
    table = transform_data([example_valid_data])

    assert isinstance(
            table['dim_plant'], pd.DataFrame)
    assert isinstance(table['dim_botanist'], pd.DataFrame)
    assert isinstance(table['fact_plant_reading'], pd.DataFrame)



def test_clean_data():
    data = [{'A': 'test',
            'B': None,
             'C': 'test'},
            {'A': 'test',
            'B': 'test',
             'C': 'test'},
            {'A': None,
            'B': None,
             'C': 'test'}]
    df_with_nan = pd.DataFrame(data)

    cleaned_data = [{'A': 'test',
                     'B': None,
                     'C': 'test'},
                    {'A': 'test',
                     'B': 'test',
                     'C': 'test'}]
    df_cleaned_expected = pd.DataFrame(cleaned_data)

    cleaned_df = remove_nan(df_with_nan, threshold=2)

    assert cleaned_df.equals(df_cleaned_expected)
