# 포켓몬 챔피언스 스피드 도움말

싱글배틀(시즌 M-3) 사용률 **상위 50** 포켓몬을 **스피드 빠른 순**으로 보여주는 정적 웹페이지입니다.
`index.html` 한 파일만 열면 동작합니다(데이터 내장, 외부 의존성 없음).

## 표시 내용
- **풀투자(252)** / **미투자(0)** 실수치 (Lv50 / 개체값 31), 각각 **채용률 1위 성격의 스피드 보정** 적용
- 성격 보정으로 값이 바뀐 칸은 **무보정 실수치**를 함께 표기, 성격 칸에 사유(예: `명랑 S↑`) 표시
- 정렬 = 풀투자(252)+성격 보정 실수치 내림차순
- **스피드 관련 특성**(쓱쓱·엽록소·가속·곡예·깨어진갑옷·불굴의마음 등) ⚡배지 + 호버 설명
- **날씨 셋업 특성**(잔비·모래날림·눈퍼뜨리기) 🌦배지
- 이름 검색 / "스피드 특성 보유만" 필터

> ⚠️ 사이트가 노력치 분포를 제공하지 않아 풀투자/미투자 두 기준을 모두 보여줍니다.
> 빠른 위협은 풀투자, 트릭룸·내구형 의심은 미투자 쪽을 참고하세요.

## 데이터 출처
- 사용률 / 채용 1위 성격·특성 / 종족값: [champs.pokedb.tokyo](https://champs.pokedb.tokyo/pokemon/list?rule=0) (rule=0 싱글배틀)
- 한국어 포켓몬 이름: [PokéAPI](https://pokeapi.co)

## 다시 빌드하기 (시즌 갱신 시)
```bash
python scrape.py     # champs.pokedb.tokyo 상위 50 → mons.json
python konames.py    # PokeAPI 한국어 이름 → konames.json
python build.py      # 실수치 계산 + 매핑 + 정렬 → data.json
python gen.py        # template.html + data.json → index.html
```
- 상위 N 변경: `scrape.py`의 `keys` 목록 수정(사용률 순서대로)
- 신규 특성/성격은 `build.py` 실행 시 `unmapped.txt`로 보고되니 `abil_kr` / `nat_kr`에 추가
