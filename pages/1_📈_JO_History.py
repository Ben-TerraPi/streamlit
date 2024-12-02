import streamlit as st
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import plotly.express as px

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
