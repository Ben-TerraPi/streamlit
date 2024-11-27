# Doc Project : JO PARIS 2024

collaborateur:

Maxime Mobailly
Matteo Cherief
Gautier Martin
Benoit Dourdet

# Dependencies Import

import pandas as pd
import numpy as np
import pandas_gbq
from google.colab import auth
import plotly.express as px
!pip install thefuzz
import thefuzz

# Datasets import from Kaggle

## Download latest version in content
!kaggle datasets download -d piterfm/paris-2024-olympic-summer-games --unzip -p ./content
!kaggle datasets download -d krzysztofszafraski/paris2024-olympics-country-level-data --unzip -p ./content
!kaggle datasets download -d josephcheng123456/olympic-historical-dataset-from-olympediaorg --unzip -p ./content

# Datasets import from Bigquery

auth.authenticate_user()
project = "jo-paris-2024-442810"

Dataframes= ["Socio_economic_Dataset",
"all_athlete_bio",
"all_athlete_event_results_summer",
"all_country_olympic_games_medal_summer",
"all_country_olympic_games_medal_intercalated",
"athletes",
"medallists",
"medals_total",
"schedules",
"teams",
"Countries_Code_ISO",
"olympics_games_summer",
"all_id_list_summer",
"athletes_id_multiple"]
Dataset = "dataset_v2"


for Dataframe in Dataframes:
  query = f"SELECT * FROM `jo-paris-2024-442810.{Dataset}.{Dataframe}`"
  locals()[Dataframe] = pd.read_gbq(query, project_id=project)



