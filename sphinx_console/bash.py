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
from pexpect import TIMEOUT
from pexpect import EOF
from bs4 import BeautifulSoup
from css_inline import inline

def execute(command: str, timeout=30, interactions=None) -> str:
    interactions = interactions or [(EOF, '')]
    try:
        process = spawn(command, timeout=timeout, encoding='utf8') #.read().decode('utf8').strip()
    except ExceptionPexpect as exception:
        return exception.value

    output = ''
    try:
        for expect, action in interactions:
            process.expect(expect)
            process.sendline(action)
            output += process.before + process.after
        output += process.read()
    except ExceptionPexpect:
        output += process.buffer

    return output.strip()

class Bash(Raw):
    """
    this directive is used to display bash and its output.
    """
    has_content = True
    required_arguments = 0

    option_spec = {
        'norun': directives.flag,
        'real_cmd': directives.unchanged,
    }

    def run(self):
        self.arguments[:] = ['html']
        convertor = Ansi2HTMLConverter(dark_bg=True, line_wrap=False, inline=True, font_size='10pt')
        command = '\n'.join(self.content)
        output = execute(command)
        header = f'{Style.BRIGHT}{Fore.RED}${Fore.WHITE} {command}{Fore.RESET}{Style.RESET_ALL}'
        html = convertor.convert(header + '\n' + output)
        soup = BeautifulSoup(inline(html), features="html.parser")
        soup.pre.attrs.update(soup.body.attrs)
        soup.pre['style'] += ';padding: 10px'

        self.content[0] = str(soup.pre)

        return super().run()

def setup(app):
    app.add_directive('bash', Bash)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True
    }
