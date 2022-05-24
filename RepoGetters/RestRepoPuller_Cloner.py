import pandas as pd
import git
import os
import stat
import sys
import time



def rmtree(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWRITE)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(top)

df_all_repos=pd.read_csv('../CSV Inputs/all-repos.csv')
df_not_found_repos=pd.read_csv('../CSV Inputs/reposNotFound.csv')
repos_not_found=df_not_found_repos['RepoName'].tolist()
df_found_repos=df_all_repos[~df_all_repos['full_name'].isin(repos_not_found)]

class Project_updater():
    def __init__(self, project,category):
        self.project = project
        self.category = category
    def update_local_repo(self):
        if self.category == "Tool":
            type = 'tool'
        elif self.category== 'Applied':
            type = 'applied'
        else:
            type = 'no-ai-ml'
        path = 'D:/PhD Work/repos/' + type + '/' + self.project
        try:
            print('working on project: ' + self.project)
            try:
                git_repo = git.repo.Repo(path)
                print(self.project+ ': git repo found locally')
                git_repo.active_branch.checkout()
                print(self.project+ ': switched to active branch')
                try:
                    git_repo.remote().pull()
                    print(self.project+ ': pulled successfully')
                except:
                    print(self.project + ': pull error, deleting local repo and recloning')
                    rmtree(path)
                    try:
                        git.Repo.clone_from("https://github.com/" + self.project + ".git", path)
                    except Exception as e:
                        print(self.project+ ': clone error')
                        return (self.project,self.category,'Fail', str(e))
            except:
                if (os.path.exists(path)):
                    print("unfinished download found at " + path + " deleting and recloning")
                    rmtree(path)
                try:
                    git.Repo.clone_from("https://github.com/" +self.project+ ".git",path)
                except Exception as e:
                    print(self.project + ': clone error')
                    return (self.project,self.category,'Fail', str(e))

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(self.project+': unknown error')
            return (self.project,self.category,'Fail', str(e))
        return(self.project,self.category,'Success','')

import multiprocessing as mp
NUM_CORE = 8
import time

def worker(arg):
    obj = arg
    return obj.update_local_repo()
if __name__ == "__main__":
    # for i in range(8000,9000,1000):
    #     print('range:'+str(i)+'  '+str(i+1000))
    #     start_time_all = time.perf_counter()
    #     list_of_objects = [Project_updater(row['full_name'], row['Category']) for index,row in df_found_repos.iterrows()]
    #     pool = mp.Pool(NUM_CORE)
    #     # doing in order. first 8000 done, run in segments of 1000
    #     list_of_results = pool.map(worker, ((obj) for obj in list_of_objects[i:i+1000])) #500, 1000
    #     pool.close()
    #     pool.join()
    #     csv_res = open('cloning_results.csv', 'a+')
    #     # csv_res.write('Project,Category,UpdateResult,Message')
    #     # csv_res.write('\n')
    #     for line in list_of_results:
    #         csv_res.write(line[0]+','+line[1]+','+line[2]+','+line[3])
    #         csv_res.write('\n')
    #     end_time_all = time.perf_counter()
    #     print(f"Execution Time : {end_time_all - start_time_all:0.6f}")
    print('9000+ finishing...')
    # start_time_all = time.perf_counter()
    # list_of_objects = [Project_updater(row['full_name'], row['Category']) for index, row in df_found_repos.iterrows()]
    # pool = mp.Pool(NUM_CORE)
    # # doing in order. first 8000 done, run in segments of 1000
    # # print('range:' + str(i) + '  ' + str(i + 1000))
    # list_of_results = pool.map(worker, ((obj) for obj in list_of_objects[9000:]))  # 500, 1000
    # pool.close()
    # pool.join()
    # csv_res = open('cloning_results.csv', 'a+')
    # # csv_res.write('Project,Category,UpdateResult,Message')
    # # csv_res.write('\n')
    # for line in list_of_results:
    #     csv_res.write(line[0] + ',' + line[1] + ',' + line[2] + ',' + str(line[3]).replace('\n','-'))
    #     csv_res.write('\n')
    # end_time_all = time.perf_counter()
    # print(f"Execution Time : {end_time_all - start_time_all:0.6f}")

    #process finished, TODO: clean csv of results





