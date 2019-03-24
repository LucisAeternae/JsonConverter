import json, sys
from html import escape
from string import ascii_lowercase
from unittest import TestCase


def control():
    data = openjson()
    if data:
        html = convert(data)
    else:
        html = "Error"
    output(html)
    return

def openjson():
    try:
        with open('source6.json') as f:
            data = json.load(f)
    except ValueError:
        data = False
    return data

def convert(data):
    html = ''
    for tags in data:
        block = ''
        if isinstance(tags, list) or isinstance(tags, dict):
            for tag in tags:
                tag = traverse(tag, tags)
                block +=tag
            block = '<li>' + block + '</li>'
        else:
            block = traverse(tags, data)
        html += block
    if isinstance(data, list):
        html = '<ul>' + html + '</ul>'
    return html

"""Function that create recursion for nested dict"""
def traverse(data, child_of=False):
    if isinstance(child_of[data], list):
        blocks_list = ''
        for tags in child_of[data]:
            block = ''
            for tag_type in tags:
                tag = traverse(tag_type, tags)
                block += tag
            block = '<li>' + block + '</li>'
            blocks_list += block
        blocks_list = '<ul>' + blocks_list + '</ul>'
        blocks_list = '<%s>' % data + blocks_list + '</%s>' % data
        return blocks_list

    else:
        tag = createtag(data, child_of)
        return tag

"""Create main html syntax with optional params"""
def createtag(data, child_of):
    checkvaildtag(data)
    tag_content = decodereserved(child_of[data])
    if '.' in data or '#' in data:
        newdata = correcttag(data)
        tag = '<%s' % newdata[0]
        if newdata[2]:
            tag += ' id="%s"' % newdata[2]
        if newdata[1]:
            tag += ' class="%s"' % ' '.join(newdata[1])
        tag += '>%s' % tag_content + '</%s>' % data[0]
    else:
        tag = '<%s>%s' % (data, tag_content) + '</%s>' % data
    if isinstance(child_of, list):
        tag = '<li>' + tag + '</li>'
    return tag

"""Decode reserved html character into html entities"""
def decodereserved(content):
    tag_content = escape(content).encode('ascii', 'xmlcharrefreplace').decode()
    return tag_content

"""Changes shortened tags into list with tag type and selectors"""
def correcttag(data):
    data = data.split('.')
    newdata = []
    for i in data:
        if '#' in i:
            tempcut = i.split("#",1)
            id = tempcut[1]
            newdata.append(tempcut[0])
        else:
            newdata.append(i)
    tag_type = newdata.pop(0)
    data = [tag_type, newdata]
    try:
        data.append(id)
    except UnboundLocalError:
        data.append('')
    return data

def checkvaildtag(data):
    if data[0] in ascii_lowercase:
        return
    output('Error. Wrong tag')

def output(html):
    sys.stdout.write(html)
    sys.exit()

if __name__ == '__main__':
    html = ''
    control()

class TestMainMethod(TestCase):
    def setUp(self):
        self.dict1 = [{'title': 'Title #1', 'body': 'Hello, World 1!'},
                {'title': 'Title #2', 'body': 'Hello, World 2!'}]
        self.result1 = '<ul><li><title>Title #1</title><body>Hello, World 1!' \
                '</body></li><li><title>Title #2</title><body>Hello, World 2!' \
                '</body></li></ul>'
        self.dict2 = [{'h3': 'Title #1', 'div': 'Hello, World 1!'}]
        self.result2 = '<ul><li><h3>Title #1</h3><div>Hello, World 1!</div>' \
                '</li></ul>'
        self.dict3 = [{'h3': 'Title #1', 'div': 'Hello, World 1!'},
                {'h3': 'Title #2', 'div': 'Hello, World 2!'}]
        self.result3 = '<ul><li><h3>Title #1</h3><div>Hello, World 1!</div>' \
                '</li><li><h3>Title #2</h3><div>Hello, World 2!</div></li></ul>'
        self.dict4 = [{'span': 'Title #1',
                'content': [{'p': 'Example 1', 'header': 'header 1'}]},
                {'div': 'div 1'}]
        self.result4 = '<ul><li><span>Title #1</span><content><ul><li><p>' \
                'Example 1</p><header>header 1</header></li></ul></content>' \
                '</li><li><div>div 1</div></li></ul>'
        self.dict5 = {'p': 'Hello'}
        self.result5 = '<p>Hello</p>'
        self.dict6 = {'p.my-class#my-id': 'hello',
                'p.my-class1.my-class2': 'example<a>asd</a>'}
        self.result6 = '<p id="my-id" class="my-class">hello</p><p ' \
                'class="my-class1 my-class2">example&lt;a&gt;asd&lt;/a&gt;</p>'

    def test_base_first(self):
        self.assertEqual(convert(self.dict1), self.result1)

    def test_base_second(self):
        self.assertEqual(convert(self.dict2), self.result2)

    def test_base_third(self):
        self.assertEqual(convert(self.dict3), self.result3)

    def test_base_fourth(self):
        self.assertEqual(convert(self.dict4), self.result4)

    def test_base_fifth(self):
        self.assertEqual(convert(self.dict5), self.result5)

    def test_base_sixth(self):
        self.assertEqual(convert(self.dict6), self.result6)
