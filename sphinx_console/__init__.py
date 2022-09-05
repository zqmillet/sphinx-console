"""
this module provides the setup function.
"""

from .bash import Bash
from .python import Python

VERSION = (1, 0, 1)

def setup(app):
    """
    this is the setup function for this directive.
    """
    app.add_directive('bash', Bash)
    app.add_directive('python', Python)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True
    }
