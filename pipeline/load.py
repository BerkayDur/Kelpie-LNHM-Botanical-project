from os import environ as ENV
from dotenv import load_dotenv
import pymssql

import transform
import extract


def get_cursor(conn):
    """gets a cursor given a connection"""
    return conn.cursor()


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
    dim_plant, dim_botanist, fact_plant_reading = transform.main(
        extract.main())
    print(fact_plant_reading.to_numpy().tolist())
    cursor = get_cursor(conn)

    cursor.executemany(
        """insert into alpha.fact_plant_reading (soil_moisture, temperature, last_watered, taken_at, botanist_id, plant_id)
        VALUES (%s, %s, %s, %s,(SELECT botanist_id FROM alpha.dim_botanist WHERE name=%s),
        (SELECT plant_id FROM alpha.dim_plant WHERE plant_name = %s));""", fact_plant_reading.to_numpy().tolist())
    conn.commit()

    cursor.close()


if __name__ == "__main__":
    conn = get_connection()
    upload_plant_data(conn)
