#%%
import pandas as pd

#%%

df = pd.read_csv("data/Athletes_medallists.csv")
df

#%%
group_discipline = df.groupby('sport_group')['disciplines'].unique().to_dict()

#%% 
discipline_name = df.groupby('disciplines')['name'].unique().to_dict()

#%%

sport_country = df.groupby('disciplines')['country_name'].unique().to_dict()
sport_country
# %%
