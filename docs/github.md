# `actions.github`

## Usage

Returns an authenticated Octokit client that follows the machine proxy settings and correctly sets GHES base urls.
See https://octokit.github.io/rest.js for the API.

```python
from actions_toolkit import core
from actions_toolkit import github

my_token = core.get_input('myToken')
octokit = github.get_octokit(my_token)

repo = octokit.rest.get_repo('yanglbme/gitee-pages-action')
pull_request = repo.get_pull(33)
print(pull_request)
```

You can also make GraphQL requests. See https://github.com/octokit/graphql.js for the API.

```python
from actions_toolkit import core
from actions_toolkit.github import get_octokit

my_token = core.get_input('myToken')
octokit = get_octokit(my_token)

query = """query {
  repository(owner:"$owner", name:"$repo") {
    issues(last:20, states:CLOSED) {
      edges {
        node {
          title
          url
          labels(first:5) {
            edges {
              node {
                name
              }
            }
          }
        }
      }
    }
  }
}"""

variables = {
    'owner': 'yanglbme',
    'repo': 'gitee-pages-action'
}
result = octokit.graphql(query, variables)
```

Finally, you can get the context of the current action:

```python
from actions_toolkit import core
from actions_toolkit.github import Context, get_octokit

my_token = core.get_input('myToken')
octokit = get_octokit(my_token)

context = Context()

user_repo = f'{context.repo.owner}/{context.repo.repo}'
repo = octokit.rest.get_repo(user_repo)
repo.create_issue(title='New issue!', body='Hello Universe!')

if context.event_name == 'push':
    core.info(f'The head commit is: {context.payload.get("head_commit")}')
```