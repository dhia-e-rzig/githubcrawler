import requests
import json
import pandas as pd
import time
import json

from json import JSONEncoder
import jsonpickle

list_of_subtopics = set()

List_of_names={"list_of_subtopics1.json","list_of_subtopics2.json","list_of_subtopics3.json","list_of_subtopics4.json", "list_of_subtopics6.json"}

for name in List_of_names:
    with open(name,'r') as infile:
        subtopicsubSet=json.load(infile)
        for subtopic in subtopicsubSet:
            list_of_subtopics.add(subtopic)

print(len(list_of_subtopics))
subTopicsJSON= jsonpickle.encode(list_of_subtopics,unpicklable=False)


with open("../JSON Files/list_of_all_subtopics.json", 'w+') as outfile:
    outfile.write(subTopicsJSON)
