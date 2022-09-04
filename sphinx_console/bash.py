"""
this module provides the Bash directive.
"""

from textwrap import wrap
from json import loads

from docutils.parsers.rst.directives.misc import Raw
from docutils.parsers.rst import directives
from ansi2html import Ansi2HTMLConverter
from colorama import Style
from colorama import Fore
from bs4 import BeautifulSoup
from css_inline import inline # pylint: disable = no-name-in-module

from .execute import execute
from .execute import setup_and_teardown

def parse_interactions(argument):
    """
    this function is used to parse interactions parameter.
    """
    return loads(argument)

def parse_overflow(argument):
    """
    this function is used to parse overflow parameter.
    """
    return directives.choice(argument, ('wrap', 'scroll'))

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
        'overflow': parse_overflow,
        'setup': directives.unchanged,
        'teardown': directives.unchanged,
        'window_width': directives.positive_int,
        'window_height': directives.positive_int,
    }

    def run(self):
        command = str(self.content[0])
        overflow_style = 'overflow-x:scroll;' if self.options.get('overflow', 'scroll') == 'scroll' else 'white-space:pre-wrap;'

        do_not_run = 'do_not_run' in self.options
        display_command = self.options.get('display_command', command)
        timeout = self.options.get('timeout', 30)
        interactions = self.options.get('interactions', None)
        window_width = self.options.get('window_width', 80)
        window_height = self.options.get('window_height', 120)

        self.arguments[:] = ['html']
        convertor = Ansi2HTMLConverter(dark_bg=True, line_wrap=False, inline=True, font_size='10pt')

        with setup_and_teardown(self.options.get('setup'), self.options.get('teardown')):
            output = ('\n' + execute(command, timeout=timeout, interactions=interactions, window_width=window_width, window_height=window_height)) if not do_not_run else ''

        header = f'{Style.BRIGHT}{Fore.RED}${Fore.WHITE} {display_command}{Fore.RESET}{Style.RESET_ALL}'
        html = convertor.convert(header + output)
        soup = BeautifulSoup(inline(html), features="html.parser")
        soup.pre.attrs.update(soup.body.attrs)
        soup.pre['style'] += ';padding: 10px; margin-bottom: 24px;' + overflow_style
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
