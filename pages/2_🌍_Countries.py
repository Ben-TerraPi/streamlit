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
    create_country_indicator,
    plot_top_10_athletes_pie,
    plot_top_10_medals_by_type
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


#>>>>>>>>>>>>>>>>>>>>>>>>>DATAFRAME

Athletes_medallists = pd.read_csv('data/Athletes_medallists.csv')
medals_total = pd.read_csv('data/medals_total.csv')

#>>>>>>>>>>>>>>>>>>>>>> Graph

#6Scorecard nb Pays
fig_nb_pays = create_country_indicator(Athletes_medallists)
st.plotly_chart(fig_nb_pays)

#1Athlètes number per country
hist1 = Athlete_histo_1(Athletes_medallists, x = 'country_name',y =Athletes_medallists["code"], histfunc='count', color="country_name", title="Athletes number per country")
hist1 = hist1.update_xaxes(categoryorder='category ascending')
st.plotly_chart(hist1)

#2Medals number per country
hist2 = Athlete_histo_1(medals_total, x = 'country_name',y =medals_total["Total"], histfunc='sum', color="country_name",range_y=[0,150],range_x=[0,92], title="Medals number per country")
hist2 = hist2.update_xaxes(categoryorder='category ascending')
st.plotly_chart(hist2)

# #3Top 10 countries with the most disciplines
# hist3 = Athlete_histo_1(Athletes_medallists.groupby('country_name')['disciplines'].nunique().sort_values(ascending=False).head(10), x = 'country_name',y = 'disciplines', histfunc='sum', color="country_name",title="Top 10 countries with the most disciplines")
# st.plotly_chart(hist3)

# #4Top 10 countries with the most athletes
# plot1 = plot_top_10_athletes_pie(Athletes_medallists)
# st.plotly_chart(plot1)

#5Graph combiné Nb de médailles/types/pays + % medailles d'or/pays
plot2 = plot_top_10_medals_by_type(medals_total)
st.plotly_chart(plot2)



