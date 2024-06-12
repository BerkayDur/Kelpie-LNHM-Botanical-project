"""takes cleaned readings data and loads it into database"""
from os import environ as ENV
from dotenv import load_dotenv
import pymssql

import transform
import extract


def get_cursor(connect):
    """gets a cursor given a connection"""
    return connect.cursor()


def get_connection():
    """gets a connection"""
    load_dotenv()
    conn = pymssql.connect(
        host=ENV["DB_HOST"],
        port=ENV["DB_PORT"],
        database=ENV["DB_NAME"],
        user=ENV["DB_USER"],
        password=ENV["DB_PASSWORD"]
    )
    return conn


def upload_plant_data(conn):
    """Uploads plant readings to the database."""
    _, _, fact_plant_reading = transform.transform_data(
        extract.extract_data(51))
    cursor = get_cursor(conn)

    cursor.executemany(
        """insert into alpha.fact_plant_reading
        (soil_moisture, temperature, last_watered, taken_at, botanist_id, plant_id)
        VALUES (%s, %s, %s, %s,
        (SELECT TOP 1 botanist_id FROM alpha.dim_botanist WHERE name=%s),
        (SELECT TOP 1 plant_id FROM alpha.dim_plant WHERE plant_name = %s))
        ;""", fact_plant_reading.to_numpy().tolist())
    conn.commit()

    cursor.close()


if __name__ == "__main__":
    connection = get_connection()
    upload_plant_data(connection)
