import requests
import json
import pandas as pd
import time
import json

from json import JSONEncoder
import jsonpickle
from github import Github
g = Github("dhia-e-rzig","SwellingGit96!")
print(g.get_rate_limit().search)

name="unnamed"
# list={"ArtificialIntelligence","MachineLearning","DeepLearning"} ; name = "list_of_subtopics1.json"
# list={"Artificial Intelligence","Machine Learning","Deep Learning"} ; name = "list_of_subtopics2.json"
# list={"Artificial-Intelligence","Machine-Learning","Deep-Learning"} ; name = "list_of_subtopics3.json"
# list={"DL"} ; name = "list_of_subtopics4.json"
# list={"AI"} ; name = "list_of_subtopics5.json"
# list={"ML"} ; name = "list_of_subtopics6.json"

list_of_subtopics = set()

for el in list:
    topics= g.search_topics(el)
    print(g.get_rate_limit().search)
    for topic in topics:
        list_of_subtopics.add(topic.name)

    time.sleep(75)




subTopicsJSON= jsonpickle.encode(list_of_subtopics,unpicklable=False)

subString= json.dumps(subTopicsJSON, indent=4)
print(subString)


with open(name,'a+') as outfile:
    outfile.write(subTopicsJSON)

