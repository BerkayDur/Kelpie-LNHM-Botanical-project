"""takes cleaned readings data and loads it into database"""
# pylint: disable=no-member
from os import environ as ENV
from dotenv import load_dotenv
import pymssql


def get_cursor(connect):
    """gets a cursor given a connection"""
    return connect.cursor()


def get_connection():
    """gets a connection"""
    conn = pymssql.connect(
        host=ENV["DB_HOST"],
        port=ENV["DB_PORT"],
        database=ENV["DB_NAME"],
        user=ENV["DB_USER"],
        password=ENV["DB_PASSWORD"]
    )
    return conn


def upload_plant_data(conn, fact_plant_readings):
    """Uploads plant readings to the database."""
    cursor = get_cursor(conn)
    cursor.executemany(
        """insert into alpha.fact_plant_reading
        (soil_moisture, temperature, last_watered, taken_at, plant_id, botanist_id)
        VALUES (%s, %s, %s, %s, %s,
        (SELECT TOP 1 botanist_id FROM alpha.dim_botanist WHERE name=%s))
        ;""", fact_plant_readings.to_numpy().tolist())
    conn.commit()
    cursor.close()


def load_data(data):
    """main function calling upload data func"""
    load_dotenv()
    connection = get_connection()
    upload_plant_data(connection, data)
