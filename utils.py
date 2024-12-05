import streamlit as st
import numpy as np
import pandas as pd
import pandas_gbq
from google.cloud import bigquery, storage
from google.oauth2 import service_account
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import gcsfs
from st_files_connection import FilesConnection
import pickle
import re



#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Query

@st.cache_data(ttl=600)
def get_data_from_bigquery(_query, _client):
    query_job = _client.query(_query)
    rows = query_job.result()
    return pd.DataFrame([dict(row) for row in rows])


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Connection to GCP Buckets

def retrieve_object_from_bucket(project_id, bucket_name, object_name, destination_file_path, service_account_file):
    
    """
        project_id (str): Your Google Cloud project ID.
        bucket_name (str): The name of the GCS bucket.
        object_name (str): The name of the object you want to retrieve.
        destination_file_path (str): The path to save the retrieved object locally.
    """
    
    #try:
    # Initialize a GCS client
    client = storage.Client.from_service_account_json(service_account_file)
    print(f"client:{client}")
    # Get the bucket
    bucket = client.get_bucket(bucket_name)
    print(f"client:{bucket}")
    # Get the blob (object) from the bucket
    blob = bucket.blob(object_name)
    print(f"client:{blob}")
    # Download the blob to the specified file path
    blob.download_to_filename(destination_file_path)
    print(f"client:{destination_file_path}")
    print(f"Object '{object_name}' retrieved and saved to '{destination_file_path}'.")

    #except Exception as e:
    #    print(f"Error: {e}")


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>SELECTION

#Selection avec filter

def Selection (df,column,selection):
  if not selection:  # Vérifie si la liste est vide
        return df
  df = df[df[column].isin(selection)]
  return (df)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>COLOR

