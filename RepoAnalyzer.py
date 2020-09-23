from git import Repo
import pandas
import os
import jsonpickle
import json
import os.path as path
import os
import shutil
import stat
from pathlib import Path
from os import walk


progress= 0
HDD= "F:"

repos_dir=HDD+"\\PhD Work\\repos\\"

output_file = open("output.txt","a+")

with open("analyzingAIMLprogress.json",'r+') as outfile:
    progress=json.load(outfile)
    print(progress)
with open("filetypes.csv", "r", newline='') as files_list:
    special_files_dataframe = pandas.read_csv(files_list, delimiter=',')


Directories=special_files_dataframe["Directory"].tolist()
FileNamesAndExtensions=special_files_dataframe["FileName"].tolist()

special_files_dataframe.set_index("FileNameandExtension")

mypath=path.join(HDD,repos_dir)

count_dict={}

f = []

count_dict["total"] = 0
count_dict["unknown"] = 0
for ext in FileNamesAndExtensions:
    count_dict[ext]=0



def test(dirpath,filename):
    count_dict["total"]+=1
    for ext in FileNamesAndExtensions:
        if filename==ext:
            output_file.write(dirpath+" is implementing CI with a "+ special_files_dataframe[ext])
            output_file.flush()
            count_dict[ext]+=1
        elif filename.endswith(ext):
            count_dict[ext]+=1
        else:
            output_file.write(dirpath+'\\'+filename+" Unknown file")
            count_dict["unknown"]+=1

for (dirpath, dirnames, filenames) in walk(mypath):
    for filename in filenames:
        test(dirpath,filename)
