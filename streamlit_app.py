import streamlit as st
import utils as u
import pandas as pd
import pandas_gbq
from google.cloud import bigquery
from google.oauth2 import service_account
import plotly.express as px

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

# BQ authentification
client = bigquery.Client(credentials=credentials)
project = "jo-paris-2024-442810"

# Perform a query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
st.cache_data(ttl=600)

Dataframes = ["athletes"]
Dataset = "dataset_v2"

for Dataframe in Dataframes:
    query = f"SELECT * FROM `jo-paris-2024-442810.{Dataset}.{Dataframe}'"
    query_job = client.query(query)  # API request
    #rows = query_job.result()  # Waits for query to finish
    locals()[Dataframe] = pandas_gbq.read_gbq(query, project_id=project)
    #print(rows)


#Athlete_histo_1(athletes, x = 'country_code',color="country_code", title="Athletes number per country")
fig1 = px.histogram(athletes, x = 'country_code',color="country_code", title="Athletes number per country")
fig1.show()

st.set_page_config(
    page_title="JO Paris 2024",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Streamlit app

st.title("JO Paris 2024")
st.markdown("#### Titre")
