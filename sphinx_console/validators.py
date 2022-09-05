"""
this module provides some validators.
"""

from json import loads

from docutils.parsers.rst import directives

def parse_interactions(argument):
    """
    this function is used to parse interactions parameter.
    """
    return loads(argument)

def parse_overflow(argument):
    """
    this function is used to parse overflow parameter.
    """
    return directives.choice(argument, ('wrap', 'scroll'))
