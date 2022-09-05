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

    assert pres[0].text.endswith(
        dedent(
            '''
            >>> 1 + 1
            2
            '''
        )
    )

    assert pres[1].text.endswith(
        dedent(
            '''
            >>> exit()
            '''
        )
    )

    assert pres[2].text.endswith(
        dedent(
            '''
            >>> from math import e
            >>> e
            2.718281828459045
            >>>
            >>> for i in range(10):
            ...     print(i)
            ...
            0
            1
            2
            3
            4
            5
            6
            7
            8
            9
            >>> print(2333)
            2333
            '''
        )
    )
