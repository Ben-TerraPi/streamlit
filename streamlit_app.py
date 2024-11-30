import streamlit as st
import utils as u
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import plotly.express as px

# code a utiliser pour re-run l'appli  >>>>>>>>>>>>>> streamlit run streamlit_app.py
# code pour list package >>>>>>>>>>>>>>>>>>>>>>>>>>>> pip list


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

    st.header("Pages")

    page = st.sidebar.radio('',["Home","History", "Countries", "Athletes"])

    st.multiselect(
        label="Filtrer par type",
        options=st.dataframe,
        #key="selected_types",
        #placeholder=,
    )

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


#>>>>>>>>>>>>>>>>>>>>>> Create API client.


credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"])


#>>>>>>>>>>>>>>>>>>>>>> BQ authentification


client = bigquery.Client(credentials=credentials)
project = "jo-paris-2024-442810"


#>>>>>>>>>>>>>>>>>>>>>> Dataframes


Dataframes = ["olympics_games_summer"]
Dataset = "dataset_v2"


#>>>>>>>>>>>>>>>>>>>>>> Streamlit app


#Title & intro

st.title('🏅 Paris JO 2024 - Data Visualization Project',
         )
st.markdown("""
    **Welcome to the Paris 2024 Olympic Games data visualization dashboard.** 
    """)

# Data overview

st.header("What this project covers:")

st.markdown("""
    - Olympic summer games history.
    - Micro analysis of Athletes.
    - *Macro analysis of participant Countries.
    """)

# Expander

with st.expander("📊 French Olympic data"):
    st.write("""
        lists of datasets.
             """)
    

#>>>>>>>>>>>>>>>>>>>>>> functions
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data_from_bigquery(query):
    query_job = client.query(query)
    rows = query_job.result()
    #return pd.DataFrame([dict(row) for row in rows])

@st.cache_data(ttl=600)
def nb_line(df, x,y, title, color=None, markers=True, hover_data='country_code', animation_frame=None,log_x=False, log_y=False, range_x=None, range_y=None, labels={}):
  line = px.line(df, x = x,y =y, color=color, title=title, hover_data=hover_data, markers=markers, animation_frame=animation_frame, log_x=log_x, log_y=log_y, range_x=range_x, range_y=range_y, labels=labels)
  #return line
  #line.show()


# Load the data


#>>>>>>>>>>>>>>>>>>>>>> Perform a query 

for Dataframe in Dataframes:      
    query = f"SELECT * FROM `jo-paris-2024-442810.{Dataset}.{Dataframe}`"
    df = get_data_from_bigquery(query)
   
    #st.write(f"Voici les données pour {Dataframe}:")
    st.dataframe(df)


#>>>>>>>>>>>>>>>>>>>>>> Graph