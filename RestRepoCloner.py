from git import Repo
import csv
import os


with open("reposT1.csv","r",newline='') as repos_list:
    csv_reader = csv.reader(repos_list, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if(line_count>5):
            break
        print(row)
        # "git@github.com:"+
        Repo.clone_from(row[2], "repos\\"+ row[0], branch='master')
        line_count += 1
