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
import seaborn as sns
from plotly.subplots import make_subplots
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

olympics_games_summer = pd.read_csv('data/olympics_games_summer.csv')

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

#>>>>>>>>>>>>>>>>>>>>>> Graph


#olympics_games_summer
hist1 = Athlete_histo_1(olympics_games_summer,
                        x = 'country_code',
                        y="city_host", histfunc='count',
                        color="country_code",
                        title="Number of summer's JO hosted by country"
                        )

hist1.update_xaxes(categoryorder='category ascending')
st.plotly_chart(hist1)

#top3 summer
top_summer = count_and_sort_editions(olympics_games_summer,
                                        'country_code',
                                        "year",
                                        descending=True,
                                        top_n=3
                                        )
st.dataframe(top_summer)

st.line_chart(olympics_games_summer,
              x="year",
              y=["nb_athletes",
                 "nb_men",
                 "nb_women"])
    
line1 = nb_line(olympics_games_summer,
                x="year",
                y=["nb_athletes",
                   "nb_men",
                   "nb_women"],
                   title="Number of athletes by edition")
    
st.plotly_chart(line1, use_container_width=True)

line2 = plot_olympics_trends(olympics_games_summer)
st.plotly_chart(line2)