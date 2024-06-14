"""
This is a script that does the following:
- Connects to the RDS
- Extracts the data which came in within the last 24 hours
- Saves them into a parquet file
"""

# pylint: disable=no-name-in-module

from os import environ as ENV
import pandas as pd
from dotenv import load_dotenv
from pymssql import connect, Connection

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


def query_and_extract_rds(conn: Connection) -> list[list]:
    """This function creates the query to get the data start from time"""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT *
            FROM alpha.FACT_plant_reading
        """)
        data = cur.fetchall()
    return data

def delete_from_plant_reading_table(conn: Connection) -> None:
    '''Deletes all data from the FACT_plant_reading table.'''
    with conn.cursor() as cur:
        cur.execute('''
            DELETE FROM alpha.FACT_plant_reading
        ''')
        conn.commit()

def load_into_parquet(data: list, cols: list[str]) -> None:
    """This function loads the given data into a parquet file"""
    if not isinstance(data, list):
        raise TypeError('Cannot insert data not of type list.')
    if not isinstance(cols, list):
        raise TypeError('cols must be of type list.')
    if not all(isinstance(col, str) for col in cols):
        raise TypeError('cols must contain a list of strings.')
    df = pd.DataFrame(data=data, columns=cols)
    df["plant_id"] = pd.to_numeric(
        df["plant_id"], errors='coerce').astype('Int64')

    df.to_parquet(ENV["FILE_NAME"], index=False)


def extract_and_delete_data() -> None:
    """
    Function that runs all the functions required to execute
    the goal of this task.
    """
    load_dotenv()


    db_conn = get_connection()
    db_data = query_and_extract_rds(db_conn)
    delete_from_plant_reading_table(db_conn)
    db_conn.close()

    load_into_parquet(db_data, COLUMNS)


if __name__ == "__main__":
    print(extract_and_delete_data())
