import pandas as pd

df = pd.read_csv("dependencies-1.6.0-2020-01-12.csv")


df_dict = {g: d for g, d in df.groupby('Platform')}

for key in df_dict:
    df_dict[key].to_csv(key+'.csv', index=True)
