# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import json
import pandas as pd

#
# query = """query {
#     characters {
#     results {
#       name
#       status
#       species
#       type
#       gender
#     }
#   }
# }"""
#
# url = 'https://rickandmortyapi.com/graphql/'
# r = requests.post(url, json={'query': query})
# print(r.status_code)
# # print(r.text)
# json_data = json.loads(r.text)
# df_data = json_data['data']['characters']['results']
# df = pd.DataFrame(df_data)
# print(df)
github_token='token 8abef4ea0fb79fdc55042fb2ce5fe643119e8ef5'
headers = {"Authorization": github_token}

def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        print(request.status_code)
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


test_query = """
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
search_query= """
{
  search(type: REPOSITORY, query: "topic: 'machine learning' ", first: 100) {
    repos: edges {
      repo: node {
        ... on Repository {
          url
          repositoryTopics(first:3){
            nodes{
              topic{name}
            }
          }
          stargazers {
            totalCount
          }
        }
      }
    }
  }
}

"""
result = run_query(search_query) # Execute the query
print(result)
remaining_rate_limit = result["data"]["search"]["repos"][0]["repo"]["stargazers"]["totalCount"]
print(remaining_rate_limit)
