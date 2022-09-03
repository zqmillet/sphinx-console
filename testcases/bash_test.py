from pytest import fixture
from pytest import mark
from bs4 import BeautifulSoup

@fixture
def build_all(app):
    app.builder.build_all()

@fixture
def index(app, build_all):
    return (app.outdir / 'index.html').read_text()

@mark.sphinx('html', testroot='bash')
def test_bash(index):
    soup = BeautifulSoup(index, 'html.parser')

    pre_blocks = soup.find_all('pre')
    assert len(pre_blocks) == 4

    assert pre_blocks[0].text.strip() == '$ ls -al'

    assert 'LICENSE' in pre_blocks[1].text
    assert 'sphinx_console' in pre_blocks[1].text

    assert '>>> 1 + 2\n3' in pre_blocks[2].text
    assert '>>> exit()' in pre_blocks[2].text

    assert pre_blocks[3].text.strip().startswith('$ rich')