def Country_color(df):
  '''
create a dictionary with country as key and color as value
  '''
  # df = Athletes_medallists
  Country_color = df["country_name"].unique().tolist()
  num_categories = len(Country_color)
  base_palette = px.colors.qualitative.Dark24
  extended_palette = (base_palette * (num_categories // len(base_palette) + 1))[:num_categories]
  # (base_palette * (num_categories // len(base_palette) + 1)) l'opération base_palette * (num_categories // len(base_palette) + 1)
  # [:num_categories] la liste finale a exactement num_categories couleurs
  color_palette_dict = {country: color for country, color in zip(Country_color, extended_palette)}
  # Filtrer le dictionnaire

  return(color_palette_dict)

         #
        # #
       #   #
      #  |  #
     #   .   #
    # # # # # #

  ### dans les graphs, si utilisation de color comme argument
  color_discrete_map = color_palette_dict

  ### dans les graphs, si utilisation de color_discrete_map comme argument

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>GRAPH

#TOP editions

def count_and_sort_editions(df, group_col, count_col, descending=True, top_n=None):
  result = (df.groupby(group_col)[count_col].count().reset_index().sort_values(by=count_col, ascending=not descending))
  if top_n:
        result = result.head(top_n)
  return result

#line
def nb_line1(df, x,y, title, color=None, markers=True, hover_data='country_code', animation_frame=None,log_x=False, log_y=False, range_x=None, range_y=None, labels={}):
  line = px.scatter(df, x = x,y =y, color=color, title=title, hover_data=hover_data, markers=markers, animation_frame=animation_frame, log_x=log_x, log_y=log_y, range_x=range_x, range_y=range_y, labels=labels)
  return line

#Scatter

def nb_line(_df, _x,_y, _title = None, _color=None, _markers=True,
            _hover_data=None,_size=None, _marginal_x=None,
            _marginal_y=None, _size_max= None, _log_x = None, _log_y = None):
  _df = _df.rename(columns={"Gender equality":"Gender Inequality"})
  # Now use the modified DataFrame for plotting
  if _size:
    _df[_size] = pd.to_numeric(_df[_size], errors='coerce') #Convert to numeric, coerce errors to NaN
    _df = _df.dropna(subset=[_size])
  line = px.scatter(_df, x = _x,y = _y,title=_title, color=_color,
                    hover_data=_hover_data,size=_size , marginal_x= _marginal_x,
                    marginal_y=_marginal_y, size_max= _size_max, log_x = _log_x, log_y = _log_y)
  return line

#hisotogramme + line

def plot_olympics_trends(data, title="Countries and Sports by Olympic Edition"):

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Line trace for number of countries
    line_trace = go.Scatter(
        x=data["year"],
        y=data["nb_country"],
        mode="lines+markers",
        name="Countries number",
        hovertemplate=(
            "Year: %{x}<br>"
            + "Number of Countries: %{y}<br>"
            + "Country Code: %{customdata}<extra></extra>"
        ),
        customdata=data["country_code"],
    )
    fig.add_trace(line_trace, secondary_y=False)

    # Bar trace for number of sports
    bar_trace = go.Bar(
        x=data["year"],
        y=data["nb_sports"],
        name="Sports number",
        marker=dict(opacity=0.6),
        marker_color ="#00FF9C",
        hovertemplate=(
            "Year: %{x}<br>"
            + "Sports number: %{y}<br>"
            + "Country Code: %{customdata}<extra></extra>"
        ),
        customdata=data["country_code"],  # Add country code to hover data
    )
    fig.add_trace(bar_trace, secondary_y=True)

    # Update layout and axis titles
    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title="Countries number",
    )

    # Update secondary y-axis title
    fig.update_yaxes(title_text="Sports number", secondary_y=True)

    return fig

#Top 10 countries with the most athletes

def plot_top_10_athletes_pie(df):
    # Count athletes per country
    athlete_counts = df['country_name'].value_counts().head(10)

    # Create the pie chart
    fig = px.pie(athlete_counts, values=athlete_counts["values"], names=athlete_counts.index,
                 title='Top 10 Countries with the Most Athletes',
                 labels={'names':'country_name'})
    fig.show()

#ratio medal non medal
def piepiepie(Athletes_medallists,values=None,name=None):
  if Athletes_medallists[Athletes_medallists["medals_number"] < 0]:
    Athletes_medallists["medals"] = 0
  else:
    Athletes_medallists["medals"] = 1
  fig = px.pie(Athletes_medallists, values=values, names=name)       
  return fig

#Graph combiné Nb de médailles/types/pays + % medailles d'or/pays

def plot_top_10_medals_by_type(df):
    """
    df = medals_total
    """
    top_10 = df.sort_values(by='Total', ascending=False).head(10)
    top_10['ratio'] = top_10['Gold Medal']/top_10['Total'] * 100
    country_medals = df.groupby('country_name').sum().sort_values(by=['Gold Medal', 'Silver Medal','Bronze Medal'], ascending=[False, False, False]).head(10)
    color_discrete_map = {
        'Gold Medal': 'gold',
        'Silver Medal': 'silver',
        'Bronze Medal': '#CD7F32'
    }
    fig= px.bar(country_medals,
                 x=country_medals.index,
                 y=['Gold Medal', 'Silver Medal', 'Bronze Medal'],
                 title='Top 10 Countries by Medal Type',
                 labels={'value':'Number of Medals', 'variable':'Medal Type', 'country_name':'Country'},
                 barmode='group',
                 color_discrete_map=color_discrete_map)
# Line chart
    data=top_10.sort_values(by=['Gold Medal','Silver Medal','Bronze Medal'], ascending=[False, False, False])

    # Ajout du line chart comme une trace
    fig.add_trace(
        go.Scatter(
            x=data.country_name,
            y=data.ratio,
            mode='lines+markers',
            name='Gold Medal Ratio (%)',
            line=dict(color='green', width=2),
            marker=dict(size=8, symbol='circle')
        )
    )
    return fig

#Scorecard nb Pays

def create_country_indicator(df):
    """
    df = Athletes_medallists

    """
    fig_nb_pays = go.Figure(go.Indicator(
        mode="number",
        value= df['country_name'].nunique(),
        number={'suffix': '', 'valueformat': ',.0f'},
        title={'text': "Number of countries"},
        domain={'x': [0, 1], 'y': [0, 1]},
        # gauge={
        #     'bar': {'color': "blue"}  # Couleur de la barre
        # }
    ))
    return fig_nb_pays


#percentile

def percentile(n):
    def percentile_(x):
        return x.quantile(n)
    percentile_.__name__ = 'percentile_{:02.0f}'.format(n*100)
    return percentile_

#gender_ratio

def gender_ratio(Athletes_medallists, column, column2):
  '''
athletes = Athletes_medallists
column = "gender"
column2 = "code"
  '''
  
  df = pd.DataFrame(Athletes_medallists.groupby("country_code")[column].value_counts(normalize=True).unstack()).reset_index().sort_values('Female', ascending= False)
  print("----------------------------------------------------------------")
  print(df.columns)
  df.fillna(0, inplace=True)
  df["athletes"] = Athletes_medallists.groupby("country_code")[column2].nunique().reset_index()[column2]
  df['Female'] = df['Female']*100
  df['Female'] = df['Female'].round().astype(int)
  df['Male'] = df['Male']*100
  df['Male'] =  df['Male'].round().astype(int)

  # Define bins and labels
  bins = [0, 20, 40, 60, 80, 100]
  labels = ['Nearly only men', '21-40%', '41-60%', '61-80%', 'Nearly only women']

  # Categorize percentage values into bins
  df['category'] = pd.cut(df['Female'], bins=bins, labels=labels, right=True)
  df['category'] = df['category'].fillna("Nearly only men")
  return(df)

#Top an bottom (5)

def Top5_Bottom5 (df):
  A = df.head(5)
  A["description"] = "top 5"
  B = df.tail(5)
  B["description"] = "bottom 5"
  result = pd.concat([A,B])
  return(result)

#Histogram

def Athlete_histo_1(df, x,y, title,barmode='relative',text_auto=False,log_x=False, log_y=False,
                    range_x=None, range_y=None, histfunc=None,color=None,facet_row=None, facet_col=None, labels=None, yaxes = True,
                    yaxes_title=True, xaxes_title=True, xaxes = True, category_orders=None,
                    facet_col_wrap=None, facet_col_spacing=None,facet_row_spacing=None):
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

#Bar

def Bar_chart_1(df, x,y, title,barmode='relative',text=None,log_x=False, log_y=False,
                    range_x=None, range_y=None,color=None,facet_row=None, facet_col=None, labels=None, yaxes = True,
                    yaxes_title=True, xaxes_title=True, xaxes = True, category_orders=None,textangle=None, textposition =None):
  fig1 = px.bar(df, x = x,y =y, color=color, title=title,barmode=barmode,text= text,log_x=log_x, log_y=log_y,
                      range_x=range_x, range_y=range_y,facet_row=facet_row, facet_col=facet_col,
                      labels=labels, category_orders = category_orders)
  if yaxes_title != True:
    fig1.update_yaxes(title_text=yaxes_title)
  if xaxes_title != True:
    fig1.update_xaxes(title_text=xaxes_title)
  fig1.update_yaxes(visible=yaxes, showticklabels=True)
  fig1.update_xaxes(visible=xaxes, showticklabels=True)

  if textangle != None:
    fig1.update_traces(textangle=0, textposition = textposition)

  return(fig1)

#TOP

def Top (df, top, gpby1, gpby2,color_palette ,title):
  '''
histogram of top athletes per Countries per Sport Family or Sport Group
  '''
  # df =  Athletes_medallists
  # top = 5
  # gpby1 = "sport_family"
  # gpby2 = "country_name"
  # color_palette = Country_color()
  # title="Top 5 nb athletes per Countries per Sport Family"

  # Step 1: Group by sport family and country, then count
  counts = df.groupby([gpby1, gpby2]).size().reset_index(name='count')

  # Step 2: Rank within each sport family
  counts['rank'] = counts.groupby(gpby1)['count'].rank(method='first', ascending=False)

  # Step 3: Filter to top 5 for each sport family
  TOP = counts[counts['rank'] <= top]

  # filtre color_palette_dict

  # keys_to_keep = df[gpby2].unique().tolist()
  # color_palette = {key: value for key, value in color_palette_dict.items() if key in keys_to_keep}
  # Step 4: Merge back to the original dataset to filter only the top 5
  df_TOP = df.merge(TOP[[gpby1, gpby2]], on=[gpby1, gpby2], how='inner').sort_values("sport_family")
  ref = df_TOP["sport_family"].sort_values().unique().tolist()
  # Step 5: Plot the histogram
  fig = px.histogram(
      df_TOP,
      x=gpby1,
      color=gpby2,
      histfunc="count",
      category_orders= {"sport_family": ref},
      color_discrete_map = color_palette,
      title=title,
      barmode='group'
  )
  fig.update_layout(
      bargap=0.1,          # Space between groups (sport families)
      bargroupgap=0.2,     # Space within groups (countries in the same sport family)
  )
  fig.show()

def doublegraph_athletes_countries_top(Hist1, Hist2):
    # Création de la figure avec sous-graphiques
    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.5, 0.5],  # Les deux lignes ont la même hauteur
        vertical_spacing=0.1,  # Espacement vertical entre les sous-graphiques
        specs=[[{"type": "histogram"}], [{"type": "histogram"}]]
    )

    fig.add_trace(
        Hist1, row=1, col=1  # Placer le graphique sur la première ligne
    )

    fig.add_trace(
        Hist2, row=2, col=1  # Placer le graphique sur la deuxième ligne
    )

    # Afficher le graphique
    fig.show()

