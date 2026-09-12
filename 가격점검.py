# -*- coding: utf-8 -*-
"""엄마 칠순 크루즈 — 트립닷컴 가격 점검 (매일 09:00, 작업 스케줄러)
읽는 것: 크루즈 12/06 · 12/14 · 12/22 객실별 최저가 + 항공 12/13 · 12/14 인천→나하, 12/18 나하→인천 (항공점검.py, 헤드리스 크롬)
남기는 것: 가격이력.json(표의 원본) · 가격로그.txt(사람이 읽는 한 줄) · docs/price.html(휴대폰용 비교표 → 깃허브)
보내는 것: 매일 텔레그램 @ysaios_bot 으로 요약 한 장 (변동 있으면 맨 위에 🔔)
알리는 것(윈도우 알림 + 바탕화면 파일): 어제보다 3만 원 이상 오르내림 · 역대 최저 갱신 · 매진 · 조회 실패
"""
import urllib.request, urllib.parse, gzip, re, json, datetime, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import 항공점검
except Exception:
    항공점검 = None

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, '가격로그.txt')
HIST = os.path.join(HERE, '가격이력.json')
SITE = os.path.join(HERE, 'docs')
DATES = ['2026-12-14', '2026-12-06', '2026-12-22']
CABINS = ['내측', '오션뷰', '발코니', '스위트']
LEGS = ['12/14 인천→나하', '12/13 인천→나하', '12/18 나하→인천']
BASE_DAY = '2026-09-12'          # 처음 조회한 날 = 표의 「기준」 열
THRESH = 30000                   # 크루즈: 하루 사이 이만큼 움직이면 알림
THRESH_AIR = 20000               # 항공
URL = 'https://kr.trip.com/cruises/line-73172-naha-hawaii-4night-msc-bellissima-msc/?departure={d}&locale=ko-KR'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36',
      'Accept-Language': 'ko-KR,ko;q=0.9', 'Accept-Encoding': 'gzip'}

# ───────── 조회 ─────────
def fetch(d):
    req = urllib.request.Request(URL.format(d=d), headers=UA)
    r = urllib.request.urlopen(req, timeout=40)
    data = r.read()
    if r.headers.get('Content-Encoding') == 'gzip':
        data = gzip.decompress(data)
    h = data.decode('utf-8', 'ignore')
    out = {}
    for m in re.finditer(r'"name":"(내측 객실|오션뷰|발코니|스위트)"[^{}]*?"isSoldOut":(true|false),"minPrice":(\d+)', h):
        name = {'내측 객실': '내측'}.get(m.group(1), m.group(1))
        out[name] = '매진' if m.group(2) == 'true' else int(m.group(3))
    if not out:
        raise RuntimeError('가격을 못 읽음')
    return out

def fmt(v):
    if v is None: return '조회 실패'
    return v if isinstance(v, str) else f'{v:,}'

def toast(title, msg):
    ps = f'''
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
$t = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
$x = $t.GetElementsByTagName("text"); $x.Item(0).AppendChild($t.CreateTextNode("{title}")) | Out-Null; $x.Item(1).AppendChild($t.CreateTextNode("{msg}")) | Out-Null
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("엄마칠순 크루즈").Show([Windows.UI.Notifications.ToastNotification]::new($t))
'''
    try:
        subprocess.run(['powershell', '-NoProfile', '-Command', ps], timeout=20, capture_output=True)
    except Exception:
        pass

# ───────── 이력 (표의 원본) ─────────
# 항목 키: 'C|12-14|내측' (크루즈) · 'F|12/14 인천→나하' (항공 최저)
# 값: 정수(원) · '매진' · None(조회 실패)
def load_hist():
    if os.path.exists(HIST):
        return json.load(open(HIST, encoding='utf-8'))
    return {}

