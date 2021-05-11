import io
from datetime import datetime
from time import sleep
import pause
from dateutil import tz

from git import Repo
from git import Git
import pandas
import os
import jsonpickle
import json
import os.path as path
import os
import shutil
import stat
from dateutil import parser as parser

from github import Github

listOfTypes = ["applied", "tool", "no-ai-ml"]
i = 0


def generate_devopsfiles_creation_date(i):
    with open("../JSON Files/lastAnalysisForType" + str(i) + ".json", 'r+') as outfile:
        last_buildfiles_fs_analysis = json.load(outfile)

    type = listOfTypes[i]
    x = datetime.now()
    time = x.strftime("%x-%X").replace(":", "-").replace("/", "-")
    output_file = open("../CSV Files/devopsfiles-creationdate-" + time + "-" + type + ".csv", "w+", encoding="utf-8")
    output_file.write("ProjectName;FilePath;CreationDate;CommitComment\n")
    error_file = open("../CSV Files/devopsfiles-creationdate-errors-" + time + "-" + type + ".csv", "w+",
                      encoding="utf-8")
    error_file.write("ProjectName;FileNameWithRelativePath;Exception\n")
    buildfiles_infs_file = open(last_buildfiles_fs_analysis, "rb")
    decoder_wrapper = io.TextIOWrapper(buildfiles_infs_file, encoding='utf-8', errors='ignore')
    devops_fromfs_df = pandas.read_csv(decoder_wrapper, sep=";", error_bad_lines=False,
                                       usecols=["ProjectName", "FilePath", "DevopsType", "DevopsTool", "Notes"])

    for index, row in devops_fromfs_df.iterrows():
        project_name = row["ProjectName"]
        full_path = row["FilePath"]
        x = project_name.split("/")

        file_with_path = full_path.split(x[1])[1]
        file_with_path = file_with_path[1:]
        repo_path = full_path.split(project_name.replace("/", "\\"))[0] + project_name
        # os.chdir(path)
        repo = Repo(repo_path)
        try:
            string_resp = repo.git.execute("git log --diff-filter=A -- " + file_with_path)
            arr = string_resp.split("\n")
            if (len(arr) < 3):
                # print(string_resp)
                continue
            Date = arr[2]
            if (len(arr) >= 5):
                Comment = arr[4]
            else:
                print(arr)
                Comment = "N/A"
            date = datetime.strptime(Date, "Date: %a %b %d %H:%M:%S %Y %z")
            date_string = date.strftime("%Y-%m-%d")
            print(repo_path)
            # file_name=file_with_path.split("/")[-1]
            output_file.write(project_name + ";" + full_path + ";" + date_string + ";" + Comment + "\n")
        except Exception as e:
            error_file.write(project_name + ";" + file_with_path + ";" + str(e) + "\n")


def generate_devopsfiles_modification_dates(i):
    with open("../JSON Files/lastAnalysisForType" + str(i) + ".json", 'r+') as outfile:
        last_buildfiles_fs_analysis = json.load(outfile)
    type = listOfTypes[i]
    x = datetime.now()
    time = x.strftime("%x-%X").replace(":", "-").replace("/", "-")
    output_file = open("../CSV Files/devopsfiles-modificationdates-" + time + "-" + type + ".csv", "w+",
                       encoding="utf-8")
    output_file.write("ProjectName;FilePath;ModificationDate;CommitComments\n")
    error_file = open("../CSV Files/devopsfiles-modificationdates-errors-" + time + "-" + type + ".csv", "w+",
                      encoding="utf-8")
    error_file.write("ProjectName;FileNameWithRelativePath;Exception\n")
    buildfiles_infs_file = open(last_buildfiles_fs_analysis, "rb")
    decoder_wrapper = io.TextIOWrapper(buildfiles_infs_file, encoding='utf-8', errors='ignore')
    devops_fromfs_df = pandas.read_csv(decoder_wrapper, sep=";", error_bad_lines=False,
                                       usecols=["ProjectName", "FilePath", "DevopsType", "DevopsTool", "Notes"])
    for index, row in devops_fromfs_df.iterrows():
        project_name = row["ProjectName"]
        full_path = row["FilePath"]
        x = project_name.split("/")
        file_with_path = full_path.split(project_name.replace("/", "\\"))[1]
        file_with_path = file_with_path[1:]
        repo_path = full_path.split(project_name.replace("/", "\\"))[0] + project_name
        repo = Repo(repo_path)
        try:
            string_resp = repo.git.execute("git log --follow --  \"" + file_with_path + "\"")
            dates_list = []
            comments_list = []
            for commit in string_resp.split("commit"):
                arr = commit.split("\n")
                # print(arr)
                if len(arr) < 5:
                    continue
                i = 2
                date_string = ""
                Comment = ""
                while True:
                    try:
                        Date = arr[i]
                        Comment = arr[i + 2]
                        date = datetime.strptime(Date, "Date: %a %b %d %H:%M:%S %Y %z")
                        date_string = date.strftime("%Y-%m-%d")
                    except:
                        if (i < 8):
                            i += 1
                            continue
                        else:
                            break
                    break
                dates_list.append(date_string)
                comments_list.append(Comment.strip())
            output_file.write(project_name + ";" + full_path + ";")
            for i in range(0, len(dates_list) - 1):
                output_file.write(dates_list[i] + ",")
            output_file.write(dates_list[-1] + ";")
            for i in range(0, len(comments_list) - 1):
                output_file.write(comments_list[i] + ",")
            output_file.write(comments_list[-1] + "\n")
            print(repo_path)
        except Exception as e:
            error_file.write(project_name + ";" + file_with_path + ";" + str(e) + "\n")


