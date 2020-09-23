from git import Repo
import pandas
import os
import jsonpickle
import json
import os.path as path
import os
import shutil
import stat

progress= 0
HDD= "L:"

repos_dir=HDD+"\\PhD Work\\repos\\"

with open("analyzingAIMLprogress.json",'r+') as outfile:
    progress=json.load(outfile)
    print(progress)






