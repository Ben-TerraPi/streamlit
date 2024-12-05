import streamlit as st
import numpy as np
import pandas as pd
import pandas_gbq
from google.cloud import bigquery
from google.cloud import storage
from google.oauth2 import service_account
from google.cloud import storage
import plotly.express as px
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import gcsfs
from st_files_connection import FilesConnection
import pickle
import re
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    retrieve_object_from_bucket,
    get_data_from_bigquery,
    Athlete_histo_1,
    plot_olympics_trends,
    nb_line
)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>DATAFRAME

olympics_games_summer = pd.read_csv('data/olympics_games_summer.csv')
athlete_id_multiple = pd.read_csv('data/athlete_id_multiple.csv')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Streamlit page

st.set_page_config(
    page_title="JO History",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Title & intro

st.title('Olympic summer Games in time ')
    
st.markdown("""**A brief history of the olympic summer games.**""")

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Tab

tab1, tab2,tab3,tab4 = st.tabs(["Historic", "Countries & Sport","Athletes", "Top participations"])

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>tab1

with tab1:


    #Number of summer's JO hosted by country
    hist1 = Athlete_histo_1(olympics_games_summer,
                            x = 'country_code',
                            y="city_host", histfunc='count',
                            color="country_code",
                            title="Summer's JO hosted by country"
                            )

    hist1.update_xaxes(title_text="country", categoryorder='category ascending')
    hist1.update_layout(showlegend=False)
    st.plotly_chart(hist1)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>tab2

with tab2:


    line2 = plot_olympics_trends(olympics_games_summer.sort_values(by='year', ascending=True, inplace=False))
    line2.update_yaxes(categoryorder='category ascending')
    st.plotly_chart(line2)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>tab3

with tab3:

#Number of athletes by edition
    line1 = nb_line(olympics_games_summer.sort_values(by='year', ascending=True, inplace=False),
                    _x="year",
                    _y=["nb_athletes",
                    "nb_men",
                    "nb_women"],
                    _title="Athletes by edition",
                    _markers=True,
                    _hover_data='country_code'
                    )
    line1 = line1.update_traces(mode="lines+markers")
    line1.add_vline(x=1980,line_color="#00FF9C",line_dash="dash",line_width=3)
    line1.update_yaxes(title_text="number")
    st.plotly_chart(line1)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>TAB4
with tab4:
    st.write("List of athletes with at least two Olympic appearances")
    with st.container():
    
        col1, col2 = st.columns(2)

        with col1:

                ids = athlete_id_multiple[["participations","name",	"gender",	"country_code"]].sort_values("participations",ascending=False).set_index("name")
                st.dataframe(ids)
                
        with col2:

            score2 = px.pie(athlete_id_multiple,
                            names="gender")
            st.plotly_chart(score2)

