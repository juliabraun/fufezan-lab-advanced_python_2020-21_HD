import requests as req
import pandas as pd
import count_aas as aas
import Bio.SeqIO as SeqIO
import os
import sys
import hydropathy as hp
import numpy as np

def create_fill_dict(text):
    """ Create and fill dict from input filepath. 
    """

    
    # add fasta sequences to dict
    
 
    for fasta in fasta_sequences:
        name, sequence = fasta.id, str(fasta.seq)
        #print("name: %s" %name)
        #print("sequence: %s" %sequence)
    
       

    return dict_lettercode, count_min_max, name_min_max, sequence_min_max


class proteinclass(object):
    def __init__(self, _id = None):
        self.clear_data()
        self.id = _id
        if self.id != None:
            self.get_data(self.id)
          
        return

    # This method reset the proteinclass
    def clear_data(self):
        self.id = None
        self.sequence = None
        self.name = None

        self.dict_lookup = {
            "hydropathy": {"A" : "..."},
            "pI": {"A": "..."},
            }
        return

    # This method initialize the proteinclass
    def get_data(self, id):
        filepath_out = "id" + ".fasta"
        protein_url = "https://www.uniprot.org/uniprot/" + str(id) + ".fasta"
        resp = req.get(protein_url)
        new_file = open(filepath_out, "w")
        new_file.write(resp.text)
        new_file.close()

        fasta_sequences = SeqIO.parse(open(filepath_out),'fasta')
        for fasta in fasta_sequences:
            self.name, self.sequence = fasta.id, str(fasta.seq)

        # prepare lookup
        filename_in = os.path.join(".", ".", "data", "amino_acid_properties.csv")

        pd_characteristics = pd.read_csv(filename_in)
        # reading csv as pandas 
        # all amino acids
        aa = pd_characteristics.iloc[:, 2]
        # all hydropathy values
        hp = pd_characteristics.iloc[:, 11]
        # all pI values
        pi_values = pd_characteristics.iloc[:, 10]
        
        # make columns "1-letter-code" and "hydropathy" a dict A: hydr.
        self.dict_lookup["hydropathy"].update(pd.Series(hp.values,index=aa).to_dict())
        self.dict_lookup["pI"].update(pd.Series(pi_values.values,index=aa).to_dict())
       
        print(self.dict_lookup)
        return resp

    # This method convert the list of amminoacid with the corresponding
    #  value of the dictionary dict_lookup
    def get_characteristics_list(self, dict_lookup):
        characteristics_list = []
        for letter in self.sequence:
            characteristics_value = dict_lookup[letter]
            characteristics_list.append(characteristics_value)
        return characteristics_list

    def map(self, **kwargs):
        characteristic = None
        lookup = None
        len_ma = None
        characteristics_list = None

        for arg in kwargs:
            if arg == "characteristic":
                characteristic = kwargs[arg]
            if arg == "lookup":
                lookup = kwargs[arg]

            if arg == "len_ma":
                len_ma = kwargs[arg]

        if None == len_ma:
            len_ma = 1
        
        if None != characteristic:
            if None != lookup:
                # if the user provides everything
                characteristics_list = self.get_characteristics_list(lookup[characteristic])
            else: 
                # if the user does not provide the lookup, use default
                characteristics_list = self.get_characteristics_list(self.dict_lookup[characteristic])
        else:
            # if the user does not provide the characteristic
            print("Please provide characteristic to map method in proteinclass")

        return characteristics_list, hp.add_moving_average(characteristics_list, len_ma)

            



    
id = "P12345"
sequence = proteinclass(id)
print(id)
hydropathy_list = []
hydropathy_list_ma = []
hydropathy_list, hydropathy_list_ma= sequence.map(characteristic = "hydropathy", len_ma=11)


pi_list = sequence.map(characteristic = "pI")
print(hydropathy_list, pi_list)

index_aa = np.linspace(1, len(hydropathy_list), len(hydropathy_list))
index_ab = np.linspace(1, len(hydropathy_list_ma), len(hydropathy_list_ma))

# plot
hp.my_plotly(index_aa, hydropathy_list, "Amino acid no.", "hydropathy index", "Hydropathy index", 1)
hp.my_plotly(index_ab, hydropathy_list_ma, "Amino acid no.", "hydropathy index moving average", "Hydropathy index", 2)

