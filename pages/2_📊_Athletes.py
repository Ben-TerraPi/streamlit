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
    piepiepie,
    Women_vs_Men_medals_distribution
)


#>>>>>>>>>>>>>>>>>>>>> Streamlit page
st.set_page_config(
    page_title="Athletes",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Title & intro

st.title('Analysis of athletes')


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>SIDEBAR
with st.sidebar:
    st.logo("images/The_Phryges.svg.png")
    st.image("./images/logo-paris-2024.png")

#>>>>>>>>>>>>>>>>>>>>>>>>>DATAFRAME

olympics_games_summer = pd.read_csv('data/olympics_games_summer.csv')
Athletes_medallists = pd.read_csv('data/Athletes_medallists.csv')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs(["Indicators","Globals", "by Sports", "Distributions", "Gender Equality","Results"])

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>tab1

with tab1:  

    with st.container():
    
        col1, col2 = st.columns(2)

        with col1:
                
            score1 = score_card_1(olympics_games_summer,
                        Athletes_medallists,
                        "year",
                        2020,
                        "nb_athletes",
                        "code"
                        )
            st.plotly_chart(score1)
        
        with col2:

            score2 = score_card_2(df1 = olympics_games_summer,
                        df2 = Athletes_medallists,
                        filter = 2020,
                        colum1 = "nb_athletes",
                        column2 = "code")
            st.plotly_chart(score2)       

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Tab2

with tab2:
        
    with st.container():
        col1, col2, col3,col4 = st.columns([2, 2, 2, 2],gap="large",vertical_alignment="bottom")
        

        col1.metric("Youngest Athlete",
                        Athletes_medallists["Age"].min())
        col2.metric("Youngest medalist",
                        Athletes_medallists[Athletes_medallists["medals_number"] > 0 ]["Age"].min())
        col3.metric("Oldest Athlete",
                        (Athletes_medallists["Age"].max()))
        col4.metric("Oldest medalist",
                    Athletes_medallists[Athletes_medallists["medals_number"] > 0 ]["Age"].max())
        
    with st.container():
        col5,col6,col7,col8 = st.columns([2, 2, 2,2],gap="large",vertical_alignment="bottom")

        col5.metric("Total events",
                    (Athletes_medallists.groupby(['events'])["gender"].value_counts().reset_index().groupby("gender").agg({"events" : "count"}).reset_index()["events"][0])+(Athletes_medallists.groupby(['events'])["gender"].value_counts().reset_index().groupby("gender").agg({"events" : "count"}).reset_index()["events"][1]))

        col6.metric("Women events",
                    Athletes_medallists.groupby(['events'])["gender"].value_counts().reset_index().groupby("gender").agg({"events" : "count"}).reset_index()["events"][0])         
        col7.metric("Men events",
                    Athletes_medallists.groupby(['events'])["gender"].value_counts().reset_index().groupby("gender").agg({"events" : "count"}).reset_index()["events"][1])
        col8.write("")

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>TAB4

with tab4:
    #9Athletes number per age
    hist5 = Hist_tab_athletes_age(Athletes_medallists)
    hist5.update_xaxes(title_text="age")
    hist5.update_yaxes(title_text="number")
    st.plotly_chart(hist5)

    #12distribution of the number of events in which an athlete has participated
    distri1 = Distribution_events_nb (Athletes_medallists)
    distri1.update_layout(showlegend=False)
    st.plotly_chart(distri1)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>TAB6

with tab6:
        
    # with st.container():

    #     col1, col2 = st.columns(2)
    #     with col1:
    #         pie1 = piepiepie(Athletes_medallists)
    #         st.plotly_chart(pie1)
    #     with col2:

            
    #11nombre de médailles par athlète
    top3 = Athlete_medals_top20(df = Athletes_medallists, filter = 'medals_number',title = "Top 20 medals per athlete", Text = "ratio_medals / events_number")
    top3.update_layout(height=650, width=1500)
    st.plotly_chart(top3)

    top4 = Athlete_medals_top20(df = Athletes_medallists, filter = "Gold Medal", title = "Top 20 gold medals per athlete", Text = 'Age')
    top4.update_layout(height=650, width=1500)
    st.plotly_chart(top4)

    #
    bar18= Women_vs_Men_medals_distribution (Athletes_medallists)
    bar18.update_xaxes(title_text="medals")
    st.plotly_chart(bar18)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>TAB5
with tab5:

        #8Athletes number Women/Men ratio category displays by country ** representing values as powers of a base 10
    hist5 = Athlete_histo_1(gender_ratio(Athletes_medallists, column = "gender", column2= "code").sort_values(['category',
                                                                                                               'athletes'],
                                                                                                               ascending = False),
                        x= "country_code" ,
                        y ='athletes',
                        histfunc='sum',
                        color="category",
                        title="Women/Men ratio category displayed by country",barmode= 'group',
                        xaxes= False,
                        yaxes_title= "Athletes number (log10)" ,
                        xaxes_title=" Country",
                        log_y= True)
    st.plotly_chart(hist5)




#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>TAB5

with tab3:

    #Athletes number per Sport Group, (events number per sport_group)
    bar2 = Bar_chart_1(Athletes_medallists.groupby(["disciplines"]).agg({"sport_group" : 'max',
                                                                          "events":"nunique",
                                                                            "name" : "count"}).sort_values(by = ["name"],
                                                                                                            ascending = False).reset_index().groupby(["sport_group"]).agg({"disciplines":"nunique",
                                                                                                                                                                            "name" : "sum",
                                                                                                                                                                            "events":"sum"}).sort_values(by = ["name"],
                                                                                                                                                                                                         ascending = False).reset_index(),
                                                                                                                                                                                                         y = 'name',
                                                                                                                                                                                                         x='sport_group',
                                                                                                                                                                                                         color = 'sport_group',
                                                                                                                                                                                                         text='events',
                                                                                                                                                                                                         yaxes_title= "Athletes number",
                                                                                                                                                                                                         title="Athletes number per sport group, (+ events number displayed)",
                                                                                                                                                                                                         textangle= 0,
                                                                                                                                                                                                         textposition = 'inside')
    bar2.update_layout(showlegend=False)
    bar2.update_xaxes(title_text="Sport group")
    st.plotly_chart(bar2)


    #4Athletes number per Sport Family, (events number per sport_family)
    bar1 = Bar_chart_1(Athletes_medallists.groupby(['sport_family']).agg({"disciplines":"nunique", "name" : "count", "events":"nunique"}).sort_values(by = ["name"], ascending = False).reset_index().head(32),
                y = 'name',x='sport_family', color = 'sport_family', text='events', yaxes_title= "Athletes number",
                title="Athletes number per Sport Family, (+ events number displayed)",
                textangle= 0, textposition = 'outside')
    bar1.update_layout(showlegend=False)
    bar1.update_xaxes(title_text="Sport family")
    st.plotly_chart(bar1)

    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # nice_tab = user1(gender_ratio(Athletes_medallists, column = "gender", column2= "code").sort_values(['category','athletes'],ascending = False))
    # st.plotly_chart(nice_tab)

#ADD LINE SCATTER FOR NB ATHLETE<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # #3Top 10 countries with the most disciplines
    # hist3 = Athlete_histo_1(Athletes_medallists.groupby('country_name')['disciplines'].nunique().sort_values(ascending=False).reset_index().head(10), x = 'country_name',y = 'disciplines', histfunc='sum', color="country_name",title="Top 10 countries with the most disciplines")
    # st.plotly_chart(hist3)



    # #10Top 5 athletes per Sport (Group : Family)
    # top1 = Top (Selection(Athletes_medallists,
    #                       "sport_family",
    #                       ["Aquatics", "Athletics","Cycling","Judo","Table Tennis", "Equestrian"]),
    #                       top = 5,
    #                       gpby1 = "sport_family",
    #                       gpby2 = "country_name",
    #                       color_palette = Country_color(Athletes_medallists),
    #                       title="Top 5 nb athletes per Countries per Sport Family")
    # st.plotly_chart(top1)

    # top2 = Top (Selection(Athletes_medallists[Athletes_medallists['medals_number']>0],"sport_family",["Aquatics", "Athletics","Cycling","Judo","Table Tennis","Equestrian"]),top = 5, gpby1 = "sport_family", gpby2 = "country_name",color_palette = Country_color(Athletes_medallists),title= "Top 5 nb medalled athletes per Countries per Sport Family")
    # st.plotly_chart(top2)




