from os import environ as ENV

from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import altair as alt


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


if __name__ == "__main__":
    conn = get_connection()
    st.title("LMNH Plant Monitors")
    data = pd.read_sql("SELECT * FROM alpha.fact_plant_readings as ")
