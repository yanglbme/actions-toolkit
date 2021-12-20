# `actions.context`

## Usage

### Import the package

```python
from actions_toolkit import github
```

#### Getting Context

```python
from actions_toolkit import core
from actions_toolkit.github import Context

context = Context()
core.info(f'repo: {context.repo.repo}, owner: {context.repo.owner}')
```