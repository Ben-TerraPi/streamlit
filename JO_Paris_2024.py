import streamlit as st
import numpy as np
import pandas as pd
import pandas_gbq
from google.cloud import bigquery
from google.cloud import storage
from google.oauth2 import service_account
from google.cloud import storage
import plotly.express as px
from plotly import graph_objects as go
import seaborn as sns
from plotly.subplots import make_subplots
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


    olympics_games_summer_csv = retrieve_object_from_bucket('jo-paris-2024-442810','project_jo_paris_2024_le_wagon_1826','olympics_games_summer.csv','data/olympics_games_summer.csv','connectors/jo-paris-2024-442810-a51044237fc3.json')
    olympics_games_summer = pd.read_csv('data/olympics_games_summer.csv')

    Athletes_medallists_csv = retrieve_object_from_bucket('jo-paris-2024-442810','project_jo_paris_2024_le_wagon_1826','Athletes_medallists.csv','data/Athletes_medallists.csv','connectors/jo-paris-2024-442810-a51044237fc3.json')
    Athletes_medallists = pd.read_csv('data/Athletes_medallists.csv')

    Countries_Code_ISO_csv = retrieve_object_from_bucket('jo-paris-2024-442810','project_jo_paris_2024_le_wagon_1826','Countries_Code_ISO.csv','data/Countries_Code_ISO.csv','connectors/jo-paris-2024-442810-a51044237fc3.json')
    Countries_Code_ISO = pd.read_csv('data/Countries_Code_ISO.csv')

    Socio_economic_Dataset_csv = retrieve_object_from_bucket('jo-paris-2024-442810','project_jo_paris_2024_le_wagon_1826','Socio_economic_Dataset.csv','data/Socio_economic_Dataset.csv','connectors/jo-paris-2024-442810-a51044237fc3.json')
    Socio_economic_Dataset = pd.read_csv('data/Socio_economic_Dataset.csv')

    all_athlete_bio_csv = retrieve_object_from_bucket('jo-paris-2024-442810','project_jo_paris_2024_le_wagon_1826','all_athlete_bio.csv','data/all_athlete_bio.csv','connectors/jo-paris-2024-442810-a51044237fc3.json')
    all_athlete_bio = pd.read_csv('data/all_athlete_bio.csv')

    athlete_id_multiple_csv = retrieve_object_from_bucket('jo-paris-2024-442810','project_jo_paris_2024_le_wagon_1826','athlete_id_multiple.csv','data/athlete_id_multiple.csv','connectors/jo-paris-2024-442810-a51044237fc3.json')
    athlete_id_multiple = pd.read_csv('data/athlete_id_multiple.csv')

    medals_day_csv = retrieve_object_from_bucket('jo-paris-2024-442810','project_jo_paris_2024_le_wagon_1826','medals_day.csv','data/medals_day.csv','connectors/jo-paris-2024-442810-a51044237fc3.json')
    medals_day = pd.read_csv('data/medals_day.csv')

    medals_total_csv = retrieve_object_from_bucket('jo-paris-2024-442810','project_jo_paris_2024_le_wagon_1826','medals_total.csv','data/medals_total.csv','connectors/jo-paris-2024-442810-a51044237fc3.json')
    medals_total = pd.read_csv('data/medals_total.csv')

    top_disciplines_csv = retrieve_object_from_bucket('jo-paris-2024-442810','project_jo_paris_2024_le_wagon_1826','top_disciplines.csv','data/top_disciplines.csv','connectors/jo-paris-2024-442810-a51044237fc3.json')
    top_disciplines = pd.read_csv('data/top_disciplines.csv')




    #>>>>>>>>>>>>>>>>>>>>>> Dataframes

    dataframes = [
        # "athletes",
        # "Socio_economic_Dataset",
        # "all_athlete_bio",
        # "all_athlete_event_results_summer",
        # "all_country_olympic_games_medal_summer",
        # "medals_total",
        # "schedules",
        # "teams",
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
        st.image("./images/logo-paris-2024.png")

        #st.header("Pages")

        #page = st.sidebar.radio('',["Sources"])

        # st.multiselect(
        #     label="Filtrer par type",
        #     options=st.dataframe,
        #     #key="selected_types",
        #     #placeholder=,
        # )

        st.subheader("About", divider="grey")

        st.markdown("""
        **The Paris 2024 Olympic Games data visualization dashboard**
        is a project developed as part of *Le Wagon* bootcamp @Rennes,
        it showcases data from the 
        **Paris 2024 Olympic games**.
        """)

        st.caption("""
            Autors : 
            
            Benoît Dourdet ([GitHub](https://github.com/Ben-TerraPi))
                
            Maxime Mobailly
                
            Matteo Cherief
                
            Gautier Martin
                
            · Août 2024
        """)

    #>>>>>>>>>>>>>>>>>>>>>> Streamlit app

    #>>>>>>>>>>>>>>>>>>>>>>HOME page


    #Title & intro

    st.title('🏅 Paris JO 2024 - Data Visualization Project'
                )
    st.markdown("""**Welcome to the Paris 2024 Olympic Games data visualization dashboard.**""")

    # Data overview

    st.header("What this project covers:")

    st.markdown("""
    - Olympic summer games history.
    - Micro analysis of Athletes.
    - *Macro analysis of participant Countries.
    """)

    # Expander
    with st.expander("Olympic datastes"):
        st.write("""lists of datasets.""")
        st.dataframe(olympics_games_summer)



    #>>>>>>>>>>>>>>>>>>>>>>>>>>>> Sub pages

    # if page == 'Sources':

    #     st.title('sources')

    #     st.title('Autors info')

    #>>>>>>>>>>>>>>>>>>>>>>>>>>>> Test

    # arr = np.random.normal(1, 1, size=100)
    # fig, ax = plt.subplots()
    # ax.hist(arr, bins=20)

    #>>>>>>>>>>>>>>>>>>>>>> Graph


    #olympics_games_summer
    hist1 = Athlete_histo_1(olympics_games_summer,
                        x = 'country_code',
                        y="city_host", histfunc='count',
                        color="country_code",
                        title="Number of summer's JO hosted by country"
                        )

    hist1.update_xaxes(categoryorder='category ascending')
    st.plotly_chart(hist1)

    #top3 summer
    top_summer = count_and_sort_editions(olympics_games_summer,
                                        'country_code',
                                        "year",
                                        descending=True,
                                        top_n=3
                                        )
    st.dataframe(top_summer)

    st.line_chart(olympics_games_summer,
                    x="year",
                    y=["nb_athletes",
                    "nb_men",
                    "nb_women"])
    
    line1 = nb_line(olympics_games_summer,
                    x="year",
                    y=["nb_athletes",
                    "nb_men",
                    "nb_women"],
                    title="Number of athletes by edition")
    
    st.plotly_chart(line1, use_container_width=True)








#>>>>>>>>>>>>>>>>>>>>>> Footer
if __name__ == "__main__":
    main()
