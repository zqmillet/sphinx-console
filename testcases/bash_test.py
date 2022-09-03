from pytest import fixture
from pytest import mark

@fixture
def build_all(app):
    app.builder.build_all()

@fixture
def index(app, build_all):
    return (app.outdir / 'index.html').read_text()

@mark.sphinx('html', testroot='bash')
def test_bash(index):
    print(index)
