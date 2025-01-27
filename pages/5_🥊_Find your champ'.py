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
from dict_jo import group_discipline, discipline_name, sport_country


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


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>SIDEBAR
with st.sidebar:
    st.logo("images/The_Phryges.svg.png")
    st.image("./images/logo-paris-2024.png")

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


sport_group = st.selectbox(
    "Select sport group of athlete",
    [""] + sorted(list(group_discipline.keys())),
    index=None
)

if sport_group:
    disciplines = sorted(group_discipline.get(sport_group, []))
else:
    disciplines = sorted(set(discipline for group in group_discipline.values() for discipline in group))

discipline = st.selectbox(
    "Select sport discipline of athlete",
    [""] + disciplines,
    index=None
)

medals = st.selectbox(
    "Which medals",
    ("Gold", "Silver", "Bronze"),
    index=None
)

if discipline:
    names = sorted(discipline_name.get(discipline, []))
else:
    names = sorted(set(name for name_list in discipline_name.values() for name in name_list))

name = st.selectbox(
    "Select name of athlete",
    [""] + names,
    index=None
)

if discipline:
    countries = sorted(set(sport_country.get(discipline, [])))
else:
    countries = sorted(set(country for country_list in sport_country.values() for country in country_list))

country_name = st.selectbox(
    "Select country of athlete",
    [""] + countries,
    index=None
)

gender = st.selectbox(
    "Select gender of athlete",
    sorted(Athletes_medallists.gender.unique()),
    index=None
)


if st.button("Generate Link"):
    nice_tab = user1(Athletes_medallists, name=name, gender=gender, country_name=country_name, 
                     sport_group=sport_group, medals=medals, discipline=discipline)
    st.plotly_chart(nice_tab)
