from sphinx_console.bash import execute

def test_execute_ls():
    output = execute('ls')
    assert 'LICENSE' in output
    assert 'testcases' in output

def test_execute_ping():
    output = execute('ping localhost -c 4')
    assert '4 packets transmitted' in output

def test_execute_ping_with_timeout():
    output = execute('ping localhost', timeout=3)
    assert 'icmp_seq' in output
    assert '4 packets transmitted' not in output

def test_execute_python():
    output = execute('python3', timeout=1)
    assert 'Python' in output

def test_execute_nonexistent_cmd():
    output = execute('gouliguojiashengsiyi')
    assert output == 'The command was not found or was not executable: gouliguojiashengsiyi.'

def test_execute_python_with_exit():
    output = execute('python3', interactions=[('>>>', '1 + 2'), ('>>>', 'exit()')])
    assert '>>> 1 + 2' in output
    assert '>>> exit()' in output
