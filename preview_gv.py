import sublime, sublime_plugin

import os
import re
import tempfile

from subprocess import call, Popen

ENVIRON = os.environ
ENVIRON['PATH'] += ':/usr/local/bin'

DIGRAPH_START = re.compile('.*(digraph([ \t\n\r]+[a-zA-Z\200-\377_][a-zA-Z\200-\3770-9_]*[ \t\n\r]*{|[ \t\n\r]*{).*)', re.DOTALL | re.IGNORECASE)

def surroundingGraphviz(data, cursor):
    '''
    Find graphviz code in source surrounding the cursor.
    '''
    data_before = data[0:cursor]
    data_after = data[cursor:]

    # find code before selector
    code_before_match = DIGRAPH_START.match(data_before)
    if not code_before_match:
        return None
    code_before = code_before_match.group(1)
    unopened_braces = len(code_before.split('{')) - len(code_before.split('}'))

    # cursor must be in the middle of the graphviz code
    if unopened_braces <= 0:
        return None

    # find code after selector
    code_after_match = re.compile('(' + ('.*\\}' * unopened_braces) + ').*', re.DOTALL).match(data_after)
    if not code_after_match:
        return None
    code_after = code_after_match.group(1)

    # done!
    code = code_before + code_after
    return code


def getText(code):
    # temporary graphviz file
    grapviz = tempfile.NamedTemporaryFile(prefix='sublime_text_graphviz_', dir=None, suffix='.viz', delete=False, mode='wb')
    grapviz.write(code.encode('utf-8'))
    grapviz.close()
    return grapviz.name

def selectionSfdp(code):
    file_name = getText(code)
    call(['sfdp', "-Tx11", file_name], env=ENVIRON)
    os.unlink(file_name)

def graphviz(dotfilter, code):
    file_name = getText(code)
    call(['xdot', "-f", dotfilter, file_name], env=ENVIRON)
    os.unlink(file_name)

def xdot(dotfilter, file_name):
    Popen(['xdot', "-f", dotfilter, file_name], env=ENVIRON);

def dot(command, file_name):
    Popen([command, "-Tx11", file_name], env=ENVIRON);

def selection(self):
    sel = self.view.sel()[0]

    if not sel.empty():
        code = self.view.substr(sel).strip()
    else:
        code = surroundingGraphviz(
            self.view.substr(sublime.Region(0, self.view.size())),
            sel.begin()
        )

    if not code:
        sublime.error_message('Graphviz: Please place cursor in graphviz code before running')
        return

    return code;

# command definitions for selection
class GraphvizPreviewDotCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        graphviz("dot",selection(self))

class GraphvizPreviewNeatoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        graphviz("neato",selection(self))

class GraphvizPreviewFdpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        graphviz("fdp",selection(self))

class GraphvizPreviewSfdpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selectionSfdp(selection(self))

class GraphvizPreviewCircoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        graphviz("circo",selection(self))

class GraphvizPreviewTwopiCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        graphviz("twopi",selection(self))

#command definition for file using xdot

class GraphvizPreviewFileXdotDotCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        fn = self.view.file_name()
        xdot("dot", fn)

class GraphvizPreviewFileXdotNeatoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        fn = self.view.file_name()
        xdot("neato",fn)

class GraphvizPreviewFileXdotFdpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        fn = self.view.file_name()
        xdot("fdp",fn)

class GraphvizPreviewFileXdotSfdpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        fn = self.view.file_name()
        dot('sfdp',fn)

class GraphvizPreviewFileXdotCircoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        fn = self.view.file_name()
        xdot("circo",fn)

class GraphvizPreviewFileXdotTwopiCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        fn = self.view.file_name()
        xdot("twopi",fn)

#command definition for file using graphviz commands

class GraphvizPreviewFileGvDotCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        fn = self.view.file_name()
        dot("dot", fn)

class GraphvizPreviewFileGvNeatoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        fn = self.view.file_name()
        dot("neato",fn)

class GraphvizPreviewFileGvFdpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        fn = self.view.file_name()
        dot("fdp",fn)

class GraphvizPreviewFileGvSfdpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        fn = self.view.file_name()
        dot('sfdp',fn)

class GraphvizPreviewFileGvCircoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        fn = self.view.file_name()
        dot("circo",fn)

class GraphvizPreviewFileGvTwopiCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        fn = self.view.file_name()
        dot("twopi",fn)

