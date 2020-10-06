import logging
import pprint
import requests
import os

GITHUB_REPO_PREFIX = 'https://github.com/'
GITHUB_API = 'https://api.github.com/repos/'
header={'Authorization': 'Bearer 'os.environ["TOKEN"]}

class Repository(object):

    all = []

    def __init__(self, url):
        self.url = url
        self.categories = []
        self.data = dict()
        self.all.append(self)

    def fetchRepoData(self):

        logging.info("Fetching data for repo %s", self.url)
        print ("header:")
        print (header)
        try:  
           os.environ["TOKEN"]
        except KeyError: 
           print ("Please set the environment variable TOKEN")
           sys.exit(1)

        if self.url.startswith(GITHUB_REPO_PREFIX):
            repo_path = self.url[len(GITHUB_REPO_PREFIX):]
            repo_info = requests.get('%s%s' % (GITHUB_API, repo_path), headers=header)
            repo_json = repo_info.json()
            if repo_info.status_code == 200:
                self.data['repo_path'] = repo_path
                self.data['description'] = repo_json['description']
                self.data['html_url'] = repo_json['html_url']
                self.data['pushed_at'] = repo_json['pushed_at']
                self.data['stargazers_count'] = repo_json['stargazers_count']
                self.data['forks_count'] = repo_json['forks_count']
            else:
                pp = pprint.PrettyPrinter(indent=4)
                raise Exception("Failed to fetch data for repo %s. Response was: %s" %
                    (self.url, pp.pformat(repo_json)))
