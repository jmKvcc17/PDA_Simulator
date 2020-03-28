import os
from resources import json_reader, pda



if __name__ == "__main__":

    file_dir = './files/'
    # Read all the files in files
    # for file in os.listdir('./files'):
        
    #     try:
    #         if file.endswith(".json"):
    #             json_r = json_reader.JsonReader()
    #             json_data = json_r.read_file(file_dir + file)
    #             nfa_type = json_r.check_nfa_type()
    #             print(f"NFA TYPE: {nfa_type}")

    #             if nfa_type == 0:
    #                 nfa = nfa_lambda.NfaLambda(json_data)
    #             if nfa_type == 1:
    #                 nfa = nfa.Nfa(json_data)
    #     except Exception as e:
    #         print(e)
    #         print(f"ERROR: There was an issue with {file}, skipping to next file.")
    #         continue
    
    # json_r = json_reader.JsonReader()
    # json_data = json_r.read_file(file_dir + 'final_563.json')
    # nfa = nfa.Nfa(json_data)
    test1 = pda.PDA(json_reader.read_file(file_dir + 'final_563.json'))