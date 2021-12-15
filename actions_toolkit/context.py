import json
import os
from collections import defaultdict


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
        self.payload = defaultdict()
        file = os.getenv('GITHUB_EVENT_PATH')
        if file:
            with open(file, 'r', encoding='utf-8') as f:
                self.payload = json.load(f)
        self.event_name = os.getenv('GITHUB_EVENT_NAME', '')
        self.sha = os.getenv('GITHUB_SHA', '')
        self.ref = os.getenv('GITHUB_REF', '')
        self.workflow = os.getenv('GITHUB_WORKFLOW', '')
        self.action = os.getenv('GITHUB_ACTION', '')
        self.job = os.getenv('GITHUB_JOB', '')
        self.run_number = int(os.getenv('GITHUB_RUN_NUMBER'))
        self.run_id = int(os.getenv('GITHUB_RUN_ID'))
        self.api_url = os.getenv('GITHUB_API_URL', 'https://api.github.com')
        self.server_url = os.getenv('GITHUB_SERVER_URL', 'https://github.com')
        self.graphql_url = os.getenv('GITHUB_GRAPHQL_URL', 'https://api.github.com/graphql')

    def get_repo(self) -> dict:
        if os.getenv('GITHUB_REPOSITORY'):
            owner, repo = os.getenv('GITHUB_REPOSITORY').split('/')
            return dict(owner=owner, repo=repo)
        if self.payload['repository']:
            return dict(owner=self.payload['repository']['owner']['login'], repo=self.payload['repository']['name'])
        raise Exception("context.repo requires a GITHUB_REPOSITORY environment variable like 'owner/repo'")

    def get_issue(self) -> dict:
        payload = self.payload
        actor = payload.get('issue') or payload.get('pull_request') or payload
        repo = self.get_repo()
        return {
            'owner': repo.get('owner'),
            'repo': repo.get('repo'),
            'number': actor.get('number')
        }
