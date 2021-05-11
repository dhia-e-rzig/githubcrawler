import os

import pandas

# projectIDs_dataframe = 0
# files_list1_dataframe=0
# files_list2_dataframe=0

#
# with open("../Excel Files/AIML.xlsx", "rb") as files_list:
#     projectIDs_dataframe = pandas.read_excel(files_list)


with open("allfiles-avg-nbreviewcounts-no-ai-ml3.csv", "rb") as files_list:
    allfiles_DF = pandas.read_csv(files_list, error_bad_lines=False, lineterminator='\n')

with open("devopsfiles-avg-nbreviewcounts-no-ai-ml3.csv", "rb") as files_list:
    DevOps_DF = pandas.read_csv(files_list, error_bad_lines=False, lineterminator='\n')

allfiles_DF.columns =allfiles_DF.columns.str.strip().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
DevOps_DF.columns =DevOps_DF.columns.str.strip().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
print(allfiles_DF.columns)
print(DevOps_DF.columns)

# projectAndTestToolsDF.drop(['TestTool'],axis=1,inplace=True)
# projectAndTestToolsDF.drop_duplicates(inplace=True)
# projectAndTestToolsDF['Test']='YES'


# print(projectAndTestToolsDF.columns)

DevOps_DF['ProjectName']=DevOps_DF['ProjectName'].str.strip().replace('"', "")
allfiles_DF['ProjectName']=allfiles_DF['ProjectName'].str.strip().replace('"', "")

allfiles_DF.rename(columns={'Avg_NBReviewCount':'All-avg'},inplace=True)
DevOps_DF.rename(columns={'Avg_NBReviewCount':'DevOps-avg'},inplace=True)

# # files_list["Name"] = files_list["Name"].replace("PhD Work\repos",files_list["Path"].split("\\")[-2]+"\\"+files_list["Path"].split("\\")[-1])
#
# df1=pandas.concat(files_list, ignore_index=False, keys=None, copy=True)
# df1["Extensions"] = df1["FileName"].apply(lambda x : str(x).split('.')[-1] )
#
# #TODO Fix bugs in joining
#
# for index, row in df1.iterrows():
#     if row["Name"] == "PhD Work\repos":
#         row["Name"]= row["Path"].split("\\")[-2]+"/"+row["Path"].split("\\")[-1]
#
# df1.to_csv(r'a.csv',index=False)

df = pandas.merge(DevOps_DF, allfiles_DF, on="ProjectName", how="outer")
df.fillna(0,inplace=True)

df['Normalized-avg']=df['DevOps-avg']/df['All-avg']

df.fillna(0,inplace=True)

# df.loc[df['Test'] == 'FALSE', 'Test'] = 0

df.to_csv(r'NOAIML_Normal_PRComms.csv',index=False)
