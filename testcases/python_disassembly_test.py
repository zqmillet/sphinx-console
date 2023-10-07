from textwrap import dedent
from sphinxcontrib.console.execute import get_python_disassembly

def test_get_python_disassembly():
    assert "LOAD_CONST" in get_python_disassembly('a = 1')

def test_get_python_disassembly_with_begin_end():
    assert "LOAD_CONST" in get_python_disassembly('a = 1\nb = 1\nc = 1', begin=3)
    assert "LOAD_CONST" in get_python_disassembly('a = 1\nb = 1\nc = 1', begin=2, end=3)
