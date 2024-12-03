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
    create_country_indicator
)


#>>>>>>>>>>>>>>>>>>>>>>>>>DATAFRAME


olympics_games_summer = pd.read_csv('data/olympics_games_summer.csv')
Athletes_medallists = pd.read_csv('data/Athletes_medallists.csv')


#>>>>>>>>>>>>>>>>>>>>> Streamlit page


st.set_page_config(
    page_title="Athletes",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

#Title & intro

st.title('Macro Analysis')

st.markdown("""**Welcome to the Paris 2024 Olympic Games data visualization dashboard.**""")


#2Scorecards
# score1 = subplots_scorecards(score_card_1(olympics_games_summer, Athletes_medallists, "year", 2020, "nb_athletes", "code"),score_card_2(df1 = olympics_games_summer,df2 = Athletes_medallists,filter = 2020,colum1 = "nb_athletes",column2 = "code") )
# st.plotly_chart(score1)

#3Athletes number per Sport Family, (events number per sport_family)
bar1 = Bar_chart_1(Athletes_medallists.groupby(['sport_family']).agg({"disciplines":"nunique", "name" : "count", "events":"nunique"}).sort_values(by = ["name"], ascending = False).reset_index().head(32),
            y = 'name',x='sport_family', color = 'sport_family', text='events', yaxes_title= "Athletes number",
            title="Athletes number per Sport Family, (events number per sport_family)",
            textangle= 0, textposition = 'outside')
st.plotly_chart(bar1)

#4Athletes number per Sport Family, (events number per sport_group)
bar2 = Bar_chart_1(Athletes_medallists.groupby(["disciplines"]).agg({"sport_group" : 'max', "events":"nunique", "name" : "count"}).sort_values(by = ["name"], ascending = False).reset_index().groupby(["sport_group"]).agg({"disciplines":"nunique", "name" : "sum", "events":"sum"}).sort_values(by = ["name"], ascending = False).reset_index(),y = 'name',
                    x='sport_group', color = 'sport_group', text='events', yaxes_title= "Athletes number", title="Athletes number per Sport Group, (events number per Sport Group)",textangle= 0, textposition = 'inside')
st.plotly_chart(bar2)

#5Athletes number per country (top 20)
hist1 = Athlete_histo_1(df = Athletes_medallists.groupby(["country_name"]).agg({"code" : "count"}).sort_values(by = ["code"], ascending = False).reset_index().head(20),
                x = 'country_name',y ="code", histfunc='sum', color="country_name", title="Athletes number per country (top 20)", yaxes_title="Athletes number")

st.plotly_chart(hist1)

# #6Athletes number per sport family
# hist2 = Athletes_number_per_sport_family (Athletes_medallists)
# st.plotly_chart(hist2)

#7Athletes number per sport group
hist3 = Athlete_histo_1(Athletes_medallists, x = 'sport_group',y =Athletes_medallists.index, histfunc='count',color="sport_group",
                title="Athletes number per sport group", category_orders = {"sport_group": Athletes_medallists["sport_group"].sort_values().unique().tolist()}, yaxes_title= "Athletes number")
st.plotly_chart(hist3)

# #8Athletes number Women/Men ratio category displays by country ** representing values as powers of a base 10
# hist4 = Athlete_histo_1(gender_ratio(Athletes_medallists, column = "gender", column2= "code").sort_values(['category','athletes'],ascending = False),
#                     x= "country_code" , y ='athletes', histfunc='sum',color="category",
#                     title="Athletes number Women/Men ratio category displays by country ** representing values as powers of a base 10",barmode= 'group',
#                     xaxes= False, yaxes_title= "Athletes number (log10)" ,xaxes_title=" Country", log_y= True)
# st.plotly_chart(hist4)

# #9Athletes number per age
# hist5 = Hist_tab_athletes_age(Athletes_medallists)
# st.plotly_chart(hist5)

# #10Top 5 athletes per Sport (Group : Family)
# top1 = Top (Selection(Athletes_medallists,"sport_family",["Aquatics", "Athletics","Cycling","Judo","Table Tennis", "Equestrian"]),top = 5, gpby1 = "sport_family", gpby2 = "country_name",color_palette = Country_color(Athletes_medallists), title="Top 5 nb athletes per Countries per Sport Family")
# st.plotly_chart(top1)

# top2 = Top (Selection(Athletes_medallists[Athletes_medallists['medals_number']>0],"sport_family",["Aquatics", "Athletics","Cycling","Judo","Table Tennis","Equestrian"]),top = 5, gpby1 = "sport_family", gpby2 = "country_name",color_palette = Country_color(Athletes_medallists),title= "Top 5 nb medalled athletes per Countries per Sport Family")
# st.plotly_chart(top2)

#11nombre de médailles par athlète
top3 = Athlete_medals_top20(df = Athletes_medallists, filter = 'medals_number',title = "Top 20 médailles par athlète", Text = "ratio_medals / events_number")
st.plotly_chart(top3)

top4 = Athlete_medals_top20(df = Athletes_medallists, filter = "Gold Medal", title = "Top 20 médailles d'or par athlète", Text = 'Age')
st.plotly_chart(top4)

#12distribution of the number of events in which an athlete has participated
distri1 = Distribution_events_nb (Athletes_medallists)
st.plotly_chart(distri1)



