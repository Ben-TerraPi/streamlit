import streamlit as st
import utils as u
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import plotly.express as px

#>>>>>>>>>>>>>>>>>>>>> Streamlit page


st.set_page_config(
    page_title="Athletes",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

#Title & intro

st.title('Macro Analysis')

st.markdown("""**Welcome to the Paris 2024 Olympic Games data visualization dashboard.**""")