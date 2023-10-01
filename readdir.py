import os
import re
from datetime import datetime
from globalVar import *

folder_path = "./userdata"

def custom_sort(a):
    parts = re.split(r'[\\/\\-]', a)
    int_parts = [int(part) for part in parts]
    return tuple(int_parts)

class File:
  def __init__(self):
      self.filepath= ""
      self.timestamp = None

def extract_r(folder_path ,file_list):
    for folder, subfolders, files in os.walk(folder_path):
        if(len(subfolders)==0):
            for file in files:
                myfile = File()
                myfile.filepath = os.path.join(folder, file)
                file_list.append(myfile)
        if(len(subfolders)>0):
            if subfolders[0].isdigit(): #for numbers
                subfolders.sort(key = lambda x : int(x))
            else:
                subfolders.sort(key = custom_sort )
        for folder in subfolders:
            extract_r(folder_path +'/' + folder, file_list)
        break
        
def extract_files_from_folder(folder_path):
    file_list = []
    extract_r(folder_path, file_list)
    return file_list