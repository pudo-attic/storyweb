import os
import json
import requests
import hashlib
from pprint import pprint
import yaml
from lxml import html

API_KEY = os.environ.get('CALAIS_KEY')
if API_KEY is None:
    raise SystemError("Set the CALAIS_KEY to be an OpenCalais API Key")
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
TAG_DIR = os.path.join(os.path.dirname(__file__), 'calais')
TAGS = {
    'entity': ['Person', 'Organization', 'Company'],
    'location': ['Country', 'Region', 'City', 'ProvinceOrState',
                 'Continent', 'NaturalFeature', 'Facility']
}


def calais_enrich(fn, text):
    sig = hashlib.sha1(text.encode('utf-8')).hexdigest()
    fn = fn.replace('.json', '.%s.json' % sig)
    fn = os.path.join(TAG_DIR, fn)
    try:
        os.makedirs(TAG_DIR)
    except:
        pass
    if os.path.exists(fn):
        with open(fn, 'r') as fp:
            result = json.load(fp)
    else:
        return
        URL = 'http://api.opencalais.com/tag/rs/enrich'
        headers = {
            'x-calais-licenseID': API_KEY,
            'content-type': 'text/raw',
            'accept': 'application/json'
        }
        res = requests.post(URL, headers=headers, data=text.encode('utf-8'))
        #print res
        result = res.json()
        with open(fn, 'w') as fp:
            json.dump(result, fp)

    sections = []
    for k, v in result.items():
        if '_type' not in v:
            continue
        
        tag = None
        for tag_, types in TAGS.items():
            if v.get('_type') in types:
                tag = tag_

        if tag is None:
            continue

        for instance in v.get('instances'):
            instance.update({
                'label': v.get('name'),
                'type': v.get('_type'),
                'tag': tag
            })
            sections.append(instance)

    offset = 0
    out = []
    for section in sorted(sections, key=lambda s: s.get('offset')):
        if section.get('offset') < offset:
            continue
        out.append(text[offset:section.get('offset')])

        if section['tag'] == 'entity':
            out.append('[[')
        if section['tag'] == 'location':
            out.append('[@')
        offset = section.get('offset') + section.get('length')

        out.append(text[section.get('offset'):offset])
        
        if section['tag'] == 'entity':
            out.extend(('|', section['label'], '|', section['type'], ']]'))
        if section['tag'] == 'location':
            out.append(']')

    out.append(text[offset:])
    return ''.join(out)


def process_doc(fn, data):
    doc = html.fromstring(data.get('content'))
    body = doc.find('.//div[@class="main-content"]')
    for p in body.findall('.//p'):
        if p.get('class') == 'xhead':
            continue
        text = p.text_content()
        strong = p.find('./strong')
        if strong is not None and strong.text_content() == text:
            continue
        if text.endswith('See article'):
            text, _ = text.rsplit('See', 1)
        if text.startswith('See article'):
            continue
        text = text.strip()
        if not len(text):
            continue
        print data.get('url'), [text]
        text = calais_enrich(fn, text)
        print [text]
        if text is None:
            continue
        date = data.get('date')
        year, month, day = date.split('-')
        label = 'The Economist, %s, %s.%s.%s' % (data.get('title'), day, month, year)
        yield {
            'text': text,
            'date': data.get('date'),
            'source_label': label,
            'source_url': data.get('url')
        }


def process_docs():
    blocks = []
    for fn in os.listdir(DATA_DIR):
        with open(os.path.join(DATA_DIR, fn), 'r') as fp:
            data = json.load(fp)
            for block in process_doc(fn, data):
                blocks.append(yaml.safe_dump(block,
                       canonical=False,
                       default_flow_style=False,
                       indent=4))
    
    with open('economist.yaml', 'w') as fh:
        fh.write('\n\n---\n\n'.join(blocks))


process_docs()
