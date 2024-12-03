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
import gcsfs
from st_files_connection import FilesConnection

from utils import (
    get_data_from_bigquery,
    Athlete_histo_1,
    count_and_sort_editions,
    nb_line,
    # Selection,
    # percentile,
    # gender_ratio,
    # Bar_chart_1,
    # Country_color,
    # Top,
    # score_card_1,
    # score_card_2,
    # subplots_scorecards,
    # Hist_tab_athletes_age,
    # Athlete_medals_top20,
    # Distribution_events_nb,
    # plot_histogram_with_line,
    # plot_top_10_medals_by_type
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

    #Create connection object and retrieve file contents.
    #conn = st.experimental_connection('gcs', type=FilesConnection)

    # Socio_economic_Dataset = conn.read("project_jo_paris_2024_le_wagon_1826/Socio_economic_Dataset.csv", input_format="csv", ttl=600)
    # st.dataframe(Socio_economic_Dataset)
    # athletes = conn.read("project_jo_paris_2024_le_wagon_1826/athletes.csv", input_format="csv", ttl=600)
    # st.dataframe(athletes)
    # medallists = conn.read("project_jo_paris_2024_le_wagon_1826/medallists.csv", input_format="csv", ttl=600)
    # st.dataframe(medallists)
    # medals_total = conn.read("project_jo_paris_2024_le_wagon_1826/medals_total.csv", input_format="csv", ttl=600)
    # st.dataframe(medals_total)
    # Countries_Code_ISO = conn.read("project_jo_paris_2024_le_wagon_1826/Countries_Code_ISO.csv", input_format="csv", ttl=600)
    # st.dataframe(Countries_Code_ISO)
    # all_athlete_bio = conn.read("project_jo_paris_2024_le_wagon_1826/all_athlete_bio.csv", input_format="csv", ttl=600)
    # st.dataframe(all_athlete_bio)
    # athlete_id_multiple = conn.read("project_jo_paris_2024_le_wagon_1826/athlete_id_multiple.csv", input_format="csv", ttl=600)
    # st.dataframe(athlete_id_multiple)
    
    # medals_day = conn.read("project_jo_paris_2024_le_wagon_1826/csv/medals_day.csv", input_format="csv", ttl=600)
    # st.dataframe(medals_day)
    
    
    
    
    
    
    
    

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

    #>>>>>>>>>>>>>>>>>>>>>> Perform a query 

    #query = f"SELECT * FROM `jo-paris-2024-442810.dataset_v2.olympics_games_summer`"
    #df = get_data_from_bigquery(query,client)
    conn = st.connection("gcs", type=FilesConnection)
          
    olympics_games_summer = conn.read("project_jo_paris_2024_le_wagon_1826/olympics_games_summer.csv", input_format="csv", ttl=600)

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
