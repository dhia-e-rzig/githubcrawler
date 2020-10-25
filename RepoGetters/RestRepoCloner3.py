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
HDD= "E:"

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




with open("../JSON Files/cloning3progress.json", 'r+') as outfile:
    progress=json.load(outfile)
    print(progress)

# with open("reposNotFoundAgain.csv", 'a+') as outfile:
#  outfile.write("error,url")


# repos_list = open("repo-metadata-sortedBySize.csv", "r", newline='')
# repos_dataframe = pandas.read_csv(repos_list, delimiter=',')

with open("../CSV Files/oldies/reposNotFoundAgain.csv", "r", newline='') as repos_list:
    notfound_dataframe = pandas.read_csv(repos_list, delimiter=',')
    for i in range (progress,len(notfound_dataframe.index)):
        df=notfound_dataframe.loc[i]
        print(df)
        # arr = str(df["url"]).strip().split("/")
        name = str(df["name"]).strip()
        # df2 = repos_dataframe.loc[repos_dataframe["full_name"] == name]
        category= df["category"]
        error=str(df["error"])
        if "404" in error:
            continue
        try :
            a = urllib.request.urlopen(df["url"])
        except Exception as e :
            with open("../CSV Files/oldies/reposNotFoundAgainAgain.csv", 'a+') as outfile:
                outfile.write(str(e)+","+category+","+name+","+df["url"]+"\n")
                outfile.flush()
            with open("../JSON Files/cloning3progress.json", 'w+') as outfile:
                progresspickled = jsonpickle.encode(progress, unpicklable=False)
                outfile.write(progresspickled)
                outfile.flush()
            continue
        # if(a.getcode == 404 ):
        #     continue

        if(category =="Tool"):
            # print(os.getcwd()+"\\repos\\"+name)
            pather=os.path.join(repos_dir+"\\tool\\", name)
            if(path.exists(pather)):
                print("unfinished download found at "+pather+" Deleting and restarting download")
                rmtree(pather)
            try:
                Repo.clone_from("https://github.com/" + name + ".git", repos_dir +"\\tool\\"+ name, branch='master')
            except Exception as e:
                with open("../CSV Files/oldies/reposNotFoundAgainAgain.csv", 'a+') as outfile:
                    outfile.write(str(e) + ","+category+","+name+"," + df["url"] + "\n")
                    outfile.flush()
                with open("../JSON Files/cloning3progress.json", 'w+') as outfile:
                    progresspickled = jsonpickle.encode(progress, unpicklable=False)
                    outfile.write(progresspickled)
                    outfile.flush()
                continue
            # Downloaded+=1
        elif (category== "Applied"):
            # print(os.getcwd()+"\\repos\\"+name)
            pather = os.path.join(repos_dir+"\\applied\\", name)
            if (path.exists(pather)):
                print("unfinished download found at " + pather + " Deleting and restarting download")
                rmtree(pather)
            try:
                Repo.clone_from("https://github.com/" + name + ".git", repos_dir+"\\applied\\"+ name,
                            branch='master')
            except Exception as e:
                with open("../CSV Files/oldies/reposNotFoundAgainAgain.csv", 'a+') as outfile:
                    outfile.write(str(e) +","+category+ ","+name+"," + df["url"] + "\n")
                    outfile.flush()
                with open("../JSON Files/cloning3progress.json", 'w+') as outfile:
                    progresspickled = jsonpickle.encode(progress, unpicklable=False)
                    outfile.write(progresspickled)
                    outfile.flush()
                continue
            # Downloaded += 1
        # else:
        #     # print(os.getcwd()+"\\repos\\"+name)
        #     pather = os.path.join(repos_dir+"\\no-ai-ml\\", name)
        #     if (path.exists(pather)):
        #         print("unfinished download found at " + pather + " Deleting and restarting download")
        #         rmtree(pather)
        #     try:
        #         Repo.clone_from("https://github.com/" + name + ".git", repos_dir +"\\no-ai-ml\\"+ name,
        #                     branch='master')
        #     except Exception as e:
        #         with open("reposNotFound.txt", 'a+') as outfile:
        #             outfile.write(str(e)+","+category+","+name+","+df["url"]+"\n")
        #             outfile.flush()
        #         with open("cloning2progress.json", 'w+') as outfile:
        #             progresspickled = jsonpickle.encode(progress, unpicklable=False)
        #             outfile.write(progresspickled)
        #             outfile.flush()
        #         continue
            # Downloaded += 1
            # if(Downloaded>=20):
            #     exit()
        progress+=1
        with open("../JSON Files/cloning3progress.json", 'w+') as outfile:
            progresspickled=jsonpickle.encode(progress,unpicklable=False)
            outfile.write(progresspickled)
            outfile.flush()

    # for row in csv_dictreader:
    #     # "git@github.com:"+
    #     Repo.clone_from(row[2], "repos\\"+ row[0], branch='master')
    #     line_count += 1
    #     if (line_count > 5):
    #         break