#
def generate_projects_creation_date(i):
    with open("../JSON Files/lastOutputForType" + str(i) + ".json", 'r+') as infile:
        last_buildfiles_fs_analysis = json.load(infile)
    type = listOfTypes[i]
    x = datetime.now()
    time = x.strftime("%x-%X").replace(":", "-").replace("/", "-")
    output_file = open("../CSV Files/projects-creationdate-" + time + "-" + type + ".csv", "w+", encoding="utf-8")
    output_file.write("ProjectName;FirstCommitDate;CommitComment\n")
    error_file = open("../CSV Files/projects-creationdate-errors-" + time + "-" + type + ".csv", "w+", encoding="utf-8")
    error_file.write("ProjectName;Exception \n")
    buildfiles_infs_file = open(last_buildfiles_fs_analysis, "rb")
    decoder_wrapper = io.TextIOWrapper(buildfiles_infs_file, encoding='utf-8', errors='ignore')
    devops_fromfs_df = pandas.read_csv(decoder_wrapper, sep=",", error_bad_lines=False,
                                       usecols=["ProjectName", "FilePath", "FileName", "Extension"])
    oldprojectname = ""
    for index, row in devops_fromfs_df.iterrows():
        project_name = row["ProjectName"]
        if oldprojectname == project_name:
            continue
        oldprojectname = project_name
        full_path = row["FilePath"]
        # x=project_name.split("/")
        # file_with_path = full_path.split(x[1])[1]
        repo_path = full_path.split(project_name.replace("/", "\\"))[0] + project_name
        print(repo_path)
        # file_name=full_path.split("/")
        # path = full_path.replace("/" + file_name, "")
        # os.chdir(path)
        try:
            repo = Repo(repo_path)
            string_resp = repo.git.execute("git rev-list --max-parents=0 HEAD")
            resp0 = string_resp.split("\n")[0]
            show = repo.git.execute("git show " + resp0)
            arr = show.split("\n")
            if (len(arr) < 2):
                continue
            Date = arr[2]
            Comment = arr[4]
            date = datetime.strptime(Date, "Date: %a %b %d %H:%M:%S %Y %z")
            date_string = date.strftime("%Y-%m-%d")
            output_file.write(project_name + ";" + date_string + ";" + Comment + "\n")
        except Exception as e:
            try:
                error_file.write(project_name + ";" + str(e) + "\n")
            except:
                print(" can not catch exception")
        # print(string_resp)


#


