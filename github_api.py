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
    @patch("requests.get")
    def test_fetch_data_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        find_repos("mfriedma1-svg")
        called_url = mock_get.call_args.kwargs.get('url')
        url_list = called_url.split("/")
        match url_list[-1]:
            case "repos":
                mock_dict = [{"name": "repo1"}, {"name": "repo2"}]
                mock_response.json.return_value = mock_dict
            case "commits":
                mock_dict = [{"test": "test"}, {"test": "test"}]
                mock_response.json.return_value = mock_dict
        mock_get.return_value = mock_response
        result = find_repos("mfriedma1-svg")

        self.assertEqual(result[0], "Repo: repo1; Number of commits: 2")
        self.assertEqual(result[1], "Repo: repo2; Number of commits: 2")

    @patch("requests.get")
    def test_fetch_data_failure(self, mock_get):
            mock_response = MagicMock()
            mock_response.status_code = 403
            mock_get.return_value = mock_response
            result = find_repos("mfriedma1-svg")

            self.assertEqual(result, "403 error, try again later.")


if __name__ == '__main__':
    unittest.main()