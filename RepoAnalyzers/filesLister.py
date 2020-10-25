import os
import pandas



def list_projects_files_with_filter(DirectoriesOfProjects, NameOfOutput, FilteringListPath):

    # output_files_list = open("repos-noai-all2.csv", "a+", newline='',encoding="utf-8")
    output_files_list = open("../CSV Files/"+str(NameOfOutput)+".csv", "w+", newline='', encoding="utf-8")
    # aiextra_liest=["atomistic-machine-learning/schnetpack","algorithmfoundry/Foundry","lim-anggun/FgSegNet","crouchred/speaker-recognition-py3","xiaoshuaishuai319/weixinxiaochengxu","Waikato/wekaDeeplearning4j","SMTorg/smt","Steven-Hewitt/Entailment-with-Tensorflow"] #"jupyterhub/helm-chart","iArunava/Python-TheNoTheoryGuide","AICommunityInno/Seminars","foo123/FILTER.js","kakao/n2","synyi/poplar","kermitt2/delft","Tiramisu-Compiler/tiramisu","sniklaus/pytorch-pwc","lixinsu/RCZoo","chovanecm/sacredboard","aliakbar09a/AI_plays_snake"
    output_files_list.write("ProjectName,FilePath,FileName,Extension\n")
    output_files_list.flush()

    with open(FilteringListPath, "rb") as projects_list:
        if(str(FilteringListPath).endswith(".xsl") or str(FilteringListPath).endswith(".xslx")):
            projectIDs_dataframe = pandas.read_excel(projects_list)
        elif str(FilteringListPath).endswith(".csv"):
            projectIDs_dataframe = pandas.read_csv(projects_list)
        else:
            raise Exception(FilteringListPath)


    topprojects = projectIDs_dataframe["Name"].tolist()
    # print(topprojects)


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
                arr = name.split("\\")
                projectname = str(arr[repos_index+2]) + '/'+ str(arr[repos_index+3])
                if projectname not in  topprojects:
                    continue
                # if(oldprojectname != projectname):
                    # i+=1
                    # oldprojectname=projectname
                filename = arr[-1]
                ext=filename.split('.')[-1] #str(i)+','+
                output_files_list.write( projectname + ',' + name + ',' + filename + ','+ext + '\n')
                output_files_list.flush()

    output_files_list.close()
    return "../CSV Files/"+str(NameOfOutput)+".csv"


def list_projects_files(DirectoriesOfProjects, NameOfOutput):


    output_files_list = open("../CSV Files/"+str(NameOfOutput)+".csv", "a+", newline='', encoding="utf-8")
    output_files_list.write("ProjectName,FilePath,FileName,Extension\n")
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
                arr = name.split("\\")
                projectname = str(arr[repos_index+2]) + '/'+ str(arr[repos_index+3])
                # if(oldprojectname != projectname):
                    # i+=1
                    # oldprojectname=projectname
                filename = arr[-1]
                ext=filename.split('.')[-1] #str(i)+','+
                output_files_list.write( projectname + ',' + name + ',' + filename + ','+ext + '\n')
                output_files_list.flush()

    output_files_list.close()
    return "../CSV Files/"+str(NameOfOutput)+".csv"
