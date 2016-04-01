#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    zifeiyu.utils.markdown
    ~~~~~~~~~~~~~~~~~~~~

    add markdown function

    :copyright: (c) 2016 by zifeiyu.
    :license: Apache License 2.0, see LICENSE for more details.
"""
from jinja2 import Markup
import markdown2
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, tostring
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound


class MDSetter(object):
    '''set markdown editor value'''

    def __init__(self, content):
        temp_content = content
        self.content = ''
        content_line = temp_content.decode('utf-8').splitlines()
        i = 0
        counts = len(content_line)
        for line in content_line:
            if i < counts -1:
                self.content = self.content + line + u'\\n'
            else:
                self.content = self.content + line

    def setMDvalue(self):
        return Markup("<script>simplemde.value(\"%s\");</script>" % self.content)



class MDconverter(object):
    """convert markdown2 string to html and highlight code"""

    def __init__(self, md_string):
        self.md_string =  markdown2.markdown(md_string, extras=['fenced-code-blocks'])
        self.highlight_code()

    def render(self):
        return Markup(self.md_string)

    def highlight_code(self):

        self.md_string = '<div>' + self.md_string + '</div>'
        tree = ET.ElementTree(ET.fromstring(self.md_string))
        root = tree.getroot()
        self.__visit_tree(root)
        self.md_string = tostring(root)

    def __visit_tree(self, root):
        i = 0
        length = len(root)
        while(i < length):
            child = root[i]
            if child.tag in ('code', 'pre'):
                code_text = ''
                if child.tag == 'code':
                    code_text = child.text
                elif len(child) > 0:
                    code_text = child[0].text
                # hightlight code
                # result is like this <div class="highlight"><pre><span class="k">print</span> <span class="s">&quot;Hello World&quot;</span></pre></div>
                try:
                    highlight_code = highlight(code_text, guess_lexer(code_text), HtmlFormatter())
                    root[i] = ET.fromstring(highlight_code)
                except ClassNotFound, e:
                    i += 1
                    continue
            elif len(child) > 0:
                self.__visit_tree(child)
            i += 1