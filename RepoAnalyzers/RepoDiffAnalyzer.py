import io

from time import sleep
import re
import datetime

from pydriller import RepositoryMining, ModificationType

from git import Repo
from git import Git
import pandas
import os
import jsonpickle
import json
import os.path as path
import os
import shutil
# import stat
from dateutil import parser as parser
# from numpy import mean

listOfTypes=["applied","tool","no-ai-ml"]
i= 0

# analyze nb line diff

def generate_devopsfiles_avg_nblines_diff_between_commits(i):
    with open("../JSON Files/lastAnalysisForType" + str(i) + ".json", 'r+') as outfile:
        last_buildfiles_fs_analysis = json.load(outfile)
    type=listOfTypes[i]
    x = datetime.now()
    time = x.strftime("%x-%X").replace(":", "-").replace("/", "-")
    output_file = open("../CSV Files/devopsfiles-nbline-diffs-" + time + "-" + type + ".csv", "w+", encoding="utf-8")
    output_file.write("ProjectName;NBlinediffv1;NBlinediffv2\n")
    error_file = open("../CSV Files/devopsfiles-nbline-diffs-errors-" + time + "-" + type + ".csv", "w+", encoding="utf-8")
    error_file.write("ProjectName;FileNameWithRelativePath;Exception\n")
    buildfiles_infs_file=open(last_buildfiles_fs_analysis, "rb")
    decoder_wrapper = io.TextIOWrapper(buildfiles_infs_file, encoding='utf-8', errors='ignore')
    devops_fromfs_df=pandas.read_csv(decoder_wrapper,sep=";",error_bad_lines=False,usecols=["ProjectName","FilePath","DevopsType","DevopsTool","Notes"])
    diff_list = []
    diff_list2 = []
    commit_set = set()
    old_projectname="empty_project"
    for index,row in devops_fromfs_df.iterrows():
        project_name=row["ProjectName"]
        if(old_projectname=="empty_project"):
            old_projectname=project_name
        elif(old_projectname!=project_name):
            if(len(commit_set)>0):
                avg = sum(diff_list) / (len(commit_set))
                avg2 = sum(diff_list2) / (len(commit_set))

            else:
                avg= 0
                avg2 = 0
            avg_rnd = round(avg, 5)
            avg_rnd2 = round(avg2, 5)

            output_file.write(project_name  + ";" + str(avg_rnd) + ";" + str(avg_rnd2) + "\n")
            diff_list.clear()
            diff_list2.clear()
            commit_set.clear()
            old_projectname=project_name
        full_path=row["FilePath"]
        x = project_name.split("/")
        file_with_path = full_path.split(project_name.replace("/","\\"))[1]
        file_with_path=file_with_path[1:]
        repo_path=full_path.split(project_name.replace("/","\\"))[0]+project_name
        repo=Repo(repo_path)

        try:
            string_resp=repo.git.execute("git log --follow --  \""+file_with_path+"\"")
            # dates_list = []
            # comments_list=[]
            commit_ids_list=[]
            for commit in string_resp.split("commit"):
                arr = commit.split("\n")
                # print(arr)
                if len(arr) < 1:
                    continue
                if(arr[0]==""):
                    continue
                commit_ids_list.append(arr[0])
            # diff = repo.git.execute("git diff " + commit_ids_list[0] + " " +  commit_ids_list[1] + " -- " + "" + file_with_path + "")
            # diff_length = len(diff)

            for i in range(0,len(commit_ids_list)-1,1):
                commit1=commit_ids_list[i]
                commit2=commit_ids_list[i+1]
                try:
                    diff=repo.git.execute("git diff --diff-algorithm=myers --ignore-all-space  --numstat "+commit1+" "+commit2+" -- " +file_with_path+"")
                    diff_arr=re.split(r'\t+',diff)
                    diff_length = int(diff_arr[0])+int(diff_arr[1])
                    diff_length2 = abs(int(diff_arr[0])-int(diff_arr[1]))
                    diff_list.append(diff_length)
                    diff_list2.append(diff_length2)
                    commit_set.add(commit1)
                    commit_set.add(commit2)
                except:
                    continue
            # avg=sum(diff_list)/(len(commit_set))
            # avg2=sum(diff_list2)/(len(diff_list2))
            # avg_rnd= round(avg,5)
            # avg_rnd2= round(avg2,5)
            # output_file.write(project_name + ";" + full_path + ";" + str(avg_rnd)+";"+str(avg_rnd2) + "\n")
            # output_file.flush()
            print(file_with_path+";"+project_name)
        except Exception as e:
            try:
                error_file.write(project_name + ";"+ file_with_path+";"+ str(e)+"\n")
                print("exception")
            except Exception  as e1:
                   print("can't record exception :" + e)
                   print("\n because of :" + e1)
    #output for last project
    if(len(commit_set)>0):
        avg = sum(diff_list) / (len(commit_set))
        avg2 = sum(diff_list2) / (len(commit_set))
    else:
        avg=0
        avg2=0
    avg_rnd = round(avg, 5)
    avg_rnd2 = round(avg2, 5)
    output_file.write(old_projectname + ";" + str(avg_rnd) + ";" + str(avg_rnd2) + "\n")

