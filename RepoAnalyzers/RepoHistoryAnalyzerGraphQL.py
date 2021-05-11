import jsonpickle
import requests
import json
from datetime import datetime
import io
import pandas

from time import sleep


listOfTypes=["applied","tool","no-ai-ml"]
i= 0

# An example to get the remaining rate limit using the Github GraphQL API.




def run_query(query):  # A simple function to use requests.post to make the API call. Note the json= section.
    # print(query)
    headers = {"Authorization": "Bearer 71da1748c79fdf251b2b34b1403ac87a60818a84"}
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    json=request.json()
    if request.status_code == 200 and "errors" not in json:
        return json
    else:
        raise Exception("Query failed to run by returning code of {}. {} . {}".format(request.status_code, query,json))

remaining_limit_query = """
{
  viewer {
    login
  }
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
}
"""

def formulate_first_query(name,owner):
    first_query= """
    {
      repository(name:\""""+str(name)+"""\", owner: \""""+str(owner)+"""\") {
        pullRequests(first: 100) {
          totalCount
          edges {
            
            node {
            number
              files(first: 100) {
                totalCount
                edges {
                  cursor
                  node {
                    path
                  }
                }
                pageInfo {
                  endCursor
                  hasNextPage
                }
              }
              comments {
                totalCount
              }
            }
          }
          pageInfo {
            endCursor
            hasNextPage
          }
        }
      }
    }
    """
    return first_query

def formulate_get_files_after_curser_query(name,owner,pullrequest_number,end_file_cursor):
    query="""
        {
      repository(name: \""""+str(name)+"""\", owner: \""""+str(owner)+"""\") {
        pullRequest(number: """+str(pullrequest_number)+""") {
          files(first: 100 after:\""""+str(end_file_cursor)+"""\") {
            totalCount
            edges {
              cursor
              node {
                path
              }
            }
            pageInfo {
            endCursor
            hasNextPage
        }
          }
          comments {
            totalCount
          }
        }
      }
    }
    """
    return query


def formulate_get_pullrequests_after_curser_query(name,owner,after_cursor):
  query = """
   {
     repository(name:\"""" + str(name) + """\", owner: \"""" + str(owner) + """\") {
       pullRequests(first: 100 after:\""""+str(after_cursor)+"""\") {
         totalCount
         edges {
           node {
           number
             files(first: 100) {
               totalCount
               edges {
                 cursor
                 node {
                   path
                 }
               }
               pageInfo {
                 endCursor
                 hasNextPage
               }
             }
             comments {
               totalCount
             }
           }
         }
         pageInfo {
           endCursor
           hasNextPage
         }
       }
     }
   }
   """
  return query

def get_remaining_limit():
    result = run_query(remaining_limit_query)  # Execute the query
    remaining_rate_limit = result["data"]["rateLimit"]["remaining"]  # Drill down the dictionary
    return format(remaining_rate_limit)


def get_progress(i):
    try:
        with open("../JSON Files/pr_comments_progress-"+str(i)+".json", 'r+') as outfile:
            progress = json.load(outfile)
            progress+=1
    except:
        progress = 0
    return progress

def save_progress(progress):
    try:
        with open("../JSON Files/pr_comments_progress.json", 'w+') as outfile:
            progresspickled = jsonpickle.encode(progress, unpicklable=False)
            outfile.write(progresspickled)
            outfile.flush()
    except:
        return



