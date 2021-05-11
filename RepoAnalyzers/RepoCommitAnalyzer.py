import jsonpickle
import nltk
import numpy as np
import random
import string
import json
import bs4 as bs
import urllib.request
import re
from stemming.porter2 import stem
from datetime import datetime
import io
import pandas
from git import Repo
from git import Git

import numpy as np

listOfTypes=["applied","tool","no-ai-ml"]


def intersection(lst1, lst2):
    # Use of hybrid method
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3


def is_commit_comment_bugfix(comment):
    corpus = nltk.sent_tokenize(comment)
    wordfreq = {}
    for i in range(len(corpus)):
        corpus[i] = corpus[i].lower()
        corpus[i] = re.sub(r'\W', ' ', corpus[i])
        corpus[i] = re.sub(r'\s+', ' ', corpus[i])
    for sentence in corpus:
        tokens = nltk.word_tokenize(sentence)
        for token in tokens:
            token = stem(token)
            if token not in wordfreq.keys():
                wordfreq[token] = 1
            else:
                wordfreq[token] += 1

    ListOfBugFixes=["error","bug","fix","issue","mistake","incorrect","fault","defect","flaw","type"]
    inter_list = intersection( ListOfBugFixes , wordfreq.keys())

    if(len(inter_list) >0):
        return True
    else:
        return False


df_loaded = False
df=""
i_df=-1
def load_df(i):
    global df_loaded
    global df
    global i_df
    if(i_df != i ):
        df_loaded = False
        df=""
        i_df=i
    if(df_loaded):
        return df
    else:
        df_loaded = True
        type = listOfTypes[i]
        df=pandas.read_csv("../CSV Files/commits-statuses-" + type + "-2.csv", sep=';', encoding="utf-8")
        return df

#TODO test this
def is_commit_build_fix(i,oid,projectname):
    dataframe=load_df(i)
    # dataframe.iterrows()
    rows = dataframe.loc[dataframe['ProjectName'] == projectname]
    current_commit= dataframe.loc[ (dataframe['ProjectName'] == projectname )&  (dataframe['CommitOID'] == oid) ]
    stats=current_commit["CommitStatus"].to_list()
    if(stats== "FAILURE"):
        return False
    for index,row in rows.iterrows():
        if(row["CommitStatus"]=="SUCCESS" and row['CommitOID'] != oid):
            return False
        elif (row["CommitStatus"]=="FAILURE"):
            # print("BuildFix")
            return True
    return False

def get_progress(i):
    try:
        with open("../JSON Files/CommitsAnalysis"+str(i)+".json", 'r+') as outfile:
            progress = json.load(outfile)
            print("progress for"+str(i)+": "+str(progress))
    except:
        progress = 0
    return progress


def save_progress(progress,i):
    try:
        with open("../JSON Files/CommitsAnalysis"+str(i)+".json", 'w+') as outfile:
            progresspickled = jsonpickle.encode(progress, unpicklable=False)
            outfile.write(progresspickled)
            outfile.flush()
    except:
        return







