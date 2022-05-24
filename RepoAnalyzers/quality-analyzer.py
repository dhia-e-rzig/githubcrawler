import pandas as pd
import os
import subprocess

types_list=['applied','tool','nonaiml']

import random
import string

rdm_str_set=set()

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    while(True):
        if result_str not in rdm_str_set:
            rdm_str_set.add(result_str)
            return result_str
        else:
            result_str = ''.join(random.choice(letters) for i in range(length))



tool_projects_df=pd.read_csv('../CSV Files/Tool-classification.csv')
applied_projects_df=pd.read_csv('../CSV Files/Applied-classification.csv')
nonml_projects_df=pd.read_csv('../CSV Files/NonML-classification.csv')
df_list=[applied_projects_df,tool_projects_df,nonml_projects_df]

pathsDict={}
pathsDict["applied"]=[ "D:\\PhD Work\\repos\\applied", "D:\\PhD Work\\repos\\tool"]
pathsDict["tool"]=[ "D:\\PhD Work\\repos\\tool" , "D:\\PhD Work\\repos\\applied" ]
pathsDict["nonaiml"] = [ "D:\\PhD Work\\repos\\no-ai-ml" ]
type=0
type_name=types_list[type]
project_and_types_out=open('project_types_'+str(type_name)+'.csv','w+')
project_and_types_out.write('projectName,isJavaProject,isMavenProject,isAntProject,isGradleProject,isCproject,isCSharpProject\n')
project_important_paths_out=open('project_paths_'+str(type_name)+'.csv','w+')
project_important_paths_out.write('projectName;Paths\n')
i = 0
for tuple_proj in df_list[0].itertuples():
    if i > 10:
        break
    i+=1
    isJavaProject = False
    isMavenProject = False
    isAntProject = False
    isGradleProject = False
    isCproject = False
    isCSharpProject = False
    breakmode=False
    for path_root in pathsDict["applied"]:
        full_path=path_root+'/'+tuple_proj[1]
        important_paths=set()
        print(full_path)
        if os.path.exists(full_path):
            for root, dirs, files in os.walk(full_path):
                if breakmode:
                    break
                for file in files:
                    arr = file.split("\\")
                    filename = arr[-1]
                    ext = filename.split('.')[-1]
                    if str(ext).lower()=='java':
                        isJavaProject=True
                    if str(filename).lower()=='pom.xml':
                        important_paths.add(root)
                        isMavenProject=True
                    if str(filename).lower() == 'build.xml':
                        important_paths.add(root)
                        isAntProject = True
                    if str(filename).lower() == 'build.gradle':
                        important_paths.add(root)
                        isGradleProject = True
                    if str(ext).lower() == 'c' or str(ext).lower() == 'cpp':
                        important_paths.add(root)
                        isCproject = True
                    if str(ext).lower() == 'cs' :
                        isCSharpProject = True
                    if str(ext).lower() == 'sln' :
                        important_paths.add(root)
                        isCSharpProject = True
                    if isJavaProject and isMavenProject and isAntProject and isGradleProject and isCproject and isCSharpProject:
                        breakmode=True
                        break
            # project_and_types_out.write(
                # 'projectName,isJavaProject,isMavenProject,isAntProject,isGradleProject,isCproject,isCSharpProject\n')
            projectName=tuple_proj[1]
            project_and_types_out.write(projectName+','+str(isJavaProject)+','+str(isMavenProject)+','+str(isAntProject)+','+str(isGradleProject)+','+str(isCproject)+','+str(isCSharpProject)+','+full_path+'\n')
            paths_list=list(important_paths)
            paths_string=','.join([str(item) for item in paths_list])
            project_important_paths_out.write(projectName+';'+paths_string+'\n')

import multiprocessing as mp
NUM_CORE = mp.cpu_count()

def worker(arg):
    obj = arg
    return obj.process_project()


