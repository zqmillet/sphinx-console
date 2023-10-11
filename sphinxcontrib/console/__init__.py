"""
this is the package sphinxcontrib.console.
"""
__version__ = (1, 0, 12)

from os.path import join
from os.path import dirname

from sphinx.util.fileutil import copy_asset

from .bash import setup as setup_bash
from .python import setup as setup_python
from .disassembly import setup as setup_disassembly

def copy_asset_files(application, execution):
    """
    this function is used to copy css file to build directory.
    """
    asset_files = [join(dirname(__file__), 'sphinx_console.css')]
    if execution is None: # build succeede
        for path in asset_files:
            copy_asset(path, join(application.outdir, '_static'))

def setup(application):
    """
    setup extension.
    """
    setup_bash(application)
    setup_python(application)
    setup_disassembly(application)

    application.add_config_value('sphinx_console_cache_dir', None, '')
    application.add_css_file('sphinx_console.css')
    application.connect('build-finished', copy_asset_files)

    return {"version": __version__, "parallel_read_safe": True}
