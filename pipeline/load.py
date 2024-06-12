from os import environ as ENV
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pymssql

import transform


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


def method(pd_table, conn, keys, data_iter):
    ...


def upload_plant_data(conn):
    """Uploads plant data to the database."""
    dim_plant, dim_botanist, fact_plant_reading = transform.main()
    cursor = get_cursor(conn)

    # dim_plant.to_sql(name='alpha.dim_plant', con=conn,
    #                  schema='alpha', method=method)
    # dim_botanist.to_sql(name='alpha.dim_botanist', con=conn,
    #                     schema='alpha', method=method)
    # fact_plant_reading.to_sql(
    #     name='fact_plant_reading', con=conn, schema='alpha', if_exists="append", method=method)
    dim_botanist_list = dim_botanist.to_numpy().tolist()
    print(dim_botanist_list)
    dim_plant_list = dim_plant.to_numpy().tolist()

    botanist_ids = cursor.executemany(
        """insert into alpha.dim_botanist(name, email, phone_no)
        VALUES (%s, %s, %s);""", dim_botanist_list)
    print(botanist_ids)
    plant_ids = cursor.executemany(
        """insert into alpha.dim_plant(plant_name, scientific_name, origin_longitude, origin_latitude, origin_town, origin_country_code, origin_region)
        VALUES (%s, %s, %s, %s, %s, %s, %s);""", dim_plant_list)
    print(plant_ids)
    # cursor.executemany(
    #     """insert into alpha.fact_plant_reading (soil_moisture, temperature, taken_at, watered_at, plant_id, botanist_id)
    #     VALUES (%s, %s, %s, %s, (SELECT plant_id FROM alpha.dim_plant WHERE plant_name = %s)
    # , %s);""", fact_plant_reading)
    conn.commit()

    cursor.close()


if __name__ == "__main__":
    conn = get_connection()
    upload_plant_data(conn)
