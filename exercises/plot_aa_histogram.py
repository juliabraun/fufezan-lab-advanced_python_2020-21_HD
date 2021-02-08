import count_aas as aa
import matplotlib.pyplot as plt
import os as os
import sys

def plot_aa_distribution(filename_in, filename_out, pdf_name):
    
    dict_lettercode = aa.count_amino_acids(filename_in, filename_out)
    keys = dict_lettercode.keys()
    values = dict_lettercode.values()
    
    figure = plt.figure()
    plt.bar(keys, values)
    plt.xlabel("Amino acid (1-letter code)")
    plt.ylabel("Count")
    
    figure.savefig(pdf_name, bbox_inches='tight')
    
    plt.show()
    return 


if __name__ == "__main__":
    for i, arg in enumerate(sys.argv):
        print(arg)
        filename_in = arg
        #filename_in = filename_in[1:-1]
    print()
    print("filename_in = " + str(filename_in))

    # does the file exist?
    if os.path.exists(filename_in) == True:
        flg_fileexist = True
    else:
        flg_fileexist = False
        raise FileNotFoundError("File was not found.")

    if filename_in.count(".fasta") > 0:
        flg_fasta = True
    else:
        flg_fasta = False
        print("Only .fasta file format allowed.")
    
    if (flg_fasta and flg_fileexist) == True:
        directory, filename = os.path.split(filename_in)
        filename_root = filename[:-6]
        print("directory : " +str(directory) + "\n" + "filename : " + str(filename))

        filename_out_no_directory = filename_root + "_aa_distribution.csv"
        pdf_name_no_directory = str(filename_root) + "_aa_distribution.pdf"
        
        filename_out = os.path.join(directory, filename_out_no_directory)
        pdf_name = os.path.join(directory, pdf_name_no_directory)

        plot_aa_distribution(filename_in, filename_out, pdf_name)