#Score Cards

def score_card_1 (df1, df2,  filtercolum, filter, colum1, column2):
  '''
df1 = olympics_games_summer
df2 = Athletes_medallists
filtercolum = "year"
filter = 2020
colum1 = "nb_athletes"
column2 = "code"
  '''
  fig = go.Figure(go.Indicator(
  mode="gauge+number+delta",
  delta={
      'reference': df1[df1[filtercolum] == filter][colum1].max(),
      'valueformat': ',.0f',
      'suffix': " Previous Game "
  },
  value=df2[column2].nunique(),
  number={'suffix': '', 'valueformat': ',.0f'},
  title={'text': "Athletes Number"},
  domain={'x': [0, 1], 'y': [0, 1]}
  ))

  return fig

def score_card_2 (df1, df2, filter, colum1, column2):
  '''
df1 = olympics_games_summer
df2 = Athletes_medallists
filter = 2020
colum1 = "nb_athletes"
column2 = "code"
  '''
  fig = go.Figure(go.Indicator(
  mode="gauge+number+delta",
  delta={
      'reference': (df1[df1["year"] == 2020]["nb_women"].max() / df1[df1["year"] == 2020]["nb_athletes"].max())*100,
      'valueformat': ',.0f',
      'suffix': " Previous Game "
  },
  value=(df2[df2["gender"] == "Female"]["code"].nunique() / df2["code"].nunique())*100,
  number={'suffix': '', 'valueformat': ',.0f'},
  title={'text': "Female vs Male"},
  domain={'x': [0, 1], 'y': [0, 1]}
  ))

  return fig

