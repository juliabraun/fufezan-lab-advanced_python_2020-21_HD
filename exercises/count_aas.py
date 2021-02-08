import Bio.SeqIO as SeqIO
import os
import sys



def create_fill_dict(filepath_in):
    """ Create and fill dict from input filepath. 
    """

    # initialise and fill dictionary
    exclude_letter = "BJOUXZ"
    dim_letter = 26
    dict_lettercode = {} 
    for digit in range(dim_letter):
        letter = chr(digit+65)
        if exclude_letter.count(letter) == 0: 
            dict_lettercode[letter] = 0
    
    # add fasta sequences to dict
    fasta_sequences = SeqIO.parse(open(filepath_in),'fasta')
    
    for fasta in fasta_sequences:
        name, sequence = fasta.id, str(fasta.seq)
        print("name: %s" %name)
        print("sequence: %s" %sequence)
    
        # count aa per letter
        for letter in dict_lettercode:
            count1 = sequence.count(letter)
            dict_lettercode[letter] += count1


    return dict_lettercode

def write_to_file(filepath_out, dict_lettercode):
    """ Open new file and write dict inside in specified format. 
    """
    # write result to file
    new_file = open(filepath_out, "w")
    new_file.write("aa, count\n")
       
    # select only keys with value not 0, thereby filtering out invalid 1 letter code
    for letter in dict_lettercode:
        if dict_lettercode[letter] != 0:
            print(letter + ": " + str(dict_lettercode[letter]))
            new_file.write(letter + ", " + str(dict_lettercode[letter]) + "\n")
    
    new_file.close()
    return 

def count_amino_acids(filename_in, filename_out):
     
    dict_lettercode = create_fill_dict(filename_in)
    write_to_file(filename_out, dict_lettercode)

    return dict_lettercode


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

    # does the file end in .fasta?
    if filename_in.count(".fasta") > 0:
        flg_fasta = True
    else:
        flg_fasta = False
        print("Only .fasta file format allowed.")
    
    # proceed only if file exists and ends in .fasta
    if (flg_fasta and flg_fileexist) == True:
        directory, filename = os.path.split(filename_in)
        filename_root = filename[:-6]
        print("directory : " +str(directory) + "\n" + "filename : " + str(filename))

        filename_out_no_directory = filename_root + "_aa_distribution.csv"
        pdf_name_no_directory = str(filename_root) + "_aa_distribution.pdf"
        
        # create filenames input for function
        filename_out = os.path.join(directory, filename_out_no_directory)
        pdf_name = os.path.join(directory, pdf_name_no_directory)

        count_amino_acids(filename_in, filename_out)