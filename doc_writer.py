"""
doc_writer.py

Writes the code unit information and the the generated docstrings to a .md file,
files keep their original name and extensions to deal with duplicate names across 
different file types
"""
import os

def setup_docs_folder():
    os.makedirs("docs", exist_ok = True)

def write_to_doc(file_path: str, code_unit_information: list):
    with open(os.path.join("docs", os.path.basename(file_path) + ".md"), 'w') as f:
        f.write("-"*60 + "\n\n")
        for unit in code_unit_information:
            f.write(f"{unit[0]} [{unit[1]}] (lines: {unit[2]}-{unit[3]}):\n\n")
            f.write(f"{unit[4]}\n\n")      
            f.write("-"*60 + "\n\n")
    

