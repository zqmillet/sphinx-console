"""
this module provides the Python directive.
"""

from docutils.parsers.rst.directives.misc import Raw
from docutils.parsers.rst import directives
from ansi2html import Ansi2HTMLConverter
from mezmorize import Cache

from .execute import setup_and_teardown
from .execute import interpret_python
from .execute import wrap_content
from .execute import wrap_header
from .validators import parse_overflow
from .validators import parse_theme

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
        'hide_information': directives.flag,
        'font_size': directives.unchanged,
        'theme': parse_theme,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.state.document.settings.env.config.sphinx_console_cache_dir:
            self.interpret_python = Cache(
                CACHE_TYPE='filesystem',
                CACHE_DIR=self.state.document.settings.env.config.sphinx_console_cache_dir
            ).memoize()(interpret_python)
        else:
            self.interpret_python = interpret_python

    def run(self):
        overflow_style = 'overflow-x:scroll;' if self.options.get('overflow', 'scroll') == 'scroll' else 'white-space:pre-wrap;'
        display_command = 'python\n'
        timeout = self.options.get('timeout', 30)
        window_width = self.options.get('window_width', 80)
        window_height = self.options.get('window_height', 120)
        font_size = self.options.get('font_size')
        theme = self.options.get('theme', 'dark')

        self.arguments[:] = ['html']
        convertor = Ansi2HTMLConverter(dark_bg=(theme == 'dark'), line_wrap=False, inline=True)

        with setup_and_teardown(self.options.get('setup'), self.options.get('teardown')):
            information, output = self.interpret_python(
                lines=self.content.data,
                timeout=timeout,
                window_height=window_height,
                window_width=window_width,
            )

        header = wrap_header(display_command, information, 'hide_information' in self.options, theme)
        html = convertor.convert(header + output)
        self.content[0] = wrap_content(html, overflow_style, theme, font_size)
        self.content[:] = self.content[:1]

        return super().run()
