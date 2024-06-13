"""
This script looks at the most recent parquet file provided and 
uses it to determine the mean readings for the plants. It then uses
the mean to determine whether incoming readings are expected or if 
they are anomalies
"""


# pylint: disable=no-name-in-module
# pylint: disable=line-too-long

from os import environ as ENV
from datetime import datetime, timedelta
import pandas as pd
from dotenv import load_dotenv
from pymssql import connect, Connection


DEFAULT_TIME_FRAME_HOURS = 24
COLUMNS = ["reading_id", "soil_moisture", "temperature", "last_watered",
           "taken_at", "plant_id", "botanist_id"]


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


def get_the_time(number_of_hours: int) -> str:
    """This function gets the time number_of_hours hours ago as a formatted string."""
    if not isinstance(number_of_hours, int) or number_of_hours < 0:
        number_of_hours = DEFAULT_TIME_FRAME_HOURS
    now = datetime.now()
    yesterday = now - timedelta(hours=number_of_hours)
    yesterday_str = yesterday.strftime('%Y-%m-%d %H:%M:%S')

    return yesterday_str


def query_and_extract_rds(time: str, conn: Connection, cols: list[str]) -> list[list]:
    """This function creates the query to get the data start from time"""
    with conn.cursor() as cur:
        cur.execute(f"""
SELECT *
FROM alpha.FACT_plant_reading
WHERE taken_at >= '{time}';
""")
        data = cur.fetchall()

    df = pd.DataFrame(data=data, columns=cols)
    df["plant_id"] = pd.to_numeric(
        df["plant_id"], errors='coerce').astype('Int64')
    return df


def get_dataframe(time: str) -> pd.DataFrame:
    """This function returns a pandas dataframe containing the plant data from the database"""
    db_conn = get_connection()
    plant_df = query_and_extract_rds(time, db_conn, COLUMNS)
    db_conn.close()

    return plant_df


def calculate_means(df: pd.DataFrame) -> list:
    """This function returns the means for both soil_moisture and temperature"""
    df_means = df.groupby("plant_id").mean()
    s_means = df_means["soil_moisture"].tolist()
    t_means = df_means["temperature"].tolist()
    return s_means, t_means


def get_recent_readings() -> list[tuple]:
    """Function that returns the last 3 readings for each plant id."""
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
    soil_moisture,
    temperature
FROM RankedData
WHERE rn <= 3
ORDER BY plant_id, taken_at DESC;
""")
        data = cur.fetchall()

    db_conn.close()

    return data


def error_message(soil_anomalies: list[int], temp_anomalies: list[int]) -> str:
    """Function that determines which error message to display"""
    if soil_anomalies and temp_anomalies:
        return f"""Anomalies regarding the soil detected in the following plants:
{[f"{plant}\n" for plant in soil_anomalies]}
Anomalies regarding the temperature of the plant detected in the following plants:
{[f"{plant}\n" for plant in temp_anomalies]}
"""
    if soil_anomalies:
        return f"""Anomalies regarding the soil detected in the following plants:
{[f"{plant}\n" for plant in soil_anomalies]}"""
    if temp_anomalies:
        return f"""Anomalies regarding the soil detected in the following plants:
{[f"{plant}\n" for plant in temp_anomalies]}"""

    return "No anomalies have been detected!"


def check_for_errors(s_mean: list[float], t_mean: list[float], readings: list[tuple], threshold: int) -> str:
    """This function compares the mean value with the values of the recent readings."""
    grouped_readings = [readings[i:i + 3] for i in range(0, len(readings), 3)]

    plants_with_soil_anomalies = []
    plants_with_temp_anomalies = []

    for subgroup in grouped_readings:
        s_errors = 0
        t_errors = 0
        for i, reading in enumerate(subgroup):
            if not reading[1]:
                s_errors += 1
            elif reading[1] > s_mean[i] + threshold or reading[1] < s_mean[i] - threshold:
                s_errors += 1

            if not reading[2]:
                t_errors += 1
            elif reading[2] > t_mean[i] + threshold or reading[2] < t_mean[i] - threshold:
                t_errors += 1

        if s_errors == 3:
            plants_with_soil_anomalies.append(subgroup[0][0])
        if t_errors == 3:
            plants_with_temp_anomalies.append(subgroup[0][0])

    resultant_message = error_message(
        plants_with_soil_anomalies, plants_with_temp_anomalies)

    return resultant_message


def calculate_anomalies():
    """Runs all the functions required to execute the purpose of this script."""
    time_yesterday = get_the_time(DEFAULT_TIME_FRAME_HOURS)

    plant_df = get_dataframe(time_yesterday)

    soil_means, temp_means = calculate_means(plant_df)

    recent_readings = get_recent_readings()

    threshold_number = int(ENV["ANOMALY_THRESHOLD"])

    result = check_for_errors(soil_means, temp_means,
                              recent_readings, threshold_number)

    return result


if __name__ == "__main__":
    load_dotenv()
    print(calculate_anomalies())
