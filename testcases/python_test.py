from pytest import fixture
from pytest import mark
from bs4 import BeautifulSoup
from textwrap import dedent

@fixture
def build_all(app):
    app.builder.build_all()

@fixture
def index(app, build_all):
    return (app.outdir / 'index.html').read_text()

@mark.sphinx('html', testroot='python')
def test_python(index):
    soup = BeautifulSoup(index, 'html.parser')
    pres = soup.find_all('pre')

    # assert pres[0].text.endswith(
    #     dedent(
    #         '''
    #         >>> 1 + 1
    #         2
    #         '''
    #     )
    # )

    # assert pres[1].text.endswith(
    #     dedent(
    #         '''
    #         >>> exit()
    #         '''
    #     )
    # )

    print(pres[0].text)
