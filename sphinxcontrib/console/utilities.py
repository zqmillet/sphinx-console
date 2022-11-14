"""
this module provides utilities.
"""

from docutils.nodes import Element
from docutils.statemachine import ViewList

def caption_wrapper(directive, node, caption_node_class, caption=None):
    """
    parse caption, and append it to the node.
    """
    if caption is None:
        caption_node = caption_node_class()
    else:
        parsed = Element()
        directive.state.nested_parse(ViewList([caption], source=""), directive.content_offset, parsed)
        paragraph, *_ = parsed
        caption_node = caption_node_class(paragraph.rawsource, "", *paragraph.children)
        caption_node.source = paragraph.source
        caption_node.line = paragraph.line
    node += caption_node
    return node