def save_hist(h):
    json.dump(h, open(HIST, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

def label(key):
    k = key.split('|')
    return f'{k[1]} {k[2]}' if k[0] == 'C' else '✈ ' + k[1]

def item_keys():
    return [f'C|{d[5:]}|{c}' for d in DATES for c in CABINS] + [f'F|{l}' for l in LEGS]

# ───────── 오늘 조회 ─────────
def collect():
    today = {'cruise': {}, 'flight': {}, 'flight_best': {}, 'fails': []}
    for d in DATES:
        try:
            p = fetch(d)
            for c in CABINS:
                today['cruise'][f'C|{d[5:]}|{c}'] = p.get(c)
        except Exception:
            today['fails'].append(d[5:])
            for c in CABINS:
                today['cruise'][f'C|{d[5:]}|{c}'] = None
    if 항공점검:
        fr = 항공점검.check()
        for l in LEGS:
            b = fr.get('best', {}).get(l)
            today['flight'][f'F|{l}'] = b[3] if b else None
            today['flight_best'][f'F|{l}'] = f'{b[0]} {b[1]}' if b else ''
        today['fails'] += fr['fails']
    else:
        for l in LEGS:
            today['flight'][f'F|{l}'] = None
        today['fails'].append('항공 모듈 없음')
    return today

# ───────── 비교·판정 ─────────
def diff_txt(now, old):
    if not isinstance(now, int) or not isinstance(old, int):
        return '', 0
    d = now - old
    if d == 0: return '－', 0
    return (f'▼{-d:,}' if d < 0 else f'▲{d:,}'), d

def analyze(hist, today_day, vals):
    """알림 문구 목록. 어제(직전 기록일) 대비 · 역대 최저 · 매진 · 조회 실패"""
    days = sorted(k for k in hist if k != today_day)
    prev_day = days[-1] if days else None
    alerts = []
    for key in item_keys():
        v = vals.get(key)
        th = THRESH if key.startswith('C|') else THRESH_AIR
        name = label(key)
        if v is None:
            continue
        if v == '매진':
            pv = hist.get(prev_day, {}).get('v', {}).get(key) if prev_day else None
            if pv != '매진':
                alerts.append(f'⛔ {name} 매진')
            continue
        pv = hist.get(prev_day, {}).get('v', {}).get(key) if prev_day else None
        if isinstance(pv, int) and abs(v - pv) >= th:
            alerts.append(f'{"🔻" if v < pv else "🔺"} {name} {pv:,} → {v:,} ({v - pv:+,})')
        past = [hist[d]['v'].get(key) for d in days if isinstance(hist[d]['v'].get(key), int)]
        if past and v < min(past):
            alerts.append(f'⭐ {name} 역대 최저 {v:,}')
    return alerts

# ───────── 텔레그램 (@ysaios_bot · 토큰은 secrets/ 에서만) ─────────
SEC = 'D:/0_YS_AIOS/secrets'
PAGE_URL = 'https://veky-7.github.io/mom-cruise/price.html'

def tg_text(hist, today_day):
    """휴대폰 한 화면. 위: 판정 · 가운데: 12/14 객실 + 항공 · 아래: 3인 합계 · 링크. 한글은 폭이 달라 표 정렬 대신 줄마다 한 항목"""
    days = sorted(hist)
    prev = [d for d in days if d < today_day]; prev = prev[-1] if prev else None
    base = BASE_DAY if BASE_DAY in hist else days[0]
    tv, pv, bv = hist[today_day]['v'], (hist[prev]['v'] if prev else {}), hist[base]['v']
    best = hist[today_day].get('best', {})
    alerts, fails = hist[today_day].get('alerts', []), hist[today_day].get('fails', [])

    def d_(now, old):
        return diff_txt(now, old)[0] or '－'
    def item(name, key, extra=''):
        v = tv.get(key)
        if v is None:
            return f'• {name}  ⚠ 조회 실패'
        if v == '매진':
            return f'• {name}  ⛔ 매진'
        past = [hist[d]['v'].get(key) for d in days if d != today_day and isinstance(hist[d]['v'].get(key), int)]
        star = '  ⭐최저' if past and v < min(past) else ''
        return f'• {name}  <b>{v:,}</b>  (어제 {d_(v, pv.get(key))} · 기준 {d_(v, bv.get(key))}){star}{extra}'

    md = today_day[5:].replace('-', '/')
    if alerts:
        head = '🔔 <b>가격 변동 있음</b>\n' + '\n'.join(alerts)
    elif fails:
        head = f'⚠ 일부 조회 실패: {", ".join(map(str, fails))} (나머지는 정상)'
    else:
        head = '✅ 어제와 변동 없음'

    lines = [f'🚢 <b>엄마 칠순 크루즈 · {md} 아침 가격</b>', head, '', '📅 <b>12/14 출항</b> · 1인(2인1실)']
    lines += [item(c, f'C|12-14|{c}') for c in CABINS]
    lines += ['', '✈ <b>항공 최저</b> · 1인·수하물 포함']
    for l in LEGS:
        k = f'F|{l}'
        lines.append(item(l, k, f'\n   └ {best[k]}' if best.get(k) else ''))

    go, back, cv = tv.get('F|12/14 인천→나하'), tv.get('F|12/18 나하→인천'), tv.get('C|12-14|내측')
    if all(isinstance(x, int) for x in (go, back, cv)):
        one = cv + go + back
        bo = (bv.get('C|12-14|내측'), bv.get('F|12/14 인천→나하'), bv.get('F|12/18 나하→인천'))
        bt = sum(bo) if all(isinstance(x, int) for x in bo) else None
        lines += ['', f'👨‍👩‍👧 <b>3인 합계</b> (내측 + 항공 왕복)  <b>{one * 3:,}원</b>' + (f'  (기준 {d_(one * 3, bt * 3)})' if bt else '')]
    others = ' · '.join(f'{d[5:].replace("-", "/")} {fmt(tv.get(f"C|{d[5:]}|내측"))}' for d in DATES[1:])
    lines += ['', f'다른 날 내측: {others}',
              f'기준 = {base[5:].replace("-", "/")} 첫 조회 · 어제 = {prev[5:].replace("-", "/") if prev else "－"}',
              f'📊 표로 보기 → {PAGE_URL}']
    return '\n'.join(lines)

def telegram(text):
    try:
        token = open(os.path.join(SEC, 'telegram_bot_token.txt'), encoding='utf-8').read().strip()
        cid = open(os.path.join(SEC, 'telegram_chat_id.txt'), encoding='utf-8').read().strip()
        data = urllib.parse.urlencode({'chat_id': cid, 'text': text, 'parse_mode': 'HTML', 'disable_web_page_preview': '1'}).encode()
        r = urllib.request.urlopen(urllib.request.Request(f'https://api.telegram.org/bot{token}/sendMessage', data=data), timeout=20)
        return json.load(r).get('ok', False)
    except Exception as e:
        print('텔레그램 실패:', str(e)[:120])
        return False

# ───────── 휴대폰용 페이지 ─────────
def build_page(hist, today_day):
    days = sorted(hist)
    prev_day = [d for d in days if d < today_day]
    prev_day = prev_day[-1] if prev_day else None
    base_day = BASE_DAY if BASE_DAY in hist else days[0]
    tv, pv, bv = hist[today_day]['v'], (hist[prev_day]['v'] if prev_day else {}), hist[base_day]['v']
    best = hist[today_day].get('best', {})

    def cell_diff(now, old):
        t, d = diff_txt(now, old)
        cls = 'dn' if d < 0 else ('up' if d > 0 else 'eq')
        return f'<td class="{cls}">{t}</td>'

    def lowest(key):
        cand = [(hist[d]['v'].get(key), d) for d in days if isinstance(hist[d]['v'].get(key), int)]
        if not cand: return '<td></td>'
        v, d = min(cand)
        mark = ' ⭐' if isinstance(tv.get(key), int) and tv[key] == v else ''
        return f'<td>{v:,} <small>{d[5:].replace("-", "/")}</small>{mark}</td>'

    rows, cur_group = [], None
    for key in item_keys():
        grp = ('출항 ' + key.split('|')[1].replace('-', '/')) if key.startswith('C|') else '항공 (1인 · 수하물 포함)'
        if grp != cur_group:
            cur_group = grp
            rows.append(f'<tr class="g"><td colspan="5">{grp}</td></tr>')
        name = key.split('|')[2] if key.startswith('C|') else key.split('|')[1]
        sub = f'<br><small>{best[key]}</small>' if key in best and best[key] else ''
        v = tv.get(key)
        vt = fmt(v) if isinstance(v, int) else f'<span class="fail">{fmt(v)}</span>'
        past = [hist[d]['v'].get(key) for d in days if d != today_day and isinstance(hist[d]['v'].get(key), int)]
        star = ' ⭐' if isinstance(v, int) and past and v < min(past) else ''
        rows.append(f'<tr><th>{name}{sub}</th><td>{fmt(bv.get(key))}</td><td class="now">{vt}{star}</td>'
                    f'{cell_diff(v, pv.get(key)) if prev_day else "<td class=eq>－</td>"}{cell_diff(v, bv.get(key))}</tr>')

    # 1인 합계 = 12/14 객실 + 12/14 인천→나하 최저 + 12/18 나하→인천 최저
    tot = []
    go, back = tv.get('F|12/14 인천→나하'), tv.get('F|12/18 나하→인천')
    for c in CABINS:
        cv = tv.get(f'C|12-14|{c}')
        if isinstance(cv, int) and isinstance(go, int) and isinstance(back, int):
            bv14 = bv.get(f'C|12-14|{c}'); bgo = bv.get('F|12/14 인천→나하'); bbk = bv.get('F|12/18 나하→인천')
            bt = bv14 + bgo + bbk if all(isinstance(x, int) for x in (bv14, bgo, bbk)) else None
            t, d = diff_txt(cv + go + back, bt) if bt else ('', 0)
            cls = 'dn' if d < 0 else ('up' if d > 0 else 'eq')
            tot.append(f'<tr><th>{c}</th><td>{cv + go + back:,}</td><td class="{cls}">{t}</td><td>{(cv + go + back) * 3:,}</td></tr>')

    hist_rows = ''.join(f'<li>{hist[d]["line"]}</li>' for d in reversed(days) if hist[d].get('line'))
    alerts = hist[today_day].get('alerts', [])
    fails = hist[today_day].get('fails', [])
    if alerts:
        banner = '<div class="ban al">' + '<br>'.join(alerts) + '</div>'
    elif fails:
        banner = f'<div class="ban wr">⚠ 일부 조회 실패: {", ".join(fails)} — 다른 항목은 정상</div>'
    else:
        banner = '<div class="ban ok">어제와 변동 없음</div>'

    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>크루즈 가격 비교</title><style>
body{{font-family:-apple-system,"Malgun Gothic",sans-serif;margin:0;padding:14px 12px 40px;background:#fbf6ee;color:#4a3728;line-height:1.5}}
h1{{font-size:19px;margin:0 0 2px}} h2{{font-size:15px;margin:22px 0 6px}} .sub{{font-size:12px;color:#8a7360;margin:0 0 10px}}
.ban{{padding:10px 12px;border-radius:10px;font-size:14px;font-weight:700;margin:10px 0 14px}}
.ok{{background:#e9f3e6;color:#2f6b2a}} .al{{background:#fff0e6;color:#b5451b}} .wr{{background:#fff8dc;color:#8a6d00}}
.tw{{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:0 -12px;padding:0 12px}}
table{{border-collapse:collapse;font-size:12.5px;white-space:nowrap;min-width:100%}}
th,td{{padding:7px 4px;border-bottom:1px solid #eadfcf;text-align:right}} th{{text-align:left;font-weight:600}}
thead th{{text-align:right;font-size:11px;color:#8a7360;font-weight:600;border-bottom:2px solid #d9c9b2}} thead th:first-child{{text-align:left}}
tr.g td{{text-align:left;font-weight:700;background:#f3ebdd;color:#6b5140;font-size:12px;padding:5px 6px}}
td.now{{font-weight:700;color:#2b1d14}} td.dn{{color:#1a5fd6;font-weight:700;font-size:12px}} td.up{{color:#c8322b;font-weight:700;font-size:12px}} td.eq{{color:#b3a494}}
.fail{{color:#c8322b;font-size:11px}} small{{color:#8a7360;font-weight:400}}
ul{{padding-left:0;list-style:none;margin:0}} li{{font-size:12px;padding:8px 0;border-bottom:1px dotted #ccc;word-break:break-all;color:#6b5140}}
.note{{font-size:11.5px;color:#8a7360;margin-top:8px}} a{{color:#8a5a2b}}
</style></head><body>
<h1>엄마 칠순 크루즈 · 가격 비교</h1>
<p class="sub">오늘 {today_day.replace("-", "/")} 조회 · 매일 아침 9시 자동 · 트립닷컴 · 2인 1실 1인 요금(항만세 포함)</p>
{banner}
<div class="tw"><table>
<thead><tr><th>항목</th><th>기준<br>{base_day[5:].replace("-", "/")}</th><th>오늘</th><th>어제<br>대비</th><th>기준<br>대비</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
<p class="note">▼ 파랑 = 내림 · ▲ 빨강 = 오름 · ⭐ = 오늘이 역대 최저 · 발코니 최저가는 시야 일부 가림 등급 기준 · 항공은 승선(17시)·하선(7시)에 맞는 직항 중 최저</p>
<h2>12/14 출항 · 1인 합계 (객실 + 항공 왕복 최저)</h2>
<div class="tw"><table><thead><tr><th>객실</th><th>1인</th><th>기준比</th><th>3인</th></tr></thead><tbody>{''.join(tot) or '<tr><td colspan="4">항공 조회 실패로 계산 불가</td></tr>'}</tbody></table></div>
<p class="note">3인 = 1인 × 3 단순 계산. 실제 3인 1실 요금은 3번째 사람 할인이 있어 이보다 낮을 수 있음</p>
<h2>역대 최저 (언제 제일 쌌나)</h2>
<div class="tw"><table><thead><tr><th>항목</th><th>최저 · 날짜</th><th>오늘</th></tr></thead><tbody>
{''.join(f'<tr><th>{label(k)}</th>{lowest(k)}<td>{fmt(tv.get(k))}</td></tr>' for k in item_keys())}
</tbody></table></div>
<h2>매일 기록</h2><ul>{hist_rows}</ul>
<p><a href="./">← 가이드북</a></p></body></html>'''

# ───────── 메인 ─────────
def main():
    today = datetime.date.today().isoformat()
    hist = load_hist()
    got = collect()
    vals = {**got['cruise'], **got['flight']}
    alerts = analyze(hist, today, vals)

    # 사람이 읽는 한 줄
    parts = []
    for d in DATES:
        seg = ' · '.join(f'{c} {fmt(vals[f"C|{d[5:]}|{c}"])}' for c in CABINS if vals.get(f'C|{d[5:]}|{c}') is not None)
        parts.append(f'{d[5:]} ' + (seg or '조회 실패'))
    for l in LEGS:
        v = vals.get(f'F|{l}')
        parts.append(f'✈ {l} ' + (f'최저 {got["flight_best"].get(f"F|{l}", "")} {v:,}' if isinstance(v, int) else '조회 실패'))
    verdict = ' / '.join(alerts) if alerts else ('⚠ 일부 조회 실패' if got['fails'] else '－ 변동 없음')
    line = f'{today} | ' + ' | '.join(parts) + f' | {verdict}'

    hist[today] = {'v': vals, 'best': got['flight_best'], 'alerts': alerts, 'fails': got['fails'], 'line': line}
    save_hist(hist)

    head = ('엄마 칠순 크루즈 — 트립닷컴 나하 벨리시마 가격 로그 (기준 2026-09-12: 12/14 내측 597,327 / 발코니(일부 가림) 738,587 · '
            '2인1실 1인 · 항공 진에어 10:10 210,700 · 이스타 15:00 218,200)\n')
    old = open(LOG, encoding='utf-8').read() if os.path.exists(LOG) else ''
    body = old[len(head):] if old.startswith(head) else old
    open(LOG, 'w', encoding='utf-8').write(head + line + '\n' + body)

    # 알림: 오르내림·최저·매진은 물론 조회 실패도 알린다 (조용히 죽는 것 방지)
    if alerts:
        toast('크루즈 가격 변동', ' / '.join(alerts)[:200])
        desk = os.path.join(os.path.expanduser('~'), 'Desktop', '🔻 크루즈 가격 알림.txt')
        open(desk, 'a', encoding='utf-8').write(line + '\n')
    elif got['fails']:
        toast('⚠ 크루즈 가격 조회 실패', ', '.join(map(str, got['fails']))[:200] + ' — 트립닷컴 페이지가 바뀌었을 수 있음')

    # 휴대폰용 비교표 → 깃허브
    try:
        open(os.path.join(SITE, 'price.html'), 'w', encoding='utf-8').write(build_page(hist, today))
        g = ['git', '-c', 'user.name=price-check', '-c', 'user.email=noreply@example.com']
        subprocess.run(g + ['add', 'price.html'], cwd=SITE, timeout=30, capture_output=True)
        subprocess.run(g + ['commit', '-q', '-m', f'가격 로그 {today}'], cwd=SITE, timeout=30, capture_output=True)
        subprocess.run(g + ['pull', '-q', '--rebase', 'origin', 'main'], cwd=SITE, timeout=60, capture_output=True)
        r = subprocess.run(g + ['push', '-q', 'origin', 'main'], cwd=SITE, timeout=60, capture_output=True, text=True)
        if r.returncode != 0:
            print('푸시 실패:', r.stderr.strip()[:200])
    except Exception as e:
        print('페이지 갱신 실패:', e)
    telegram(tg_text(hist, today))
    print(line)

if __name__ == '__main__':
    main()
