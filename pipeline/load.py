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


def upload_plant_data(conn):
    """Uploads plant data to the database."""
    dim_plant, dim_botanist, fact_plant_reading = transform.main()
    cursor = get_cursor(conn)

    dim_botanist_list = [['Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'], ['Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'], ['Eliza Andrews', 'eliza.andrews@lnhm.co.uk', '(846)669-6651x75948'], ['Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'], ['Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'], ['Eliza Andrews', 'eliza.andrews@lnhm.co.uk', '(846)669-6651x75948'], [None, None, None], ['Eliza Andrews', 'eliza.andrews@lnhm.co.uk', '(846)669-6651x75948'], ['Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'], ['Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'], ['Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'], ['Eliza Andrews', 'eliza.andrews@lnhm.co.uk', '(846)669-6651x75948'], ['Eliza Andrews', 'eliza.andrews@lnhm.co.uk', '(846)669-6651x75948'], ['Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'], ['Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'], ['Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'], ['Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'], ['Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'], ['Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'], ['Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'], ['Eliza Andrews', 'eliza.andrews@lnhm.co.uk', '(846)669-6651x75948'], ['Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'], ['Eliza Andrews', 'eliza.andrews@lnhm.co.uk', '(846)669-6651x75948'], ['Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'], ['Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'], [
        'Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'], ['Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'], ['Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'], ['Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'], ['Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'], ['Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'], ['Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'], ['Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'], ['Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'], ['Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'], ['Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'], ['Eliza Andrews', 'eliza.andrews@lnhm.co.uk', '(846)669-6651x75948'], ['Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'], ['Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'], ['Eliza Andrews', 'eliza.andrews@lnhm.co.uk', '(846)669-6651x75948'], ['Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'], ['Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'], [None, None, None], ['Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'], ['Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'], ['Eliza Andrews', 'eliza.andrews@lnhm.co.uk', '(846)669-6651x75948'], ['Eliza Andrews', 'eliza.andrews@lnhm.co.uk', '(846)669-6651x75948'], ['Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'], ['Eliza Andrews', 'eliza.andrews@lnhm.co.uk', '(846)669-6651x75948'], ['Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992']]

    cursor.executemany(
        """insert into alpha.fact_plant_reading (soil_moisture, temperature, taken_at, watered_at, plant_id, botanist_id)
        VALUES (%s, %s, %s, %s, (SELECT plant_id FROM alpha.dim_plant WHERE plant_name = %s)
    , (SELECT botanist_id FROM alpha.dim_botanist WHERE botanist_name=%s));""", fact_plant_reading)
    conn.commit()

    cursor.close()


if __name__ == "__main__":
    conn = get_connection()
    upload_plant_data(conn)
