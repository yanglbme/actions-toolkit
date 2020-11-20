import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='actions-toolkit',
    version='0.0.5',
    description='🛠 The GitHub ToolKit for developing GitHub Actions in Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='yanglbme',
    author_email='contact@yanglibin.info',
    url='https://github.com/yanglbme/actions-toolkit',
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
