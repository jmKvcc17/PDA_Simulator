import os
from resources import json_reader, pda



if __name__ == "__main__":

    file_dir = './files/'
    test1 = pda.PDA(json_reader.read_file(file_dir + 'pda_1_edit.json'))