import requests
import unittest
from unittest.mock import patch, MagicMock

def find_repos(id):
    link = f"https://api.github.com/users/{str(id)}/repos"
    r = requests.get(url=link)
    if r.status_code == 403:
        return(("403 error, try again later."))
    elif r.status_code == 404:
        return(("404 error, try a different id."))
    
    data = r.json()
    name_list = []
    commit_list = []
    step = 0
    result_list = []
    for i in data:
        name = i["name"]
        name_list.append(name)
        link2 = f"https://api.github.com/repos/{str(id)}/{name}/commits"
        q = requests.get(url=link2)
        commits = 0
        data2 = q.json()
        for j in data2:
            commits += 1
        commit_list.append(commits)
        result_list.append("Repo: " + name_list[step] + "; Number of commits: " + str(commit_list[step]))
        step += 1
    return result_list

class TestGithubAPI(unittest.TestCase):
    def test_api(self):
        result = find_repos("mfriedma1-svg")
        self.assertEqual(result[0], "Repo: github-api; Number of commits: 1")
        self.assertEqual(result[1], "Repo: helloworld; Number of commits: 1")
        self.assertEqual(result[2], "Repo: triangles; Number of commits: 2")

if __name__ == '__main__':
    unittest.main()