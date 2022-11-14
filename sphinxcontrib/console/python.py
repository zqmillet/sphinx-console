
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
from .execute import interpret_python
from .execute import setup_and_teardown
from .execute import wrap_header
from .execute import wrap_content
from .utilities import caption_wrapper

class PythonNode(General, Element):
    """
    python directive.
    """

class PythonContentNode(General, Element):
    """
    content of python.
    """

class PythonCaptionNode(caption):
    """
    caption of python directive.
    """

class PythonDirective(SphinxDirective):
    """
    an environment for python.
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True

    option_spec = {
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
        'hide-information': directives.flag,
    }

    def run(self):
        """Render this environment"""
        overflow_style = 'overflow-x:auto;' if self.options.get('overflow', 'scroll') == 'scroll' else 'white-space:pre-wrap;'
        display_command = 'python\n'
        timeout = self.options.get('timeout', 30)
        window_width = self.options.get('window-width', 80)
        window_height = self.options.get('window-height', 120)
        font_size = self.options.get('font-size')
        theme = self.options.get('theme', 'dark')
        hide_information = self.options.get('hide-information', False)

        self.arguments[:] = ['html']
        convertor = Ansi2HTMLConverter(dark_bg=(theme == 'dark'), line_wrap=False, inline=True)

        with setup_and_teardown(self.options.get('setup'), self.options.get('teardown')):
            information, output = interpret_python(
                lines=self.content.data,
                timeout=timeout,
                window_height=window_height,
                window_width=window_width,
            )

        header = wrap_header(display_command, '', False, theme)
        html = convertor.convert(header + ('' if hide_information else information) + output)
        node = caption_wrapper(self, PythonNode(), PythonCaptionNode, self.options.get("caption"))

        content = PythonContentNode()
        content.children.append(raw('', wrap_content(html, overflow_style, theme, font_size), format='html'))
        node.children.append(content)
        self.add_name(node)
        return [node]

def visit_python_node(self, node):
    """
    enter :class:`PythonNode` in html builder.
    """
    self.body.append(self.starttag(node, "div", CLASS="python"))

def depart_python_node(self, node):
    """
    leave :class:`PythonNode` in html builder.
    """
    self.body.append("</div>")

def visit_caption_node(self, node):
    """
    enter :class:`PythonCaptionNode` in html builder
    """
    if not node.astext():
        return

    self.body.append(self.starttag(node, "div", CLASS="python-caption"))
    self.add_fignumber(node.parent)
    self.body.append(" — ")
    self.body.append(self.starttag(node, "span", CLASS="caption-text"))

def depart_caption_node(self, node):
    """
    leave :class:`PythonCaptionNode` in html builder
    """
    if not node.astext():
        return

    self.body.append("</span>")
    self.body.append("</div>")

def visit_content_node(self, node):
    """
    enter :class:`PythonContentNode` in html builder.
    """
    self.body.append(self.starttag(node, "div", CLASS='highlight-rst notranslate highlight'))

def depart_content_node(self, node):
    """
    leave :class:`PythonContentNode` in HTML builder.
    """
    self.body.append("</div>")

def initialize_numfig_format(application, config):
    """
    initialize :confval:`numfig_format`.
    """
    config.numfig_format['python'] = 'Python %s'

def setup(application: Sphinx):
    """
    setup python directive.
    """

    application.add_directive('python', PythonDirective)

    application.connect(event="config-inited", callback=initialize_numfig_format)

    application.add_enumerable_node(
        node=PythonNode,
        figtype='python',
        html=(visit_python_node, depart_python_node),
        singlehtml=(visit_python_node, depart_python_node),
    )
    application.add_node(
        node=PythonCaptionNode,
        override=True,
        html=(visit_caption_node, depart_caption_node),
        singlehtml=(visit_caption_node, depart_caption_node),
    )
    application.add_node(
        node=PythonContentNode,
        html=(visit_content_node, depart_content_node),
        singlehtml=(visit_content_node, depart_content_node),
    )
