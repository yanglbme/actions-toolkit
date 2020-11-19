# Actions Toolkit

**Actions Toolkit** is A GitHub Actions Development Tools in Python.

[![Downloads](https://pepy.tech/badge/actions-toolkit/month)](https://pepy.tech/project/actions-toolkit/month)
[![Supported Versions](https://img.shields.io/pypi/pyversions/actions-toolkit.svg)](https://pypi.org/project/actions-toolkit)
[![Contributors](https://img.shields.io/github/contributors/yanglbme/actions-toolkit.svg)](https://github.com/yanglbme/actions-toolkit/graphs/contributors)

```python
>>> import os
>>> from actions_toolkit import core
>>> os.environ['INPUT_NAME'] = 'Actions Toolkit'
>>> core.get_input('name')
'Actions Toolkit'
>>> core.error('something got wrong')
::error::something got wrong
>>> core.info('run successfully')
run successfully
>>> core.set_failed('error occurred')
::error::error occurred
```

## Installing Actions Toolkit and Supported Versions

Action Toolkit is available on PyPI:

```bash
$ python -m pip install actions-toolkit
```

Action Toolkit officially supports Python 3.6+.

## License

MIT