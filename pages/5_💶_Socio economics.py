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
    spearman_corr
)

#>>>>>>>>>>>>>>>>>>>>> Streamlit page


st.set_page_config(
    page_title="Socio economics",
    page_icon="💶",
    layout="wide",
    initial_sidebar_state="expanded",
)

#Title & intro

st.title('Socio Economics Analysis')

st.markdown("""**Welcome to the Paris 2024 Olympic Games data visualization dashboard.**""")

#>>>>>>>>>>>>>>>>>>>>>>>>>DATAFRAME

Socio_economic_Dataset = pd.read_csv('data/Socio_economic_Dataset.csv')
Athletes_medallists = pd.read_csv('data/Athletes_medallists.csv')
medals_total = pd.read_csv('data/medals_total.csv')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>> Sub tab

tab1, tab2,tab3 = st.tabs(["World", "Europe","extra"])

with tab1:

    #>>>>>>>>>>>>>>>>>>>>>> Graph

    corr1 = spearman_corr(Socio_economic_Dataset)
    st.plotly_chart(corr1)

    #1Correlation between GDP and Total medals by Gold medals
    line1 = nb_line(Socio_economic_Dataset, _x = 'Total medals', _y = 'GDP',
            _title = 'Correlation between GDP and Total medals by Gold medals',
            _color = 'Continent', _hover_data='country_name', _size='Gold medals',_marginal_x='violin',_marginal_y='violin')
    st.plotly_chart(line1)

    #2Correlation between GDP per capita and Total medals
    line2 = nb_line(Socio_economic_Dataset, _y = 'Total medals', _x = 'GDP per capita',
            _title = 'Correlation between GDP per capita and Total medals (size = Gold medals)', _color = 'country_name', _size = 'Gold medals')
    line2.update_layout(showlegend=False)
    st.plotly_chart(line2)

    # #3Correlation between GDP and Total medals by continent
    line3 = nb_line(Socio_economic_Dataset, _x = 'GDP', _y = 'Total medals',
            _title = 'Correlation between GDP and Total medals by continent',_color='Continent',
            _hover_data='country_name', _size = 'Population', _log_y=True, _marginal_x='violin', _marginal_y='violin')
    st.plotly_chart(line3)

    #4Life expectancy vs Total medals,(circle size = Population)
    line4 = nb_line(_df= Socio_economic_Dataset, _y='Total medals', _x ="Life expectancy",
            _color= "Continent",_title = "Life expectancy vs Total medals,(circle size = Population)",
            _markers=True, _hover_data='country_name', _size="Population", _size_max = 40, _marginal_y = "violin",_marginal_x = "violin")
    st.plotly_chart(line4)

    #5Life expectancy vs Total medals
    line5 = nb_line(_df= Socio_economic_Dataset, _y='Total medals', _x ="Life expectancy",
            _color= "Continent",_title = "Life expectancy vs Total medals,(circle size = GDP per capita)",
            _markers=True, _hover_data='country_name', _size="GDP per capita", _size_max = 40, _marginal_y = "violin",_marginal_x = "violin")
    st.plotly_chart(line5)

    #6Democracy Index vs Total medals
    line6 = nb_line(_df= Socio_economic_Dataset, _y='Total medals', _x ="Democracy",
            _color= "Continent",_title = "Democracy Index vs Total medals,(circle size = GDP per capita)",
            _markers=True, _hover_data='country_name', _size="GDP per capita", _size_max = 40, _marginal_y = "violin",_marginal_x = "violin")
    st.plotly_chart(line6)

    #7Gender Inequality Index vs Total medals
    line6 = nb_line(_df= Socio_economic_Dataset, _y='Total medals', _x ="Gender equality",
            _color= "Continent",_title = "Gender Inequality Index vs Total medals,(circle size = GDP)",
            _markers=True, _hover_data='country_name', _size="GDP per capita", _size_max = 40, _marginal_y = "violin",_marginal_x = "violin")
    st.plotly_chart(line6)

    #11urban population
    line11 = nb_line(Socio_economic_Dataset,
            _x = 'urban_population',
            _y ='Total medals',
            _title='Urban population for Total medals, size = GDP',
            _color='Continent',
            _hover_data='Total medals',
            _size='GDP',
            _size_max = 50)
    st.plotly_chart(line11)

    #12tot pop by medal
    line12 = nb_line(Socio_economic_Dataset,
                    _x = 'total_population',
                    _y ='Total medals',
                    _title='Total population for Total medals, size = GDP',
                    _color='Continent',
                    _hover_data='Total medals',
                    _size='GDP',
                    _size_max = 50)
    st.plotly_chart(line12)

    #13
    line13 = nb_line(_df = Socio_economic_Dataset,                
                    _x='Number of athletes',
                    _y='Total medals',
                    _title='Number of athletes for Total medals, size = GDP',
                    _color='Continent',
                    _hover_data='Total medals',
                    _size='total_population',
                    _size_max=50)
    st.plotly_chart(line13)


with tab2:

    #8percentage_of_total_employment linked to Sports vs Total medals
    line7 = nb_line(_df= Socio_economic_Dataset.loc[Socio_economic_Dataset['Continent'] == 'Europe'], _y='Total medals', _x ="percentage_of_total_employment",
            _color= "country_name",_title = "percentage_of_total_employment linked to Sports vs Total medals,(circle size = Number of athletes)",
            _markers=True, _hover_data='country_name', _size="Number of athletes", _size_max = 40)
    line7.update_layout(showlegend=False)
    st.plotly_chart(line7)

    #8Share of the budget allocated to sports vs Total medals
    line8 = nb_line(_df= Socio_economic_Dataset.loc[Socio_economic_Dataset['Continent'] == 'Europe'], _y='Total medals', _x ="GF0801",
            _color= "country_name",_title = "Share of the budget allocated to sports vs Total medals,(circle size = Number of athletes)",
            _markers=True, _hover_data='country_name', _size="Number of athletes", _size_max = 40)
    line8.update_layout(showlegend=False)
    st.plotly_chart(line8)

    #9Share of the budget allocated to sports vs Gold medals
    line9 = nb_line(_df= Socio_economic_Dataset.loc[Socio_economic_Dataset['Continent'] == 'Europe'], _y='Gold medals', _x ="GF0801",
            _color= "country_name",_title = "Share of the budget allocated to sports vs Gold medals,(circle size = Number of athletes)",
            _markers=True, _hover_data='country_name', _size="Number of athletes", _size_max = 40)
    line9.update_layout(showlegend=False)
    st.plotly_chart(line9)

    #10
    line10 = nb_line(_df= Socio_economic_Dataset.loc[Socio_economic_Dataset['Continent'] == 'Europe'], _y='Gold medals', _x ="sports_facilities_very_satisfied_2023",
            _color= "country_name",_title = "sports_facilities_very_satisfied_2023 vs Gold medals,(circle size = Number of athletes)",
            _markers=True, _hover_data='country_name', _size="Number of athletes", _size_max = 40)
    line10.update_layout(showlegend=False)
    st.plotly_chart(line10)
