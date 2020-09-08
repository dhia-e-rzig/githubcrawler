import requests
import json
import pandas as pd
import time
import pickle as pickle
import csv

from github import Github
g = Github("dhia-e-rzig","SwellingGit96!")
print(g.get_rate_limit())


list_of_subtopics = set()
repo_tuples=[]

infile = open("list_of_subtopics.pkl",'rb')
# print(list_of_subtopics)

list_of_subtopics = pickle.load(infile)
infile.close()
with open("repos.csv","a+",newline='') as f:
    csvwriter =  csv.writer(f, delimiter=',',  quotechar='|')
    for topic in list_of_subtopics:
        v= g.search_repositories(query="topic:"+topic)
        for repo in v :
            tup=(repo.name,repo.id,repo.url)
            print(tup)
            repo_tuples.append(tup)
            csvwriter.writerow(tup)
            f.flush()
        time.sleep(10) #avoid surpassing the search request limit of github

