# Actions Toolkit

The GitHub Actions ToolKit provides a set of packages to make creating actions easier in Python.

[![Downloads](https://pepy.tech/badge/actions-toolkit/month)](https://pepy.tech/project/actions-toolkit)
[![Supported Versions](https://img.shields.io/pypi/pyversions/actions-toolkit.svg)](https://pypi.org/project/actions-toolkit)
[![Pypi Versions](https://img.shields.io/pypi/v/actions-toolkit.svg)](https://pypi.python.org/pypi/actions-toolkit)
[![Contributors](https://img.shields.io/github/contributors/yanglbme/actions-toolkit.svg)](https://github.com/yanglbme/actions-toolkit/graphs/contributors)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyanglbme%2Factions-toolkit.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyanglbme%2Factions-toolkit?ref=badge_shield)

```python
>>> import os
>>> from actions_toolkit import core
>>> os.environ['INPUT_NAME'] = 'Actions Toolkit'
>>> core.get_input('name')
'Actions Toolkit'
>>> core.error('Something went wrong.')
::error::Something went wrong.
>>> core.info('Run successfully.')
Run successfully.
>>> core.set_failed('SSL certificates installation failed.')
::error::SSL certificates installation failed.
```

## Installing Actions Toolkit and Supported Versions

Action Toolkit is available on PyPI:

```bash
$ python -m pip install actions-toolkit
```

Action Toolkit officially supports Python 3.6+.

## Packages

- `actions.core`: Provides functions for inputs, outputs, results, logging, secrets and variables. Read
  more [here](/actions_toolkit/core/README.md).
- `actions.exec`: Provides functions to exec cli tools and process output.
- `actions.glob`: Provides functions to search for files matching glob patterns.
- `actions.io`: Provides disk i/o functions like cp, mv, rmRF, which etc.
- `actions.tool-cache`: Provides functions for downloading and caching tools. e.g. setup-* actions.
- `actions.github`: Provides an Octokit client hydrated with the context that the current action is being run in.
- `actions.artifact`: Provides functions to interact with actions artifacts.
- `actions.cache`: Provides functions to cache dependencies and build outputs to improve workflow execution time.

## Contributing

We welcome contributions.

## License

The scripts and documentation in this project are released under the [MIT License](LICENSE).

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyanglbme%2Factions-toolkit.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyanglbme%2Factions-toolkit?ref=badge_large)