def subplots_scorecards (figure1, figure2):
  fig = make_subplots(
      rows=1,
      cols=2,
      specs=[[{"type": "domain"}, {"type": "domain"}]],  # Indique que les deux subplots sont de type 'domain'
  )

  # Ajout des traces de la première figure au subplot
  for trace in figure1.data:
      fig.add_trace(trace, row=1, col=1)

  # Ajout des traces de la deuxième figure au subplot
  for trace in figure2.data:
      fig.add_trace(trace, row=1, col=2)

  fig.update_layout(height=600, width=800, title_text="")
  fig.show()

#Hist_tab_athletes_age

def Hist_tab_athletes_age(df):
  '''
df = Athletes_medallists
  '''
  hist_fig = px.histogram(df, x="Age", histfunc='count', color="gender", barmode='group')

  # Créer un tableau avec l'âge min et max par gender
  age_stats = df.groupby('gender').agg(
      age_min=('Age', 'min'),
      age_max=('Age', 'max'),
      age_mean=('Age', 'mean'),
      age_median=('Age', 'median'),
      age_Q1=('Age', percentile(0.25)),
      age_Q3=('Age', percentile(0.75))
  ).reset_index()

  age_stats2 = age_stats[['gender','age_min','age_max']].melt(id_vars=['gender'], var_name='age_extreme', value_name='age').sort_values('gender')
  age_stats_2 = age_stats2.merge(df[["name", "gender", "country_code","Age","disciplines", "events", "sport_family", "sport_group"]], left_on=["gender","age"], right_on=["gender","Age"])

  # Créer le subplot avec 1 ligne et 2 colonnes (graphique et tableau)
  fig = make_subplots(
      rows=3, cols=1,
      row_heights=[0.8, 0.5 ,1],  # La première ligne plus grande
      shared_xaxes=True,  # Partage les axes X entre le graphique et le tableau
      vertical_spacing=0.1,  # Espacement vertical entre les graphes
      subplot_titles=("Athletes Distribution per Age", ""),
      specs=[[{"type": "xy"}], [{"type": "table"}],[{"type": "table"}]]  # Définir le type de graphique pour chaque ligne
  )

  # Ajouter l'histogramme au subplot
  fig.add_trace(
      hist_fig.data[0],  # Ajoute la trace de l'histogramme (en général, hist_fig.data[0] contient la trace principale)
      row=1, col=1
  )
  fig.add_trace(
      hist_fig.data[1],  # Ajoute la deuxième trace pour le genre (si disponible)
      row=1, col=1
  )

  # Ajouter le tableau sous l'histogramme
  table_trace_1 = go.Table(
      header=dict(values=["Gender", "Min Age", "Max Age", "Ave Age", "Median","Q1","Q3"]),
      cells=dict(values=[age_stats['gender'], age_stats['age_min'], age_stats['age_max'],
                        age_stats['age_mean'].round(0),age_stats['age_median'],age_stats['age_Q1'],
                        age_stats['age_Q3']])
  )

  table_trace_2 = go.Table(
    header=dict(values=["Gender","age_extreme","age","name", "country_code", "disciplines", "events", "sport_family", "sport_group"]),
    cells=dict(values=[age_stats_2['gender'], age_stats_2['age_extreme'], age_stats_2['age'], age_stats_2['name'],
                       age_stats_2["country_code"],age_stats_2["disciplines"],age_stats_2["events"],
                       age_stats_2["sport_family"],age_stats_2["sport_group"]])
)

  fig.add_trace(
    table_trace_1,  # Ajoute la trace du tableau
    row=2, col=1  # Place dans la deuxième ligne
  )
  fig.add_trace(
    table_trace_2,  # Ajoute la trace du tableau
    row=3, col=1  # Place dans la deuxième ligne
  )

  # Mise à jour de la mise en page pour ajuster l'apparence
  fig.update_layout(
      #title="Athletes Distribution per Age",
      height=800,  # Hauteur totale
      showlegend=True  # Affiche la légende
  )

  # Affichage du graphique avec le tableau
  return(fig)

