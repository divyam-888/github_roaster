import requests
import random


def get_github_user_data(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
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
    response = requests.get(url)
    # return json response in dictionary format

    data = response.json()

    # pick 5 repos randomly from the list
    if len(data) < 5:
        return [repo['name'] for repo in data]
    else:
        random.shuffle(data)
    shortlisted = []
    idx = 0
    while len(shortlisted) < 5:
        if data[idx]['name'] not in shortlisted and not data[idx]['fork']:
            shortlisted.append(data[idx]['name'])
        idx += 1
    # pull name of the repo  and return
    return shortlisted

def get_commits(username, repos):
    commits = {}
    for repo in repos:
        commits[repo] = get_commits_for_repo(username, repo)
    return commits

def get_commits_for_repo(username, repo):
    url = f"https://api.github.com/repos/{username}/{repo}/commits"
    response = requests.get(url)
    data = response.json()

    if len(data) < 10:
        return [commit['commit']['message'] for commit in data]
    else:
        random.shuffle(data)
    shortlisted = data[:10]

    return [commit['commit']['message'] for commit in shortlisted]


if __name__ == "__main__":
    username = input("Enter your github username: ")
    repos = get_repos(username)
    commits = get_commits(username, repos)
    print(commits)