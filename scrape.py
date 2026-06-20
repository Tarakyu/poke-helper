import re, html, json, urllib.request

keys = "0445-00 1018-00 0026-00 0908-00 0778-00 0398-00 0260-00 0006-00 0823-00 0376-00 0450-00 0279-00 0902-00 0730-00 0257-00 0130-00 1000-00 0861-00 0038-01 0149-00 0970-00 0983-00 0681-00 0303-00 0635-00 0479-02 0094-00 0911-00 0691-00 0655-00 0584-00 0212-00 0637-00 0428-00 0154-00 0658-00 0121-00 0503-01 0937-00 0979-00 0887-00 0003-00 0903-00 0670-05 0197-00 0448-00 0547-00 0009-00 0939-00 0479-01 0473-00 0700-00 0752-00 0184-00 0248-00 0036-00 0478-00 0530-00 0956-00 0132-00 0604-00 0571-01 0282-00 0748-00 0689-00 0143-00 0254-00 0227-00 0497-00 0475-00 0115-00 1013-00 0350-00 0660-00 0952-00 0560-00 0545-00 0900-00 0936-00 0460-00 0858-00 0668-00 0302-00 0080-00 0199-01 0354-00 0395-00 0855-00 0706-01 0727-00 0652-00 0609-00 0904-00 0534-00 0666-18 0479-05 0733-00 0925-00 0695-00 0071-00".split()

# 아이템명 -> 해당 메가폼 key (같은 페이지 forms JSON에서 파싱)
MEGA_ITEM_TO_FORM = {
    'ライチュウナイトＹ': '0026-03',
    'ゲンガナイト':      '0094-01',
    'スターミナイト':    '0121-01',
    'ミミロップナイト':  '0428-01',
    'ルカリオナイト':    '0448-01',
    'リザードナイトＹ':  '0006-02',
    'メタグロスナイト':  '0376-01',
    'ギャラドスナイト':  '0130-01',
    'バシャーモナイト':  '0257-01',
    'カイリュナイト':    '0149-01',
    'カメックスナイト':  '0009-01',
    'ラグラージナイト':  '0260-01',
    'フシギバナイト':    '0003-01',
    'ハッサムナイト':    '0212-01',
    'クチートナイト':    '0303-01',
    'ドラミドナイト':    '0691-01',
    'マフォクシナイト':  '0655-01',
    'ムクホークナイト':  '0398-01',
    'ゲッコウガナイト':  '0658-03',
    'フラエッテナイト':  '0670-06',
    'メガニウムナイト':  '0154-01',
    'バンギラスナイト':  '0248-01',
    'ピクシナイト':     '0036-01',
    'ユキメノコナイト':  '0478-01',
    'シビルドナイト':   '0604-01',
    'サーナイトナイト':  '0282-01',
    'ガメノデスナイト':  '0689-01',
    'ジュカインナイト':  '0254-01',
    'ガルーラナイト':   '0115-01',
    'スコヴィラナイト':  '0952-01',
    'ズルズキナイト':   '0560-01',
    'ペンドラナイト':   '0545-01',
    'ユキノオナイト':   '0460-01',
    'カエンジシナイト':  '0668-02',
    'ヤミラミナイト':   '0302-01',
    'ヤドランナイト':   '0080-01',
    'ジュペッタナイト':  '0354-01',
    'ブリガロナイト':   '0652-01',
    'ウツボットナイト':  '0071-01',
}

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

def parse_forms(raw_html):
    """페이지 내 forms JSON 파싱 → {form_key: {display_name, stats, abilities}, ...}"""
    idx = raw_html.find('"forms":')
    if idx < 0:
        return {}
    obj_start = raw_html.index('{', idx)
    forms_str = grab_obj(raw_html, obj_start)
    if not forms_str:
        return {}
    return json.loads(forms_str)

def parse_top_ev(raw_html):
    """합산 1위 포인트 배분 파싱 → {ev: {H/A/B/C/D/S: pt}, rate: float}"""
    idx = raw_html.find('usage-list--stats')
    if idx < 0:
        return {}
    section = raw_html[idx:]
    li_start = section.find('<li ')
    if li_start < 0:
        return {}
    li_end = section.find('</li>', li_start)
    item_html = section[li_start:li_end + 5]

    rate_m = re.search(r'usage-rate[^>]*>([\d.]+)%<', item_html)
    rate = float(rate_m.group(1)) if rate_m else None

    labels = re.findall(r'pokemon-stat-spread__label[^>]*>([^<]+)<', item_html)
    values = re.findall(r'pokemon-stat-spread__value[^>]*>([^<]+)<', item_html)

    ev = {}
    for label, val in zip(labels, values):
        label = label.strip()
        val = val.strip()
        if label in ('H', 'A', 'B', 'C', 'D', 'S') and val.isdigit():
            ev[label] = int(val)

    return {'ev': ev, 'rate': rate}