# Athlete_medals_top20

def Athlete_medals_top20(df, filter, title = None, Text = None):
  '''
  filter = "medals_number"
  df = Athletes_medallists
  '''
  # Extract the top 20 athlete names sorted by medals_number
  top_20_names = df.sort_values(filter, ascending=False)["name"].tolist()
  z = df.sort_values("medals_number", ascending = False)
  df["ratio_medals / events_number"] = round(z["medals_number"] / z["events_nb"]*100)
  Fig1 = Bar_chart_1(df.sort_values(filter, ascending = False).head(20),
                  color = 'country_name', facet_row= 'gender',x = 'name', y = filter,
                        title = f"{title}( {Text} )" ,category_orders= {"gender": ["Female","Male"],
                                                                                        "name": top_20_names},  # Ensure names are sorted by medals_number
                        yaxes_title= "", text= Text)
  Fig1.update_layout(height=800, width=1500)
  Fig1.update_xaxes(showline=True,linecolor="#00FF9C",linewidth=3,showticklabels=False, row=2)
  Fig1.update_xaxes(showticklabels=True, row=1)
  return(Fig1)


#Distribution_events_nb

def Distribution_events_nb (df):
  '''
  df = Athletes_medallists
  '''
  Fig = Athlete_histo_1(df.groupby(["sport_group","events_nb"]).agg({"code":"count"}).reset_index(),
                        y = "code", x = "events_nb", histfunc='sum', color ="sport_group", facet_col= "sport_group",facet_col_wrap=4,
                        facet_col_spacing=0.2,facet_row_spacing=0.3, title="distribution of the number of events in which an athlete has participated",
                        barmode= 'group',yaxes_title= "Athletes number")
  Fig.update_xaxes(matches=None, title_font=dict(size=8), showticklabels=True)  # Afficher les ticks et labels pour chaque sous-graphe
  Fig.update_yaxes(matches=None, title_font=dict(size=8),showticklabels=True)
  Fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
  return(Fig)

