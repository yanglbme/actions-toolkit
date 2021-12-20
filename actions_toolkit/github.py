import json
import os
import sys
from collections import namedtuple
from string import Template

import requests

t = sys.path[0]
sys.path.remove(t)
from github import Github

sys.path.insert(0, t)

Repo = namedtuple('Repo', ['owner', 'repo'])
Issue = namedtuple('Issue', ['owner', 'repo', 'number'])


class Context:
    payload: dict
    event_name: str
    sha: str
    ref: str
    workflow: str
    action: str
    actor: str
    job: str
    run_number: int
    run_id: int
    api_url: str
    server_url: str
    graphql_url: str

    def __init__(self):
        self.payload = {}
        file = os.getenv('GITHUB_EVENT_PATH')
        if file:
            with open(file, 'r', encoding='utf-8', newline='') as f:
                self.payload = json.load(f)
        self.event_name = os.getenv('GITHUB_EVENT_NAME', '')
        self.sha = os.getenv('GITHUB_SHA', '')
        self.ref = os.getenv('GITHUB_REF', '')
        self.workflow = os.getenv('GITHUB_WORKFLOW', '')
        self.action = os.getenv('GITHUB_ACTION', '')
        self.job = os.getenv('GITHUB_JOB', '')
        self.run_number = int(os.getenv('GITHUB_RUN_NUMBER', '0'))
        self.run_id = int(os.getenv('GITHUB_RUN_ID', '0'))
        self.api_url = os.getenv('GITHUB_API_URL', 'https://api.github.com')
        self.server_url = os.getenv('GITHUB_SERVER_URL', 'https://github.com')
        self.graphql_url = os.getenv('GITHUB_GRAPHQL_URL', 'https://api.github.com/graphql')

    def _repo(self):
        if os.getenv('GITHUB_REPOSITORY'):
            owner, repo = os.getenv('GITHUB_REPOSITORY').split('/')
            return owner, repo
        repository = self.payload.get('repository')
        if not repository:
            return None, None
        return repository['owner']['login'], repository['name']

    def _issue(self):
        payload = self.payload
        actor = payload.get('issue') or payload.get('pull_request') or payload
        owner, repo = self._repo()
        return owner, repo, actor.get('number')

    @property
    def repo(self):
        return Repo(*self._repo())

    @property
    def issue(self):
        return Issue(*self._issue())


class Octokit:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {self.token}'
        }
        self.rest = Github(token)

    def graphql(self, query: str, variables: dict) -> dict:
        q = {
            'query': Template(query).substitute(variables)
        }
        resp = requests.post('https://api.github.com/graphql', json=q, headers=self.headers)
        if resp.status_code != 200:
            raise Exception(f'Query failed to run by returning code of {resp.status_code}. {query}')
        return resp.json()


def get_octokit(token):
    return Octokit(token)