class sonar_scanner():
    def __init__(self,projecttuple,projectkey,token,importantPaths):
        self.name=projecttuple[1]
        self.isJavaProject = projecttuple[2]
        self.isMavenProject =  projecttuple[3]
        self.isAntProject =  projecttuple[4]
        self.isGradleProject =  projecttuple[5]
        self.isCproject =  projecttuple[6]
        self.isCSharpProject =  projecttuple[7]
        self.rootPath=projecttuple[8]
        self.key=projectkey
        self.token=token
        self.importantPaths=importantPaths
    def process_project(self):
        mvn_build_fail=False
        gdl_build_fail=False
        ant_build_fail=False
        temp_list=self.rootPath+list(self.importantPaths)
        if self.isJavaProject:
            for project_root_path in temp_list:
                os.chdir(project_root_path)
                if self.isMavenProject:
                    result = subprocess.run(["mvn","clean"], stdout=subprocess.PIPE, text=True)
                    result = subprocess.run(["mvn","compile"], stdout=subprocess.PIPE, text=True)
                    if 'BUILD FAILURE' in result.stdout:
                        mvn_build_fail=True
                if not (not mvn_build_fail and self.isMavenProject):
                    if self.isGradleProject:
                        result = subprocess.run([".\gradlew","clean"], stdout=subprocess.PIPE, text=True)
                        result = subprocess.run([".\gradlew","build"], stdout=subprocess.PIPE, text=True)
                        if 'FAILURE: Build failed' in result.stdout:
                            gdl_build_fail=True
                if not (not gdl_build_fail and self.isMavenProject):
                    if self.isAntProject:
                        result = subprocess.run(["ant"], stdout=subprocess.PIPE, text=True)
                        if 'BUILD FAILED'in result.stdout:
                            ant_build_fail=True
            result = subprocess.run(["sonnar-scanner","-D\"sonar.projectKey=slo\"","-D\"sonar.sources=.\"","-D\"sonar.host.url=http://localhost:9000\"","-D\"sonar.login="+self.token+"\""], stdout=subprocess.PIPE, text=True)
            if 'EXECUTION SUCCESS' not in result.stdout:
               return(self.name,self.key,'Fail',"JavaProject,mvn_build_fail="+str(mvn_build_fail)+",gdl_build_fail="+str(gdl_build_fail)+",ant_build_fail"+str(ant_build_fail)+","+result.stdout.replace('\n', ',').replace(';', ','))
        elif self.isCSharpProject:
            result = subprocess.run(["dotnet","sonarscanner","begin", "-D\"sonar.projectKey=slo\"", "-D\"sonar.sources=.\"",
                                     "-D\"sonar.host.url=http://localhost:9000\"",
                                     "-D\"sonar.login="+self.token+"\""],
                                    stdout=subprocess.PIPE, text=True)

            result = subprocess.run(["dotnet", "build"], stdout=subprocess.PIPE, text=True)
            result = subprocess.run(
                ["dotnet", "sonarscanner", "end",
                 "-D\"sonar.login="+self.token+"\""],
                stdout=subprocess.PIPE, text=True)
            if 'EXECUTION SUCCESS' not in result.stdout:
                return (self.name,self.key, 'Fail', result.stdout.replace('\n', ',').replace(';', ','))
            else:
                return (self.name,self.key, 'Success')
        elif self.isCproject:
            result = subprocess.run(["sonnar-scanner", "-D\"sonar.projectKey=slo\"", "-D\"sonar.sources=.\"",
                                     "-D\"sonar.host.url=http://localhost:9000\"",
                                     "-D\"sonar.login=" + self.token + "\""], stdout=subprocess.PIPE, text=True)
            if 'EXECUTION SUCCESS' not in result.stdout:
                return(self.name,self.key,'Fail','CPROJECT,'+result.stdout.replace('\n',',').replace(';',','))
            else:
                return(self.name,self.key,'Success')
        else:
            result = subprocess.run(["sonnar-scanner", "-D\"sonar.projectKey=slo\"", "-D\"sonar.sources=.\"",
                                     "-D\"sonar.host.url=http://localhost:9000\"", "-D\"sonar.login=" + self.token + "\""],
                                    stdout=subprocess.PIPE, text=True)
            if 'EXECUTION SUCCESS' not in result.stdout:
                return (self.name,self.key, 'Fail', 'CSPROJECT,'+result.stdout.replace('\n', ',').replace(';', ','))
            else:
                return (self.name,self.key,'Success')

if __name__ == "__main__":
    output_file = open("../CSV Files/sonar-ids-scan-status-"+type_name + ".csv", "w+", encoding="utf-8")
    output_file.write(
        "ProjectName;Key;Status\n")
    error_file = open("../CSV Files/sonar-scan-errors-" + type_name + ".csv", "w+", encoding="utf-8")
    error_file.write("ProjectName;Error\n")
    project_and_types_df=pd.read_csv('project_types_' + str(type_name) + '.csv').to
    project_and_paths_df=pd.read_csv('project_paths_' + str(type_name) + '.csv')
    mp_object_list = []
    token='INSERT TOKEN HERE'
    for proj_tuple in project_and_types_df:
        key=get_random_string(5)
        df_temp=project_and_paths_df.loc[project_and_paths_df['projectName'] == proj_tuple[1]]
        paths_list_1=df_temp['Paths'].tolist()
        paths_list_2=[str(temp).split(',') for temp in paths_list_1]
        paths_list_3=[]
        for arr in paths_list_2:
            for elem in arr:
                paths_list_3.append(elem)
        temp_object = sonar_scanner(proj_tuple,key,token,paths_list_3)
        print(temp_object)
        exit()
        mp_object_list.append(temp_object)
        pool = mp.Pool(NUM_CORE)
        list_of_results = pool.map(worker, ((obj) for obj in mp_object_list))  # 500, 1000
        pool.close()
        pool.join()
        for res in list_of_results:
            output_file.write(','.join([str(item) for item in res[:4]])+'\n')
            if res[2] == 'Fail':
                error_file.write(res+'\n')
