"""XML: DEFAULT Writer Style

This style writes an xml document by showing its tree structure. It
removes extra spaces in the text nodes.

"""

from lexor import init, load_aux

INFO = init(
    version=(0, 0, 1, 'final', 0),
    lang='xml',
    type='writer',
    description='Writes XML files by displaying its tree structure.',
    url='http://jmlopez-rod.github.io/lexor-lang/xml-writer-default',
    author='Manuel Lopez',
    author_email='jmlopez.rod@gmail.com',
    license='BSD License',
    path=__file__
)
DEFAULTS = {
    'entity': '%s',
    'tab': '    ',
}
MOD = load_aux(INFO)['nw']
MAPPING = {
    '#text': MOD.TextNW,
    '#entity': '#text',
    '#comment': MOD.CommentNW,
    '#doctype': MOD.DoctypeNW,
    '#cdata-section': MOD.CDataNW,
    '__default__': MOD.DefaultNW,
}
