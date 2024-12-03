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

#Title & intro

st.title('Give it a try')

st.markdown("""**Welcome to the Paris 2024 Olympic Games data visualization dashboard.**""")


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
sport_family = st.selectbox("Select sport family of athlete",
                            Athletes_medallists.sport_family.unique(),
                            index = None
                            ) 
sport_group = st.selectbox("Select sport group of athlete",
                    Athletes_medallists.sport_group.unique(),
                    index = None
)

#1
nice_tab = user1(Athletes_medallists, name = name , gender = gender, country_name = country_name , Age = Age, sport_family = sport_family, sport_group = sport_group)
st.plotly_chart(nice_tab)