results = []
failed = []
for k in keys:
    try:
        rh = fetch(k)
    except Exception as e:
        print(f"FETCH FAILED {k}: {e}")
        failed.append(k)
        continue
    try:
        raw = html.unescape(rh)
        title = re.search(r'<title>([^<｜|]+)', rh)
        jp = title.group(1).strip() if title else None
        if jp and jp.endswith('のデータ・採用技・テラスタイプ シーズンM-3（シングルバトル）'):
            jp = jp.split('の')[0]

        # 기본폼 stats
        ms = re.search(r'"stats"\s*:\s*\{', raw)
        if not ms:
            raise ValueError('stats not found')
        stats = json.loads(grab_obj(raw, raw.index('{', ms.start())))

    # 모든 폼 데이터 파싱
    forms = parse_forms(raw)

    abil = re.search(r'"abilities"\s*:\s*\[(.*?)\]\s*,\s*"types"', raw, re.S)
    abil_names = re.findall(r'"name"\s*:\s*"([^"]+)"', abil.group(1)) if abil else []

    nat = None; abil_top = None; item_top = None
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
        if cat == 'items' and arr:
            e = arr[0]; item_top = {'name': e['name'], 'rate': e.get('rate')}

    # 기술 상위 4개 파싱
    top_moves = []
    seen_ranks = set()
    for mr in re.findall(r'data-move-detail="({.*?})"', rh):
        try:
            mdata = json.loads(html.unescape(mr))
            if mdata['rank'] not in seen_ranks and mdata['rank'] <= 4:
                seen_ranks.add(mdata['rank'])
                top_moves.append({
                    'rank': mdata['rank'],
                    'name': mdata['name'],
                    'rate': mdata.get('rate'),
                    'category': mdata.get('category'),        # 1=물리 2=특수 3=변화
                    'category_label': mdata.get('category_label'),
                    'power': mdata.get('power'),               # '100' or '−'
                    'type_id': mdata['type']['id'],
                    'type_name': mdata['type']['name'],
                })
        except Exception:
            continue
    top_moves.sort(key=lambda x: x['rank'])

    top_ev = parse_top_ev(raw)
    sp = stats['speed']

    # 메가폼 데이터 추출
    mega_form_data = None
    if item_top:
        mega_form_key = MEGA_ITEM_TO_FORM.get(item_top['name'])
        if mega_form_key and mega_form_key in forms:
            mf = forms[mega_form_key]
            mega_form_data = {
                'key': mega_form_key,
                'display_name': mf.get('display_name', ''),
                'stats': mf['stats'],
                'abilities': [a['name'] for a in mf.get('abilities', [])],
                'types': mf.get('types', []),
                'effectiveness': mf.get('effectiveness', {}),
            }

    # 약점/반감: 메가폼 있으면 메가폼 기준, 없으면 기본폼
    eff_form = mega_form_data if mega_form_data else forms.get(k, {})
    effectiveness = eff_form.get('effectiveness', {})
    types = eff_form.get('types', forms.get(k, {}).get('types', []))

        results.append({
            'key': k, 'dex': int(k.split('-')[0]), 'form': k.split('-')[1], 'jp_name': jp,
            'base_speed': sp['base'], 'neutral': sp['neutral'], 'max': sp['max'],
            'noEV': sp['noEV'], 'down': sp['down'],
            'all_abilities': abil_names, 'top_ability': abil_top,
            'top_nature': nat, 'top_item': item_top,
            'top_ev': top_ev,
            'top_moves': top_moves,
            'stats': stats,
            'mega_form': mega_form_data,
            'types': types,
            'weaknesses': [
                {'type_id': w['type_id'], 'multiplier': w['multiplier']}
                for w in effectiveness.get('weaknesses', [])
            ],
            'resistances': [
                {'type_id': r['type_id'], 'multiplier': r['multiplier']}
                for r in effectiveness.get('resistances', [])
            ],
        })
        print("done", k, jp.encode('ascii', 'replace').decode() if jp else None)
    except Exception as e:
        print(f"PARSE FAILED {k}: {e}")
        failed.append(k)

json.dump(results, open('mons.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print("WROTE", len(results))
if failed:
    print("FAILED KEYS:", failed)
