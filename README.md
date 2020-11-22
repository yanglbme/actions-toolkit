# Actions Toolkit

The GitHub Actions ToolKit provides a set of packages to make creating actions easier in Python.

[![Downloads](https://pepy.tech/badge/actions-toolkit/month)](https://pepy.tech/project/actions-toolkit/month)
[![Supported Versions](https://img.shields.io/pypi/pyversions/actions-toolkit.svg)](https://pypi.org/project/actions-toolkit)
[![Pypi Versions](https://img.shields.io/pypi/v/actions-toolkit.svg)](https://pypi.python.org/pypi/actions-toolkit)
[![Contributors](https://img.shields.io/github/contributors/yanglbme/actions-toolkit.svg)](https://github.com/yanglbme/actions-toolkit/graphs/contributors)

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

## License

The scripts and documentation in this project are released under the [MIT License](LICENSE).