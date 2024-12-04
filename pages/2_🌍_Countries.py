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

#>>>>>>>>>>>>>>>>>>>>>>>>>>>> Sub tab

tab1, tab2 = st.tabs(["Globals", "Sport group"])

with tab1:


    #>>>>>>>>>>>>>>>>>>>>>> Graph
    with st.container():
            col1, col2, col3 = st.columns([3, 3, 3],gap="large",vertical_alignment="bottom")
            

            col1.metric("Countries", len(Athletes_medallists["country_name"].unique()))
            col2.metric("Athlete numbers", Athletes_medallists["name"].value_counts().sum())
            col3.metric("Average age",round(Athletes_medallists["Age"].mean(),1))

    with st.container():
            col4, col5, col6 = st.columns([3, 3, 3],gap="large",vertical_alignment="bottom")

            col4.metric("Total medals", Athletes_medallists["medals_number"].count())
            col5.metric("Total sports", len(Athletes_medallists["sport_group"].unique()))
            col6.metric("Total events", len(Athletes_medallists["events"].unique()))
            

    #1Athletes per countries distribution
    x = Athlete_histo_1(Athletes_medallists.groupby("country_name")["code"].nunique().reset_index().groupby("code").agg({"country_name": "count"}).reset_index(),
                x = 'code', y = 'country_name', barmode = "stack", log_y = True, histfunc= 'sum', title = "Athletes per countries distribution", text_auto = True)
    x.update_traces(marker_line_width=1.5, marker_line_color="black", marker_color="lightgreen",textangle=0)  # Ajouter un contour noir
    x.update_layout(
        bargap=0.2,  # Espace entre les barres (entre 0 et 1, où 1 signifie aucun chevauchement)
        yaxis_title="Number of countries",
        xaxis_title="Number of athletes"
        )
    x.update_xaxes(nticks=20)
    st.plotly_chart(x)


    #1Athlètes number per country
    hist1 = Athlete_histo_1(Athletes_medallists,
                            x = 'country_name',
                            y =Athletes_medallists["code"],
                            histfunc='count',
                            color="country_name",
                            title="Athletes number per country")
    
    hist1 = hist1.update_xaxes(categoryorder='category ascending')
    st.plotly_chart(hist1)


            #1Medals per countries distribution
    x1 = Athlete_histo_1(Athletes_medallists.groupby("country_name")["medals_number"].nunique().reset_index().groupby("medals_number").agg({"country_name": "count"}).reset_index(),
                x = 'medals_number', y = 'country_name', barmode = "stack", log_y = True, histfunc= 'sum', title = "Medals per countries distribution", text_auto = True)
    x1.update_traces(marker_line_width=1.5, marker_line_color="black", marker_color="lightgreen",textangle=0)  # Ajouter un contour noir
    x1.update_layout(
        bargap=0.2,  # Espace entre les barres (entre 0 et 1, où 1 signifie aucun chevauchement)
        yaxis_title="Number of countries",
        xaxis_title="Number of medals"
        )
    x1.update_xaxes(nticks=10)
    st.plotly_chart(x1)

    #2Medals number per country
    hist2 = Athlete_histo_1(medals_total,
                            x = 'country_name',
                            y =medals_total["Total"],
                            histfunc='sum', color="country_name",
                            range_y=[0,150],
                            range_x=[0,92],
                            title="Medals number per country")
    
    hist2 = hist2.update_xaxes(categoryorder='category ascending')
    st.plotly_chart(hist2)


    #5Graph combiné Nb de médailles/types/pays + % medailles d'or/pays
    plot2 = plot_top_10_medals_by_type(medals_total)
    st.plotly_chart(plot2)

with tab2:

    sport_groups = st.selectbox("Select sport group of athlete",
                    Athletes_medallists.sport_group.unique(),
                    index = None
                    )        

    sport_group_filter = sport_groups
    filtered_Athletes_medallists = Athletes_medallists[Athletes_medallists["sport_group"] == sport_group_filter]
    grouped_medallists = filtered_Athletes_medallists.groupby("country_name", as_index=False)["medals_number"].sum()
    top_10 = grouped_medallists.sort_values("medals_number", ascending=False).head(10)

    bar1 = px.bar(
        top_10,
        x="country_name",
        y="medals_number",
        title=f"Medals by Country for {sport_group_filter}",
        labels={"medals_number": "Total Medals", "country_name": "Country"},
        #text="medals_number",
        color="country_name"
    )
    #bar1.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    bar1.update_layout(
        xaxis_title="Country",
        yaxis_title="Total Medals",
        uniformtext_minsize=8,
        uniformtext_mode="hide",
    )
    st.plotly_chart(bar1)

