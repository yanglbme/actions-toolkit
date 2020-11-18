import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='actions_toolkit',
    version='0.0.1',
    description='A Python toolkit for building GitHub Actions',
    author='yanglbme',
    author_email='contact@yanglibin.info',
    url="https://github.com/yanglbme/actions-toolkit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)