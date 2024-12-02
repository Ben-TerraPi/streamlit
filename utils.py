import streamlit as st
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import plotly.express as px
import numpy as np



#>>>>>>>>>>>>>>>>>>>>>> Create API client.
'''
@st.cache_data(ttl=600)
def get_bigquery():
   project = "jo-paris-2024-442810"
   credentials = service_account.Credentials.from_service_account_info(
      st.secrets["gcp_service_account"])
      return result
'''
#>>>>>>>>>>>>>>>>>>>>>> Create API client.

project = "jo-paris-2024-442810"
credentials = service_account.Credentials.from_service_account_info(
st.secrets["gcp_service_account"])

#>>>>>>>>>>>>>>>>>>>>>> BQ authentification

#client = get_bigquery()
client = bigquery.Client(credentials=credentials)

#>>>>>>>>>>>>>>>>>>>>>> Dataframes

dataframes = [
    "athletes",
    "Socio_economic_Dataset",
    "all_athlete_bio",
    "all_athlete_event_results_summer",
    "all_country_olympic_games_medal_summer",
    "medals_total",
    "schedules",
    "teams",
    "Countries_Code_ISO",
    "olympics_games_summer",
    "athlete_id_multiple"
    ]


dataset = "dataset_v2"

for dataframe in dataframes:
    query = f"SELECT * FROM `jo-paris-2024-442810.{dataset}.{dataframe}`"
    locals()[dataframe] = pd.read_gbq(query, project_id=project)


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

#-----------------------------------------DESIGN

@st.cache_data(ttl=600)
def Country_color(df):
  Country_color = df["country_name"].unique().tolist()
  num_categories = len(df)
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


#----------------------------------------SELECTION

@st.cache_data(ttl=600)
def Selection (df,column,selection):
  if not selection:  # Vérifie si la liste est vide
        return df
  df = df[df[column].isin(selection)]
  return (df)

#--------------------------------------------QUARTILE
@st.cache_data(ttl=600)
def percentile(n):
    def percentile_(x):
        return x.quantile(n)
    percentile_.__name__ = 'percentile_{:02.0f}'.format(n*100)
    return percentile_

#----------------------------------------GENDER RATIO
@st.cache_data(ttl=600)
def gender_ratio(athletes, column = "gender", column2= "code"):
  df = pd.DataFrame(athletes.groupby("country_code")[column].value_counts(normalize=True).unstack()).reset_index().sort_values('Female', ascending= False)
  df.fillna(0, inplace=True)
  df["athletes"] = athletes.groupby("country_code")[column2].nunique().reset_index()[column2]
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

#--------------------------------------------TOP
@st.cache_data(ttl=600)
def Top (df, top = 5, gpby1 = "sport_family", gpby2 = "country_name",color_palette = Country_color() ,title="Top 5 nb athletes per Countries per Sport Family"):
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

#------------------------------------------------------SCORECARD
@st.cache_data(ttl=600)
def score_card_1 (df1, df2,  filtercolum, filter, colum1, column2):
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

@st.cache_data(ttl=600)
def score_card_2 ():
  fig = go.Figure(go.Indicator(
  mode="gauge+number+delta",
  delta={
      'reference': (olympics_games_summer[olympics_games_summer["year"] == 2020]["nb_women"].max() / olympics_games_summer[olympics_games_summer["year"] == 2020]["nb_athletes"].max())*100,
      'valueformat': ',.0f',
      'suffix': " Previous Game "
  },
  value=(athletes[athletes["gender"] == "Female"]["code"].nunique() / athletes["code"].nunique())*100,
  number={'suffix': '', 'valueformat': ',.0f'},
  title={'text': "Female vs Male"},
  domain={'x': [0, 1], 'y': [0, 1]}
  ))

  return fig

@st.cache_data(ttl=600)
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


#-------------------------------------------Hist_tab_athletes_age
@st.cache_data(ttl=600)
def Hist_tab_athletes_age():
  hist_fig = px.histogram(Athletes_medallist, x="Age", histfunc='count', color="gender", title="Athletes number per age", barmode='group')

  # Créer un tableau avec l'âge min et max par gender
  age_stats = Athletes_medallists.groupby('gender').agg(
      age_min=('Age', 'min'),
      age_max=('Age', 'max'),
      age_mean=('Age', 'mean'),
      age_median=('Age', 'median'),
      age_Q1=('Age', percentile(0.25)),
      age_Q3=('Age', percentile(0.75))
  ).reset_index()

  age_stats2 = age_stats[['gender','age_min','age_max']].melt(id_vars=['gender'], var_name='age_extreme', value_name='age').sort_values('gender')
  age_stats_2 = age_stats2.merge(Athletes_medallists[["name", "gender", "country_code","Age","disciplines", "events", "sport_family", "sport_group"]], left_on=["gender","age"], right_on=["gender","Age"])

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
      title="Athletes Distribution per Age with Gender-based Age Stats",
      height=800,  # Hauteur totale
      showlegend=True  # Affiche la légende
  )

  # Affichage du graphique avec le tableau
  return(fig)

