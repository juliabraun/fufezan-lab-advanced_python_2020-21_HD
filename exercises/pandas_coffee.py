import pandas as pd
import os
import plotly.express as px
import hydropathy as hp
import numpy as np

if __name__ == "__main__":

    # read arabica in df
    filename_in = os.path.join(".", "data", "arabica_data_clean.xlsx")
    df_coffee = pd.read_excel(filename_in)
    
    
    #remove first columns
    df_coffee = df_coffee.drop(df_coffee.columns[[0,1]], axis = 1)
    
    # filter: columns, rename
    df_interest = df_coffee[["Country.of.Origin", "Producer", "Processing.Method"]]
    column_names = df_interest.columns
    
    # rename
    for i in range(len(column_names)):
        old_name = column_names[i]
        new_name = column_names[i].replace(".", " ")
        df_interest.rename(columns={(old_name): (new_name)}, inplace=True)
    
    column_names = df_interest.columns
    
    
    # median not applicable to strings, used mode instead
    modes = df_interest.mode(axis = 0)
    modes = modes.values.tolist()

    # replace nan with mode
    for n in range(df_interest.shape[0]):
        for m in range(df_interest.shape[1]):
            if "nan" == str(df_interest.iloc[n,m]):
                df_interest.iloc[n,m] = str(modes[0][m])
     

    # countries > 10 < 30 entries
    countries = df_interest.iloc[:,0]
    freq_countries = countries.value_counts()
    name_countries = freq_countries.index.to_list()
 
    np_freq_countries = freq_countries.to_numpy()
    
    match = np.where((np_freq_countries > 10) & (np_freq_countries < 30))

    print("The countries with more than 10 and less than 30 entries are: ")
    country_match = []
    for n in range(len(match[0])):
        cmatch = name_countries[match[0][n]]
        country_match.append(cmatch)
        print(cmatch)
    print()

  
    # producer with most entries
    producer = df_interest.iloc[:,1]
    freq_producer = producer.value_counts(normalize = True)
    freq_top_producer = freq_producer.head() 
    print(freq_top_producer)
    producer_most_entries = freq_top_producer.index[0]
    print("The producer with most entries is " + str(producer_most_entries))


    # most common and least common processing method
    processing = df_interest.iloc[:,2]
    freq_processing = processing.value_counts(normalize = True)
    freq_top_processing = freq_processing.head() 
    processing_most_entries = freq_top_processing.index[0]
    processing_least_entries = freq_top_processing.index[-1]

    print("The producer with most entries is " + str(producer_most_entries))
    print("The most common processing method is " + str(processing_most_entries))
    print("The least common processing method is " + str(processing_least_entries))
  
    freq_producer_top_10 = freq_producer.index.to_list()
    freq_producer_top_10 = freq_producer_top_10[0:9]
    name_producer_top_10 = freq_producer.to_list()
    name_producer_top_10 = name_producer_top_10[0:9]


    df_plot_producer_hist = pd.DataFrame(list(zip(freq_producer_top_10, name_producer_top_10)), 
               columns =["producer", "market share"])
    fig = px.bar(df_plot_producer_hist, x='producer', y='market share', title = "top 9 producer")
    fig.write_html((str("figure_") + ".html"), auto_open=True)


for i in range(1):
    fig = px.histogram(data_frame = df_interest, x = column_names[i], title = str(column_names[i]))
    fig.write_html((str("figure_") + ".html"), auto_open=True)