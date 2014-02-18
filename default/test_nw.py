"""XML: DEFAULT writer NW test

Testing suite to write XML in the DEFAULT style.

"""

import lexor
from lexor.command.test import compare_with

DOCUMENT = """<!DOCTYPE xml>
<?python
print 'Hello xml!'
?><parent att="val">
<child1>child 1 
content</child1>     <child2> child 2 
content with entity &amp; </child2>
<child3>
    &lt;  
&amp; <!-- Multiline comment goes
here and there... 
done... --></child3>
 <child4>
  child
 4 &lt; 
  content
<apples>    <bananas>  </bananas>
</apples><![CDATA[a < b]]> </child4>
&lt;
text
&amp;
<a> <b/> </a>
</parent>
"""

EXPECTED = """<!DOCTYPE xml>
<?python
print 'Hello xml!'
?>
<parent att="val">
    <child1>child 1 content</child1>
    <child2> child 2 content with entity &amp; </child2>
    <child3>
        &lt; &amp; 
        <!-- Multiline comment goes
        here and there...
        done... -->
    </child3>
    <child4>
         child 4 &lt; content 
        <apples>
            <bananas> </bananas>
        </apples>
        <![CDATA[a < b]]>
    </child4>
    &lt; text &amp; 
    <a>
        <b/>
    </a>
</parent>
"""
EXPECTED_ENTITY = """<!DOCTYPE xml>
<?python
print 'Hello xml!'
?>
<parent att="val">
    <child1>child 1 content</child1>
    <child2> child 2 content with entity <&amp;> </child2>
    <child3>
        <&lt;> <&amp;> 
        <!-- Multiline comment goes
        here and there...
        done... -->
    </child3>
    <child4>
         child 4 <&lt;> content 
        <apples>
            <bananas> </bananas>
        </apples>
        <![CDATA[a < b]]>
    </child4>
    <&lt;> text <&amp;> 
    <a>
        <b/>
    </a>
</parent>
"""
EXPECTED_TAB = """<!DOCTYPE xml>
<?python
print 'Hello xml!'
?>
<parent att="val">
****<child1>child 1 content</child1>
****<child2> child 2 content with entity &amp; </child2>
****<child3>
********&lt; &amp; 
********<!-- Multiline comment goes
********here and there...
********done... -->
****</child3>
****<child4>
******** child 4 &lt; content 
********<apples>
************<bananas> </bananas>
********</apples>
********<![CDATA[a < b]]>
****</child4>
****&lt; text &amp; 
****<a>
********<b/>
****</a>
</parent>
"""


def test_default():
    """xml.writer.default.nw """
    doc, _ = lexor.parse(DOCUMENT, 'xml')
    doc.style = 'default'
    compare_with(str(doc), EXPECTED)
    doc.defaults = {'entity': '<%s>'}
    compare_with(str(doc), EXPECTED_ENTITY)
    doc.defaults = {'tab': '****'}
    compare_with(str(doc), EXPECTED_TAB)
