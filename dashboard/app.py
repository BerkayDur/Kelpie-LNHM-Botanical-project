from os import environ as ENV
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import altair as alt
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


def create_map(readings):
    st.subheader("Origin of plants")
    st.map(data=readings, latitude="origin_latitude",
           longitude="origin_longitude")


def create_pie_chart(readings):
    """creates desired pie chart for regions"""
    st.subheader("Proportion of plants per region")
    regions = readings["origin_region"].value_counts(
        normalize=True).reset_index()
    regions
    st.altair_chart(alt.Chart(regions).mark_arc().encode(
        theta="proportion",
        color="origin_region:N"
    ))


if __name__ == "__main__":
    load_dotenv()
    conn = get_connection()
    cursor = get_cursor(conn)
    st.title("LMNH Plant Monitors")
    readings = pd.read_sql("""SELECT reading_id, soil_moisture, temperature, last_watered, taken_at, p.plant_id,
    plant_name, scientific_name, origin_longitude, origin_latitude, origin_town, origin_country_code, origin_region, b.botanist_id, name, email, phone_no
    FROM alpha.fact_plant_reading as pr
    JOIN alpha.dim_botanist as b ON pr.botanist_id = b.botanist_id
    JOIN alpha.dim_plant as p ON p.plant_id = pr.plant_id;""", conn)
    latest = pd.read_sql("""SELECT soil_moisture, temperature, taken_at, DISTINCT p.plant_id
    FROM alpha.fact_plant_reading as pr
    JOIN alpha.dim_plant as p ON p.plant_id = pr.plant_id
    ORDER BY taken_at DESC;""", conn)
    latest
    # cursor.execute("""SELECT reading_id, soil_moisture, temperature, last_watered, taken_at, p.plant_id,
    # plant_name, scientific_name, origin_longitude, origin_latitude, origin_town, origin_country_code, origin_region, b.botanist_id, name, email, phone_no
    # FROM alpha.fact_plant_reading as pr
    # JOIN alpha.dim_botanist as b ON pr.botanist_id = b.botanist_id
    # JOIN alpha.dim_plant as p ON p.plant_id = pr.plant_id""")
    # data = cursor.fetchall()
    # reading = Dataframe(data)
    st.subheader("Latest data")
    readings
    create_pie_chart(readings)
    create_map(readings)
