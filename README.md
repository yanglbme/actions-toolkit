# Actions Toolkit

The GitHub Actions ToolKit provides an SDK to make creating actions easier in Python.

[![Downloads](https://pepy.tech/badge/actions-toolkit)](https://pepy.tech/project/actions-toolkit)
[![Supported Versions](https://img.shields.io/pypi/pyversions/actions-toolkit.svg)](https://pypi.org/project/actions-toolkit)
[![Pypi Versions](https://img.shields.io/pypi/v/actions-toolkit.svg)](https://pypi.python.org/pypi/actions-toolkit)
[![Contributors](https://img.shields.io/github/contributors/yanglbme/actions-toolkit.svg)](https://github.com/yanglbme/actions-toolkit/graphs/contributors)

## Installation

Action Toolkit is available on PyPI:

```bash
$ python -m pip install actions-toolkit
```

Action Toolkit officially supports Python 3.6+.

## Usage

```python
>>> import os
>>> from actions_toolkit import core
>>> os.environ['INPUT_NAME'] = 'Actions Toolkit'
>>> core.get_input('name', required=True)
'Actions Toolkit'
>>> core.error('Something went wrong.')
::error::Something went wrong.
>>> core.info('Run successfully.')
Run successfully.
>>> core.set_failed('SSL certificates installation failed.')
::error::SSL certificates installation failed.
```

For more examples and API documentation, please see the [core](./docs/core.md) & [github](./docs/github.md).

## Contributing

Contributions are always welcomed!

Here are the workflow for contributors:

- Fork to your own
- Clone fork to local repository
- Create a new branch and work on it
- Keep your branch in sync
- Commit your changes (make sure your commit message concise)
- Push your commits to your forked repository
- Create a pull request

Please refer to [CONTRIBUTING](./CONTRIBUTION.md) for detailed guidelines.

## License

The scripts and documentation in this project are released under the [MIT License](LICENSE).