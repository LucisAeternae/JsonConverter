import json, sys
from unittest import TestCase


def control():
    data = openjson()
    html = convert(data)
    output(html)
    return

def openjson():
    try:
        with open('source2.json') as f:
            data = json.load(f)
    except ValueError:
        print('error')
    return data

def convert(data):
    html = ''
    for tags in data:
        for tag in tags:
            tag = '<%s>%s' % (tag, tags[tag]) + '</%s>' % tag
            html += tag
    return html

def output(html):
    sys.stdout.write(html)

if __name__ == '__main__':
    control()

class TestMainMethod(TestCase):
    def setUp(self):
        self.dict1 = [{'title': 'Title #1', 'body': 'Hello, World 1!'},
                {'title': 'Title #2', 'body': 'Hello, World 2!'}]
        self.result1 = '<title>Title #1</title><body>Hello, World 1!</body>' \
                '<title>Title #2</title><body>Hello, World 2!</body>'
        self.dict2 = [{'h3': 'Title #1', 'div': 'Hello, World 1!'}]
        self.result2 = '<h3>Title #1</h3><div>Hello, World 1!</div>'

    def test_base_first(self):
        self.assertEqual(convert(self.dict1), self.result1)

    def test_base_second(self):
        self.assertEqual(convert(self.dict2), self.result2)
