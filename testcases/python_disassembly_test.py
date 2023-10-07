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
    assert get_python_disassembly('a = 1\nb = 1\nc = 1', begin=3).strip().startswith('3')
    assert get_python_disassembly('a = 1\nb = 1\nc = 1', begin=2, end=3).strip().startswith('2')