def get_avg_review_count(i):

    current_rate_limit= get_remaining_limit()
    print(current_rate_limit)
    with open("../JSON Files/lastAnalysisForType" + str(i) + ".json", 'r+') as outfile:
        last_buildfiles_fs_analysis = json.load(outfile)
    type = listOfTypes[i]
    x = datetime.now()
    time = x.strftime("%x-%X").replace(":", "-").replace("/", "-")
    output_file = open("../CSV Files/devopsfiles-nbreviewcounts-2-"+ type + ".csv", "a+", encoding="utf-8")
    output_file.write("ProjectName;FilePath;NBReviewCount\n")
    error_file = open("../CSV Files/devopsfiles-nbreviewcounts-errors-2-"+ type + ".csv", "a+",
                      encoding="utf-8")
    error_file.write("ProjectName;FileNameWithRelativePath;Exception\n")
    buildfiles_infs_file = open(last_buildfiles_fs_analysis, "rb")
    decoder_wrapper = io.TextIOWrapper(buildfiles_infs_file, encoding='utf-8', errors='ignore')
    devops_fromfs_df = pandas.read_csv(decoder_wrapper, sep=";", error_bad_lines=False,
                                       usecols=["ProjectName", "FilePath", "DevopsType", "DevopsTool", "Notes"])
    previous_project=""
    progress=get_progress(i)
    for i  in range(progress,len(devops_fromfs_df.index)):
        row=devops_fromfs_df.loc[i,["ProjectName"]]
        project_name = row["ProjectName"]
        if(previous_project == project_name):
            continue
        previous_project=project_name
        # full_path = row["FilePath"]
        x = project_name.split("/")
        owner=x[0]
        name=x[1]

        list_of_paths_and_number_of_comments = []
        try:
            first_run= run_query(formulate_first_query(name,owner))
            endCursor_prs=first_run["data"]["repository"]["pullRequests"]["pageInfo"]["endCursor"]
            # print("endCursor_prs: "+str(endCursor_prs))
            has_nextpage_prs=first_run["data"]["repository"]["pullRequests"]["pageInfo"]["hasNextPage"]
            # print("has_nextpage_prs: "+str(has_nextpage_prs))
            for pr in first_run["data"]["repository"]["pullRequests"]["edges"]:
                pr_number=pr["node"]["number"]
                # print("pr_number: "+str(pr_number))
                pr_number_of_comments=pr["node"]["comments"]["totalCount"]
                # print("pr_number_of_comments: "+str(pr_number_of_comments))
                endCursor_files = pr["node"]["files"]["pageInfo"]["endCursor"]
                # print("endCursor_files: " + str(endCursor_files))
                has_nextpage_files = pr["node"]["files"]["pageInfo"]["hasNextPage"]
                # print("has_nextpage_files: " + str(has_nextpage_files))
                files=pr["node"]["files"]["edges"]
                for f in files:
                    list_of_paths_and_number_of_comments.append((f["node"]["path"],pr_number_of_comments))
                while(bool(has_nextpage_files)== True ):
                    continue_list_files=run_query(formulate_get_files_after_curser_query(name,owner,pr_number,endCursor_files))
                    files = continue_list_files["data"]["repository"]["pullRequest"]["files"]["edges"]
                    for f in files:
                        list_of_paths_and_number_of_comments.append((f["node"]["path"],pr_number_of_comments))
                    endCursor_files = continue_list_files["data"]["repository"]["pullRequest"]["files"]["pageInfo"]["endCursor"]
                    # print("endCursor_files: "+str(endCursor_files))
                    has_nextpage_files = continue_list_files["data"]["repository"]["pullRequest"]["files"]["pageInfo"]["hasNextPage"]
                    # print("has_nextpage_files: "+str(has_nextpage_files))
            while (bool(has_nextpage_prs) == True):
                other_run=run_query(formulate_get_pullrequests_after_curser_query(name,owner,endCursor_prs))
                endCursor_prs = other_run["data"]["repository"]["pullRequests"]["pageInfo"]["endCursor"]
                # print("endCursor_prs: "+str(endCursor_prs))
                has_nextpage_prs = other_run["data"]["repository"]["pullRequests"]["pageInfo"]["hasNextPage"]
                # print("has_nextpage_prs: "+str(has_nextpage_prs))
                for pr in other_run["data"]["repository"]["pullRequests"]["edges"]:
                    pr_number = pr["node"]["number"]
                    # print("pr_number: "+str(pr_number))
                    pr_number_of_comments = pr["node"]["comments"]["totalCount"]
                    # print("pr_number_of_comments: "+str(pr_number_of_comments))
                    endCursor_files = pr["node"]["files"]["pageInfo"]["endCursor"]
                    # print("endCursor_files: "+str(endCursor_files))
                    has_nextpage_files = pr["node"]["files"]["pageInfo"]["hasNextPage"]
                    # print("has_nextpage_files: "+str(has_nextpage_files))
                    files = pr["node"]["files"]["edges"]
                    for f in files:
                        list_of_paths_and_number_of_comments.append((f["node"]["path"],pr_number_of_comments))
                    while (bool(has_nextpage_files) == True):
                        continue_list_files = run_query(formulate_get_files_after_curser_query(name, owner, pr_number, endCursor_files))
                        # print(continue_list_files)
                        files = continue_list_files["data"]["repository"]["pullRequest"]["files"]["edges"]
                        for f in files:
                            list_of_paths_and_number_of_comments.append((f["node"]["path"],pr_number_of_comments))
                        endCursor_files = continue_list_files["data"]["repository"]["pullRequest"]["files"]["pageInfo"]["endCursor"]
                        # print("endCursor_files: "+str(endCursor_files))
                        has_nextpage_files = continue_list_files["data"]["repository"]["pullRequest"]["files"]["pageInfo"]["hasNextPage"]
                        # print("has_nextpage_files: "+str(has_nextpage_files))
        except Exception as e:
            save_progress(i)
            print("Exception")
            if("HTTPSConnectionPool") in str(e):
                print("internet error")
                i = i - 1
                previous_project = ""
                continue
            elif("404" in str(e)):
                print(404)
                continue
            elif ("502" in str(e)):
                print(502)
                continue
            else:
                print(e)
                print("sleeping")
                sleep(60)
                i=i-1
                previous_project=""
        for(a,b) in list_of_paths_and_number_of_comments:
            output_file.write(project_name+";"+str(a)+";"+str(b)+"\n")
            output_file.flush()
        print(project_name)
        save_progress(i)

