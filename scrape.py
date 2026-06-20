import re, html, json, urllib.request

keys = "0445-00 1018-00 0026-00 0260-00 0398-00 0778-00 0908-00 0279-00 0823-00 0376-00 0006-00 0902-00 0730-00 1000-00 0450-00 0257-00 0130-00 0861-00 0681-00 0038-01 0149-00 0303-00 0970-00 0983-00 0479-02 0094-00 0635-00 0637-00 0584-00 0911-00 0154-00 0979-00 0212-00 0428-00 0937-00 0691-00 0655-00 0658-00 0503-01 0121-00 0670-05 0903-00 0887-00 0939-00 0003-00 0197-00 0009-00 0479-01 0448-00 0547-00".split()

def grab_obj(s, start):
    depth = 0
    for i in range(start, len(s)):
        if s[i] == '{':
            depth += 1
        elif s[i] == '}':
            depth -= 1
            if depth == 0:
                return s[start:i + 1]
    return None

def fetch(key):
    url = "https://champs.pokedb.tokyo/pokemon/show/%s?season=3&rule=0" % key
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req, timeout=60).read().decode('utf-8')

results = []
for k in keys:
    rh = fetch(k)
    raw = html.unescape(rh)
    title = re.search(r'<title>([^<｜|]+)', rh)
    jp = title.group(1).strip() if title else None
    if jp and jp.endswith('のデータ・採用技・テラスタイプ シーズンM-3（シングルバトル）'):
        jp = jp.split('の')[0]
    ms = re.search(r'"stats"\s*:\s*\{', raw)
    stats = json.loads(grab_obj(raw, raw.index('{', ms.start())))
    abil = re.search(r'"abilities"\s*:\s*\[(.*?)\]\s*,\s*"types"', raw, re.S)
    abil_names = re.findall(r'"name"\s*:\s*"([^"]+)"', abil.group(1)) if abil else []
    nat = None; abil_top = None
    for m in re.finditer(r'usagePieChart\((\[.*?\])\)', raw, re.S):
        pre = raw[max(0, m.start() - 600):m.start()]
        cls = re.findall(r'pokemon-trend__column-(\w+)', pre)
        cat = cls[-1] if cls else '?'
        try:
            arr = json.loads(m.group(1))
        except Exception:
            continue
        if cat == 'personalities' and arr:
            e = arr[0]; dec = re.sub(r'<[^>]+>', '', e.get('decoration', '') or '')
            nat = {'name': e['name'], 'dec': dec.strip(), 'rate': e.get('rate')}
        if cat == 'abilities' and arr:
            e = arr[0]; abil_top = {'name': e['name'], 'rate': e.get('rate')}
    sp = stats['speed']
    results.append({
        'key': k, 'dex': int(k.split('-')[0]), 'form': k.split('-')[1], 'jp_name': jp,
        'base_speed': sp['base'], 'neutral': sp['neutral'], 'max': sp['max'],
        'noEV': sp['noEV'], 'down': sp['down'],
        'all_abilities': abil_names, 'top_ability': abil_top, 'top_nature': nat,
    })
    print("done", k, jp.encode('ascii', 'replace').decode() if jp else None)

json.dump(results, open('mons.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print("WROTE", len(results))
