import requests
import json
import pandas as pd
import time
import pickle as pickle

from github import Github
g = Github("dhia-e-rzig","SwellingGit96!")
print(g.get_rate_limit())

list={"Artificial Intelligence","Machine Learning"}

list_of_subtopics = set()

for el in list:
    topics= g.search_topics(el)
    for topic in topics:
        list_of_subtopics.add(topic.name)

outfile = open("list_of_subtopics.pkl",'wb')

pickle.dump(list_of_subtopics,outfile)
outfile.close()
