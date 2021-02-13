import pandas as pd
import os
import plotly.express as px
import hydropathy as hp
import numpy as np

# read arabica in df
filename_in = os.path.join(".", "data", "arabica_data_clean_test.xlsx")
df_coffee = pd.read_excel(filename_in)


#remove first columns
df_coffee = df_coffee.drop(df_coffee.columns[[0,1]], axis = 1)

# filter: columns, rename
df_interest = df_coffee[["Country.of.Origin", "Producer", "Processing.Method"]]
column_names = df_interest.columns


print(range(len(column_names)))

for i in range(len(column_names)):
    old_name = column_names[i]
    new_name = column_names[i].replace(".", " ")
    df_interest.rename(columns={(old_name): (new_name)}, inplace=True)

column_names = df_interest.columns



# median not applicable to strings, used mode instead
modes = df_interest.mode(axis = 0)
modes = modes.values.tolist()
print(modes[0][0])


print(df_interest.shape[0])
print(df_interest.shape[1])

for n in range(df_interest.shape[0]):
    for m in range(df_interest.shape[1]):
        if "nan" == str(df_interest.iloc[n,m]):
            df_interest.iloc[n,m] = str(modes[0][m])






# plots
    for i in range(len(column_names)):
        fig = px.histogram(data_frame = df_interest, x = column_names[i], title = str(column_names[i]))
        fig.write_html((str("figure_") + ".html"), auto_open=True)


# outliers