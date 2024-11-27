import streamlit as st
import utils as u
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import plotly.express as px

# code a utiliser pour re-run l'appli  >>>>>>>>>>>>>> streamlit run streamlit_app.py

#>>>>>>>>>>>>>>>>>>>>> Streamlit page

st.set_page_config(
    page_title="JO Paris 2024",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded",
)

#>>>>>>>>>>>>>>>>>>>>>> Streamlit app

st.title("JO Paris 2024")
st.markdown("#### Titre")

#>>>>>>>>>>>>>>>>>>>>>> Application : sidebar

with st.sidebar:
    st.image("./images/logo-paris-2024.png")

#>>>>>>>>>>>>>>>>>>>>>> Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

#>>>>>>>>>>>>>>>>>>>>>> BQ authentification
client = bigquery.Client(credentials=credentials)
project = "jo-paris-2024-442810"

#>>>>>>>>>>>>>>>>>>>>>> Dataframes
Dataframes = ["athletes"]
Dataset = "dataset_v2"


#>>>>>>>>>>>>>>>>>>>>>> functions
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data_from_bigquery(query):
    query_job = client.query(query)
    rows = query_job.result()
    return pd.DataFrame([dict(row) for row in rows])

@st.cache_data(ttl=600)
def Athlete_histo_1(athletes, x, color, title):
  fig1 = px.histogram(athletes, x = x, color=color, title=title)
  fig1.show()

#>>>>>>>>>>>>>>>>>>>>>> Perform a query.

for Dataframe in Dataframes:
    query = f"SELECT * FROM `jo-paris-2024-442810.{Dataset}.{Dataframe}`"
    df = get_data_from_bigquery(query)
    st.write(f"Voici les données pour {Dataframe}:")
    st.dataframe(df)
