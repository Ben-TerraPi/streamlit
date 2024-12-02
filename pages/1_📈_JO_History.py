import streamlit as st
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import plotly.express as px
from utils import Athlete_histo
from utils import count_and_sort_editions
from utils import nb_line


#>>>>>>>>>>>>>>>>>>>>>> Create API client.

project = "jo-paris-2024-442810"
credentials = service_account.Credentials.from_service_account_info(
st.secrets["gcp_service_account"])

#>>>>>>>>>>>>>>>>>>>>>> BQ authentification

#client = get_bigquery()
client = bigquery.Client(credentials=credentials)

#>>>>>>>>>>>>>>>>>>>>>> Dataframes

dataframes = [
    "Socio_economic_Dataset",
    "all_athlete_bio",
    "all_athlete_event_results_summer",
    "all_country_olympic_games_medal_summer",
    "medals_total",
    "schedules",
    "teams",
    "Countries_Code_ISO",
    "olympics_games_summer",
    "athlete_id_multiple"
    ]


dataset = "dataset_v2"

    

#>>>>>>>>>>>>>>>>>>>>> Streamlit page


st.set_page_config(
    page_title="JO History",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

#Title & intro

st.title('Olympic summer Games in time ')
    
st.markdown("""**A brief history of the olympic summer games.**""")


#>>>>>>>>>>>>>>>>>>>>>> Graph

query = f"SELECT * FROM `jo-paris-2024-442810.dataset_v2.olympics_games_summer`"
df = get_data_from_bigquery(query,client)


#olympics_games_summer
hist1 = Athlete_histo("olympics_games_summer",
                      x = 'country_code',
                      y="city_host", histfunc='count',
                      color="country_code",
                      title="Number of summer's JO hosted by country"
                      )

hist1.update_xaxes(categoryorder='category ascending')

#top3 summer
top_summer = count_and_sort_editions("olympics_games_summer",
                                     'country_code',
                                     "year",
                                     descending=True,
                                     top_n=3
                                     )
top_summer


line1 = nb_line("olympics_games_summer",
                x="year",
                y=["nb_athletes",
                   "nb_men",
                   "nb_women"],
                 title="Number of athletes by edition"
                 )
line1.show()
