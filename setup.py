from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='actions-toolkit',
    version='0.1.12',
    description='🛠 The GitHub ToolKit for developing GitHub Actions in Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='yanglbme',
    author_email='contact@yanglibin.info',
    url='https://github.com/yanglbme/actions-toolkit',
    packages=find_packages(),
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'requests',
        'PyGithub'
    ],
    python_requires='>=3.6',
)
