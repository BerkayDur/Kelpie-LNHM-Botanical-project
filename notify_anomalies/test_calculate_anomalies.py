from unittest.mock import patch
import pytest
import pandas as pd

from calculate_anomalies import get_the_time, calculate_means, error_message, DEFAULT_TIME_FRAME_HOURS

@patch('calculate_anomalies.timedelta')
@patch('calculate_anomalies.datetime')
def test_get_the_time_valid(mock_datetime, mock_timedelta):
    get_the_time(24)
    assert mock_datetime.now.call_count == 1
    assert mock_timedelta.call_count == 1
    assert mock_timedelta.call_args[1]['hours'] == 24

@pytest.mark.parametrize('fake_hours', [-10, '10', -1, 'as32', []])
@patch('calculate_anomalies.timedelta')
@patch('calculate_anomalies.datetime')
def test_get_the_time_valid(mock_datetime, mock_timedelta, fake_hours):
    get_the_time(fake_hours)
    assert mock_datetime.now.call_count == 1
    assert mock_timedelta.call_count == 1
    assert mock_timedelta.call_args[1]['hours'] == DEFAULT_TIME_FRAME_HOURS

def test_calculate_means():
    sample_df = pd.DataFrame([
        {'plant_id': 0, 'soil_moisture': 10, 'temperature': 10},
        {'plant_id': 0, 'soil_moisture': 20, 'temperature': 30},
        {'plant_id': 0, 'soil_moisture': 30, 'temperature': 20},
        {'plant_id': 1, 'soil_moisture': 10, 'temperature': 10},
        {'plant_id': 1, 'soil_moisture': 20, 'temperature': 20},
        ])
    assert calculate_means(sample_df) == ([20.0, 15.0], [20.0, 15.0])

def test_soil_anomalies_true_true():
    sample_soil_anomalies = [15, 40]
    sample_temp_anomalies = [15, 40]
    assert error_message(sample_soil_anomalies, sample_temp_anomalies) == """Anomalies regarding the soil detected in the following plants:
['15', '40']
Anomalies regarding the temperature of the plant detected in the following plants:
['15', '40']"""

def test_soil_anomalies_true_false():
    sample_soil_anomalies = [15, 40]
    sample_temp_anomalies = []
    assert error_message(sample_soil_anomalies, sample_temp_anomalies) == """Anomalies regarding the soil detected in the following plants:
['15', '40']"""

def test_soil_anomalies_false_true():
    sample_soil_anomalies = []
    sample_temp_anomalies = [15, 40]
    assert error_message(sample_soil_anomalies, sample_temp_anomalies) == """Anomalies regarding the temperature of the plant detected in the following plants:
['15', '40']"""

def test_soil_anomalies_true_true_2():
    sample_soil_anomalies = [15, 40]
    sample_temp_anomalies = [11]
    assert error_message(sample_soil_anomalies, sample_temp_anomalies) == """Anomalies regarding the soil detected in the following plants:
['15', '40']
Anomalies regarding the temperature of the plant detected in the following plants:
['11']"""