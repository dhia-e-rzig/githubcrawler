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


# print(list_of_subtopics)

with open("../JSON Files/list_of_all_subtopics.json", 'r') as infile:
    list_of_subtopics=json.load(infile)



with open("../CSV Files/reposT1.csv", "a+", newline='') as f:
    csvwriter =  csv.writer(f, delimiter=',',  quotechar='|')
    for topic in list_of_subtopics:
        v= g.search_repositories(query="topic:"+topic)
        for repo in v :
            tup=(repo.name,repo.id,repo.git_url)
            print(tup)
            repo_tuples.append(tup)
            csvwriter.writerow(tup)
            f.flush()
        time.sleep(60)


