"""
this is the setup of this package.
"""

from setuptools import setup
from setuptools import find_packages

from sphinxcontrib.console import __version__

with open('sphinxcontrib/requirements.txt', 'r', encoding='utf8') as file:
    install_requires = list(map(lambda x: x.strip(), file.readlines()))

setup(
    name='sphinx_console',
    version='.'.join(map(str, __version__)),
    author='kinopico',
    author_email='zqmillet@qq.com',
    url='https://github.com/zqmillet/sphinx-console',
    description='an extension for sphinx to display console in sphinx documents',
    packages=find_packages(),
    install_requires=install_requires,
)
