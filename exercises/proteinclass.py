import os

class proteinclass(object):
    def __init__(self, sequence):
        self.sequence = sequence

    def get_data(self, id):
        protein_url = os.join("https://www.uniprot.org/uniprot/?query=" + str(id) + "&format=fasta")
        print(protein_url)
        return protein_url



id = proteinclass(9606)
protein_url = id.get_data
print(protein_url)


print(protein_url)
# method to get data

#.get_data(id)


# method to map sequence against a lookup and return value list
#.map(kwarg)



# calculate the values based on a sliding window


# plot