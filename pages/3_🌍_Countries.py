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
    Country_color,
    Athlete_histo_1,
    plot_top_10_medals_by_type
)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Streamlit page


st.set_page_config(
    page_title="Countries",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Title & intro

st.title('Analysis of participating countries')


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>SIDEBAR
with st.sidebar:
    st.logo("images/The_Phryges.svg.png")
    st.image("./images/logo-paris-2024.png")



#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>DATAFRAME

Athletes_medallists = pd.read_csv('data/Athletes_medallists.csv')
medals_total = pd.read_csv('data/medals_total.csv')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Sub tab

tab1, tab2,tab3,tab4 = st.tabs(["Globals","Distributions", "Sport groups","Results"])

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
            col6.metric("Medallist country", len(medals_total["country_name"].unique()))
           

    #1Athlètes number per country
    hist1 = Athlete_histo_1(Athletes_medallists,
                            x = 'country_name',
                            y =Athletes_medallists["code"],
                            histfunc='count',
                            color="country_name",
                            title="Athletes number per country")
    
    hist1 = hist1.update_xaxes(title_text="country",categoryorder='category ascending')
    hist1.update_yaxes(title_text="number")
    hist1.update_layout(showlegend=False)
    st.plotly_chart(hist1)


    #2Medals number per country
    hist2 = Athlete_histo_1(medals_total,
                            x = 'country_name',
                            y =medals_total["Total"],
                            histfunc='sum', color="country_name",
                            range_y=[0,150],
                            range_x=[0,92],
                            title="Medals number per country")
    
    hist2 = hist2.update_xaxes(title_text="country",categoryorder='category ascending')
    hist2.update_yaxes(title_text="number")
    hist2.update_layout(showlegend=False)
    st.plotly_chart(hist2)

with tab2:


    #>>>>>>>>>>>Athletes per countries distribution
    x = Athlete_histo_1(Athletes_medallists.groupby("country_name")["code"].nunique().reset_index().groupby("code").agg({"country_name": "count"}).reset_index(),
                x = 'code', y = 'country_name', barmode = "stack", log_y = True, histfunc= 'sum', title = "Athletes per country distribution", text_auto = True)
    x.update_traces(marker_line_width=1.5, marker_line_color="black", marker_color="lightgreen",textangle=0)  # Ajouter un contour noir
    x.update_layout(
        bargap=0.2,  # Espace entre les barres (entre 0 et 1, où 1 signifie aucun chevauchement)
        yaxis_title="Countries number",
        xaxis_title="Athletes number"
        )
    x.update_xaxes(nticks=20)
    st.plotly_chart(x)

    #>>>>>>>>>Medals per countries distribution
    x2 = Athlete_histo_1(medals_total.groupby("country_name")["Total"].sum().reset_index().sort_values("Total", ascending= False).groupby("Total").agg({"country_name": "count"}).reset_index(),
                    x = 'Total', y = 'country_name', barmode = "stack", log_y = False, histfunc= 'sum', title = "Medals number per countries distribution", text_auto = True)
    x2.update_traces(marker_line_width=1.5, marker_line_color="black", marker_color="lightgreen")  # Ajouter un contour noir
    x2.update_layout(
        bargap=0.2,  # Espace entre les barres (entre 0 et 1, où 1 signifie aucun chevauchement)
        yaxis_title="Countries number",
        xaxis_title="Medals number"
    )
    x2.update_xaxes(nticks=20)
    x2.update_traces(textangle=0)
    st.plotly_chart(x2)
      


with tab3:

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
    bar1.update_layout(showlegend=False)
    st.plotly_chart(bar1)

with tab4:

    #5Graph combiné Nb de médailles/types/pays + % medailles d'or/pays
    plot2 = plot_top_10_medals_by_type(medals_total)
    st.plotly_chart(plot2)

