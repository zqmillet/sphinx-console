"""
this is the call entry of this module.
"""

from . import VERSION

print('hello, sphinx-console')
print('version:', '.'.join(map(str, VERSION)))