def analyze_past_git_commits(i):
    progress=get_progress(i)
    counter=-1
    # with open("../JSON Files/lastAnalysisForType" + str(i) + ".json", 'r+') as outfile:
    #     last_buildfiles_fs_analysis = json.load(outfile)
    last_buildfiles_fs_analysis="../CSV Files/IntersectionDevOpsFS-Applied.csv"
    type = listOfTypes[i]
    x = datetime.now()
    time = x.strftime("%x-%X").replace(":", "-").replace("/", "-")
    output_file = open("../CSV Files/commit-types-" + time + "-" + type + ".csv", "a+", encoding="utf-8")
    output_file.write("ProjectName;CommitOID;CommitDateAndTime;IsBuildFix;IsBugFix;IsCodeImprovement\n")
    output_file2 = open("../CSV Files/commit-types-comments-" + time + "-" + type + ".csv", "a+", encoding="utf-8")
    output_file2.write("ProjectName;CommitOID;CommitDateAndTime;CommitComment;IsBuildFix;IsBugFix;IsCodeImprovement\n")
    output_file3 = open("../CSV Files/commit-types-files-" + time + "-" + type + ".csv", "a+", encoding="utf-8")
    output_file3.write("ProjectName;CommitOID;CommitDateAndTime;CommitFiles;IsBuildFix;IsBugFix;IsCodeImprovement\n")
    error_file = open("../CSV Files/commit-types-errors-" + time + "-" + type + ".csv", "a+",
                      encoding="utf-8")
    error_file.write("ProjectName;Exception\n")
    buildfiles_infs_file = open(last_buildfiles_fs_analysis, "rb")
    decoder_wrapper = io.TextIOWrapper(buildfiles_infs_file, encoding='utf-8', errors='ignore')
    devops_fromfs_df = pandas.read_csv(decoder_wrapper, sep=",", error_bad_lines=False,
                                       usecols=["ProjectName", "FilePath"])
    oldprojectname = ""
    for index, row in devops_fromfs_df.iterrows():
        project_name = row["ProjectName"]
        if(project_name==oldprojectname):
            continue
        else:
            counter+=1
        oldprojectname = project_name
        print(project_name)
        print(counter)
        if(counter<=progress):
            continue
        full_path = row["FilePath"]
        x = project_name.split("/")
        file_with_path = full_path.split(project_name.replace("/", "\\"))[1]
        file_with_path = file_with_path[1:]
        repo_path = full_path.split(project_name.replace("/", "\\"))[0] + project_name
        try:
            repo = Repo(repo_path)
            commits=list(repo.iter_commits("master"))
            for commit in commits:
                oid=commit.hexsha
                msg=commit.message
                date=commit.committed_datetime
                files = repo.git.execute("git diff-tree --no-commit-id --name-only -r "+str(oid))
                # print(str(date))
                build_fix=is_commit_build_fix(i,oid,project_name)
                bug_fix=is_commit_comment_bugfix(msg)
                code_improvment=not build_fix and not bug_fix
                output_file.write(project_name+";"+str(oid)+";"+str(date)+";"+str(build_fix)+";"+str(bug_fix)+";"+str(code_improvment)+"\n")
                output_file2.write(project_name+";"+str(oid)+";"+str(date)+";"+str(msg).replace(";","--").replace("\n"," ")+";"+str(build_fix)+";"+str(bug_fix)+";"+str(code_improvment)+"\n")
                output_file3.write(project_name+";"+str(oid)+";"+str(date)+";"+str(files).replace("\n","==")+";"+str(build_fix)+";"+str(bug_fix)+";"+str(code_improvment)+"\n")
                save_progress(counter,i)
        except Exception as e:
            try:
                error_file.write(project_name+";"+str(e))
            except:
                print(e)

#TODO RUn these


# print ("Start 1 date and time : ")
# now = datetime.now()
# print (now.strftime("%Y-%m-%d %H:%M:%S"))
# analyze_past_git_commits(1)
#applied
# now = datetime.now()
# print ("Start 0 date and time : ")
# print (now.strftime("%Y-%m-%d %H:%M:%S"))
# analyze_past_git_commits(0)
# now = datetime.now()
# print ("Start 2 date and time : ")
# print (now.strftime("%Y-%m-%d %H:%M:%S"))
# analyze_past_git_commits(2)
#

with open("..\\Excel Files\ConfigFiles_all.xlsx","rb") as configFile:
    special_files_dataframe=pandas.read_excel(configFile)
temp_list=special_files_dataframe["Tool"].tolist()
Tools_list=res = [i for n, i in enumerate(temp_list) if i not in temp_list[:n]]
Directories = special_files_dataframe["Directory"].tolist()
FileNamesAndExtensions = special_files_dataframe["Files"].tolist()
FileNamesAndExtensionsAndDirectories = list(zip(FileNamesAndExtensions, Directories))


ignored_ext=['.gitignore', 'README.md', 'LICENSE', "AUTHORS", "CONTRIBUTORS", "PATENTS", "OWNERS", "SECURITY_CONTACTS", "NOTICE", "Readme", ".DS_Store", ".gitattributes", "CODEOWNERS", ".gitkeep", ".gitmodules", "GOLANG_CONTRIBUTORS"]


def is_devops_file(filepath):
    dirpath="".join(filepath.split("/")[:-1])
    filename = filepath.split("/")[-1]

    for iext in ignored_ext:
        if filename==iext:
            return False

    for i in range(0, len(FileNamesAndExtensionsAndDirectories)):
        (ext, dir) = FileNamesAndExtensionsAndDirectories[i]
        # if  math.isnan(dir):
        #     print(dir)
        #     return
        if isinstance(dir, str):
            if dir !='NA' and dir not in dirpath:
                continue
        if(len(ext) <= 6):
            if filename.lower().endswith(ext.lower()):
                return True
        else:
            if '*' == ext :
               return True
            elif '*' in ext :
               return True
            elif filename.lower() == ext.lower() or "."+filename.lower() == ext.lower() or filename.lower() == "."+ext.lower():
                return True
    return False



