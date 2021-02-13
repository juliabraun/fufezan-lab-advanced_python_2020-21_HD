import os
import pandas as pd
import plotly
import plotly.express as px
import plotly.io as pio

filename_in = os.path.join(".", ".", "data", "amino_acid_properties.csv")
print(filename_in)

# reading csv as pandas 
pd_hydropathy = pd.read_csv(filename_in)
print(pd_hydropathy)

# list of strings 
lst = ['Geeks', 'For', 'Geeks', 'is', 'portal', 'for', 'Geeks'] 
  
# list of int 
lst2 = [11, 22, 33, 44, 55, 66, 77] 

def my_plotly(x, y, xlabel, ylabel, titlestr, fig_index):
# Calling DataFrame constructor after zipping 
# both lists, with columns specified 
    df = pd.DataFrame(list(zip(x, y)), 
               columns =[xlabel, ylabel])

    fig = px.scatter(df, x=xlabel, y=ylabel,
                    title=titlestr)
    fig.write_html((str("figure_") + str(fig_index) + ".html"), auto_open=True)

my_plotly(lst, lst2, "ciao", "miau", "wau", 1)



fig = px.scatter(pd_hydropathy, x="pka1", y="pka2",
                 title="Hydropathy")

## Add range slider
#fig.update_layout(
#    xaxis=dict(
#        rangeselector=dict(
#            buttons=list([
#                dict(count=1,
#                     label="1m",
#                     step="month",
#                     stepmode="backward"),
#                dict(count=6,
#                     label="6m",
#                     step="month",
#                     stepmode="backward"),
#                dict(count=1,
#                     label="YTD",
#                     step="year",
#                     stepmode="todate"),
#                dict(count=1,
#                     label="1y",
#                     step="year",
#                     stepmode="backward"),
#                dict(step="all")
#            ])
#        ),
#        rangeslider=dict(
#            visible=True
#        ),
#        type="date"
#    )
#)
#

fig.write_html('first_figure.html', auto_open=True)








#df = px.data.iris()
fig = px.scatter(df, x="sepal_length", y="sepal_width", color="species",
                 labels={
                     "sepal_length": "Sepal Length (cm)",
                     "sepal_width": "Sepal Width (cm)",
                     "species": "Species of Iris"
                 },
                title="Manually Specified Labels")
fig.show()