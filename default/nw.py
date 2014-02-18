"""XML: DEFAULT NodeWriters

Collection of NodeWriter objects to write an xml file by showing
its tree structure.

"""

import re
from lexor.core.writer import NodeWriter
import lexor.core.elements as core
RE = re.compile(r'\s+')


def printable_prev(node):
    """Check if any of node.prev is a printable text or entity
    node."""
    while node.prev is not None and node.prev.name in ['#entity', '#text']:
        if node.prev.data.strip() == '':
            node = node.prev
        else:
            return True
    return False


def printable_next(node):
    """Check if any of node.next is a printable text or entity node.
    """
    while node.next is not None and node.next.name in ['#entity', '#text']:
        if node.next.data.strip() == '':
            node = node.next
        else:
            return True
    return False


class TextNW(NodeWriter):
    """Writes text nodes with multiple spaces removed. """
    tab_printed = False

    def format(self, node):
        """This function may be used by other NodeWriters. If the
        node is indeed an entity node then it returns a formatted
        entity."""
        if node.name == '#entity':
            try:
                return self.writer.defaults['entity'] % node.data
            except TypeError:
                pass
        return re.sub(RE, ' ', node.data)

    def data(self, node):
        tab = self.writer.defaults['tab']
        text = re.sub(RE, ' ', node.data)
        if text.strip() == '':
            if text != ' ':
                if node.next is None and printable_prev(node):
                    self.write('\n')
                return
        if node.prev is None or not printable_prev(node):
            if text != ' ' or printable_next(node):
                if self.writer.prev_str[-1] == '\n':
                    self.tab_printed = False
                if not self.tab_printed:
                    self.write(tab*node.level)
                    self.tab_printed = True
            else:
                return
        if text != ' ' or printable_prev(node):
            if node.name == '#entity':
                try:
                    text = self.writer.defaults['entity'] % text
                except TypeError:
                    pass
            self.write(text)
        nnext = node.next
        if nnext is None or nnext.name not in ['#entity', '#text']:
            self.write('\n')


class DefaultNW(NodeWriter):
    """Default way of writing XML elements. """

    def start(self, node):
        tab = self.writer.defaults['tab']
        if isinstance(node, core.ProcessingInstruction):
            self.write('%s<%s' % (tab*node.level, node.name))
            if '\n' in node.data:
                self.write('\n')
            else:
                self.write(' ')
            return
        att = ' '.join(['%s="%s"' % (k, v) for k, v in node.items()])
        self.write('%s<%s' % (tab*node.level, node.name))
        if att != '':
            self.write(' %s' % att)
        if isinstance(node, core.RawText) or node.child:
            self.write('>')
        else:
            self.write('/>\n')

    def child(self, node):
        for child in node.child:
            if child.name not in ['#text', '#entity']:
                self.write('\n')
                return True
        text_nw = self.writer.get_node_writer('#text')
        for child in node.child:
            self.write(text_nw.format(child))
        self.write('</%s>\n' % node.name)

    def end(self, node):
        tab = self.writer.defaults['tab']
        if node.child:
            self.write('%s</%s>\n' % (tab*node.level, node.name))
        elif isinstance(node, core.ProcessingInstruction):
            self.write('?>\n')
        elif isinstance(node, core.RawText):
            self.write('</%s>\n' % node.name)


class DoctypeNW(NodeWriter):
    """Writes the doctype node: `<!DOCTYPE ...>`. """

    def start(self, node):
        tab = self.writer.defaults['tab']
        self.write('%s<!DOCTYPE ' % (tab*node.level))

    def data(self, node):
        self.write(re.sub(RE, ' ', node.data).strip())

    def end(self, node):
        self.write('>\n')


class CDataNW(NodeWriter):
    """Writes the CDATA node. """

    def start(self, node):
        tab = self.writer.defaults['tab']
        self.write('%s<![CDATA[' % (tab*node.level))

    def data(self, node):
        data = node.data.split(']]>')
        for index in xrange(len(data)-1):
            self.write(data[index] + ']]]]><![CDATA[>')
        self.write(data[-1])

    def end(self, node):
        self.write(']]>\n')


class CommentNW(NodeWriter):
    """Comment can also follow the tree structure. They have to be
    formatted to reflect this. """

    def start(self, node):
        tab = self.writer.defaults['tab']
        self.write('%s<!--' % (tab*node.level))

    def data(self, node):
        tab = self.writer.defaults['tab']
        lines = node.data.split('\n')
        if len(lines) == 1:
            self.write(lines[0])
            return
        self.write(lines[0])
        self.write('\n')
        for num in xrange(1, len(lines)-1):
            self.write(tab*node.level)
            self.write(lines[num].strip())
            self.write('\n')
        self.write(tab*node.level)
        self.write(lines[-1].lstrip())

    def end(self, node):
        self.write('-->\n')