def getDevopsCommits(i):
    type = listOfTypes[i]
    x = datetime.now()
    time = x.strftime("%x-%X").replace(":", "-").replace("/", "-")

    commit_files_old_lists=["../CSV Files/commit-types-files-12-09-20-21-54-39-applied.csv","../CSV Files/commit-types-files-12-09-20-09-41-56-tool.csv","../CSV Files/commit-types-files-12-11-20-08-02-01-no-ai-ml.csv"]
    commit_files_new_lists=["../CSV Files/commit-types-files-12-31-20-11-01-20-applied.csv","../CSV Files/commit-types-files-12-31-20-11-01-36-tool.csv","../CSV Files/commit-types-files-12-31-20-11-31-37-no-ai-ml.csv"]

    commits_old_file=commit_files_old_lists[i]
    commits_new_file=commit_files_new_lists[i]

    commits_new_file_pd = pandas.read_csv(commits_new_file, sep=';', encoding="utf-8", error_bad_lines=False)
    commits_old_file_pd = pandas.read_csv(commits_old_file, sep=';', encoding="utf-8", error_bad_lines=False)

    commits_file_pd=commits_old_file_pd.append(commits_new_file_pd,ignore_index=True)

    if(i ==1 ):
        temp_pd=  pandas.read_csv("../CSV Files/commit-types-files-12-08-20-05-37-34-tool.csv", sep=';', encoding="utf-8", error_bad_lines="ignore")
        commits_file_pd=temp_pd.append(commits_file_pd,ignore_index=True)
    output_file = open("../CSV Files/devsonly_commit-types-files-" + time + "-" + type + ".csv", "a+", encoding="utf-8")
    output_file.write("ProjectName;CommitOID;CommitDateAndTime;CommitFiles;IsBuildFix;IsBugFix;IsCodeImprovement\n")

    error_file = open("../CSV Files/devsonly_commit-types-errors-" + time + "-" + type + ".csv", "a+",
                      encoding="utf-8")
    error_file.write("ProjectName;Exception\n")


    for (_,projectname,commitoid,commitdt,commitfiles,buildfix,bugfix,codeimprov) in commits_file_pd.itertuples():
        if not isinstance(commitfiles, str):
            continue
        if (commitfiles == "NA"):
            continue
        arr_files=str(commitfiles).split("==")
        for file in arr_files:
            if is_devops_file(file):
                output_file.write(
                    projectname + ";" + str(commitoid) + ";" + str(commitdt) + ";" + str(commitfiles) + ";" + str(buildfix) + ";" + str(
                        bugfix) + ";" + str(codeimprov) + "\n")
                break


getDevopsCommits(2)


def reclassify_commits(i):
    type = listOfTypes[i]
    x = datetime.now()
    time = x.strftime("%x-%X").replace(":", "-").replace("/", "-")
    commits_files_list=["../CSV Files/devsonly_commit-types-files-01-03-21-17-22-19-applied.csv","../CSV Files/devsonly_commit-types-files-01-03-21-17-23-01-tool.csv","../CSV Files/devsonly_commit-types-files-01-03-21-17-23-24-no-ai-ml.csv"]
    output_file = open("../CSV Files/devsonly_reclassified_commit-types-files-" + time + "-" + type + ".csv", "a+", encoding="utf-8")
    output_file.write("ProjectName;CommitOID;CommitDateAndTime;CommitFiles;IsBuildANDBugFix;IsOnlyBuildFix;IsOnlyBugFix;IsCodeImprovement\n")

    error_file = open("../CSV Files/devsonly_reclassified_commit-types-errors-" + time + "-" + type + ".csv", "a+",
                      encoding="utf-8")
    error_file.write("ProjectName;Exception\n")
    commits_file_pd = pandas.read_csv(commits_files_list[i], sep=';', encoding="utf-8", error_bad_lines=False)
    for (_,projectname,commitoid,commitdt,commitfiles,buildfix,bugfix,codeimprov) in commits_file_pd.itertuples():
        if(str(bugfix)=="False"):
            bool_bugfix=False
        else:
            bool_bugfix=True
        if (str(buildfix) == "False"):
            bool_buildfix = False
        else:
            bool_buildfix = True
        both= bool_buildfix and bool_bugfix
        only_buildfix=bool_buildfix and (not bool_bugfix)
        only_bugfix= bool_bugfix and (not bool_buildfix)
        output_file.write(projectname + ";" + str(commitoid) + ";" + str(commitdt) + ";" + str(commitfiles) +  ";" + str(both)+ ";" + str(only_buildfix) + ";" + str(only_bugfix) + ";" + str(codeimprov) + "\n")

reclassify_commits(2)
