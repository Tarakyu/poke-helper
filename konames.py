import json, urllib.request, time

mons = json.load(open('mons.json', encoding='utf-8'))
dexes = sorted(set(m['dex'] for m in mons))

def ko_species(dex):
    url = "https://pokeapi.co/api/v2/pokemon-species/%d/" % dex
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    d = json.loads(urllib.request.urlopen(req, timeout=60).read().decode('utf-8'))
    for n in d['names']:
        if n['language']['name'] == 'ko':
            return n['name']
    return None

ko = {}
for dex in dexes:
    ko[dex] = ko_species(dex)
    print(dex, ko[dex].encode('ascii', 'replace').decode() if ko[dex] else None)

json.dump(ko, open('konames.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print("WROTE", len(ko))
