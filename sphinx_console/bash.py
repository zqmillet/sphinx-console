"""
this module provides the Bash directive.
"""

from docutils.parsers.rst.directives.misc import Raw
from docutils.parsers.rst import directives
from ansi2html import Ansi2HTMLConverter
from colorama import Style
from colorama import Fore
from pexpect import spawn
from pexpect import ExceptionPexpect
from pexpect import EOF
from bs4 import BeautifulSoup
from css_inline import inline # pylint: disable = no-name-in-module
from json import loads
from os import environ

def execute(command: str, timeout=30, interactions=None) -> str:
    """
    this function is used to execute the command and get its output.
    """
    interactions = interactions or []
    try:
        process = spawn('TERM=vt100 ' + command, timeout=timeout, encoding='utf8', env={**environ, 'TERM': 'xterm-256color'})
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

def parse_interactions(argument):
    return loads(argument)

class Bash(Raw):
    """
    this directive is used to display bash and its output.
    """
    has_content = True
    required_arguments = 0

    option_spec = {
        'do_not_run': directives.flag,
        'display_command': directives.unchanged,
        'timeout': directives.nonnegative_int,
        'interactions': parse_interactions,
    }

    def run(self):
        command = '\n'.join(self.content)

        do_not_run = 'do_not_run' in self.options
        display_command = self.options.get('display_command', command)
        timeout = self.options.get('timeout', 30)
        interactions = self.options.get('interactions', None)

        self.arguments[:] = ['html']
        convertor = Ansi2HTMLConverter(dark_bg=True, line_wrap=False, inline=True, font_size='10pt')
        output = ('\n' + execute(command, timeout=timeout, interactions=interactions)) if not do_not_run else ''
        header = f'{Style.BRIGHT}{Fore.RED}${Fore.WHITE} {display_command}{Fore.RESET}{Style.RESET_ALL}'
        html = convertor.convert(header + output)
        soup = BeautifulSoup(inline(html), features="html.parser")
        soup.pre.attrs.update(soup.body.attrs)
        soup.pre['style'] += ';padding: 10px'
        self.content[0] = str(soup.pre)

        return super().run()

def setup(app):
    """
    this is the setup function for this directive.
    """
    app.add_directive('bash', Bash)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True
    }
