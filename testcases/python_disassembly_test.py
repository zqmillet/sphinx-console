from textwrap import dedent
from sphinxcontrib.console.execute import get_python_disassembly

def test_get_python_disassembly():
    assert get_python_disassembly('a = 1') == dedent(
        '''
        1           0 LOAD_CONST               0 (1)
                    2 STORE_NAME               0 (a)
                    4 LOAD_CONST               1 (None)
                    6 RETURN_VALUE
        '''
    ).strip()

def test_get_python_disassembly_with_begin_end():
    assert get_python_disassembly('a = 1\nb = 1\nc = 1', begin=3) == dedent(
        '''
        3           0 LOAD_CONST               0 (1)
                    2 STORE_NAME               0 (c)
                    4 LOAD_CONST               1 (None)
                    6 RETURN_VALUE
        '''
    ).strip()

    assert get_python_disassembly('a = 1\nb = 1\nc = 1', begin=2, end=3) == dedent(
        '''
        2           0 LOAD_CONST               0 (1)
                    2 STORE_NAME               0 (b)

        3           4 LOAD_CONST               0 (1)
                    6 STORE_NAME               1 (c)
                    8 LOAD_CONST               1 (None)
                   10 RETURN_VALUE
        '''
    ).strip()