#Athletes_number_per_sport_family

def Athletes_number_per_sport_family (df):
  '''
  Remove swimmng from the graph
  Error due to the family group creation
  df = Athletes_medallists
  '''
  df2 = df[df['sport_family']!= "Swimming"]
  graph = Athlete_histo_1(df2, x = 'sport_family',y =df2.index, histfunc='count',color="sport_family",
                  title="Athletes number per sport family", category_orders = {"sport_family": df2["sport_family"].sort_values().unique().tolist()}, yaxes_title= "Athletes number")
  return(graph)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>INTERACTIVE TABLE

def user1(df, name = None, gender = None, country_name = None,Age = 0, sport_family = None, sport_group = None, medals = None, discipline=None ):
    df = df.sort_values(["Gold Medal", "Silver Medal", "Bronze Medal"], ascending = [False, False, False])
    Table = df[['name', 'country_name','gender','Age','disciplines',
       'sport_family', 'sport_group','events_nb','disciplines_nb', 'Gold Medal',
       'Silver Medal','Bronze Medal','team_nb_medal','Student','Employed']]
    Table = Table.rename(columns={'name': "Name", 'country_name' : "Country","gender" : "Gender",'sport_family' : "Sport Family", 'sport_group' : "Sport Group",
                  'events_nb' : "Events",'disciplines_nb' : "Disciplines number", 'disciplines' : 'Disciplines', 'Gold Medal' : "Gold",
                  'Silver Medal' : "Silver",'Bronze Medal' : "Bronze",'team_nb_medal' : "Team medalist" })
    Table.fillna(0, inplace=True)
    # Appliquer les filtres dynamiquement
    if medals is not None:
       if medals == 'Gold':
          Table = Table[Table["Gold"] >= 1]
       if medals == 'Silver':
          Table = Table[Table["Silver"] >= 1]
       if medals == 'Bronze':
          Table = Table[Table["Bronze"] >= 1]
    if name is not None:
        Table = Table[Table["Name"].str.contains(name, na=False, case=False)]
    if gender is not None:
        Table = Table[Table["Gender"] == gender]
    if country_name is not None:
        Table = Table[Table["Country"] == country_name]
    if Age != None:
        Table = Table[Table["Age"] == Age]
    if sport_family is not None:
        Table = Table[Table["Sport Family"] == sport_family]
    if sport_group is not None:
        Table = Table[Table["Sport Group"] == sport_group]
    if discipline is not None:
        Table = Table[Table["Disciplines"].str.contains(discipline, na=False, case=False)]
    if Table.empty:
        print("No results to display.")
        return None

    fig = go.Figure(
      data=[
          go.Table(
              header=dict(
                  values=list(Table.columns),  # Colonnes du tableau
                  line_color='rgb(105, 105, 105)',  # Gris foncé pour les bordures
                  fill_color='#b2b5c2',  # Doré
                  align=['left', 'center'],
                  font=dict(color='rgb(255, 255, 255)', size=12)  # Texte blanc
              ),
              cells=dict(
                  values=[Table[col].tolist() for col in Table.columns],  # Données des cellules
                  line_color='rgb(105, 105, 105)',  # Gris foncé pour les bordures
                  fill=dict(
                      # Couleurs des cellules : Bleu pour la 1ère colonne, alternance rouge et blanc pour les autres
                      color=[
                          ['#d8dbc3'] * len(Table) if i == 0 else
                          ['#f4f5ed' if j % 2 == 0 else '#dadbd5' for j in range(len(Table))]
                          for i, col in enumerate(Table.columns)
                      ]
                  ),
                  align=['left', 'center'],
                  font=dict(color='rgb(0, 0, 0)', size=10),  # Texte noir
                  height=30
              ),
              columnwidth = [30, 20, 20, 15, 20, 20, 30, 20, 20, 15, 15, 15, 20, 20, 20]
          )
      ]
  )


    return(fig)

