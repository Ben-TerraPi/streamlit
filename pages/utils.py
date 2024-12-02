import streamlit as st
import pages.utils as u
import pandas as pd
import pandas_gbq
from google.cloud import bigquery
from google.oauth2 import service_account
import plotly.express as px

#>>>>>>>>>>>>>>>>>>>>>> Create API client.

@st.cache_data(ttl=600)
def get_bigquery():
   project = "jo-paris-2024-442810"
   credentials = service_account.Credentials.from_service_account_info(
      st.secrets["gcp_service_account"])


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Query

@st.cache_data(ttl=600)
def get_data_from_bigquery(_query, _client):
    query_job = _client.query(_query)
    rows = query_job.result()
    return pd.DataFrame([dict(row) for row in rows])

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Graph

@st.cache_data(ttl=600)
def Athlete_histo(df, x,y, color, title,barmode='relative', text_auto=False,log_x=False, log_y=False, range_x=None, range_y=None, histfunc=None, labels={}):
    fig1 = px.histogram(df, x = x,y =y, color=color, title=title,barmode=barmode, text_auto=text_auto,log_x=log_x, log_y=log_y, range_x=range_x, range_y=range_y, histfunc=histfunc,labels=labels)
    return fig1

@st.cache_data(ttl=600)
def count_and_sort_editions(df, group_col, count_col, descending=True, top_n=None):
  result = (df.groupby(group_col)[count_col].count().reset_index().sort_values(by=count_col, ascending=not descending))
  if top_n:
        result = result.head(top_n)

@st.cache_data(ttl=600)
def nb_line(df, x,y, title, color=None, markers=True, hover_data='country_code', animation_frame=None,log_x=False, log_y=False, range_x=None, range_y=None, labels={}):
  line = px.line(df, x = x,y =y, color=color, title=title, hover_data=hover_data, markers=markers, animation_frame=animation_frame, log_x=log_x, log_y=log_y, range_x=range_x, range_y=range_y, labels=labels)
  