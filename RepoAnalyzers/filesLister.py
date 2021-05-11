import os
import pandas



def list_projects_files_with_filter(DirectoriesOfProjects, NameOfOutput, FilteringListPath):

    # output_files_list = open("repos-noai-all2.csv", "a+", newline='',encoding="utf-8")
    output_files_list = open("../CSV Files/"+str(NameOfOutput)+".csv", "w+", newline='', encoding="utf-8")
    # aiextra_liest=["atomistic-machine-learning/schnetpack","algorithmfoundry/Foundry","lim-anggun/FgSegNet","crouchred/speaker-recognition-py3","xiaoshuaishuai319/weixinxiaochengxu","Waikato/wekaDeeplearning4j","SMTorg/smt","Steven-Hewitt/Entailment-with-Tensorflow"] #"jupyterhub/helm-chart","iArunava/Python-TheNoTheoryGuide","AICommunityInno/Seminars","foo123/FILTER.js","kakao/n2","synyi/poplar","kermitt2/delft","Tiramisu-Compiler/tiramisu","sniklaus/pytorch-pwc","lixinsu/RCZoo","chovanecm/sacredboard","aliakbar09a/AI_plays_snake"
    output_files_list.write("ProjectName,FilePath,FileName,Extension,ProjectSizeKB\n")
    output_files_list.flush()

    with open(FilteringListPath, "rb") as projects_list:
        if(str(FilteringListPath).endswith(".xls") or str(FilteringListPath).endswith(".xlsx")):
            projectIDs_dataframe = pandas.read_excel(projects_list)
        elif str(FilteringListPath).endswith(".csv"):
            projectIDs_dataframe = pandas.read_csv(projects_list)
        else:
            raise Exception(FilteringListPath)

    topprojects = projectIDs_dataframe["Name"].tolist()
    # print(topprojects)


    # i =999 #NOAIML
    oldprojectname=""
    if type(DirectoriesOfProjects) is not list:
        DirectoriesOfProjects=[DirectoriesOfProjects]
    for path in DirectoriesOfProjects:
        orr=str(path).split("\\")
        repos_index=orr.index("repos")
        for root, dirs, files in os.walk(path):
            for file in files:
                name = os.path.join(root, file)
                file_size = os.path.getsize(name)
                arr = name.split("\\")
                projectname = str(arr[repos_index+2]) + '/'+ str(arr[repos_index+3])
                file_size_kb = file_size / 1024
                format_file_size_kb = "{:.2f}".format(file_size_kb)
                if projectname not in  topprojects:
                    continue
                # if(oldprojectname != projectname):
                #     i+=1
                #     oldprojectname=projectname
                # if (i >= 2000):
                #     break
                filename = arr[-1]
                ext=filename.split('.')[-1] #str(i)+','+
                exts = ['ru',
                        'rb']  # 'c','cpp','c++','cc','h','hpp','hh','h','cs','java','r','rd','.profile','py','pyi','pyw','pyx','pxd',
                if (ext.lower() in exts and ("test" in name.lower() or "spec" in name.lower())):
                    output_files_list.write(
                        projectname + ',' + name + ',' + filename + ',' + ext + ',' + format_file_size_kb  + '\n')
                    output_files_list.flush()

    output_files_list.close()
    return "../CSV Files/"+str(NameOfOutput)+".csv"

def list_projects_files(DirectoriesOfProjects, NameOfOutput):


    output_files_list = open("../CSV Files/"+str(NameOfOutput)+".csv", "a+", newline='', encoding="utf-8")
    output_files_list.write("ProjectName,FilePath,FileName,Extension,FileSizeKB\n")
    output_files_list.flush()


    # i =999
    # oldprojectname=""
    if type(DirectoriesOfProjects) is not list:
        DirectoriesOfProjects=[DirectoriesOfProjects]

    for path in DirectoriesOfProjects:
        orr=str(path).split("\\")
        repos_index=orr.index("repos")
        for root, dirs, files in os.walk(path):
            for file in files:
                name = os.path.join(root, file)
                file_size=os.path.getsize(name)
                arr = name.split("\\")
                projectname = str(arr[repos_index+2]) + '/'+ str(arr[repos_index+3])
                # if(oldprojectname != projectname):
                    # i+=1
                    # oldprojectname=projectname
                file_size_kb=file_size/1024
                format_file_size_kb = "{:.2f}".format(file_size_kb)
                filename = arr[-1]
                ext=filename.split('.')[-1] #str(i)+','+
                exts=['ru','rb'] #'c','cpp','c++','cc','h','hpp','hh','h','cs','java','r','rd','.profile','py','pyi','pyw','pyx','pxd',
                if(ext.lower() in exts and ("test" in name.lower() or "spec" in name.lower)):
                    output_files_list.write( projectname + ',' + name + ',' + filename + ','+ext +','+format_file_size_kb+ '\n')
                    output_files_list.flush()

    output_files_list.close()
    return "../CSV Files/"+str(NameOfOutput)+".csv"

pathsDict={}
# # pathsDict["applied"]=[ "E:\\PhD Work\\repos\\applied", "F:\\PhD Work\\repos\\applied"]
# # pathsDict["tool"]=[ "E:\\PhD Work\\repos\\tool" , "F:\\PhD Work\\repos\\tool" ]
pathsDict["ai-ml"]=[ "E:\\PhD Work\\repos\\tool" , "F:\\PhD Work\\repos\\tool" , "E:\\PhD Work\\repos\\applied", "F:\\PhD Work\\repos\\applied" ]
pathsDict["no-ai-ml"] = [ "D:\\PhD Work\\repos\\no-ai-ml","E:\\PhD Work\\repos\\no-ai-ml","F:\\PhD Work\\repos\\no-ai-ml" ]
AllPaths=pathsDict["ai-ml"]+pathsDict["no-ai-ml"]
# # give path
filepath=list_projects_files_with_filter(pathsDict["no-ai-ml"],"Top1000NoAIMLRubyTestFiles","..\\Excel Files\\Top1000NoAIML.xlsx")
print(filepath)
filepath=list_projects_files_with_filter(pathsDict["ai-ml"],"Top1000AIMLRubyTestFiles","..\\Excel Files\\Top1000AIML.xlsx")
print(filepath)
