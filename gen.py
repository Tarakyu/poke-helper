import json

data = json.load(open('data.json', encoding='utf-8'))
datajs = json.dumps(data, ensure_ascii=False)

TEMPLATE = open('template.html', encoding='utf-8').read()
html = TEMPLATE.replace('__DATA__', datajs)
open('index.html', 'w', encoding='utf-8').write(html)
print('wrote index.html', len(html), 'bytes')
