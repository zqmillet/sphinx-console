from os.path import dirname
from sys import path

path.append(dirname(dirname(__file__)))

author = 'kinopico'
project = 'the manual of sphinx-console'
html_favicon = './statics/logo.png'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_console',
]

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

autodoc_default_options = {
    'member-order': 'bysource',
    'special-members': True,
    'exclude-members': 'request, __weakref__',
}
autodoc_typehints = 'both'
autodoc_class_signature = 'separated'

autodoc_pydantic_model_show_json = False
autodoc_pydantic_settings_show_json = False
