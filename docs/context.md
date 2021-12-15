# `actions.context`

## Usage

### Import the package

```python
from actions_toolkit.context import Context
```

#### Getting Context

```python
from actions_toolkit import core
from actions_toolkit.context import Context

context = Context()
payload = context.payload
repo = context.get_repo()
core.info(f'current repo:{repo["owner"]}/{repo["repo"]}')
```