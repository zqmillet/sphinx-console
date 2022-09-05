"""
this module provides the function execute and contextmanager setup_and_teardown.
"""

from os import environ
from sys import executable
from contextlib import contextmanager

from pexpect import spawn
from pexpect import ExceptionPexpect

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

def interpret_python(lines, timeout=30, window_width=80, window_height=120):
    """
    this function is used to get output of python interpreter.
    """
    process = spawn(executable, encoding='utf8', timeout=timeout, env={**environ, 'TERM': 'xterm-256color'})
    process.setwinsize(window_height, window_width)
    process.expect('>>>')
    header = process.before
    auto_exit_expressions = ['', 'exit() # auto exit']

    output = ''
    try:
        for line in lines + auto_exit_expressions:
            process.sendline(line)

        output = '>>>' + process.read().rstrip()
    except ExceptionPexpect as exception:
        output = '>>>' + process.before.replace('\r', '').rstrip()

    # remote auto exit code.
    output_lines = output.splitlines()
    removed_count = 0
    for auto_exit_expression, output_line in zip(auto_exit_expressions[::-1], output_lines[::-1]):
        if '>>> ' + auto_exit_expression == output_line:
            removed_count += 1
            continue
        break

    for _ in range(removed_count):
        output_lines.pop()

    return header, '\n'.join(line.rstrip() for line in output_lines).rstrip()

@contextmanager
def setup_and_teardown(setup, teardown):
    """
    this is a contextmanager that can execute setup and teardown.
    """
    if setup:
        print('executing setup', setup)
        print(execute(setup))

    yield

    if teardown:
        print('executing teardown', teardown)
        print(execute(teardown))
