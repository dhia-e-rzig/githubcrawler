import csv
import gzip
import io
import math
from codecs import encode
from datetime import datetime
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
import RepoAnalyzers.filesLister as fL
import RepoAnalyzers.buildFileAnayzer as bFA

x = datetime.now()
time = x.strftime("%x-%X").replace(":", "-").replace("/", "-")

progress = 0

listOfTypes=["applied","tool","no-ai-ml"]

def set_type(i):
    return listOfTypes[i]

#Define variables and fields
def setup_env_for_type(i):
    # x = datetime.now()
    # time=x.strftime("%x-%X").replace(":","-").replace("/","-")

    type = listOfTypes[i]
    output_file = open("../CSV Files/devopsfiles-"+time+"-"+type+".csv", "w+", encoding="utf-8")
    output_file.write("ProjectName;FilePath;DevopsType;DevopsTool;Notes\n")
    unknowns_file = open("../CSV Files/unknowns-"+time+"-"+type+".csv", "w+", encoding="utf-8")
    unknowns_file.write("ProjectName;Filepath\n")
    return(output_file,unknowns_file,type)

#Define paths for projects
pathsDict={}
pathsDict["applied"]=[ "E:\\PhD Work\\repos\\applied", "F:\\PhD Work\\repos\\applied"]
pathsDict["tool"]=[ "E:\\PhD Work\\repos\\tool" , "F:\\PhD Work\\repos\\tool" ]
pathsDict["no-ai-ml"] = [ "D:\\PhD Work\\repos\\no-ai-ml","E:\\PhD Work\\repos\\no-ai-ml","F:\\PhD Work\\repos\\no-ai-ml" ]

#Load Defintionss of devops file
with open("..\\Excel Files\ConfigFiles.xlsx","rb") as configFile:
    special_files_dataframe=pandas.read_excel(configFile)
temp_list=special_files_dataframe["Tool"].tolist()
Tools_list=res = [i for n, i in enumerate(temp_list) if i not in temp_list[:n]]
Directories = special_files_dataframe["Directory"].tolist()
FileNamesAndExtensions = special_files_dataframe["Files"].tolist()
FileNamesAndExtensionsAndDirectories = list(zip(FileNamesAndExtensions, Directories))



count_dict = {}

f = []

count_dict["total"] = 0
count_dict["unknown"] = 0
for ext in FileNamesAndExtensions:
    count_dict[ext] = 0

generic_ext = ['.csv', '.py', '.java', '.c', '.cpp', '.exe', '.cs', '.md', '.txt','.html','.ts','.go','.png','.js','.css','.s','.ini','.jpg','.bmp','ipynb','.map','.scss','.gif','.markdown','.pem','.sh','.xaml','.csproj','.onnx','.svg','.lock','.sln','.pdf','.resx','.tdb','.log','.p','.pbtxt',".xaml",'.tsv','.bmp','.h',".pt",'.pyc',".xml",'.yaml','.yml']
ignored_ext=['.gitignore', 'README.md', 'LICENSE', "AUTHORS", "CONTRIBUTORS", "PATENTS", "OWNERS", "SECURITY_CONTACTS", "NOTICE", "Readme", ".DS_Store", ".gitattributes", "CODEOWNERS", ".gitkeep", ".gitmodules", "GOLANG_CONTRIBUTORS"]

for t1ext in generic_ext:
    count_dict[t1ext] = 0

for t2ext in ignored_ext:
    count_dict[t2ext] = 0

def classify_file(dirpath, filename,projectname,output_file,unknowns_file):
    filename = str(filename).strip()
    count_dict["total"] += 1

    # if ".git" in dirpath:
    #     return
    # if ".idea" in dirpath:
    #     return
    # if ".vscode" in dirpath:
    #     return
    for iext in ignored_ext:
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

        if  filename.lower().endswith(ext.lower()):
            category = str(special_files_dataframe.loc[special_files_dataframe['Files'] == ext]['Category'].values).replace('[', '').replace(']', '').replace('\'','')
            tool = str(special_files_dataframe.loc[special_files_dataframe['Files'] == ext]['Tool'].values).replace('[', '').replace(']', '').replace('\'','')
            string=projectname+";"+dirpath+';'+ category +';'+ tool +";N/A"+"\n"
            output_file.write(string)
            output_file.flush()
            count_dict[ext] += 1
            continue

    for gext in generic_ext:
        if filename.lower().endswith(gext):
            count_dict[gext] += 1
            return

    count_dict["unknown"] += 1
    unknowns_file.write(projectname+";"+dirpath+"\n")
    unknowns_file.flush()
    return



# list_dirs = list(walk(mypath))
#listOfTypes=["applied","tool","no-ai-ml"]
i = 2
type=set_type(i)
refreshFromFs=False
#load/create fs csv

myPaths = pathsDict[type]
filesystem_csv=""

try:
    recentFile= open("../JSON Files/lastOutputForType" + str(i) + ".json", "r+")
    lastfilename=json.load(recentFile)
