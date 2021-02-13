import Bio.SeqIO as SeqIO
import os
import sys
import pandas as pd
import plotly
import plotly.express as px
import plotly.io as pio
import numpy as np
import count_aas as aas
import matplotlib.pyplot as plt


def add_moving_average(hydropathy_list, len_ma):
    # check if len_ma is an odd number
    if len_ma % 2 == 1 and len_ma > 1:
            
        side = np.int32((len_ma-1)/2)
        # extend the dataset left and right 
        #outborders = hydropathy_list[0:len_ma]
        #hydropathy_list.append(outborders)
        hp_list_ma = np.linspace(0,len(hydropathy_list),len(hydropathy_list))*0
        ma = np.linspace(0,len_ma,len_ma)*0
        dim_hydropathy_list = len(hydropathy_list)
        iterator = 0
        # stop iteration len_sw times before end
        while iterator < dim_hydropathy_list:
            next_start = iterator - side
            #next_stop = iterator + side
            for n in range(len_ma):
                m = (next_start + n) % dim_hydropathy_list
                ma[n] = hydropathy_list[m]
            hp_average = np.mean(ma)
            hp_list_ma[iterator] = hp_average
            iterator = iterator + 1
        
            
    else: 
        print("len_ma must be an odd number.")
        hp_list_ma = hydropathy_list
               
    return hp_list_ma

# function with sequence and mapping dict
def return_hydropathy_list(sequence, dict_mapping):
    hydropathy_list = []
    for letter in sequence:
        hydropathy_value = dict_mapping[letter]
        hydropathy_list.append(hydropathy_value)
    return hydropathy_list


def my_plotly(x, y, xlabel, ylabel, titlestr, fig_index):
# Calling DataFrame constructor after zipping 
    df = pd.DataFrame(list(zip(x, y)), 
               columns =[xlabel, ylabel])

    fig = px.bar(df, x=xlabel, y=ylabel,
                    title=titlestr)
    fig.write_html((str("figure_") + str(fig_index) + ".html"), auto_open=True)
    return




if __name__ == "__main__":
    filename_in = os.path.join(".", ".", "data", "amino_acid_properties.csv")
    
    # reading csv as pandas 
    pd_hydropathy = pd.read_csv(filename_in)
    # all amino acids
    aa = pd_hydropathy.iloc[:,2]
    # all hydropathy values
    hp = pd_hydropathy.iloc[:,11]
    
    # make columns "1-letter-code" and "hydropathy" a dict A: hydr.
    dict_hydropathy = pd.Series(hp.values,index=aa).to_dict()
    
    
    filename_in = os.path.join(".", "exercises", "data", "P32249.fasta")
    
    dict_lettercode, count_min_max, name_min_max, sequence_min_max = aas.create_fill_dict(filename_in)
    sequence = sequence_min_max[0]
    hydropathy_list = return_hydropathy_list(sequence, dict_hydropathy)
    print(hydropathy_list, hydropathy_list[0:5])
    
    
    
    hp_list_ma = add_moving_average(hydropathy_list, 5)
    
    
    #index_aa = np.linspace(1, len(aa), len(aa))
    index_aa = np.linspace(1, len(hydropathy_list), len(hydropathy_list))
    index_ab = np.linspace(1, len(hp_list_ma), len(hp_list_ma))
    
    
    
    my_plotly(index_aa, hydropathy_list, "Amino acid no.", "hydropathy index", "Hydropathy index", 1)
    my_plotly(index_ab, hp_list_ma, "Amino acid no.", "hydropathy index", "Hydropathy index, moving average = 5", 2)
    