def process_avg_count_csv(i):
    type = listOfTypes[i]
    df= pandas.read_csv("../CSV Files/devopsfiles-nbreviewcounts-2-"+ type + ".csv",usecols=["ProjectName","FilePath","NBReviewCount"], sep=";",error_bad_lines="ignore")
    # df["ProjectAndFile"]=str(df["ProjectName"].astype(str)+"^"+df["FilePath"].astype(str))
    # df.drop(columns=["ProjectName","FilePath"],inplace=True)
    df["NBReviewCount"].fillna(0,inplace=True)
    df["NBReviewCount"]=pandas.to_numeric(df["NBReviewCount"])


    # print(df)
    # df.set_index('ProjectAndFile',inplace=True)
    with open("../JSON Files/lastAnalysisForType" + str(i) + ".json", 'r+') as outfile:
        last_buildfiles_fs_analysis = json.load(outfile)

    buildfiles_infs_file = open(last_buildfiles_fs_analysis, "rb")
    decoder_wrapper = io.TextIOWrapper(buildfiles_infs_file, encoding='utf-8', errors='ignore')
    devops_fromfs_df = pandas.read_csv(decoder_wrapper, sep=";", error_bad_lines=False,
                                       usecols=["ProjectName", "FilePath", "DevopsType", "DevopsTool", "Notes"])
    list_of_devopsfs_paths=[]
    for index,row in devops_fromfs_df.iterrows():
        project_name=row["ProjectName"]
        full_path=row["FilePath"]
        x = project_name.split("/")
        file_with_path = full_path.split(project_name.replace("/","\\"))[1]
        file_with_path=file_with_path[1:]
        list_of_devopsfs_paths.append(str(file_with_path).replace("\\","/"))

    # df_new = df.groupby(["ProjectName", "FilePath"]).agg({'NBReviewCount': 'mean'}).reset_index()
    # df_new.rename(columns={'NBReviewCount': 'Avg_NBReviewCount'}, inplace=True)
    # df[['ProjectName','FilePath']] = df["ProjectAndFile"].str.split("^",expand=True)
    # df.drop(columns=["ProjectAndFile"], inplace=True)

    df_new = df[df['FilePath'].isin(list_of_devopsfs_paths)]
    df_new2 = df.copy()

    df_new = df_new.groupby(["ProjectName"]).agg({'NBReviewCount': 'mean'}).reset_index()
    df_new.rename(columns={'NBReviewCount': 'Avg_NBReviewCount'}, inplace=True)

    df_new2 = df_new2.groupby(["ProjectName"]).agg({'NBReviewCount': 'mean'}).reset_index()
    df_new2.rename(columns={'NBReviewCount': 'Avg_NBReviewCount'}, inplace=True)

    df_new.to_csv("../CSV Files/devopsfiles-avg-nbreviewcounts-"+ type + "3.csv",index=False)
    df_new2.to_csv("../CSV Files/allfiles-avg-nbreviewcounts-"+ type + "3.csv",index=False)

# process_avg_count_csv(0)
#
#
# process_avg_count_csv(2)

#
# get_avg_review_count(0)
# get_avg_review_count(1)
# get_avg_review_count(2)

# process_avg_count_csv(2)
process_avg_count_csv(0)
process_avg_count_csv(1)
process_avg_count_csv(2)
