import urllib.request

from git import Repo
from git import Remote
import pandas
import os
import jsonpickle
import json
import os.path as path
import os
import shutil
import stat

progress= 0
HDD= "F:"

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


with open("../JSON Files/cloningprogress.json", 'r+') as outfile:
    progress=json.load(outfile)
    print(progress)

Downloaded=0
with open("../CSV Files/oldies/repo-metadata-sortedBySize.csv", "r", newline='') as repos_list:
    repos_dataframe = pandas.read_csv(repos_list, delimiter=',')
    for i in range (progress,len(repos_dataframe.index)):
        df=repos_dataframe.loc[i,["Category","full_name"]]
        print(df)

        try :
            a = urllib.request.urlopen("https://github.com/"+df["full_name"]+".git")
        except:
            with open("../CSV Files/oldies/reposNotFound.txt", 'a+') as outfile:
                outfile.write("https://github.com/"+df["full_name"]+".git \n")
                outfile.flush()
            continue
        # if(a.getcode == 404 ):
        #     continue
        if(df["Category"] =="Tool"):
            # print(os.getcwd()+"\\repos\\"+df["full_name"])
            pather=os.path.join(repos_dir+"\\tool\\", df["full_name"])
            if(path.exists(pather)):
                print("unfinished download found at "+pather+" Deleting and restarting download")
                rmtree(pather)
            try:
                Repo.clone_from("https://github.com/"+df["full_name"]+".git", repos_dir +"\\tool\\"+ df["full_name"], branch='master')
            except:
                with open("../CSV Files/oldies/reposNotFound.txt", 'a+') as outfile:
                    outfile.write("https://github.com/" + df["full_name"] + ".git \n")
                    outfile.flush()
                continue
            Downloaded+=1
        elif (df["Category"] == "Applied"):
            # print(os.getcwd()+"\\repos\\"+df["full_name"])
            pather = os.path.join(repos_dir+"\\applied\\", df["full_name"])
            if (path.exists(pather)):
                print("unfinished download found at " + pather + " Deleting and restarting download")
                rmtree(pather)
            try:
                Repo.clone_from("https://github.com/" + df["full_name"] + ".git", repos_dir+"\\applied\\"+ df["full_name"],
                            branch='master')
            except:
                with open("../CSV Files/oldies/reposNotFound.txt", 'a+') as outfile:
                    outfile.write("https://github.com/" + df["full_name"] + ".git \n")
                    outfile.flush()
                continue
            Downloaded += 1
        else:
            # print(os.getcwd()+"\\repos\\"+df["full_name"])
            pather = os.path.join(repos_dir+"\\no-ai-ml\\", df["full_name"])
            if (path.exists(pather)):
                print("unfinished download found at " + pather + " Deleting and restarting download")
                rmtree(pather)
            try:
                Repo.clone_from("https://github.com/" + df["full_name"] + ".git", repos_dir +"\\no-ai-ml\\"+ df["full_name"],
                            branch='master')
            except:
                with open("../CSV Files/oldies/reposNotFound.txt", 'a+') as outfile:
                    outfile.write("https://github.com/" + df["full_name"] + ".git \n")
                    outfile.flush()
                continue
            Downloaded += 1
            # if(Downloaded>=20):
            #     exit()
        progress+=1
        with open("../JSON Files/cloningprogress.json", 'w+') as outfile:
            progresspickled=jsonpickle.encode(progress,unpicklable=False)
            outfile.write(progresspickled)
            outfile.flush()

    # for row in csv_dictreader:
    #     # "git@github.com:"+
    #     Repo.clone_from(row[2], "repos\\"+ row[0], branch='master')
    #     line_count += 1
    #     if (line_count > 5):
    #         break

