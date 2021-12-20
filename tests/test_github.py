import json
import os

from actions_toolkit.github import Context, Repo, Issue

os.environ['GITHUB_REPOSITORY'] = 'yanglbme/actions-toolkit'
os.environ['GITHUB_EVENT_PATH'] = os.path.join(os.getcwd(), 'payload.json')
context = Context()

with open('./payload.json', 'r', encoding='utf-8') as f:
    assert context.payload == json.load(f)

os.environ.pop('GITHUB_EVENT_PATH', None)
context = Context()
assert context.payload == {}

assert context.repo == Repo(owner='yanglbme', repo='actions-toolkit')

os.environ.pop('GITHUB_REPOSITORY', None)
context.payload['repository'] = {
    'name': 'test',
    'owner': {
        'login': 'user'
    }
}
assert context.repo == Repo(owner='user', repo='test')

os.environ['GITHUB_REPOSITORY'] = 'yanglbme/actions-toolkit'
os.environ['GITHUB_EVENT_PATH'] = os.path.join(os.getcwd(), 'payload.json')
context = Context()
assert context.issue == Issue(owner='yanglbme', repo='actions-toolkit', number=1)

os.environ.pop('GITHUB_REPOSITORY', None)
context.payload = {
    'pull_request': {
        'number': 2
    },
    'repository': {
        'owner': {
            'login': 'user'
        },
        'name': 'test'
    }
}
assert context.issue == Issue(owner='user', repo='test', number=2)

os.environ.pop('GITHUB_REPOSITORY', None)
context.payload = {
    'number': 2,
    'repository': {
        'owner': {
            'login': 'user'
        },
        'name': 'test'
    }
}
assert context.issue == Issue(owner='user', repo='test', number=2)