#---------------------------------------------------Athlete_medals_top20
@st.cache_data(ttl=600)
def Athlete_medals_top20(filter = "medals_number", title = None, Text = None):
  # Extract the top 20 athlete names sorted by medals_number
  top_20_names = Athletes_medallists.sort_values(filter, ascending=False)["name"].tolist()
  z = Athletes_medallists.sort_values("medals_number", ascending = False)
  Athletes_medallists["ratio_medals / evenet_number"] = round(z["medals_number"] / z["events_nb"]*100)
  Fig1 = Bar_chart_1(Athletes_medallists.sort_values(filter, ascending = False).head(20),
                  color = 'country_name', facet_row= 'gender',x = 'name', y = filter,
                        title = f"{title}( {Text} )" ,category_orders= {"gender": ["Female","Male"],
                                                                                        "name": top_20_names},  # Ensure names are sorted by medals_number
                        yaxes_title= "", text= Text)
  Fig1.update_layout(height=800, width=1500)
  Fig1.update_xaxes(showline=True,linecolor="black",linewidth=1,showticklabels=False, row=2)
  Fig1.update_xaxes(showticklabels=True, row=1)
  return(Fig1)

#--------------------------------------------------Distribution_events_nb
@st.cache_data(ttl=600)
def Distribution_events_nb ():
  Fig = Athlete_histo_1(Athletes_medallists.groupby(["sport_group","events_nb"]).agg({"code":"count"}).reset_index(),
                        y = "code", x = "events_nb", histfunc='sum', color ="sport_group", facet_col= "sport_group",facet_col_wrap=4,
                        facet_col_spacing=0.2,facet_row_spacing=0.3, title="distribution of the number of events in which an athlete has participated",
                        barmode= 'group',yaxes_title= "athletes number")
  Fig.update_xaxes(matches=None, title_font=dict(size=8), showticklabels=True)  # Afficher les ticks et labels pour chaque sous-graphe
  Fig.update_yaxes(matches=None, title_font=dict(size=8),showticklabels=True)
  Fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
  return(Fig)

#---------------------------------------------------Athletes_number_per_sport_family
@st.cache_data(ttl=600)
def Athletes_number_per_sport_family ():
  '''
  Remove swimmng from the graph
  Error due to the family group creation
  '''
  df = Athletes_medallists[Athletes_medallists['sport_family']!= "Swimming"]
  graph = Athlete_histo_1(df, x = 'sport_family',y =df.index, histfunc='count',color="sport_family",
                  title="Athletes number per sport family", category_orders = {"sport_family": df["sport_family"].sort_values().unique().tolist()})
  return(graph)




@st.cache_data(ttl=600)
def plot_histogram_with_line(data, bins=10, title="Histogram with Line Chart", xlabel="Values", ylabel="Frequency", line_color='red'):
    """
    Trace un histogramme accompagné d'une courbe.

    Paramètres :
        data (array-like): Les données à afficher.
        bins (int): Nombre de barres de l'histogramme.
        title (str): Titre du graphique.
        xlabel (str): Titre de l'axe X.
        ylabel (str): Titre de l'axe Y.
        line_color (str): Couleur de la courbe superposée.
    """
    # Calculer l'histogramme
    counts, bin_edges = np.histogram(data, bins=bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Créer le graphique
    fig, ax1 = plt.subplots(figsize=(8, 5))

    # Histogramme
    ax1.bar(bin_centers, counts, width=bin_edges[1] - bin_edges[0], alpha=0.7, color='blue', label="Histogram")
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel, color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Line chart (courbe)
    ax2 = ax1.twinx()  # Crée un second axe Y
    ax2.plot(bin_centers, counts, color=line_color, label="Line Chart", marker='o')
    ax2.set_ylabel("Line Value", color=line_color)
    ax2.tick_params(axis='y', labelcolor=line_color)

    # Titre et légende
    fig.suptitle(title)
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    plt.show()



#--------------------------------------------------Graph combiné Nb de médailles/types/pays + % medailles d'or/pays
@st.cache_data(ttl=600)
def plot_top_10_medals_by_type(medals_total):
    country_medals = medals_total.groupby('country_name').sum().sort_values(by=['Gold Medal', 'Silver Medal','Bronze Medal'], ascending=[False, False, False]).head(10)
    color_discrete_map = {
        'Gold Medal': 'gold',
        'Silver Medal': 'silver',
        'Bronze Medal': '#CD7F32'
    }
    fig = px.bar(country_medals,
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