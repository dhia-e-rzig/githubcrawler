import locale
import urllib.request
from pyquery import PyQuery

from git import Repo
from git import Remote
import pandas
import jsonpickle
import json
import os.path as path
import os
import shutil

import sys

from stripe.http_client import requests

import Github_Utils
from github import Github
g=Github(Github_Utils.get_github_token())

with open("../CSV Outputs/reposNotFound2.csv", 'w+',encoding='utf-8') as outfile:
    outfile.write("RepoName,Category,RepoURL\n")
    outfile.flush()


out_tool=open("../CSV Outputs/Tool_Descriptions.csv", 'a+',encoding='utf-8')
out_tool.write("ProjectRepo,Description,GithubPageLink,NbContributors,NbCommits\n")
out_tool.flush()


out_applied= open("../CSV Outputs/Applied_Descriptions.csv", 'a+',encoding='utf-8')
out_applied.write("ProjectRepo,Description,GithubPageLink,NbContributors,NbCommits\n")
out_applied.flush()


out_nonml=open("../CSV Outputs/Nonml_Descriptions.csv", 'a+',encoding='utf-8')
out_nonml.write("ProjectRepo,Description,GithubPageLink,NbContributors,NbCommits\n")
out_nonml.flush()


with open("../CSV Files/oldies/repo-metadata-sortedBySize.csv", "r", newline='') as repos_list:
    repos_dataframe = pandas.read_csv(repos_list, delimiter=',')
    repos_not_found1=pandas.read_csv("../CSV Outputs/reposNotFound.csv", delimiter=',')
    list_projects_not_found=repos_not_found1['RepoName']
    repos_dataframe = repos_dataframe[repos_dataframe['full_name'].isin(list_projects_not_found)]
    for index,row in repos_dataframe.iterrows():
        # df=repos_dataframe.loc[i,["Category","full_name"]]
        category=row["Category"]
        full_name=row["full_name"]
        # try :
        #     a = urllib.request.urlopen("https://github.com/"+full_name)
        # except:
        #     with open("../CSV Outputs/reposNotFound.csv", 'a+') as outfile:
        #         outfile.write(full_name+",https://github.com/"+df["full_name"]+"\n")
        #         outfile.flush()
        #     continue
        finished= False
        while(not finished):
            try:
                print(full_name)
                gh_repo = g.get_repo(full_name)
                name=full_name
                description=gh_repo.description
                if description is None:
                    description = "Description was not given"
                url=gh_repo.git_url.replace('.git','').replace('git:','https:')
                commmits=gh_repo.get_commits()
                nb_commits=commmits.totalCount
                stra="https://github.com/" + full_name+'/issues/show_menu_content?partial=issues/filters/authors_content'
                html = requests.get("https://github.com/" + full_name+'/issues/show_menu_content?partial=issues/filters/authors_content')
                e = PyQuery(html.content)
                nb_committers=int(len(e.text().split('\n')))
                finished = True
            except Exception as e:
                if Github_Utils.is_over_core_rate(g):
                    Github_Utils.sleep_until_core_rate_reset(g)
                else:
                    with open("../CSV Outputs/reposNotFound2.csv", 'a+') as outfile:
                        outfile.write(full_name+','+category+",https://github.com/"+full_name+"\n")
                        print(full_name+','+category+",https://github.com/"+full_name+"\n")
                        outfile.flush()
                    break
        # if not finished:
        #     continue
        # outfile.write("ProjectRepo,Description,GithubPageLink,NbContributors,NbCommits\n")
        # if(category=="Tool"):
        #     out_tool.write(full_name+','+description+','+url+','+str(nb_committers)+','+str(nb_commits)+'\n')
        #     print(full_name+','+description+','+url+','+str(nb_committers)+','+str(nb_commits)+'\n')
        #
        # elif (category == "Applied"):
        #     out_applied.write(full_name + ',' + description + ',' + url + ',' + str(nb_committers) + ',' + str(nb_commits) + '\n')
        #     print(full_name + ',' + description + ',' + url + ',' + str(nb_committers) + ',' + str(nb_commits) + '\n')
        #
        # else:
        #     out_nonml.write(str(full_name) + ',' + str(description) + ',' + str(url) + ',' + str(nb_committers) + ',' + str(nb_commits) + '\n')
        #     print(str(full_name) + ',' + str(description) + ',' + str(url) + ',' + str(nb_committers) + ',' + str(nb_commits) + '\n')
        #
