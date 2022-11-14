from os.path import dirname
from sys import path

path.insert(0, dirname(dirname(__file__)))

author = 'kinopico'
project = 'the manual of sphinx-console'
html_favicon = './statics/logo.png'

extensions = [
    'sphinx.ext.autodoc',
    'sphinxcontrib.console',
]

numfig = True
numfig_format = {
    'code-block': '代码 %s',
    'figure': '图 %s',
    'section': '章节 %s',
    'bash': '控制台 %s',
}

rst_prolog = '''
.. role:: py(code)
   :language: py
   :class: highlight

.. role:: sh(code)
   :language: console
   :class: highlight
'''

html_theme = 'sphinx_rtd_theme'
source_suffix = ['.rst']

sphinx_console_cache_dir = '../.cache'
