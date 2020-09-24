import math

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

progress = 0
HDD = "F:"

repos_dir = HDD + "\\PhD Work\\repos\\"

output_file = open("output.csv", "wt+")
output_file.write("Devops file?;Filepath;Devops Type \n")

# with open("analyzingAIMLprogress.json", 'r+') as outfile:
#     progress = json.load(outfile)
#     print(progress)
with open("filetypes.csv", "r", newline='') as files_list:
    special_files_dataframe = pandas.read_csv(files_list, delimiter=',')

Directories = special_files_dataframe["Directory"].tolist()
FileNamesAndExtensions = special_files_dataframe["FileNameAndExtension"].tolist()
FileNamesAndExtensionsAndDirectories = list(zip(FileNamesAndExtensions, Directories))
# special_files_dataframe.set_index("FileNameandExtension", inplace=True, drop=False)
#
# print(special_files_dataframe)


mypath = path.join(HDD, repos_dir)

count_dict = {}

f = []

count_dict["total"] = 0
count_dict["unknown"] = 0
for ext in FileNamesAndExtensions:
    count_dict[ext] = 0

generic_ext = ['.csv', '.py', '.java', '.c', '.cpp', '.exe', '.cs', '.md', '.txt','.html','.ts','.go','.png','.js','.css','.s','.ini','.jpg','.bmp','ipynb','.map','.scss','.gif','.markdown','.pem','.sh','.xaml','.csproj','.onnx','.svg','.lock','.sln','.pdf','.resx','.tdb','.log','.p','.pbtxt',".xaml",'.tsv','.bmp','.h',".pt",'.pyc']
ignorder_ext=['.gitignore','README.md','LICENSE',"AUTHORS","CONTRIBUTORS","PATENTS","OWNERS","SECURITY_CONTACTS","NOTICE","Readme",".DS_Store",".gitattributes","CODEOWNERS",".gitkeep",".gitmodules","GOLANG_CONTRIBUTORS"]

for t1ext in generic_ext:
    count_dict[t1ext] = 0

for t2ext in ignorder_ext:
    count_dict[t2ext] = 0

def test(dirpath, filename):
    filename = filename.strip()
    count_dict["total"] += 1

    if ".git" in dirpath:
        return

    if ".idea" in dirpath:
        return
    if ".vscode" in dirpath:
        return
    for iext in ignorder_ext:
        if filename==iext:
            count_dict[iext] += 1
            return

    for i in range(0, len(FileNamesAndExtensionsAndDirectories)):
        (ext, dir) = FileNamesAndExtensionsAndDirectories[i]
        # if  math.isnan(dir):
        #     print(dir)
        #     return
        if isinstance(dir, str):
            if dir !='NA' and dir not in dirpath:
                continue

        if filename == ext:
            filetype = str(special_files_dataframe.loc[special_files_dataframe['FileNameAndExtension'] == ext]['FileType'].values).replace('[', '').replace(']', '').replace('\'','')
            output_file.write("Yes"+';'+dirpath+ '\\' + filename +';'+ filetype + "\n")
            output_file.flush()
            count_dict[ext] += 1
            return
        elif filename.lower().endswith(ext):
            filetype = str(special_files_dataframe.loc[special_files_dataframe['FileNameAndExtension'] == ext][
                               'FileType'].values).replace('[', '').replace(']', '').replace('\'', '')
            count_dict[ext] += 1
            output_file.write("Unknown"+';'+dirpath + '\\' + filename +';'+ filetype +"\n")
            output_file.flush()
            return

    for gext in generic_ext:
        if filename.lower().endswith(gext):
            count_dict[gext] += 1
            return

    count_dict["unknown"] += 1
    output_file.write("Unknown"+';'+dirpath + '\\'+ filename + ';'+"Unknown file"+"\n")
    output_file.flush()
    return


list_dirs = list(walk(mypath))

for i in range(progress, len(list_dirs)):
    (dirpath, dirnames, filenames) = list_dirs[i]
    for filename in filenames:
        test(dirpath, filename)
    with open("analyzingAIMLprogress.json", 'w+') as outfile:
        progresspickled = jsonpickle.encode(i, unpicklable=False)
        outfile.write(progresspickled)


with open("output_overall.txt", 'w+') as outfile:
    outfile.write(str(count_dict) + "\n")
