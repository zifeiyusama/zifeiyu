#!/usr/bin/env python
# -*- coding: utf-8 -*-
from jinja2 import Markup
import markdown2
from lxml import etree
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound


class MDSetter(object):

    def __init__(self, content):
        temp_content = content
        self.content = ''
        content_line = temp_content.decode('utf-8').splitlines()
        print content_line
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
    """convert markdown2 string to html"""

    def __init__(self, md_string):
        self.md_string =  markdown2.markdown(md_string, extras=['fenced-code-blocks'])
        self.highlight_code()

    def render(self):
        return Markup(self.md_string)

    def highlight_code(self):
        result = etree.Element("div")
        root = etree.fromstring('<div>' + self.md_string + '</div>')
        self.__visit_tree(root)
        self.md_string = etree.tostring(root)

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
                    root[i] = etree.fromstring(highlight_code)
                except ClassNotFound, e:
                    i += 1
                    continue
            elif len(child) > 0:
                self.__visit_tree(child)
            i += 1
            print i

    @classmethod
    def formatContent(self, content):
        '''format multiline to show it in a markdown editor'''
        result = []
        content_line = content.splitlines()
        for line in content_line:
            print line
            result.append(str(line))
        print result
        return result