import jsonpickle
import requests
import json
from datetime import datetime
import io
import pandas

from time import sleep

listOfTypes = ["applied", "tool", "no-ai-ml"]
i = 0


# An example to get the remaining rate limit using the Github GraphQL API.


def run_query(query):  # A simple function to use requests.post to make the API call. Note the json= section.
    # print(query)
    headers = {"Authorization": "Bearer 71da1748c79fdf251b2b34b1403ac87a60818a84"}
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    json = request.json()
    if request.status_code == 200 and "errors" not in json:
        return json
    else:
        raise Exception("Query failed to run by returning code of {}. {} . {}".format(request.status_code, query, json))


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


def formulate_first_query(name, owner):
    first_query = """
    {
      repository(name:\"""" + str(name) + """\", owner: \"""" + str(owner) + """\") {
      ref(qualifiedName: "master") {
      target {
        ... on Commit {
          history(first: 2) {
            pageInfo {
              hasNextPage
              endCursor
            }
            edges {
              node {
                oid
                id
                pushedDate
                status {
                  state
                  id
                }
              }
            }
          }
        }
      }
    }
      }
    }
    """
    return first_query


def formulate_get_commits_after_cursor(name, owner, end_commit_commands_cursor):
    query = """
    {
      repository(name:\"""" + str(name) + """\", owner: \"""" + str(owner) + """\") {
        ref(qualifiedName: "master") {
      target {
        ... on Commit {
          history(first: 100 , after: \"""" + str(end_commit_commands_cursor) + """\") {
            pageInfo {
              hasNextPage
              endCursor
            }
            edges {
              node {
                oid
                id
                pushedDate
                status {
                  state
                  id
                }
              }
            }
          }
        }
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


def get_progress():
    try:
        with open("../JSON Files/commits_statuses.json", 'r+') as outfile:
            progress = json.load(outfile)
            progress += 1
    except:
        progress = 0
    return progress


def save_progress(progress):
    try:
        with open("../JSON Files/commits_statuses.json", 'w+') as outfile:
            progresspickled = jsonpickle.encode(progress, unpicklable=False)
            outfile.write(progresspickled)
            outfile.flush()
    except:
        return


def get_commit_dates_and_statuses(i):
    current_rate_limit = get_remaining_limit()
    with open("../JSON Files/lastAnalysisForType" + str(i) + ".json", 'r+') as outfile:
        last_buildfiles_fs_analysis = json.load(outfile)


    last_buildfiles_fs_analysis="../CSV Files/New_DevOps_NOAIML.csv"
    type = listOfTypes[i]
    x = datetime.now()
    time = x.strftime("%x-%X").replace(":", "-").replace("/", "-")
    output_file = open("../CSV Files/commits-statuses-" + type + "-2.csv", "a+", encoding="utf-8")
    output_file.write("ProjectName;CommitID;CommitOID;CommitDate;CommitTimeAndZone;CommitStatus\n")
    error_file = open("../CSV Files/commits-statuses--errors-" + type + "-2.csv", "a+",
                      encoding="utf-8")
    error_file.write("ProjectName;FileNameWithRelativePath;Exception\n")
    buildfiles_infs_file = open(last_buildfiles_fs_analysis, "rb")
    decoder_wrapper = io.TextIOWrapper(buildfiles_infs_file, encoding='utf-8', errors='ignore')
    devops_fromfs_df = pandas.read_csv(decoder_wrapper, sep=",", error_bad_lines=False,
                                       usecols=["ProjectName", "FilePath"])
    previous_project = ""
    progress = get_progress()
    for i in range(progress, len(devops_fromfs_df.index)):
        row = devops_fromfs_df.loc[i, ["ProjectName"]]
        project_name = row["ProjectName"]
        if (previous_project == project_name):
            continue
        previous_project = project_name
        # full_path = row["FilePath"]
        x = project_name.split("/")
        owner = x[0]
        name = x[1]

        list_of_paths_and_number_of_comments = []
        try:
            first_run = run_query(formulate_first_query(name, owner))
            endCursor_prs = first_run["data"]["repository"]["ref"]["target"]["history"]["pageInfo"]["endCursor"]
            # print("endCursor_prs: "+str(endCursor_prs))
            has_nextpage_prs = first_run["data"]["repository"]["ref"]["target"]["history"]["pageInfo"]["hasNextPage"]
            # print("has_nextpage_prs: "+str(has_nextpage_prs))
            old_oid=""
            if first_run is None:
                continue
            for cc in first_run["data"]["repository"]["ref"]["target"]["history"]["edges"]:
                commit_oid = cc["node"]["oid"]
                if old_oid == commit_oid:
                    continue
                old_oid=commit_oid
                commit_id = cc["node"]["id"]
                commit_date=cc["node"]["pushedDate"]
                commit_status=cc["node"]["status"]
                if commit_date is None:
                    continue
                if commit_status is None:
                    commit_status = "Unknown"
                else:
                    commit_status=commit_status["state"]
                date = str(commit_date).split("T")[0]
                time = str(commit_date).split("T")[1]
                # output_file.write("ProjectName;CommitID;CommitOID;CommitDate;CommitStatus\n")
                print(str(project_name)+";"+str(commit_id)+";"+str(commit_oid)+";"+str(date)+";"+str(time)+";"+str(commit_status))
                output_file.write(str(project_name)+";"+str(commit_id)+";"+str(commit_oid)+";"+str(date)+";"+str(time)+";"+str(commit_status)+'\n')

            while (bool(has_nextpage_prs) == True):
                other_run = run_query(formulate_get_commits_after_cursor(name,owner,endCursor_prs))
                if other_run is None:
                    break
                endCursor_prs = other_run["data"]["repository"]["ref"]["target"]["history"]["pageInfo"]["endCursor"]
                # print("endCursor_prs: "+str(endCursor_prs))
                has_nextpage_prs = other_run["data"]["repository"]["ref"]["target"]["history"]["pageInfo"]["hasNextPage"]
                # print("has_nextpage_prs: "+str(has_nextpage_prs))

                for cc in other_run["data"]["repository"]["ref"]["target"]["history"]["edges"]:
                    commit_oid = cc["node"]["oid"]
                    commit_id = cc["node"]["id"]
                    commit_date = cc["node"]["pushedDate"]
                    commit_status = cc["node"]["status"]
                    if commit_date is None:
                        continue
                    if commit_status is None:
                        commit_status = "Unknown"
                    else:
                        commit_status = commit_status["state"]
                    date = str(commit_date).split("T")[0]
                    time = str(commit_date).split("T")[1]
                    print(
                        str(project_name) + ";" + str(commit_id) + ";" + str(commit_oid) + ";" + str(date) + ";" + str(
                            time) + ";" + str(commit_status) )
                    output_file.write(
                        str(project_name) + ";" + str(commit_id) + ";" + str(commit_oid) + ";" + str(date) + ";" + str(
                            time) + ";" + str(commit_status) + '\n')
                    if old_oid == commit_oid:
                        continue
                    old_oid = commit_oid
        except Exception as e:
            save_progress(i)
            print("Exception")
            if ("HTTPSConnectionPool") in str(e):
                print("internet error")
                error_file.write(project_name+";"+"internet error"+'\n')
                i = i - 1
                previous_project = ""
                continue
            elif ("404" in str(e)):
                print(404)
                error_file.write(project_name + ";" + str(e) + '\n')
                continue
            elif ("502" in str(e)):
                print(502)
                error_file.write(project_name + ";" + str(e) + '\n')
                continue
            else:
                print(e)
                error_file.write(project_name + ";" + str(e) + '\n')
                print("sleeping")
                sleep(60)
                i = i - 1
                previous_project = ""
        save_progress(i)

# get_commit_dates_and_statuses(2)
#reset commits statuses to -1
