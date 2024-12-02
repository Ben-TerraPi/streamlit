import streamlit as st
import numpy as np
import pandas as pd
import pandas_gbq
from google.cloud import bigquery
from google.oauth2 import service_account
import plotly.express as px
from plotly import graph_objects as go
import gcsfs
from st_files_connection import FilesConnection


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Query

@st.cache_data(ttl=600)
def get_data_from_bigquery(_query, _client):
    query_job = _client.query(_query)
    rows = query_job.result()
    return pd.DataFrame([dict(row) for row in rows])

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Graph

#HISTOGRAMME
@st.cache_data(ttl=600)
def Athlete_histo_1(df, x,y, title,barmode='relative',text_auto=False,log_x=False, log_y=False,
                    range_x=None, range_y=None, histfunc=None,color=None,facet_row=None, facet_col=None, labels=None, yaxes = True,
                    yaxes_title=True, xaxes_title=True, xaxes = True, category_orders=None,facet_col_wrap=None, facet_col_spacing=None,facet_row_spacing=None):
  fig1 = px.histogram(df, x = x,y =y, color=color, title=title,barmode=barmode,text_auto= text_auto,log_x=log_x, log_y=log_y,
                      range_x=range_x, range_y=range_y,facet_row=facet_row, facet_col=facet_col, histfunc=histfunc,
                      labels=labels, category_orders = category_orders,
                      facet_col_wrap=facet_col_wrap, facet_col_spacing=facet_col_spacing,facet_row_spacing=facet_row_spacing)
  if yaxes_title != True:
    fig1.update_yaxes(title_text=yaxes_title)
  if xaxes_title != True:
    fig1.update_xaxes(title_text=xaxes_title)
  fig1.update_yaxes(visible=yaxes, showticklabels=True)
  fig1.update_xaxes(visible=xaxes, showticklabels=True)
  return(fig1)

#BAR
@st.cache_data(ttl=600)
def Bar_chart_1(df, x,y, title,barmode='relative',text=None,log_x=False, log_y=False,
                    range_x=None, range_y=None,color=None,facet_row=None, facet_col=None, labels=None, yaxes = True,
                    yaxes_title=True, xaxes_title=True, xaxes = True, category_orders=None,):
  fig1 = px.bar(df, x = x,y =y, color=color, title=title,barmode=barmode,text= text,log_x=log_x, log_y=log_y,
                      range_x=range_x, range_y=range_y,facet_row=facet_row, facet_col=facet_col,
                      labels=labels, category_orders = category_orders)
  if yaxes_title != True:
    fig1.update_yaxes(title_text=yaxes_title)
  if xaxes_title != True:
    fig1.update_xaxes(title_text=xaxes_title)
  fig1.update_yaxes(visible=yaxes, showticklabels=True)
  fig1.update_xaxes(visible=xaxes, showticklabels=True)
  return(fig1)


#-------------------------------------------------------------------------------------------------------------------

@st.cache_data(ttl=600)
def count_and_sort_editions(df, group_col, count_col, descending=True, top_n=None):
  result = (df.groupby(group_col)[count_col].count().reset_index().sort_values(by=count_col, ascending=not descending))
  if top_n:
        result = result.head(top_n)
  return result

@st.cache_data(ttl=600)
def nb_line(df, x,y, title, color=None, markers=True, hover_data='country_code', animation_frame=None,log_x=False, log_y=False, range_x=None, range_y=None, labels={}):
  line = px.line(df, x = x,y =y, color=color, title=title, hover_data=hover_data, markers=markers, animation_frame=animation_frame, log_x=log_x, log_y=log_y, range_x=range_x, range_y=range_y, labels=labels)
  return line