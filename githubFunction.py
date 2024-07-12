import requests
import random
from Timer import timer_annotation
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("GITHUB_ACCESS_TOKEN")
if token is None:
    token=""

@timer_annotation
def get_github_user_data(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url,headers={
        "Authorization":"token "+ token
    })
    data = response.json()
    if response.status_code == 200:
        name = data["name"]
        bio = data["bio"]
        location = data["location"]
        email = data["email"]
        followers = data["followers"]
        following = data["following"]
        public_repos = data["public_repos"]

        # prevent inserting empty values as keys in the dictionary

        github_data = {
            "name": name,
            "followers": followers,
            "following": following,
            "public_repos": public_repos,
        }

        if bio:
            github_data["bio"] = bio
        if location:
            github_data["location"] = location
        if email:
            github_data["email"] = email

        repos = get_repos(username)
        github_data["5_random_repos"] = repos

        ## get commits for each repo
        commits = get_commits(username, repos)
        github_data["commits_of_5_random_repos"] = commits

        return github_data
    else:
        print(f"Error: {response.status_code}")
        return None

def get_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url,headers={
        "Authorization":"token "+ str(os.getenv("GITHUB_ACCESS_TOKEN"))
    })
    # return json response in dictionary format

    data = response.json()

    # pick 5 repos randomly from the list
    random.shuffle(data)
    shortlisted = []
    idx = 0
    while len(shortlisted) <min(5, len(data)) and idx < len(data):
        # print(data[idx]['name'], data[idx]['fork'], data[idx]['size'])
        if data[idx]['name'] not in shortlisted and not data[idx]['fork'] and data[idx]['size'] > 0:
            shortlisted.append(data[idx]['name'])
        idx += 1
    # pull name of the repo  and return
    return shortlisted

def get_commits(username, repos):
    commits = {}
    for repo in repos:
        # print(f"Getting commits for {repo}")
        commits[repo] = get_commits_for_repo(username, repo)
    return commits

def get_commits_for_repo(username, repo):
    url = f"https://api.github.com/repos/{username}/{repo}/commits"
    response = requests.get(url,headers={
        "Authorization":"token "+os.getenv("GITHUB_ACCESS_TOKEN")
    })
    data = response.json()

    if len(data) < 10:
        return [commit['commit']['message'] for commit in data]
    else:
        random.shuffle(data)
    shortlisted = data[:10]
    # print("Shortlisted commits:")
    # print(shortlisted)

    return [commit['commit']['message'] for commit in shortlisted]


if __name__ == "__main__":
    username = input("Enter your github username: ")
    repos = get_repos(username)
    print(repos)
    commits = get_commits(username, repos)
    print(commits)
    
    