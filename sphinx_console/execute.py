"""
this module provides the function execute and contextmanager setup_and_teardown.
"""

from os import environ
from sys import executable
from re import sub
from contextlib import contextmanager
from time import sleep

from pexpect import spawn
from pexpect import ExceptionPexpect
from bs4 import BeautifulSoup
from css_inline import inline # pylint: disable = no-name-in-module
from colorama import Style
from colorama import Fore

def wrap_header(display_command, information, hide_information, theme):
    header = f'{Style.BRIGHT}{Fore.RED}${Fore.WHITE if theme == "dark" else Fore.BLACK} {display_command}{Fore.RESET}{Style.RESET_ALL}'
    if not hide_information:
        header += information
    return header

def wrap_content(html, overflow_style, theme, font_size):
    soup = BeautifulSoup(inline(html), features="html.parser")
    soup.pre.attrs['class'] = []
    soup.pre['style'] = overflow_style

    if theme == 'dark':
        soup.pre['style'] += 'color: #BBBBBB;background-color: #000000;'

    if font_size:
        soup.pre['style'] += f'font-size: {font_size}'

    return f'<div class="highlight-rst notranslate"><div class="highlight">{str(soup.pre).strip()}</div></div>'

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

    return output.rstrip()

def interpret_python(lines, timeout=30, window_width=80, window_height=120, interval=0.1):
    """
    this function is used to get output of python interpreter.
    """
    process = spawn(executable, encoding='utf8', timeout=timeout, env={**environ, 'TERM': 'xterm-256color'})
    process.setwinsize(window_height, window_width)
    process.expect('>>>')
    header = sub(r'\x1b(\[.*?[@-~]|\].*?(\x07|\x1b\\))', '', process.before)
    auto_exit_expressions = ['', 'exit() # auto exit']

    output = ''
    try:
        for line in lines + auto_exit_expressions:
            sleep(interval)
            if not process.isalive():
                break
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