#analuze commit ratio to overall commit ratio


def generate_commit_ratio_of_devops_files(i):
    with open("../JSON Files/lastAnalysisForType" + str(i) + ".json", 'r+') as outfile:
        last_buildfiles_fs_analysis = json.load(outfile)
    type=listOfTypes[i]
    x = datetime.datetime.now()
    # counter=0
    time = x.strftime("%x-%X").replace(":", "-").replace("/", "-")
    output_file = open("../CSV Files/devopsfiles-commit-ratios-" + time + "-" + type + ".csv", "w+", encoding="utf-8")
    output_file.write("ProjectName;CommitRatio\n")
    error_file = open("../CSV Files/devopsfiles-commit-ratios-errors-" + time + "-" + type + ".csv", "w+", encoding="utf-8")
    error_file.write("ProjectName;FileNameWithRelativePath;Exception\n")
    buildfiles_infs_file=open(last_buildfiles_fs_analysis, "rb")
    decoder_wrapper = io.TextIOWrapper(buildfiles_infs_file, encoding='utf-8', errors='ignore')
    devops_fromfs_df=pandas.read_csv(decoder_wrapper,sep=";",error_bad_lines=False,usecols=["ProjectName","FilePath","DevopsType","DevopsTool","Notes"])
    old_projectname = "empty_project"
    devops_commits=set()
    nbtotalcommits="Unk"
    update_nbtotal=True
    reached=False
    for index,row in devops_fromfs_df.iterrows():
        # if counter > 7:
        #     exit()
        project_name=row["ProjectName"]
        full_path=row["FilePath"]
        if project_name =='RTradeLtd/Lens':
            reached=True
        if not reached:
            continue
        if(old_projectname=="empty_project"):
            old_projectname=project_name
        elif(old_projectname!=project_name):
            if(nbtotalcommits>0):

                ratio = len(devops_commits) / nbtotalcommits
                print(len(devops_commits))
                print(nbtotalcommits)
                print(ratio)
            else:
                ratio=0
            ratio_str = "{:1.5f}".format(ratio)
            output_file.write(old_projectname  + ";" + ratio_str + " \n")
            old_projectname=project_name
            update_nbtotal=True
            devops_commits.clear()
            # counter +=1
        x = project_name.split("/")
        file_with_path = full_path.split(project_name.replace("/","\\"))[1]
        file_with_path=file_with_path[1:]
        repo_path=full_path.split(project_name.replace("/","\\"))[0]+project_name
        try:
            repo = Repo(repo_path)
            string_resp=repo.git.execute("git rev-list  HEAD  \""+file_with_path+"\"")
            commits=string_resp.split("\n")
            devops_commits.update(commits)
            dates_list = []
            comments_list=[]
            if(nbtotalcommits=="Unk" or update_nbtotal==True):
                nbtotalcommits=int(repo.git.execute("git rev-list HEAD --count"))
                update_nbtotal=False
            # output_file.flush()
            print(repo_path)
        except Exception as e:
            try:
                error_file.write(project_name + ";"+ file_with_path+";"+ str(e)+"\n")
            except Exception  as e1:
                print("can't record exception :"+e)
                print("\n because of :"+e1)
    #output for last project`
    if(nbtotalcommits>0):
        ratio = len(devops_commits) / nbtotalcommits
    else:
        ratio=0
    ratio_str = "{:1.5f}".format(ratio)
    output_file.write(old_projectname + ";" + ratio_str + " \n")