except:
    refreshFromFs=True

if refreshFromFs:
    filesystem_csv = fL.list_projects_files(myPaths, type+"-Analysis-"+time)
    with open("../JSON Files/lastOutputForType"+str(i)+".json", 'w+') as outfile:
        filesystem_csv_pickled = jsonpickle.encode(filesystem_csv, unpicklable=False)
        outfile.write(filesystem_csv_pickled)
        outfile.flush()
elif lastfilename != "" :
    filesystem_csv=lastfilename
else:
    # Can't find last analysis file
    filesystem_csv = fL.list_projects_files(myPaths, type+"-Analysis-"+time)
    with open("../JSON Files/lastOutputForType" + str(i) + ".json", 'w+') as outfile:
        filesystem_csv_pickled = jsonpickle.encode(filesystem_csv, unpicklable=False)
        outfile.write(filesystem_csv_pickled)
        outfile.flush()

#analyze fileSystem
skip_analysis=True
fs_df = pandas.read_csv(filesystem_csv, usecols=["ProjectName", "FilePath", "FileName", "Extension"])
list_of_projects=fs_df["ProjectName"].tolist()

if(not skip_analysis):
    (out, unk, type) = setup_env_for_type(i)
    with open("../JSON Files/lastAnalysisForType" + str(i) + ".json", 'w+') as outfile:
        out_pickled = jsonpickle.encode(out.name, unpicklable=False)
        outfile.write(out_pickled)
        outfile.flush()

    last_fs_analysis=out.name

    for index, row in fs_df.iterrows():
       classify_file(row['FilePath'],row['FileName'],row['ProjectName'],out,unk)

    #save the summary
    saveTheSummary=True
    if saveTheSummary:
        with open("../Text Files/output_overall-"+time+".txt", 'w+') as outfile:
            outfile.write(str(count_dict) + "\n")

else:
    with open("../JSON Files/lastAnalysisForType" + str(i) + ".json", 'r+') as outfile:
        last_fs_analysis = json.load(outfile)
#analyze files

#extract build files from fs analysis
fs_file=open(last_fs_analysis,"rb")
decoder_wrapper = io.TextIOWrapper(fs_file, encoding='utf-8', errors='ignore')
devops_fromfs_df=pandas.read_csv(decoder_wrapper,sep=";",error_bad_lines=False,usecols=["ProjectName","FilePath","DevopsType","DevopsTool","Notes"])
# print(devops_fromfs_df.columns)

MavenRows=devops_fromfs_df[devops_fromfs_df["FilePath"].str.endswith("pom.xml")]
GradleRows=devops_fromfs_df[devops_fromfs_df["FilePath"].str.endswith("build.gradle")]
RakeRows=devops_fromfs_df[devops_fromfs_df["FilePath"].str.endswith("Rakefile")]

build_analysis_output_file = open("../CSV Files/devopsfrombuildfiles-"+time+"-"+type+".csv", "w+", encoding="utf-8")
build_analysis_output_file.write("ProjectName;FilePath;ToolDetected;CorrespondingTextInFile\n")

for index,row in MavenRows.iterrows():
    bFA.analyzeMavenProject(row["ProjectName"], row["FilePath"], Tools_list, build_analysis_output_file)

for index,row in GradleRows.iterrows():
    bFA.analyzeGradleProject(row["ProjectName"], row["FilePath"], Tools_list, build_analysis_output_file)

for index,row in RakeRows.iterrows():
    bFA.analyzeRakeProject(row["ProjectName"], row["FilePath"], Tools_list, build_analysis_output_file)

final_results_dict={}
for project in list_of_projects:
    final_results_dict[project]={}

for project in list_of_projects:
    for tool in Tools_list:
        final_results_dict[project][tool]=False

fs_results= pandas.read_csv(last_fs_analysis,sep=";")

build_analysis_results=pandas.read_csv("../CSV Files/devopsfrombuildfiles-"+time+"-"+type+".csv",sep=";",encoding="utf-8", usecols=["ProjectName","FilePath","ToolDetected","CorrespondingTextInFile"])

for index,row in fs_results.iterrows():
    for tool in Tools_list:
        if str(row["DevopsTool"]).strip().lower() == tool.lower():
            final_results_dict[row["ProjectName"]][tool] = True

for index,row in build_analysis_results.iterrows():
    for tool in Tools_list:
        if str(row["ToolDetected"]).strip().lower() == tool.lower():
            final_results_dict[row["ProjectName"]][tool] = True

fields= ["ProjectName"] + Tools_list
print(fields)
def mergedict(a,b):
    a.update(b)
    return a

print()

with open("..\\CSV Files\\final_output-"+time+"-"+type+".csv", "w+") as f:
    w = csv.DictWriter(f, fields)
    w.writeheader()
    for k,d in sorted(final_results_dict.items()):
        w.writerow(mergedict({'ProjectName': k},d))