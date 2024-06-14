from os import environ as ENV
from dotenv import load_dotenv
from boto3 import client
import os
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


def get_files(bucket_name, s3):
    """gets all files from the specified bucket"""
    return s3.list_objects(Bucket=bucket_name)


def create_data_folder():
    if not os.path.exists("./data"):
        os.mkdir("./data")


def get_most_recent(my_files: list):
    last_modified = max([file["LastModified"]
                        for file in my_files["Contents"]])
    print(last_modified)
    recent_file = [
        file for file in my_files["Contents"] if file["LastModified"] == last_modified]
    return recent_file[0]


def get_bucket_data():
    s3 = client('s3', aws_access_key_id=ENV["ACCESS_KEY"],
                aws_secret_access_key=ENV["SECRET_ACCESS_KEY"])
    create_data_folder()
    files = get_files("c11-kelpie-lmnh-plant-data", s3)
    recent_file = get_most_recent(files)
    recent_key = recent_file["Key"]
    s3.download_file("c11-kelpie-lmnh-plant-data", recent_key,
                     os.path.join("data", "recent_data.parquet"))
    df = pd.read_parquet(os.path.join("data", "recent_data.parquet"))
    return df


def create_map(readings):
    st.map(data=readings, latitude="origin_latitude",
           longitude="origin_longitude", color="#38761d")


def create_pie_chart_regions(readings):
    """creates desired pie chart for regions"""
    st.subheader("Proportion of plants by their origin regions")
    regions = readings["origin_region"].value_counts(
        normalize=True).reset_index()
    st.altair_chart(alt.Chart(regions).mark_arc().encode(
        theta="proportion",
        color=alt.Color("origin_region:N",
                        scale=alt.Scale(scheme="lightorange"), title="Region")
    ))


def create_pie_chart_countries(readings):
    """creates desired pie chart for countries"""
    st.subheader("Proportion of plants by their origin countries")
    regions = readings["origin_country_code"].value_counts(
        normalize=True).reset_index()
    st.altair_chart(alt.Chart(regions).mark_arc().encode(
        theta="proportion",
        color=alt.Color("origin_country_code:N",
                        scale=alt.Scale(scheme="tableau10"), title="Country code")
    ))


def create_latest_readings_bar(latest):
    """creates bar chart for latest readings for each plant"""
    st.markdown(
        "### Latest soil moisture and temperature readings for each plant")
    st.markdown("Scroll while hovering over the graphs to zoom in and out!")
    temp = latest[["plant_id", "temperature", "soil_moisture"]]
    st.altair_chart(alt.Chart(temp).mark_bar().encode(
        x=alt.X("plant_id:N", title="Plant ID").sort("ascending"),
        y=alt.Y("temperature:Q", title="Temperature"),
        color=alt.Color("temperature", scale=alt.Scale(
            scheme="yelloworangered"))
    ).interactive())
    st.altair_chart(alt.Chart(temp).mark_bar(color="green").encode(
        x=alt.X("plant_id:N", title="Plant ID").sort("ascending"),
        y=alt.Y("soil_moisture", title="soil moisture"),
        color=alt.Color("soil_moisture", scale=alt.Scale(
            scheme="brownbluegreen"))
    ).interactive())


def create_line_graph_temp(data):
    st.altair_chart(alt.Chart(data).mark_line().encode(
        x=alt.X("taken_at:T", title="Time of reading"),
        y=alt.Y("temperature:Q", title="Temperature"),
        color=alt.Color("plant_id:N", title="Plant ID", scale=alt.Scale(
            scheme="darkred"))
    ).interactive(), use_container_width=True)


def create_line_graph_soil(data):
    st.altair_chart(alt.Chart(data).mark_line().encode(
        x=alt.X("taken_at:T", title="Time of reading"),
        y=alt.Y("soil_moisture:Q", title="Soil moisture"),
        color=alt.Color("plant_id:N", title="Plant ID", scale=alt.Scale(scheme="darkblue"))).interactive(), use_container_width=True)


def filter_history_by_id(history, id: int):
    return history[history["plant_id"] == id]


if __name__ == "__main__":
    load_dotenv()
    conn = get_connection()
    cursor = get_cursor(conn)
    history = get_bucket_data()

    st.title("LMNH Plant Monitoring System 🌱")
    readings = pd.read_sql("""SELECT reading_id, soil_moisture, temperature, last_watered, taken_at, p.plant_id,
    plant_name, scientific_name, origin_longitude, origin_latitude, origin_town, origin_country_code, origin_region, b.botanist_id, name, email, phone_no
    FROM alpha.fact_plant_reading as pr
    JOIN alpha.dim_botanist as b ON pr.botanist_id = b.botanist_id
    JOIN alpha.dim_plant as p ON p.plant_id = pr.plant_id
    WHERE p.origin_latitude IS NOT NULL;""", conn)
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
    st.markdown("## Latest readings")
    create_latest_readings_bar(latest)
    st.markdown("## Previous readings")

    plant_id = st.slider(
        label="Choose a plant ID to display", min_value=0, max_value=50)
    plant = pd.read_sql("""SELECT soil_moisture, temperature, taken_at, p.plant_id, p.plant_name
    FROM alpha.fact_plant_reading as pr
    JOIN alpha.dim_plant as p ON p.plant_id = pr.plant_id
    WHERE p.plant_id=%s;""", con=conn, params=plant_id)
    cursor.execute("""Select plant_name FROM alpha.dim_plant
    WHERE plant_id=%s;""", plant_id)
    plant_name = cursor.fetchone()
    cursor.close()
    conn.close()

    st.markdown(f"### Plant {plant_id}:{str(plant_name).strip("(,\")")}")
    st.markdown("### Last 24 hours")
    create_line_graph_temp(plant)
    create_line_graph_soil(plant)

    st.subheader("Historical data")
    filtered_history = filter_history_by_id(history, plant_id)
    create_line_graph_temp(filtered_history)
    create_line_graph_soil(filtered_history)

    st.markdown("## Plant origin information")
    col = st.columns(3)

    with col[0]:
        create_pie_chart_regions(readings)
    with col[2]:
        create_pie_chart_countries(readings)
    create_map(readings)
