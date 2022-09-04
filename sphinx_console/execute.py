from os import environ
from contextlib import contextmanager

from pexpect import spawn
from pexpect import ExceptionPexpect
from pexpect import EOF

def execute(command: str, timeout=30, interactions=None, window_width=80, window_height=120) -> str:
    """
    this function is used to execute the command and get its output.
    """
    if not command:
        return ''

    interactions = interactions or []
    try:
        process = spawn(command, timeout=timeout, encoding='utf8', env={**environ, 'TERM': 'xterm-256color'})
        process.setwinsize(window_height, window_width)
    except ExceptionPexpect as exception:
        return exception.value

    output = ''
    try:
        for pattern, action in interactions:
            process.expect(pattern)
            process.sendline(action)
            output += process.before + process.after
        output += process.read()
    except ExceptionPexpect:
        output += process.buffer

    return output.strip()

@contextmanager
def setup_and_teardown(setup, teardown):
    if setup:
        print('executing setup', setup)
        print(execute(setup))

    yield

    if teardown:
        print('executing teardown', teardown)
        print(execute(teardown))
