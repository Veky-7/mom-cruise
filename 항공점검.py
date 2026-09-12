# -*- coding: utf-8 -*-
"""트립닷컴 항공권 점검 — 헤드리스 크롬(Playwright)으로 페이지를 실제로 열어 읽는다.
가격점검.py 가 매일 09:00 함께 호출. 단독 실행: python 항공점검.py
"""
import asyncio, re, datetime
from playwright.async_api import async_playwright

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'
LEGS = [  # (표시, dcity, acity, 날짜, 쓸 수 있는 시간 조건)
    ('12/14 인천→나하', 'sel', 'oka', '2026-12-14', lambda dep, arr: arr <= '14:30'),   # 승선 마감 17:00
    ('12/13 인천→나하', 'sel', 'oka', '2026-12-13', lambda dep, arr: True),
    ('12/18 나하→인천', 'oka', 'sel', '2026-12-18', lambda dep, arr: dep >= '11:00'),   # 하선 07:00
]
BASE = {  # 2026-09-12 조회 기준 (1인, 위탁 수하물 포함)
    ('12/14 인천→나하', '진에어', '10:10'): 210700,
    ('12/14 인천→나하', '이스타항공', '11:25'): 205100,
    ('12/13 인천→나하', '진에어', '10:10'): 187300,
    ('12/18 나하→인천', '이스타항공', '15:00'): 218200,
    ('12/18 나하→인천', '진에어', '12:40'): 253700,
}
THRESH = 20000
AIRPORTS = {'ICN', 'GMP', 'PUS', 'OKA', 'TAE', 'CJJ'}

def parse(txt):
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    out = []
    for i, l in enumerate(lines):
        if not re.fullmatch(r'\d{2}:\d{2}', l) or i + 8 >= len(lines) or lines[i + 1] not in AIRPORTS:
            continue
        air = lines[i - 1] if lines[i - 1] != '저비용 항공사' else lines[i - 2]
        if not re.fullmatch(r'[가-힣A-Za-z ()]+', air):
            continue
        seg = lines[i + 2:i + 12]
        arr = next((s for s in seg if re.fullmatch(r'\d{2}:\d{2}', s)), None)
        price = next((s for s in seg if re.fullmatch(r'[\d,]+원', s)), None)
        direct = '직항' in seg[:5]
        if arr and price and direct:
            out.append((air, l, arr, int(price.replace(',', '').replace('원', ''))))
    # 중복 제거
    seen, res = set(), []
    for r in out:
        k = r[:3]
        if k not in seen:
            seen.add(k); res.append(r)
    return res

async def fetch_leg(pg, dcity, acity, date):
    url = f'https://kr.trip.com/flights/showfarefirst?dcity={dcity}&acity={acity}&ddate={date}&triptype=ow&class=y&quantity=3&locale=ko-KR&curr=KRW'
    await pg.goto(url, wait_until='domcontentloaded', timeout=60000)
    try:
        await pg.wait_for_selector('text=개 항공편 검색됨', timeout=45000)
    except Exception:
        pass
    await pg.wait_for_timeout(4000)
    return parse(await pg.inner_text('body'))

async def run():
    result = {'parts': [], 'alerts': [], 'fails': [], 'best': {}}
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(locale='ko-KR', user_agent=UA, viewport={'width': 1280, 'height': 900})
        pg = await ctx.new_page()
        for name, d, a, date, ok in LEGS:
            try:
                fl = await fetch_leg(pg, d, a, date)
                usable = [f for f in fl if ok(f[1], f[2])]
                if not usable:
                    raise RuntimeError('항공편 없음')
                best = min(usable, key=lambda f: f[3])
                result['best'][name] = list(best)
                result['parts'].append(f"{name} 최저 {best[0]} {best[1]} {best[3]:,}")
                for f in fl:
                    base = BASE.get((name, f[0], f[1]))
                    if base and base - f[3] >= THRESH:
                        result['alerts'].append(f'{name} {f[0]} {f[1]} {base:,} → {f[3]:,} (-{base - f[3]:,})')
            except Exception as e:
                result['fails'].append(name); result['parts'].append(f'{name} 조회 실패')
        await b.close()
    return result

def check():
    try:
        return asyncio.run(run())
    except Exception as e:
        return {'parts': ['항공 전체 조회 실패'], 'alerts': [], 'fails': ['항공 전체'], 'best': {}}

if __name__ == '__main__':
    r = check()
    print(datetime.date.today().isoformat(), '|', ' | '.join(r['parts']), '|', ('🔻 ' + ' / '.join(r['alerts'])) if r['alerts'] else '－ 변동 없음')
