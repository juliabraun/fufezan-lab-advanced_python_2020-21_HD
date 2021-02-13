import Bio.SeqIO as SeqIO
import os
import sys
import pandas as pd
import plotly
import plotly.express as px
import plotly.io as pio
import numpy as np
import count_aas as aas


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



# compute new hydropathy_list according to sliding window

def add_sliding_window(hydropathy_list, len_sw):
    iterator = 0
    

    # extend the dataset by the first sw times elements 
    outborders = hydropathy_list[0:len_sw]
    hydropathy_list.append(outborders)
    hp_list_sw = np.linspace(0,len(hydropathy_list))

    # stop iteration len_sw times before end
    while iterator < len(hydropathy_list) - len_sw:
        for element in hydropathy_list:
            next_stop = iterator + len_sw
            hp_average = sum(hydropathy_list[iterator : (next_stop)])
            hp_average = hp_average / len_sw
            hp_list_sw[iterator] = hp_average
        iterator = iterator + 1
           
    return hp_list_sw

hydropathy_list = [4,1,-2,3,0]
add_sliding_window(hydropathy_list, 5)




index_aa = np.linspace(1, len(aa), len(aa))

my_plotly(index_aa, hydropathy_list, "Amino acid no.", "hydropathy index", "Hydropathy index", 1)




#if __name__ == "__main__":
#    if 1 == len(sys.argv):
#    else: 
#        for i, arg in enumerate(sys.argv):
#            filename_in = arg
#    
#    print("filename_in = " + str(filename_in))
#
#    # does the file exist?
#    if os.path.exists(filename_in) == True:
#        flg_fileexist = True
#    else:
#        flg_fileexist = False
#        raise FileNotFoundError("File was not found.")
#
#    # does the file end in .fasta?
#    if filename_in.count(".fasta") > 0:
#        flg_fasta = True
#    else:
#        flg_fasta = False
#        print("Only .fasta file format allowed.")
#    
#    # proceed only if file exists and ends in .fasta
#    if (flg_fasta and flg_fileexist) == True:
#        directory, filename = os.path.split(filename_in)
#        filename_root = filename[:-6]
#        print("directory : " +str(directory) + "\n" + "filename : " + str(filename))
#
#        pdf_name_no_directory = str(filename_root) + "_aa_distribution.pdf"
#        
#        # create filenames input for function
#        filename_out = os.path.join(directory, filename_out_no_directory)
#        pdf_name = os.path.join(directory, pdf_name_no_directory)
#
#       