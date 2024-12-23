import streamlit as st
import numpy as np
import pandas as pd
import pandas_gbq
from google.cloud import bigquery
from google.cloud import storage
from google.oauth2 import service_account
from google.cloud import storage
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import gcsfs
from st_files_connection import FilesConnection
import pickle
import re
from utils import (
    retrieve_object_from_bucket,
    get_data_from_bigquery,
    Country_color,
    Athlete_histo_1,
    count_and_sort_editions,
    plot_olympics_trends,
    nb_line,
    Selection,
    percentile,
    gender_ratio,
    Bar_chart_1,
    Top,
    doublegraph_athletes_countries_top,
    score_card_1,
    score_card_2,
    subplots_scorecards,
    Hist_tab_athletes_age,
    Athlete_medals_top20,
    Distribution_events_nb,
    Athletes_number_per_sport_family,
    user1,
    create_country_indicator
)


# code a utiliser pour re-run l'appli  >>>>>>>>>>>>>> streamlit run streamlit_app.py
# code pour list package >>>>>>>>>>>>>>>>>>>>>>>>>>>> pip list


# Main
def main():

    #>>>>>>>>>>>>>>>>>>>>>> Create API client.

    project = "jo-paris-2024-442810"
    credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"])

    #>>>>>>>>>>>>>>>>>>>>>> BQ authentification
    
    #client = get_bigquery()
    client = bigquery.Client(credentials=credentials)

    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Perform a query 


    # query = f"SELECT * FROM `jo-paris-2024-442810.dataset_v2.olympics_games_summer`"
    # olympics_games_summer = get_data_from_bigquery(query,client)

    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Connection to GBQ

    #Work ON:
    #olympics_games_summer_csv = retrieve_object_from_bucket('jo-paris-2024-442810','project_jo_paris_2024_le_wagon_1826','olympics_games_summer.csv','data/olympics_games_summer.csv','connectors/jo-paris-2024-442810-a51044237fc3.json')
    olympics_games_summer = pd.read_csv('data/olympics_games_summer.csv')

    #Athletes_medallists_csv = retrieve_object_from_bucket('jo-paris-2024-442810','project_jo_paris_2024_le_wagon_1826','Athletes_medallists.csv','data/Athletes_medallists.csv','connectors/jo-paris-2024-442810-a51044237fc3.json')
    Athletes_medallists = pd.read_csv('data/Athletes_medallists.csv')

    #Socio_economic_Dataset_csv = retrieve_object_from_bucket('jo-paris-2024-442810','project_jo_paris_2024_le_wagon_1826','Socio_economic_Dataset.csv','data/Socio_economic_Dataset.csv','connectors/jo-paris-2024-442810-a51044237fc3.json')
    Socio_economic_Dataset = pd.read_csv('data/Socio_economic_Dataset.csv')

    #medals_total_csv = retrieve_object_from_bucket('jo-paris-2024-442810','project_jo_paris_2024_le_wagon_1826','medals_total.csv','data/medals_total.csv','connectors/jo-paris-2024-442810-a51044237fc3.json')
    medals_total = pd.read_csv('data/medals_total.csv')

    #athlete_id_multiple_csv = retrieve_object_from_bucket('jo-paris-2024-442810','project_jo_paris_2024_le_wagon_1826','athlete_id_multiple.csv','data/athlete_id_multiple.csv','connectors/jo-paris-2024-442810-a51044237fc3.json')
    athlete_id_multiple = pd.read_csv('data/athlete_id_multiple.csv')

    #Not work on:
    #Countries_Code_ISO_csv = retrieve_object_from_bucket('jo-paris-2024-442810','project_jo_paris_2024_le_wagon_1826','Countries_Code_ISO.csv','data/Countries_Code_ISO.csv','connectors/jo-paris-2024-442810-a51044237fc3.json')
    Countries_Code_ISO = pd.read_csv('data/Countries_Code_ISO.csv')

    #all_athlete_bio_csv = retrieve_object_from_bucket('jo-paris-2024-442810','project_jo_paris_2024_le_wagon_1826','all_athlete_bio.csv','data/all_athlete_bio.csv','connectors/jo-paris-2024-442810-a51044237fc3.json')
    all_athlete_bio = pd.read_csv('data/all_athlete_bio.csv')



    #medals_day_csv = retrieve_object_from_bucket('jo-paris-2024-442810','project_jo_paris_2024_le_wagon_1826','medals_day.csv','data/medals_day.csv','connectors/jo-paris-2024-442810-a51044237fc3.json')
    medals_day = pd.read_csv('data/medals_day.csv')

    #top_disciplines_csv = retrieve_object_from_bucket('jo-paris-2024-442810','project_jo_paris_2024_le_wagon_1826','top_disciplines.csv','data/top_disciplines.csv','connectors/jo-paris-2024-442810-a51044237fc3.json')
    top_disciplines = pd.read_csv('data/top_disciplines.csv')




    #>>>>>>>>>>>>>>>>>>>>>> Dataframes

    dataframes = [
        # "Socio_economic_Dataset",
        # "all_athlete_bio",
        # "all_athlete_event_results_summer",
        # "all_country_olympic_games_medal_summer",
        # "medals_total",
        # "medals_day",
        # "Countries_Code_ISO",
        # "olympics_games_summer",
        # "athlete_id_multiple"
        ]

    dataset = "dataset_v2"

    # for dataframe in dataframes:
    #     query = f"SELECT * FROM `jo-paris-2024-442810.{dataset}.{dataframe}`"
    #     locals()[dataframe] = pd.read_gbq(query, project_id=project)


    #>>>>>>>>>>>>>>>>>>>>> Streamlit page


    st.set_page_config(
        page_title="JO Paris 2024",
        page_icon="🏅",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    #>>>>>>>>>>>>>>>>>>>>>> Streamlit sidebar


    with st.sidebar:
        st.logo("images/The_Phryges.svg.png")
        st.image("./images/logo-paris-2024.png")

        #st.header("Pages")

        #page = st.sidebar.radio('',["Sources"])

        # st.multiselect(
        #     label="Filtrer par type",
        #     options=st.dataframe,
        #     #key="selected_types",
        #     #placeholder=,
        # )

 
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>HOME page


    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Title & intro

    st.title('🏅 Paris JO 2024 - Data Visualization Project'
                )
    st.markdown("""**Welcome to the Paris 2024 Olympic Games data visualization dashboard.**""")


    st.header("What this project covers:")

    st.write("Browse pages on the left")

    st.markdown("""
    - Olympic summer games history.
    - Analysis of participating countries.
    - Analysis of athletes.
    - Socio-economic analysis.             
    """)


    # Expander
    with st.expander("Olympic datasets"):
        st.write("""olympics_games_summer:""")
        st.dataframe(olympics_games_summer)
        st.write("""Athletes_medallists:""")
        st.dataframe(Athletes_medallists)
        st.write("""medals_total:""")
        st.dataframe(medals_total)
        st.write("Socio_economic_Dataset")
        st.dataframe(Socio_economic_Dataset)     


    st.header("Sources:")
    st.write("https://olympics.com/en/paris-2024")


if __name__ == "__main__":
    main()
