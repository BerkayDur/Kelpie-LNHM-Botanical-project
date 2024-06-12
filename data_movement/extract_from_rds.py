"""
This is a script that does the following:
- Connects to the RDS
- Extracts the data which came in within the last 24 hours
- Saves them into a parquet file
"""

# pylint: disable=no-name-in-module

from os import environ as ENV
from datetime import datetime, timedelta
import pandas as pd
from dotenv import load_dotenv
from pymssql import connect, Connection


HOURS = 24
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
    """This function gets the time 24 hours ago as a formatted string."""
    now = datetime.now()
    yesterday = now - timedelta(hours=number_of_hours)
    yesterday_str = yesterday.strftime('%Y-%m-%d %H:%M:%S')

    return yesterday_str


def query_and_extract_rds(time: str, conn: Connection) -> list[list]:
    """This function creates the query to get the data from the last 24 hours"""
    with conn.cursor() as cur:
        cur.execute(f"""
SELECT *
FROM alpha.FACT_plant_reading
WHERE taken_at >= '{time}'
""")
        data = cur.fetchall()

    return data


def load_into_parquet(data: list, cols: list[str]) -> None:
    """This function loads the given data into a parquet file"""
    df = pd.DataFrame(data=data, columns=cols)
    df["plant_id"] = pd.to_numeric(
        df["plant_id"], errors='coerce').astype('Int64')

    df.to_parquet(ENV["FILE_NAME"], index=False)


def extract_data() -> None:
    """
    Function that runs all the functions required to execute
    the goal of this task.
    """
    load_dotenv()

    time_24_hours_ago = get_the_time(HOURS)

    db_conn = get_connection()
    db_data = query_and_extract_rds(time_24_hours_ago, db_conn)
    db_conn.close()

    load_into_parquet(db_data, COLUMNS)


if __name__ == "__main__":
    print(extract_data())
