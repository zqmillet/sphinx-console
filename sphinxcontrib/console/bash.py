from docutils.parsers.rst import directives
from docutils.nodes import raw
from docutils.nodes import General
from docutils.nodes import Element
from docutils.nodes import caption
from sphinx.util.docutils import SphinxDirective
from sphinx.application import Sphinx
from mezmorize import Cache
from ansi2html import Ansi2HTMLConverter

from .validators import parse_interactions
from .validators import parse_overflow
from .validators import parse_theme
from .execute import execute
from .execute import setup_and_teardown
from .execute import wrap_header
from .execute import wrap_content
from .utilities import caption_wrapper

class BashNode(General, Element):
    """
    bash directive.
    """

class BashContentNode(General, Element):
    """
    content of bash.
    """

class BashCaptionNode(caption):
    """
    caption of bash directive.
    """

class BashDirective(SphinxDirective):
    """
    an environment for bash
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True

    option_spec = {
        'do-not-run': directives.flag,
        'display-command': directives.unchanged,
        'timeout': directives.nonnegative_int,
        'interactions': parse_interactions,
        'overflow': parse_overflow,
        'setup': directives.unchanged,
        'teardown': directives.unchanged,
        'window-width': directives.positive_int,
        'window-height': directives.positive_int,
        'font-size': directives.unchanged,
        'theme': parse_theme,
        'caption': directives.unchanged_required,
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
        """Render this environment"""
        command, *custom_output = self.content
        custom_output = '\n'.join(custom_output)
        overflow_style = 'overflow-x:auto;' if self.options.get('overflow', 'scroll') == 'scroll' else 'white-space:pre-wrap;'
        do_not_run = 'do-not-run' in self.options
        display_command = self.options.get('display-command', command)
        timeout = self.options.get('timeout', 30)
        interactions = self.options.get('interactions', None)
        window_width = self.options.get('window-width', 80)
        window_height = self.options.get('window-height', 120)
        font_size = self.options.get('font-size')
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
        node = caption_wrapper(self, BashNode(), BashCaptionNode, self.options.get("caption"))

        content = BashContentNode()
        content.children.append(raw('', wrap_content(html, overflow_style, theme, font_size), format='html'))
        node.children.append(content)
        self.add_name(node)
        return [node]

def visit_bash_node(self, node):
    """
    enter :class:`BashNode` in html builder.
    """
    self.body.append(self.starttag(node, "div", CLASS="bash"))

def depart_bash_node(self, node):
    """
    leave :class:`BashNode` in html builder.
    """
    self.body.append("</div>")

def visit_caption_node(self, node):
    """
    enter :class:`BashCaptionNode` in html builder
    """
    if not node.astext():
        return

    self.body.append(self.starttag(node, "div", CLASS="bash-caption"))
    self.add_fignumber(node.parent)

    self.body.append(" — ")
    self.body.append(self.starttag(node, "span", CLASS="caption-text"))

def depart_caption_node(self, node):
    """
    leave :class:`BashCaptionNode` in html builder
    """
    if not node.astext():
        return

    self.body.append("</span>")
    self.body.append("</div>")

def visit_content_node(self, node):
    """
    enter :class:`BashContentNode` in html builder.
    """
    self.body.append(self.starttag(node, "div", CLASS='highlight-rst notranslate highlight'))

def depart_content_node(self, node):
    """
    leave :class:`BashContentNode` in HTML builder.
    """
    self.body.append("</div>")

def initialize_numfig_format(application, config):
    """
    initialize :confval:`numfig_format`.
    """
    config.numfig_format['bash'] = 'Bash %s'

def setup(application: Sphinx):
    """
    setup bash directive.
    """

    application.add_directive('bash', BashDirective)

    application.connect(event="config-inited", callback=initialize_numfig_format)

    application.add_enumerable_node(
        node=BashNode,
        figtype='bash',
        html=(visit_bash_node, depart_bash_node),
        singlehtml=(visit_bash_node, depart_bash_node),
    )
    application.add_node(
        node=BashCaptionNode,
        override=True,
        html=(visit_caption_node, depart_caption_node),
        singlehtml=(visit_caption_node, depart_caption_node),
    )
    application.add_node(
        node=BashContentNode,
        html=(visit_content_node, depart_content_node),
        singlehtml=(visit_content_node, depart_content_node),
    )