#correlation
def spearman_corr(df):
  '''
  df = Socio_economic_Dataset
  '''
  x = df.corr(method="spearman",min_periods=3, numeric_only=True)
  x = x.sort_values(by = "Total medals",ascending = False)
  x = x.sort_values(by = "Total medals",ascending = False, axis = 1)
  x = x[(x["Total medals"] >= 0.4) | (x["Total medals"] <= - 0.4)]
  x = x[["Total medals","Bronze medals","Silver medals","Gold medals"]]
  x = x.round(2)
  fig1 = px.imshow(x, aspect="auto",color_continuous_scale='PiYG',text_auto=True,title="Spearman correlation")
  fig1.update_xaxes(side="top")

  return(fig1)


#
def Women_vs_Men_medals_distribution (_df):
  Subset =  _df[_df['gender'] == 'Female'].groupby("name").agg({"medals_number" : "sum"}).reset_index().groupby(["medals_number"]).agg({"name" : "count"}).reset_index()
  Subset1 = _df[_df['gender'] == 'Male'].groupby("name").agg({"medals_number" : "sum"}).reset_index().groupby(["medals_number"]).agg({"name" : "count"}).reset_index()
  Subset = Subset.merge(Subset1[['medals_number',"name"]], on = "medals_number", how = "left")
  Subset.rename(columns = {"name_x" : "Female", "name_y" : "Male"}, inplace = True)
  Subset.sort_values("medals_number", ascending = False)
  _df["medallist"] = (_df['medals_number']>0).astype(int)
  x = _df.groupby("gender")["medallist"].value_counts(normalize = True).reset_index()
  WA = _df[_df['gender'] == 'Female']['medals_number'].mean().round(2)
  MA = _df[_df['gender'] == 'Male']['medals_number'].mean().round(2)
  WP = x[(x["gender"] == 'Female')&(x["medallist"] == 1)]["proportion"].min()
  MP = x[(x["gender"] == 'Male')&(x["medallist"] == 1)]["proportion"].min()
  WP = round(WP*100,2)
  MP = round(MP*100,2)
  Bar1 = Bar_chart_1(Subset, x = "medals_number", y = ["Female", "Male"], yaxes_title= " Athletes number (log 10)", barmode = "group", log_y= True, title = "Women vs Men medals distribution")
  Bar1.add_trace(go.Scatter(
    x=[4, 4, 4,4],
    y=[3500, 1500, 800,350],
    mode="text",
    name="Descriptive information",
    text=[f"Women medallist average : {WA}",f"Men medallist ave : {MA}",f"Women  medallist percent : {WP}",f"Men medallist percent : {MP}"],
    textposition="bottom center",
  ))

  return(Bar1)