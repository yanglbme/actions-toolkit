import json
import os


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
            with open(file, 'r', encoding='utf-8') as f:
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
        if self.payload.get('repository'):
            return self.payload['repository']['owner']['login'], self.payload['repository']['name']
        return None, None

    def get_repo(self) -> dict:
        owner, repo = self._repo()
        return dict(owner=owner, repo=repo)

    def get_issue(self) -> dict:
        payload = self.payload
        actor = payload.get('issue') or payload.get('pull_request') or payload
        owner, repo = self._repo()
        return dict(owner=owner, repo=repo, number=actor.get('number'))
