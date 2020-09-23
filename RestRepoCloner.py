from git import Repo
import pandas
import os
import jsonpickle
import json
import os.path as path
import os
import shutil
import stat

progress= 0
HDD= "L:"

repos_dir=HDD+"\\PhD Work\\repos\\"

def rmtree(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWRITE)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(top)


with open("cloningAIMLprogress.json",'r+') as outfile:
    progress=json.load(outfile)
    print(progress)

Downloaded=0
with open("repo-metadata-sortedBySize.csv", "r", newline='') as repos_list:
    repos_dataframe = pandas.read_csv(repos_list, delimiter=',')
    for i in range (progress,len(repos_dataframe.index)):
        df=repos_dataframe.loc[i,["Category","full_name"]]
        print(df)
        if(df["Category"] !="No AI-ML"):
            # print(os.getcwd()+"\\repos\\"+df["full_name"])
            if(path.exists(os.path.join(repos_dir, df["full_name"]))):
                path=os.path.join(repos_dir, df["full_name"])
                print("unfinished download found at "+path+" Deleting and restarting download")
                rmtree(path)
            Repo.clone_from("https://github.com/"+df["full_name"]+".git", repos_dir + df["full_name"], branch='master')
            Downloaded+=1
            if(Downloaded>=20):
                exit()
        progress+=1
        with open("cloningAIMLprogress.json", 'w+') as outfile:
            progresspickled=jsonpickle.encode(progress,unpicklable=False)
            outfile.write(progresspickled)

    # for row in csv_dictreader:
    #     # "git@github.com:"+
    #     Repo.clone_from(row[2], "repos\\"+ row[0], branch='master')
    #     line_count += 1
    #     if (line_count > 5):
    #         break

