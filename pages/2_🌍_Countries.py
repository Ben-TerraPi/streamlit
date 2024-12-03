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
import seaborn as sns
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

#>>>>>>>>>>>>>>>>>>>>> Streamlit page


st.set_page_config(
    page_title="Countries",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

#Title & intro

st.title('Micro analysis')

st.markdown("""**Welcome to the Paris 2024 Olympic Games data visualization dashboard.**""")