def process_project_commits(projectname,repo_path,devops_files_paths,outfile,outfile2,errfile):
    try:
        trav_forward = RepositoryMining(repo_path).traverse_commits()
        start_commit = next(trav_forward)
        start_date = start_commit.committer_date
        # initial_number_of_all_files = commits[0].files
        # initial_number_of_devops_files = len([element for idx, element in enumerate(commits[0].modifications) if
        #                                       isDevOpsModification(element,devops_files_paths)])
        # initial_number_of_source_files = initial_number_of_all_files - initial_number_of_devops_files
        trav_backward = RepositoryMining(repo_path, order='reverse').traverse_commits()
        end_commit = next(trav_backward)
        end_date = end_commit.committer_date
        curr_date = start_date
        curr_date -= datetime.timedelta(days=1)
        periodnumber=0
        totalperiodnumber=((end_date-start_date).days // 30)+1
        monthly_nb_devops_commits = []
        monthly_nb_source_commits = []
        monthly_nb_both_commits = []
        monthly_nb_all_commits = []
        monthly_nb_merge_commits = []
        monthly_nb_nonmerge_commits = []
        print(projectname + " is processing commit frequency ")
        while curr_date < end_date:
            periodnumber+=1
            normali_period_number = periodnumber / totalperiodnumber
            formatted_normali_period_number = "{:.3f}".format(normali_period_number)
            print(str(periodnumber)+"out of "+str(totalperiodnumber))
            curr_date_end = min(curr_date +datetime.timedelta(days=30) , end_date)
            commits_in_period = RepositoryMining(repo_path, since=curr_date, to=curr_date_end).traverse_commits()
            devops_commits=[]
            source_commits=[]
            both_commits=[]
            all_commits=[]
            merge_commits=[]
            nonmerge_commits=[]
            i = 1
            for commit in commits_in_period:
                print('commit nb ' + str(i) + ' in period processing')
                i += 1
                if (i >= 100000):
                    errfile.write(projectname + ';' + ' too many comments in one period')
                    break
                all_modifications = commit.modifications
                devops_modifications = [element for idx, element in enumerate(all_modifications) if
                                        isDevOpsModification(element, devops_files_paths)]
                source_modifications = [item for item in all_modifications if item not in devops_modifications]
                all_commits.append(commit)
                if(len(devops_modifications)>0 and len(source_modifications)>0) :
                    both_commits.append(commit)
                elif (len(devops_modifications)>0):
                    devops_commits.append(commit)
                elif(len(source_modifications)>0):
                    source_commits.append(commit)
                if(commit.merge):
                    merge_commits.append(commit)
                else:
                    nonmerge_commits.append(commit)
            monthly_nb_devops_commits.append(len(devops_commits))
            devops_commits.clear()
            monthly_nb_source_commits.append(len(source_commits))
            source_commits.clear()
            monthly_nb_both_commits.append(len(both_commits))
            both_commits.clear()
            outfile.write(projectname+';'+str(len(merge_commits))+';'+str(len(nonmerge_commits))+';'+str(len(all_commits))+';'+str(curr_date)+';'+str(curr_date_end)+';'+str(periodnumber)+';'+formatted_normali_period_number+'\n')
            outfile.flush()
            monthly_nb_all_commits.append(len(all_commits))
            all_commits.clear()
            monthly_nb_merge_commits.append(len(merge_commits))
            merge_commits.clear()
            monthly_nb_nonmerge_commits.append(len(nonmerge_commits))
            nonmerge_commits.clear()
            curr_date += datetime.timedelta(days=30)
        formatted_source_rate= "{:.2f}".format(sum(monthly_nb_source_commits)/totalperiodnumber)
        formatted_devops_rate= "{:.2f}".format(sum(monthly_nb_devops_commits)/totalperiodnumber)
        formatted_both_rate= "{:.2f}".format(sum(monthly_nb_both_commits)/totalperiodnumber)
        formatted_all_rate= "{:.2f}".format(sum(monthly_nb_all_commits)/totalperiodnumber)
        formatted_merge_rate= "{:.2f}".format(sum(monthly_nb_merge_commits)/totalperiodnumber)
        formatted_nonmerge_rate= "{:.2f}".format(sum(monthly_nb_nonmerge_commits)/totalperiodnumber)
        # output_file.write("ProjectName;SourceCodeChurn;DevOpsCodeChurn;DateBeginning;DateEnding;PeriodNumber;NormalizedPeriodNumber\n")
        outfile2.write(projectname+";"+formatted_source_rate+";"+formatted_devops_rate+";"+formatted_both_rate+";"+formatted_merge_rate+";"+formatted_nonmerge_rate+";"+formatted_all_rate+'\n')
        outfile2.flush()
        print(projectname+"is commit frequency and commit merge processed")
    except Exception as e:
        errfile.write(projectname+';'+str(e)+'\n')
        print(e)
        errfile.flush()

def generate_commit_frequency(i):
    with open("../JSON Files/lastAnalysisForType" + str(i) + ".json", 'r+') as outfile:
        last_buildfiles_fs_analysis = json.load(outfile)
    type=listOfTypes[i]
    x = datetime.datetime.now()
    time = x.strftime("%x-%X").replace(":", "-").replace("/", "-")
    output_file = open("../CSV Files/devopsfiles-commitfrequncy-" + time + "-" + type + ".csv", "w+", encoding="utf-8")
    output_file.write("ProjectName;MonthlySourceCommitAvg;MonthlyDevOpsCommitAvg;MonthlyBothCommitAvg;MonthlyMergingCommitsAvg;MonthlyNonMergingCommitsAvg;MonthlyAllCommitAvg\n")
    output_file2 = open("../CSV Files/devopsfiles-mergingcommits-" + time + "-" + type + ".csv", "w+", encoding="utf-8")
    output_file2.write(
        "ProjectName;NbMergingCommits;NbNonMergingCommits;NbAllMergingCommits;StartDate;EndDate;PeriodNb;NormalPeriod\n")

    error_file = open("../CSV Files/devopsfiles-mergingcommits-errors-" + time + "-" + type + ".csv", "w+", encoding="utf-8")
    error_file.write("ProjectName;Error\n")
    buildfiles_infs_file=open(last_buildfiles_fs_analysis, "rb")
    decoder_wrapper = io.TextIOWrapper(buildfiles_infs_file, encoding='utf-8', errors='ignore')
    devops_fromfs_df=pandas.read_csv(decoder_wrapper,sep=";",error_bad_lines=False,usecols=["ProjectName","FilePath","DevopsType","DevopsTool","Notes"])
    old_projectname="empty_project"
    devops_files_paths=[]
    repo_path=""
    project_name=""
    for index,row in devops_fromfs_df.iterrows():
        project_name=row["ProjectName"]
        if(old_projectname=="empty_project"):
            old_projectname=project_name
        elif(old_projectname!=project_name):
            process_project_commits(old_projectname,repo_path,devops_files_paths,output_file,output_file2,error_file)
            old_projectname=project_name
            devops_files_paths.clear()
            # quit()
        full_path=row["FilePath"]
        file_with_path = full_path.split(project_name.replace("/","\\"))[1]
        file_with_realtive_path=file_with_path[1:]
        devops_files_paths.append(file_with_realtive_path)
        repo_path=full_path.split(project_name.replace("/","\\"))[0]+project_name
    process_project_commits(project_name, repo_path, devops_files_paths, output_file,output_file2,error_file)




#using normalized churn. First, we count the number of
# source files and the number of build files that were changed
# in each month-long development period.
# Then, we divide  each count by the total number of source files or the total
# number of build files that existed in that period. We repeat
# this process for each month


def inbetween(x,a,b):
    return x.committer_date > a and x.committer_date < b

def isDevOpsModification(mod,devops_files_paths):
    return either_path(mod) in devops_files_paths

def either_path(modification):
    oldpath=modification.old_path
    newpath=modification.new_path
    if(oldpath is None):
        return newpath
    else:
        return oldpath




def process_project(projectname,repo_path,devops_files_paths,outfile,errfile):
    # try:
    trav_forward=RepositoryMining(repo_path).traverse_commits()
    start_commit=next(trav_forward)
    start_date =start_commit.committer_date
    # initial_number_of_all_files = commits[0].files
    # initial_number_of_devops_files = len([element for idx, element in enumerate(commits[0].modifications) if
    #                                       isDevOpsModification(element,devops_files_paths)])
    # initial_number_of_source_files = initial_number_of_all_files - initial_number_of_devops_files
    trav_backward = RepositoryMining(repo_path,order='reverse').traverse_commits()
    end_commit = next(trav_backward)
    end_date = end_commit.committer_date
    curr_date = start_date
    curr_date -= datetime.timedelta(days=1)
    curr_source_files_set = set()
    curr_devops_files_set=set()
    devops_files_modified_set = set()
    source_files_modified_set = set()
    periodnumber=0
    totalperiodnumber=((end_date-start_date).days // 30)+1
    source_deletions_files=[]
    devops_deletions_files=[]
    print(projectname + " is processing")
    print(datetime.datetime.now())
    while curr_date < end_date:
        periodnumber+=1
        print(str(periodnumber) + "out of " + str(totalperiodnumber))
        print(datetime.datetime.now())
        curr_date_end = min(curr_date +datetime.timedelta(days=30) , end_date)
        commits_in_period = RepositoryMining(repo_path,since=curr_date,to=curr_date_end).traverse_commits()
        i=1
        for commit in commits_in_period:
            print('commit nb '+str(i)+' in period processing')
            i+=1
            if (i>=100000):
                errfile.write(projectname+';'+' too many comments in one period')
                break
            all_modifications = commit.modifications
            all_additions = [element for idx, element in enumerate(all_modifications) if
                             element.change_type.value == ModificationType.ADD.value]
            all_deletions = [element for idx, element in enumerate(all_modifications) if
                             element.change_type.value == ModificationType.DELETE.value]

            devops_additions = [element for idx, element in enumerate(all_additions) if isDevOpsModification(element,devops_files_paths)]
            devops_deletions = [element for idx, element in enumerate(all_deletions) if
                                isDevOpsModification(element, devops_files_paths)]

            source_additions = [element for idx, element in enumerate(all_additions) if element not in devops_additions]
            source_deletions = [element for idx, element in enumerate(all_deletions) if element not in devops_deletions]

            devops_additions_files = [either_path(mod) for idx, mod in enumerate(devops_additions)]
            curr_devops_files_set.update(devops_additions_files)
            devops_deletions_files.extend([either_path(mod) for idx, mod in enumerate(devops_deletions)])

            source_additions_files = [either_path(mod) for idx, mod in enumerate(source_additions)]
            curr_source_files_set.update(source_additions_files)
            source_deletions_files.extend([either_path(mod) for idx, mod in enumerate(source_deletions)])

            all_other_modifications=[element for idx, element in enumerate(all_modifications) if element not in all_additions and element not in all_deletions and element.change_type.value!=ModificationType.RENAME.value]

            devops_modifications = [element for idx, element in enumerate(all_other_modifications) if
                                    isDevOpsModification(element, devops_files_paths)]

            source_modifications = [item for item in all_other_modifications if item not in devops_modifications]

            devops_modifications_files = [either_path(mod) for idx, mod in enumerate(devops_modifications)]
            devops_files_modified_set.update(devops_modifications_files)
            source_modifications_files=[either_path(mod) for idx, mod in enumerate(source_modifications)]
            source_files_modified_set.update(source_modifications_files)
        try:
            source_ratio=len(source_files_modified_set)/len(curr_source_files_set)
            source_files_modified_set.clear()
        except:
            source_ratio=0
        try:
            devops_ratio=len(devops_files_modified_set)/len(curr_devops_files_set)
            devops_files_modified_set.clear()
        except:
            devops_ratio=0
        if(source_ratio > 1):
            source_ratio=1
        if (devops_ratio > 1):
            devops_ratio = 1
        curr_source_files_set.difference_update(source_deletions_files)
        source_deletions_files.clear()
        curr_devops_files_set.difference_update(devops_deletions_files)
        devops_deletions_files.clear()
        formatted_source_ratio= "{:.2f}".format(source_ratio)
        formatted_devops_ratio= "{:.2f}".format(devops_ratio)
        # output_file.write("ProjectName;SourceCodeChurn;DevOpsCodeChurn;DateBeginning;DateEnding;PeriodNumber;NormalizedPeriodNumber\n")
        normali_period_number=periodnumber/totalperiodnumber
        formatted_normali_period_number = "{:.3f}".format(normali_period_number)
        outfile.write(projectname+";"+formatted_source_ratio+";"+formatted_devops_ratio+";"+str(curr_date)+";"+str(curr_date_end)+";"+str(periodnumber)+";"+formatted_normali_period_number+'\n')
        curr_date+=datetime.timedelta(days=30)
        outfile.flush()
    print(projectname+" is processed")
    print(datetime.datetime.now())




    #
    # except Exception as e:
    #     raise(e)



def generate_codechurn_metrics(i):
    with open("../JSON Files/lastAnalysisForType" + str(i) + ".json", 'r+') as outfile:
        last_buildfiles_fs_analysis = json.load(outfile)
        print(last_buildfiles_fs_analysis)
    type=listOfTypes[i]
    x = datetime.datetime.now()
    time = x.strftime("%x-%X").replace(":", "-").replace("/", "-")
    output_file = open("../CSV Files/devopsfiles-churn-" + time + "-" + type + ".csv", "w+", encoding="utf-8")
    output_file.write("ProjectName;SourceCodeChurn;DevOpsCodeChurn;DateBeginning;DateEnding;PeriodNumber;NormalizedPeriodNumber\n")
    error_file = open("../CSV Files/devopsfiles-churn-errors-" + time + "-" + type + ".csv", "w+", encoding="utf-8")
    error_file.write("ProjectName;Error\n")
    buildfiles_infs_file=open(last_buildfiles_fs_analysis, "rb")
    decoder_wrapper = io.TextIOWrapper(buildfiles_infs_file, encoding='utf-8', errors='ignore')
    devops_fromfs_df=pandas.read_csv(decoder_wrapper,sep=";",error_bad_lines=False,usecols=["ProjectName","FilePath","DevopsType","DevopsTool","Notes"])
    old_projectname="empty_project"
    devops_files_paths=[]
    repo_path=""
    project_name=""
    unreached=False
    for index,row in devops_fromfs_df.iterrows():
        project_name=row["ProjectName"]
        if(project_name!="" and unreached):#continue project name here
                continue
        else:
            unreached=False
        if(old_projectname=="empty_project"):
            old_projectname=project_name
        elif(old_projectname!=project_name):
            try:
                process_project(old_projectname,repo_path,devops_files_paths,output_file,error_file)
            except Exception as e:
                error_file.write(project_name+';'+str(e))
            old_projectname=project_name
            devops_files_paths.clear()
            # quit()
        full_path=row["FilePath"]
        file_with_path = full_path.split(project_name.replace("/","\\"))[1]
        file_with_realtive_path=file_with_path[1:]
        devops_files_paths.append(file_with_realtive_path)
        repo_path=full_path.split(project_name.replace("/","\\"))[0]+project_name
    try:
        process_project(project_name, repo_path, devops_files_paths, output_file,error_file)
    except Exception as e:
        error_file.write(project_name + ';' + str(e))


# generate_codechurn_metrics(0)
# generate_codechurn_metrics(1)
# generate_codechurn_metrics(2)





# generate_commit_frequency(0)
generate_commit_frequency(1)
generate_commit_frequency(2)
