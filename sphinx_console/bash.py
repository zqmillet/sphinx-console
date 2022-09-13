"""
this module provides the Bash directive.
"""

from docutils.parsers.rst.directives.misc import Raw
from docutils.parsers.rst import directives
from ansi2html import Ansi2HTMLConverter
from colorama import Style
from colorama import Fore
from bs4 import BeautifulSoup
from css_inline import inline # pylint: disable = no-name-in-module
from mezmorize import Cache

from .execute import execute
from .execute import setup_and_teardown
from .execute import wrap_header
from .execute import wrap_content

from .validators import parse_interactions
from .validators import parse_overflow
from .validators import parse_theme

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
        'font_size': directives.unchanged,
        'theme': parse_theme,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.state.document.settings.env.config.sphinx_console_cache_dir:
            self.execute = Cache(
                CACHE_TYPE='filesystem',
                CACHE_DIR=self.state.document.settings.env.config.sphinx_console_cache_dir
            ).memoize()(execute)
        else:
            self.execute = execute

    def run(self):
        command, *custom_output = self.content
        custom_output = '\n'.join(custom_output)

        overflow_style = 'overflow-x:scroll;' if self.options.get('overflow', 'scroll') == 'scroll' else 'white-space:pre-wrap;'

        do_not_run = 'do_not_run' in self.options
        display_command = self.options.get('display_command', command)
        timeout = self.options.get('timeout', 30)
        interactions = self.options.get('interactions', None)
        window_width = self.options.get('window_width', 80)
        window_height = self.options.get('window_height', 120)
        font_size = self.options.get('font_size')
        theme = self.options.get('theme', 'dark')

        self.arguments[:] = ['html']
        convertor = Ansi2HTMLConverter(dark_bg=(theme == 'dark'), line_wrap=False, inline=True)

        with setup_and_teardown(self.options.get('setup'), self.options.get('teardown')):
            output = custom_output or (
                '\n' + self.execute(
                    command=command,
                    timeout=timeout,
                    interactions=interactions,
                    window_width=window_width,
                    window_height=window_height
                )
            ) if not do_not_run else ''

        header = wrap_header(display_command, '', False, theme)
        html = convertor.convert(header + output)
        self.content[0] = wrap_content(html, overflow_style, theme, font_size)
        self.content[:] = self.content[:1]

        return super().run()
