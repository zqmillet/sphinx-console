from platform import system

from sphinx.util.docutils import SphinxDirective

class Directive(SphinxDirective):
    @property
    def do_not_run(self):
        if system() == 'Windows':
            return True
        return 'do-not-run' in self.options
