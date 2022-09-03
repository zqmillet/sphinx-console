from pytest import fixture
from sphinx.testing.path import path

pytest_plugins = 'sphinx.testing.fixtures'

@fixture(scope='session')
def rootdir():
    return path(__file__).parent.abspath() / 'statics'
