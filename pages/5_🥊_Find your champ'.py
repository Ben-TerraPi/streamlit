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
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import user1


#>>>>>>>>>>>>>>>>>>>>>>>>>DATAFRAME

Athletes_medallists = pd.read_csv('data/Athletes_medallists.csv')


#>>>>>>>>>>>>>>>>>>>>> Streamlit page


st.set_page_config(
    page_title="Choose your champ'",
    page_icon="🥊",
    layout="wide",
    initial_sidebar_state="expanded",
)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Title & intro

st.title('Give it a try')
st.write("you can search with one multiple conditions")


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>SIDEBAR
with st.sidebar:
    st.logo("images/The_Phryges.svg.png")
    st.image("./images/logo-paris-2024.png")

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# sport_group = st.selectbox("Select sport group of athlete",
#                     Athletes_medallists.sport_group.unique(),
#                     index = None
#                     )
discipline = st.selectbox("Select sport discipline of athlete",
                            Athletes_medallists.disciplines.unique(),
                            index = None
                            ) 

medals = st.selectbox("Which medals",
                          ("Gold", "Silver", "Bronze"),
                          index=None
                          )

name = st.selectbox("Select name of athlete",
                    Athletes_medallists.name,
                    index = None
                    )
gender = st.selectbox("Select gender of athlete",
                    Athletes_medallists.gender.unique(),
                    index = None
)
country_name = st.selectbox("Select country of athlete",
                    Athletes_medallists.country_name.unique(),
                    index = None
)
Age = st.selectbox("Select age of athlete",
                    Athletes_medallists.Age.unique(),
                    index = None
)


#1
nice_tab = user1(Athletes_medallists, name = name , gender = gender, country_name = country_name , Age = Age, sport_group = sport_group, medals = medals, discipline = discipline)
st.plotly_chart(nice_tab)