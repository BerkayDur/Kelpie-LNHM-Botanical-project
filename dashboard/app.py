from os import environ as ENV
from dotenv import load_dotenv
from boto3 import client
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
           longitude="origin_longitude", color="#38761d")


def create_pie_chart(readings):
    """creates desired pie chart for regions"""
    st.subheader("Proportion of plants by their origin regions")
    regions = readings["origin_region"].value_counts(
        normalize=True).reset_index()
    # regions
    st.altair_chart(alt.Chart(regions).mark_arc().encode(
        theta="proportion",
        color=alt.Color("origin_region:N",
                        scale=alt.Scale(scheme="lightorange"))
    ))


def create_latest_readings_bar(latest):
    """creates bar chart for latest readings for each plant"""
    st.subheader("Latest soil moisture and temp")
    st.markdown("Scroll while hovering over the graphs to zoom in and out!")
    temp = latest[["plant_id", "temperature", "soil_moisture"]]
    st.altair_chart(alt.Chart(temp).mark_bar().encode(
        x=alt.X("plant_id:N").sort("ascending"),
        y=alt.Y("temperature:Q", title="temperature"),
        color=alt.Color("temperature", scale=alt.Scale(
            scheme="yelloworangered"))
    ).interactive())
    st.altair_chart(alt.Chart(temp).mark_bar(color="green").encode(
        x=alt.X("plant_id:N").sort("ascending"),
        y=alt.Y("soil_moisture", title="soil moisture"),
        color=alt.Color("soil_moisture", scale=alt.Scale(
            scheme="brownbluegreen"))
    ).interactive())


if __name__ == "__main__":
    load_dotenv()
    conn = get_connection()
    cursor = get_cursor(conn)
    st.title("LMNH Plant Monitoring System 🌱")
    readings = pd.read_sql("""SELECT reading_id, soil_moisture, temperature, last_watered, taken_at, p.plant_id,
    plant_name, scientific_name, origin_longitude, origin_latitude, origin_town, origin_country_code, origin_region, b.botanist_id, name, email, phone_no
    FROM alpha.fact_plant_reading as pr
    JOIN alpha.dim_botanist as b ON pr.botanist_id = b.botanist_id
    JOIN alpha.dim_plant as p ON p.plant_id = pr.plant_id;""", conn)
    latest = pd.read_sql("""SELECT soil_moisture, temperature, taken_at, p.plant_id, p.plant_name
    FROM alpha.fact_plant_reading as pr
    JOIN alpha.dim_plant as p ON p.plant_id = pr.plant_id
    WHERE taken_at > DATEADD(minute, -1, (SELECT CURRENT_TIMESTAMP))
    ORDER BY plant_id;""", conn)
    # cursor.execute("""SELECT reading_id, soil_moisture, temperature, last_watered, taken_at, p.plant_id,
    # plant_name, scientific_name, origin_longitude, origin_latitude, origin_town, origin_country_code, origin_region, b.botanist_id, name, email, phone_no
    # FROM alpha.fact_plant_reading as pr
    # JOIN alpha.dim_botanist as b ON pr.botanist_id = b.botanist_id
    # JOIN alpha.dim_plant as p ON p.plant_id = pr.plant_id""")
    # data = cursor.fetchall()
    # reading = Dataframe(data)
    st.subheader("Latest data")
    create_latest_readings_bar(latest)

    st.subheader("All data")
    create_pie_chart(readings)
    create_map(readings)
