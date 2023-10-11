from platform import system

from pytest import mark
from sphinxcontrib.console.bash import execute

@mark.skipif(system() == 'Windows', reason='only for macos and linux')
def test_execute_ls():
    output = execute('ls')
    assert 'LICENSE' in output
    assert 'testcases' in output

@mark.skipif(system() == 'Windows', reason='only for macos and linux')
def test_execute_ping():
    output = execute('ping localhost -c 4')
    assert '4 packets transmitted' in output

@mark.skipif(system() == 'Windows', reason='only for macos and linux')
def test_execute_ping_with_timeout():
    output = execute('ping localhost', timeout=3)
    assert 'icmp_seq' in output
    assert '4 packets transmitted' not in output

@mark.skipif(system() == 'Windows', reason='only for macos and linux')
def test_execute_python():
    output = execute('python3', timeout=1)
    assert 'Python' in output

@mark.skipif(system() == 'Windows', reason='only for macos and linux')
def test_execute_nonexistent_cmd():
    output = execute('gouliguojiashengsiyi')
    assert 'command not found' in output.lower()

@mark.skipif(system() == 'Windows', reason='only for macos and linux')
def test_execute_python_with_exit():
    output = execute('python3', interactions=[('>>>', '1 + 2'), ('>>>', 'exit()')])
    assert '>>> 1 + 2' in output
    assert '>>> exit()' in output
