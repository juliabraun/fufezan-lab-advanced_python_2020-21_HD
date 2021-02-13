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
lst = [11, 22, 33, 44, 55, 66, 77] 


def my_plotly(x, y, xlabel, ylabel, titlestr, fig_index):
# Calling DataFrame constructor after zipping 
# both lists, with columns specified 
    df = pd.DataFrame(list(zip(x, y)), 
               columns =[xlabel, ylabel])

    fig = px.scatter(df, x=xlabel, y=ylabel,
                    title=titlestr)
    fig.write_html((str("figure_") + str(fig_index) + ".html"), auto_open=True)

my_plotly(lst, lst2, "ciao", "miau", "wau", 1)


fig = px.line(pd_hydropathy, x="pka1", y="pka2",
                 title="Hydropathy")
lst3 = [5,2,-10,-3,5]
lst4 = [1,2,-10,-4,5]


# Only thing I figured is - I could do this 
fig.add_scatter(x=lst3,y= lst4,mode = "lines") # Not what is desired - need a line



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