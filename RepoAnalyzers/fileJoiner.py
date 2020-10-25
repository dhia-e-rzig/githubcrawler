import os

import pandas

# projectIDs_dataframe = 0
# files_list1_dataframe=0
# files_list2_dataframe=0


with open("../Excel Files/AIML.xlsx", "rb") as files_list:
    projectIDs_dataframe = pandas.read_excel(files_list)


with open("../CSV Files/oldies/repos-ai-applied-all.csv", "rb") as files_list:
    files_list1_dataframe = pandas.read_csv(files_list,error_bad_lines=False, lineterminator='\n')

with open("../CSV Files/oldies/repos-ai-tool-all.csv", "rb") as files_list:
    files_list2_dataframe = pandas.read_csv(files_list,error_bad_lines=False, lineterminator='\n')

files_list=[files_list1_dataframe,files_list2_dataframe]



# files_list["Name"] = files_list["Name"].replace("PhD Work\repos",files_list["Path"].split("\\")[-2]+"\\"+files_list["Path"].split("\\")[-1])

df1=pandas.concat(files_list, ignore_index=False, keys=None, copy=True)
df1["Extensions"] = df1["FileName"].apply(lambda x : str(x).split('.')[-1] )

#TODO Fix bugs in joining

for index, row in df1.iterrows():
    if row["Name"] == "PhD Work\repos":
        row["Name"]= row["Path"].split("\\")[-2]+"/"+row["Path"].split("\\")[-1]

df1.to_csv(r'a.csv',index=False)

# df = pandas.merge(projectIDs_dataframe,df1,on="Name",how="inner")

# df.to_csv(r'AIML-Merged.csv',index=False)