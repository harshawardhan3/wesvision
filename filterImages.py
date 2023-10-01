import fileinput
import os
from globalVar import *

#row start from 0
def filter_files(target_line_numbers, replace_file):
    filename = replace_file 

    with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
        for line_number, line in enumerate(file, start=0):
            if line_number in target_line_numbers and line.strip():
                new_line = line[:-2] + '0\n'
            else:
                new_line = line[:-2] + '1\n'
            print(new_line, end='')
    os.remove(f"{filename}.bak")

#input are two list
def transform_to_rows(names, pred_blur, pred_glare):
    rows = []
    length = len(names)
    assert(length == len(pred_blur))
    assert(length == len(pred_glare))
    siz = len("destination")
    for i in range(length):
        rowNo = int(names[i][siz:-4])
        if(pred_blur[i] == "blur" or pred_glare[i] =="glare"):
            rows.append(rowNo-1)
    return rows


if __name__ == "__main__":
    filter_files(g_rows, f"{g_file_dir}/time.txt")
    print("done")
