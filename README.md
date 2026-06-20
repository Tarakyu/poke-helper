# 포켓몬 챔피언스 스피드 순위

싱글배틀(시즌 M-3) 사용률 **상위 100** 포켓몬을 **스피드 빠른 순**으로 보여주는 정적 웹페이지입니다.
`index.html` 한 파일만 열면 동작합니다(데이터 내장, 외부 의존성 없음).

## 표시 내용

- **스피드 실수치**: 채용률 1위 능력포인트 세팅 + 1위 성격 보정 기준. 메가진화 나이트가 1위 아이템이면 메가폼 종족값 기준.
- **정렬**: 구애스카프 등 스피드 배율 아이템 반영 실수치 내림차순
- **능력포인트 직접 입력** (0~32): 실수치 실시간 재계산
- **성격 버튼** (▲●▼): 스피드 보정 수동 조정
- **랭크 버튼** (▲▼): 스피드 랭크 -6~+6. 스피드 관련 특성 ON 시 자동 반영
- **특성 ON/OFF**: 쓱쓱·가속·깨어진갑옷 등 스피드 배율 특성 적용
- **내구지수**: HP × 방어 / HP × 특방 / 0.411. 생명의구슬·진화의휘석·멀티스케일 등 반영
- **결정력**: 공격실수치 × 기술위력 × 자속보정 / 0.411. 구애머리띠·구애안경·생명의구슬·적응력 반영
- **타입 아이콘** / **약점** / **반감**: 메가진화 시 메가폼 기준
- **포켓몬 검색 4칸**: OR 조건으로 동시 비교

## 데이터 출처

- 사용률 / 채용 1위 성격·특성·아이템·능력포인트·기술: [champs.pokedb.tokyo](https://champs.pokedb.tokyo) (rule=0 싱글배틀)
- 한국어 포켓몬 이름: [PokéAPI](https://pokeapi.co)
- 용어 번역: `pokemon_dict.json` (로컬 사전)

## 빌드 파이프라인

```
scrape.py  →  mons.json   (champs.pokedb.tokyo 스크래핑)
konames.py →  konames.json (PokéAPI 한국어 이름)
build.py   →  data.json   (실수치·내구·결정력 계산 + 매핑)
gen.py     →  index.html  (template.html + data.json 합성)
```

### 시즌 갱신 시

```bash
python scrape.py     # 상위 100 포켓몬 데이터 수집
python konames.py    # 신규 포켓몬 한국어 이름 추가
python build.py      # 계산 및 매핑
python gen.py        # 최종 HTML 생성
```

### 상위 N 변경

`scrape.py`의 `keys` 목록을 사용률 순서대로 수정.
새 포켓몬 추가 시 `konames.py` 재실행 필요.

### 신규 특성·기술·아이템 번역 누락 시

`build.py` 실행 결과에 `UNMAPPED: ABIL:xxx` 형태로 콘솔 출력됨.
`abil_kr` / `move_kr` / `item_kr` 딕셔너리에 추가하거나, `pokemon_dict.json`에 없으면 직접 추가.

### 신규 메가진화 나이트 아이템 추가 시

1. `scrape.py`의 `MEGA_ITEM_TO_FORM`에 `아이템명: 메가폼key` 추가
2. `build.py`의 `item_kr`에 번역명 추가 (`포켓몬한국어명` + `나이트` 형식)
3. `mons.json` 부분 업데이트 또는 `scrape.py` 재실행
