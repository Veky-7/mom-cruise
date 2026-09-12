# -*- coding: utf-8 -*-
"""엄마 칠순 크루즈 — 트립닷컴 가격 점검 (매일 09:00, 작업 스케줄러)
읽는 것: 크루즈 12/06 · 12/14 · 12/22 객실별 최저가 + 항공 12/13 · 12/14 인천→나하, 12/18 나하→인천 (항공점검.py, 헤드리스 크롬)
하는 것: 가격로그.txt 에 한 줄 기록 → 3만 원 이상 내리면 윈도우 알림 + 바탕화면 알림 파일 + 휴대폰용 페이지(깃허브) 갱신
"""
import urllib.request, gzip, re, json, datetime, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import 항공점검
except Exception:
    항공점검 = None

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, '가격로그.txt')
SITE = os.path.join(HERE, 'docs')
DATES = ['2026-12-14', '2026-12-06', '2026-12-22']
BASE = {  # 2026-09-12 조회 기준값 (2인 1실 1인, 항만세 포함)
    '2026-12-14': {'내측': 597327, '발코니': 738587},  # 발코니 최저가 = 시야 일부 가림 등급 기준
    '2026-12-06': {'내측': 610780},
    '2026-12-22': {'내측': 610780},
}
THRESH = 30000
URL = 'https://kr.trip.com/cruises/line-73172-naha-hawaii-4night-msc-bellissima-msc/?departure={d}&locale=ko-KR'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36',
      'Accept-Language': 'ko-KR,ko;q=0.9', 'Accept-Encoding': 'gzip'}

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

def main():
    today = datetime.date.today().isoformat()
    parts, alerts, fails = [], [], []
    for d in DATES:
        try:
            p = fetch(d)
        except Exception as e:
            fails.append(d); parts.append(f'{d[5:]} 조회 실패'); continue
        seg = ' · '.join(f'{k} {fmt(p[k])}' for k in ['내측', '오션뷰', '발코니', '스위트'] if k in p)
        parts.append(f'{d[5:]} {seg}')
        for cab, base in BASE[d].items():
            v = p.get(cab)
            if isinstance(v, int) and base - v >= THRESH:
                alerts.append(f'{d[5:]} {cab} {base:,} → {v:,} (-{base - v:,})')
    # 항공권 (헤드리스 크롬)
    if 항공점검:
        fr = 항공점검.check()
        parts += ['✈ ' + x for x in fr['parts']]
        alerts += ['✈ ' + x for x in fr['alerts']]
        fails += fr['fails']
    verdict = '🔻 할인 ' + ' / '.join(alerts) if alerts else ('⚠ 일부 조회 실패' if fails else '－ 변동 없음')
    line = f'{today} | ' + ' | '.join(parts) + f' | {verdict}'

    old = open(LOG, encoding='utf-8').read() if os.path.exists(LOG) else ''
    head = '엄마 칠순 크루즈 — 트립닷컴 나하 벨리시마 가격 로그 (기준 2026-09-12: 12/14 내측 597,327 / 발코니(일부 가림) 738,587 · 2인1실 1인 · 항공 진에어 10:10 210,700 · 이스타 15:00 218,200)\n'
    body = old[len(head):] if old.startswith(head) else old
    open(LOG, 'w', encoding='utf-8').write(head + line + '\n' + body)

    if alerts:
        toast('🔻 크루즈 가격 내림', ' / '.join(alerts)[:200])
        desk = os.path.join(os.path.expanduser('~'), 'Desktop', '🔻 크루즈 할인 알림.txt')
        open(desk, 'a', encoding='utf-8').write(line + '\n')

    # 휴대폰용 페이지 갱신 → 깃허브 (실패해도 조용히 넘어감)
    try:
        rows = ''.join(f'<li>{l}</li>' for l in (head + line + '\n' + body).splitlines()[1:] if l.strip())
        html = ('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                '<meta name="robots" content="noindex"><title>크루즈 가격 로그</title><style>body{font-family:sans-serif;padding:16px;background:#fbf6ee;color:#4a3728;line-height:1.6}'
                'h1{font-size:20px}li{font-size:13px;padding:8px 0;border-bottom:1px dotted #ccc;word-break:break-all}li:first-child{background:#fff8e6;font-weight:700}</style></head><body>'
                f'<h1>엄마 칠순 크루즈 · 가격 로그</h1><p style="font-size:13px">{head.strip()}</p><ul>{rows}</ul><p><a href="./">← 가이드북</a></p></body></html>')
        open(os.path.join(SITE, 'price.html'), 'w', encoding='utf-8').write(html)
        subprocess.run(['git', 'add', 'price.html'], cwd=SITE, timeout=30, capture_output=True)
        subprocess.run(['git', '-c', 'user.name=price-check', '-c', 'user.email=noreply@example.com', 'commit', '-q', '-m', f'가격 로그 {today}'], cwd=SITE, timeout=30, capture_output=True)
        subprocess.run(['git', 'push', '-q', 'origin', 'main'], cwd=SITE, timeout=60, capture_output=True)
    except Exception:
        pass
    print(line)

if __name__ == '__main__':
    main()
