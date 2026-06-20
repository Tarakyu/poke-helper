import json, math

mons = json.load(open('mons.json', encoding='utf-8'))
ko = json.load(open('konames.json', encoding='utf-8'))  # dex(str) -> ko name

form_suffix = {
    '0038-01': '(알로라)', '0479-01': '(히트)', '0479-02': '(워시)',
    '0503-01': '(히스이)', '0670-05': '(영원의 꽃)', '0902-00': '(수컷)',
}

nat_kr = {
    "ようき": "명랑", "おくびょう": "겁쟁이", "いじっぱり": "고집", "ひかえめ": "조심",
    "わんぱく": "장난꾸러기", "ずぶとい": "대담", "のんき": "무사태평", "なまいき": "건방",
    "しんちょう": "신중", "おだやか": "차분", "れいせい": "냉정", "ゆうかん": "용감",
    "おっとり": "덜렁", "うっかりや": "촐랑", "やんちゃ": "천진난만", "さみしがり": "외로움",
    "ゆうのう": "성실", "がんばりや": "노력", "すなお": "성실", "てれや": "수줍음",
    "まじめ": "성실", "きまぐれ": "변덕", "のうてんき": "낙천", "おとなしい": "얌전",
    "むじゃき": "천진난만", "せっかち": "성급", "なまけ": "촐랑",
}
abil_kr = {
    "あめうけざら": "빗물받이", "あめふらし": "잔비", "いかく": "위협", "いたずらごころ": "짓궂은마음",
    "うるおいボイス": "촉촉보이스", "おうごんのからだ": "황금몸체", "おみとおし": "통찰", "かいりきバサミ": "괴력집게",
    "かそく": "가속", "かたやぶり": "틀깨기", "かるわざ": "곡예", "がんじょう": "옹골참",
    "きょうせい": "공생", "きれあじ": "칼끝", "きんちょうかん": "긴장감", "くだけるよろい": "깨어진갑옷",
    "げきりゅう": "급류", "さめはだ": "까칠한피부", "しぜんかいふく": "자연회복", "しめりけ": "습기",
    "しんりょく": "심록", "じきゅうりょく": "지구력", "じしんかじょう": "자기과신", "じゅうなん": "유연",
    "すいすい": "쓱쓱", "すじがねいり": "일편단심", "すてみ": "이판사판", "すなおこし": "모래날림",
    "すながくれ": "모래숨기", "すなのちから": "모래의힘", "すりぬけ": "빠져나가기", "するどいめ": "날카로운눈",
    "せいぎのこころ": "정의의마음", "せいしんりょく": "정신력", "せいでんき": "정전기", "そうだいしょう": "총대장",
    "ちからずく": "우격다짐", "てきおうりょく": "적응력", "てんねん": "천진", "でんきにかえる": "일렉트릭변환",
    "どくげしょう": "독화장", "どくしゅ": "독수", "どくのトゲ": "독가시", "のろわれボディ": "저주받은바디",
    "はっこう": "발광", "ばけのかわ": "분장", "ひらいしん": "피뢰침", "ふくつのこころ": "불굴의마음",
    "ふしょく": "부식", "ふゆう": "부유", "ぶきよう": "서투름", "へんげんじざい": "변환자재",
    "ほのおのからだ": "불꽃몸", "まけんき": "오기", "むしのしらせ": "벌레의알림", "もうか": "맹화",
    "もらいび": "타오르는불꽃", "やるき": "의기양양", "ゆきがくれ": "눈숨기", "ゆきふらし": "눈퍼뜨리기",
    "ようりょくそ": "엽록소", "わるいてぐせ": "나쁜손버릇", "アイスボディ": "얼음몸", "アナライズ": "분석력",
    "クリアボディ": "클리어바디", "サンパワー": "선파워", "シンクロ": "싱크로", "テクニシャン": "테크니션",
    "バトルスイッチ": "배틀스위치", "フラワーベール": "플라워베일", "プレッシャー": "위압감", "マジシャン": "매지션",
    "マルチスケイル": "멀티스케일", "ミラーアーマー": "미러아머", "メロメロボディ": "헤롱헤롱바디",
    "ライトメタル": "라이트메탈", "リーフガード": "리프가드",
}
spd_abil = {
    "すいすい": "비가 올 때 스피드 2배",
    "ようりょくそ": "쾌청할 때 스피드 2배",
    "すなかき": "모래바람일 때 스피드 2배",
    "ゆきかき": "설경(눈)일 때 스피드 2배",
    "かそく": "매 턴 종료 시 스피드 +1랭크",
    "かるわざ": "지닌 도구가 사라지면 스피드 2배",
    "くだけるよろい": "물리 공격 피격 시 방어 -1 / 스피드 +2랭크",
    "ふくつのこころ": "풀죽을 때마다 스피드 +1랭크",
}
weather_note = {
    "あめふらし": "날씨: 비 (아군 쓱쓱 발동)",
    "すなおこし": "날씨: 모래바람 (아군 모래헤치기 발동)",
    "ゆきふらし": "날씨: 설경 (아군 눈치우기 발동)",
}

unmapped = set()
out = []
for rank, m in enumerate(mons, 1):
    k = m['key']
    name = ko[str(m['dex'])] + form_suffix.get(k, '')
    neutral, noEV = m['neutral'], m['noEV']
    dec = m['top_nature']['dec']
    if 'S↑' in dec:
        eff = 'up'; full = math.floor(neutral * 1.1); zero = math.floor(noEV * 1.1)
    elif 'S↓' in dec:
        eff = 'down'; full = math.floor(neutral * 0.9); zero = math.floor(noEV * 0.9)
    else:
        eff = 'none'; full = neutral; zero = noEV
    # sanity vs site-provided values
    assert eff != 'up' or full == m['max'], (k, full, m['max'])
    assert eff != 'down' or zero == m['down'], (k, zero, m['down'])

    natj = m['top_nature']['name']
    if natj not in nat_kr:
        unmapped.add('NAT:' + natj)
    notes = []
    for ab in m['all_abilities']:
        if ab not in abil_kr:
            unmapped.add('ABIL:' + ab)
        if ab in spd_abil:
            top = (ab == m['top_ability']['name'])
            notes.append({'abil': abil_kr.get(ab, ab), 'text': spd_abil[ab],
                          'top': top, 'tag': '채용 1위 특성' if top else '선택 가능 특성'})
    tab = m['top_ability']['name']
    if tab not in abil_kr:
        unmapped.add('ABIL:' + tab)
    out.append({
        'rank': rank, 'key': k, 'name': name, 'base': m['base_speed'],
        'full': full, 'full_orig': neutral, 'zero': zero, 'zero_orig': noEV, 'eff': eff,
        'nature': nat_kr.get(natj, natj), 'nature_dec': dec, 'nature_rate': m['top_nature']['rate'],
        'ability': abil_kr.get(tab, tab), 'ability_rate': m['top_ability']['rate'],
        'spd_notes': notes, 'weather': weather_note.get(tab),
    })

out.sort(key=lambda x: (-x['full'], x['rank']))
json.dump(out, open('data.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print("WROTE data.json", len(out))
if unmapped:
    open('unmapped.txt', 'w', encoding='utf-8').write('\n'.join(sorted(unmapped)))
    print("UNMAPPED ->", len(unmapped), "see unmapped.txt")
else:
    print("all natures/abilities mapped")
