import json, sys
from unittest import TestCase

def control():
    data = openjson()
    html = convert(data)
    output(html)
    return

def openjson():
    try:
        with open('source.json') as f:
            data = json.load(f)
    except ValueError:
        print('error')
    return data

def convert(data):
    html = ''
    for tag in data:
        title = '<h1>%s' % tag['title'] + '</h1>'
        html += title
        body = '<p>%s' % tag['body'] + '</p>'
        html += body
    return html

def output(html):
    sys.stdout.write(html)

if __name__ == '__main__':
    control()

class TestMainMethod(TestCase):
    def setUp(self):
        self.dict1 = [{'title': 'Title #1', 'body': 'Hello, World 1!'},
                {'title': 'Title #2', 'body': 'Hello, World 2!'}]
        self.result1 = '<h1>Title #1</h1><p>Hello, World 1!</p><h1>Title #2' \
                '</h1><p>Hello, World 2!</p>'

    def test_base_first(self):
        self.assertEqual(convert(self.dict1), self.result1)
