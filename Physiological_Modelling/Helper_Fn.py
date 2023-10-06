# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 12:41:19 2023

@author: Lasse
"""

# %% Difference Checker
from difflib import Differ

def difference_checker(file1: str, file2: str, output_file: str) -> None:
    """ Checks difference in content between 2 codefiles. 
    Appends output to .txt.
    
    Symbol mapping:
        - = Line unique to sequence 1
        + = line unique to sequence 2
        '' = line common to both sequence
        ? = line not present in either input sequence
    

    Parameters
    ----------
    file1 : str
        filename of reference codefile.
    file2 : str
        filename of comparison codefile.
    output_file : str
        filename of output file.

    """
    
    with open(file1) as file_1, open(file2) as file_2:
        differ = Differ()
     
        with open(output_file,"a") as f:
            for line in differ.compare(file_1.readlines(), file_2.readlines()):
                print(line,file=f)


