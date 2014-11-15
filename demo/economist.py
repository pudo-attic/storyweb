import os
import json
import requests
from urlparse import urljoin
from lxml import html
from slugify import slugify

INDEX_PAGE = 'http://www.economist.com/printedition/covers'
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def get_issues():
    for year in [2012, 2011]: #[2014, 2013, 2012, 2011]:
        params = {
            'date_filter[value][year]': year
        }
        res = requests.get(INDEX_PAGE, params=params)
        doc = html.fromstring(res.content)
        for a in doc.findall('.//a'):
            href = urljoin(INDEX_PAGE, a.get('href'))
            if a.text == 'Contents':
                get_toc(href)


def get_toc(url):
    _, date = url.rsplit('/', 1)
    res = requests.get(url)
    doc = html.fromstring(res.content)
    for a in doc.findall('.//div[@id="section-93"]//a'):
        href = urljoin(INDEX_PAGE, a.get('href'))
        if a.text is not None and 'this week' in a.text:
            get_document(href, date, a.text)


def get_document(url, date, title):
    print [url, date, title]
    try:
        os.makedirs(DATA_DIR)
    except:
        pass
    fn = '%s.json' % slugify(url)
    fn = os.path.join(DATA_DIR, fn)
    if os.path.exists(fn):
        return
    res = requests.get(url)
    data = {
        'url': url,
        'date': date,
        'title': title,
        'content': res.content
    }
    test_print(res)
    with open(fn, 'w') as fp:
        json.dump(data, fp)


def test_print(res):
    doc = html.fromstring(res.content)
    body = doc.find('.//div[@class="main-content"]')
    for p in body.findall('.//p'):
        if p.get('class') == 'xhead':
            continue
        text = p.text_content()
        if not len(text):
            continue
        print [text]

get_issues()
