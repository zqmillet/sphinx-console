"""
this module provides the Python directive.
"""

from docutils.parsers.rst.directives.misc import Raw
from docutils.parsers.rst import directives
from ansi2html import Ansi2HTMLConverter
from colorama import Style
from colorama import Fore
from bs4 import BeautifulSoup
from css_inline import inline # pylint: disable = no-name-in-module

from .execute import setup_and_teardown
from .validators import parse_overflow
from .execute import interpret_python

class Python(Raw):
    """
    this directive is used to display bash and its output.
    """
    has_content = True
    required_arguments = 0

    option_spec = {
        'timeout': directives.nonnegative_int,
        'overflow': parse_overflow,
        'setup': directives.unchanged,
        'teardown': directives.unchanged,
        'window_width': directives.positive_int,
        'window_height': directives.positive_int,
        'hide_header': directives.flag,
    }

    def run(self):
        overflow_style = 'overflow-x:scroll;' if self.options.get('overflow', 'scroll') == 'scroll' else 'white-space:pre-wrap;'
        display_command = 'python\n'
        timeout = self.options.get('timeout', 30)
        window_width = self.options.get('window_width', 80)
        window_height = self.options.get('window_height', 120)

        self.arguments[:] = ['html']
        convertor = Ansi2HTMLConverter(dark_bg=True, line_wrap=False, inline=True, font_size='10pt')

        with setup_and_teardown(self.options.get('setup'), self.options.get('teardown')):
            header, output = interpret_python(
                lines=self.content.data,
                timeout=timeout,
                window_height=window_height,
                window_width=window_width,
            )

        if 'hide_header' not in self.options:
            header = f'{Style.BRIGHT}{Fore.RED}${Fore.WHITE} {display_command}{Fore.RESET}{Style.RESET_ALL}{header}'
        else:
            header = f'{Style.BRIGHT}{Fore.RED}${Fore.WHITE} {display_command}{Fore.RESET}{Style.RESET_ALL}'

        html = convertor.convert(header + output)
        soup = BeautifulSoup(inline(html), features="html.parser")
        soup.pre.attrs.update(soup.body.attrs)
        soup.pre['style'] += ';padding: 10px; margin-bottom: 24px;' + overflow_style
        self.content[0] = str(soup.pre)
        self.content[:] = self.content[:1]

        return super().run()