def download_bug_reports(i):
    g = Github("549d6bfa963038635d18713f84740a5cf4066647")
    with open("../JSON Files/lastOutputForType" + str(i) + ".json", 'r+') as infile:
        last_buildfiles_fs_analysis = json.load(infile)
    type = listOfTypes[i]
    x = datetime.now()
    time = x.strftime("%x-%X").replace(":", "-").replace("/", "-")
    output_file = open("../CSV Files/projects-issuereports-" + time + "-" + type + ".csv", "w+", encoding="utf-8")
    output_file.write("ProjectName;IssueNumber;IssueTitle;DateOpened;DateClose;Duration\n")
    error_file = open("../CSV Files/projects-issuereports-errors-" + time + "-" + type + ".csv", "w+", encoding="utf-8")
    error_file.write("ProjectName;Exception\n")
    buildfiles_infs_file = open(last_buildfiles_fs_analysis, "rb")
    decoder_wrapper = io.TextIOWrapper(buildfiles_infs_file, encoding='utf-8', errors='ignore')
    devops_fromfs_df = pandas.read_csv(decoder_wrapper, sep=",", error_bad_lines=False,
                                       usecols=["ProjectName", "FilePath", "FileName", "Extension"])
    oldprojectname = ""
    skipThisProject = False
    ProjectToSkip = ''
    projectfound = False
    recovering_from_timeout = False
    if 'remaining=0' in str(g.get_rate_limit()):
        print(g.get_rate_limit())
        ts = g.rate_limiting_resettime
        dateutc = datetime.utcfromtimestamp(ts)
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('America/New_York')
        utc = dateutc.replace(tzinfo=from_zone)
        central = utc.astimezone(to_zone)
        t = datetime.now()
        t = t.astimezone(to_zone)
        seconds=min((central-t).seconds,3600)
        print('sleeping for '+str(seconds)+' seconds starting at'+str(t))
        pause.seconds(seconds)
    for index, row in devops_fromfs_df.iterrows():
        if (row["ProjectName"] != 'microsoft/typescript-styled-plugin' and i == 2 and not projectfound):
            print('looking for continue project')
            continue
        else:
            projectfound = True

        if (skipThisProject):
            oldprojectname = ProjectToSkip

        if (skipThisProject and row["ProjectName"] == ProjectToSkip):
            print('skipping skip project')
            continue
        elif (row["ProjectName"] != ProjectToSkip and oldprojectname == ProjectToSkip):
            print('skipped skip project, continuings')
            skipThisProject = False

        if (recovering_from_timeout):
            project_name = oldprojectname
            recovering_from_timeout = False
        else:
            project_name = row["ProjectName"]
            if oldprojectname == project_name:
                continue

        print('downloading bug reports of ' + project_name)
        try:
            repo = g.get_repo(project_name)
            issues_list = list(repo.get_issues(state='all'))
            if (len(issues_list) == 0):
                print('no issues for ' + project_name)
                oldprojectname = project_name
                continue
            for issue in issues_list:
                issuenumber = issue.number
                print(issuenumber)
                issuetitle = issue.title.strip().replace(';', ':')
                date_created = issue.created_at
                date_closed = issue.closed_at
                if date_closed is None:
                    date_closed = datetime.today()
                duration = abs((date_closed - date_created).days)
                output_file.write(
                    project_name + ";" + str(issuenumber) + ";" + issuetitle + ';' + str(date_created) + ';' + str(
                        date_closed) + ";" + str(int(duration)) + '\n')
                output_file.flush()
            print('bug reports of ' + project_name + ' downloaded')
            oldprojectname = project_name
        except Exception as e:
            try:
                print("Exception")
                print(e)
                # exit()
                if ("HTTPSConnectionPool") in str(e):
                    print("internet error")
                    continue
                elif ("404" in str(e)):
                    print(404)
                    skipThisProject = True
                    ProjectToSkip = project_name
                    continue
                elif ("502" in str(e)):
                    skipThisProject = True
                    ProjectToSkip = project_name
                    print(502)
                    continue
                if ('remaining=0' in str(g.get_rate_limit()) ) or ('403' in str(e)):
                    print(g.get_rate_limit())
                    ts = g.rate_limiting_resettime
                    dateutc = datetime.utcfromtimestamp(ts)
                    from_zone = tz.gettz('UTC')
                    to_zone = tz.gettz('America/New_York')
                    utc = dateutc.replace(tzinfo=from_zone)
                    central = utc.astimezone(to_zone)
                    t = datetime.now()
                    t = t.astimezone(to_zone)
                    seconds = min((central - t).seconds, 3600)
                    print('sleeping for ' + str(seconds) + ' seconds starting at' + str(t))
                    pause.seconds(seconds)
                else:
                    error_file.write(project_name + ';' + 'error:' + str(e) + '\n')
                    error_file.flush()
                    skipThisProject = True
                    ProjectToSkip = project_name
            except Exception as e1:
                error_file.write(project_name + ';' + str(e1) + '\n')
                error_file.flush()


# repo=Repo("F:\\PhD Work\\repos\\no-ai-ml\\amireh\\happypack\\")
# string_resp=repo.git.execute("git log --follow -- scripts\\loader-support-status\\index.js")
# L=[]
# for commit in string_resp.split("commit"):
#     arr= commit.split("\n")
#     # print(arr)
#     if len(arr)<3 :
#         continue
#     Date = arr[2]
#     date = datetime.strptime(Date, "Date: %a %b %d %H:%M:%S %Y %z")
#     date_string = date.strftime("%Y-%m-%d")
#     print(date_string)
#     L.append(date_string)
# L.reverse()
# generate_devopsfiles_creation_date(0)
# listOfTypes=["applied","tool","no-ai-ml"]
# generate_devopsfiles_creation_date(0)
# generate_devopsfiles_creation_date(1)
# generate_devopsfiles_creation_date(2)
# generate_projects_creation_date(1)
# generate_projects_creation_date(2)


# download_bug_reports(0)
# download_bug_reports(1)
download_bug_reports(2)
