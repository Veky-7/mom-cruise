# _build — 가이드북 HTML 만드는 재료

- `build.py` → `../엄마칠순_크루즈_2차안.html` (PC판) · `build_mobile.py` → `../엄마칠순_크루즈_2차안_모바일.html` (모바일판)
- 실행: `python _build/build.py && python _build/build_mobile.py` 그리고 `python _build/publish.py` 로 docs/ 에 감싸 넣고 커밋
- `data.py` — 객실·시설·기항지 본문(한국어). 내용 고칠 땐 여기
- `template.html` — PC판 뼈대 · `hotel_sec.html` — 전날 도착 안 섹션
- `b64.json` / `ship_b64.json` / `ports_b64.json` — 사진(base64). 원본 jpg 는 `img/`
- 사진 출처: MSC 크루즈 공식 사이트(msccruises.com) 벨리시마·기항지 페이지 — 가족 계획용
