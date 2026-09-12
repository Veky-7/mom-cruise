# -*- coding: utf-8 -*-
"""모바일 전용 반응형 버전 — 엄마칠순_크루즈_2차안_모바일.html"""
import json, re, html, base64, io, importlib.util
from PIL import Image

import os
D = os.path.dirname(os.path.abspath(__file__)) + '/'
OUT = 'D:/정이서/엄마칠순/엄마칠순_크루즈_2차안_모바일.html'
spec = importlib.util.spec_from_file_location('data', D+'data.py'); data = importlib.util.module_from_spec(spec); spec.loader.exec_module(data)
CABINS, FAC, PORTS = data.CABINS, data.FAC, data.PORTS

b = json.load(open(D+'b64.json')); ship = json.load(open(D+'ship_b64.json')); ports = json.load(open(D+'ports_b64.json'))
RAW = {}; RAW.update(ship); RAW.update(ports)
for k in ['hero_wide','mini','galleria_sq','buffet_sq','theatre_sq','pool_sq','pool','balcony','galleria','skylounge','aquapark','interior','oceanview','buffet','lighthouse','theatre','spa','cerisier']:
    RAW[k] = b[k]

def shrink(v, w, q=72):
    head, body = v.split(',', 1)
    if 'webp' in head: return v
    im = Image.open(io.BytesIO(base64.b64decode(body))).convert('RGB')
    if im.width > w: im = im.resize((w, int(im.height*w/im.width)), Image.LANCZOS)
    o = io.BytesIO(); im.save(o, 'JPEG', quality=q, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(o.getvalue()).decode()

IMG = {}
def use(k, w=520):
    if k not in IMG: IMG[k] = shrink(RAW[k], w)
    return k

def esc(s): return html.escape(s, quote=True)

# ───────────────────────── CSS ─────────────────────────
CSS = '''
:root{--cream:#fbf6ee;--cream2:#f6eee1;--paper:#fffdf8;--ink:#4a3728;--ink2:#7d6753;--line:#e6d9c6;--terra:#c4703f;--sage:#8fae96;--rose:#d99b9b;--gold:#d9a441;--sea:#3f7f97;
--f-ttl:'Hakgyoansim Allimjang TTF B','Hakgyoansim Allimjang TTF R',Jua,sans-serif;--f-hd:Jua,sans-serif;--f-num:Dongle,Jua,sans-serif;--f-hand:'Gamja Flower',Gaegu,cursive;--f-en:'Nothing You Could Do','Gamja Flower',cursive}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;-webkit-tap-highlight-color:transparent}
body{background:var(--cream);color:var(--ink);font-family:Pretendard,'Apple SD Gothic Neo','Malgun Gothic',sans-serif;font-size:15.5px;line-height:1.65;padding-block:0 84px;padding-inline:0;font-variant-numeric:tabular-nums;overflow-x:hidden}
body::before{content:'';position:fixed;inset:0;z-index:0;pointer-events:none;opacity:.5;background-image:radial-gradient(rgba(120,90,60,.05) 1px,transparent 1px);background-size:4px 4px}
b{font-weight:800;color:var(--ink)}
img{max-width:100%}
.wrap{position:relative;z-index:1;padding:0 16px;max-width:640px;margin:0 auto}
h1,h2{font-family:var(--f-ttl);font-weight:400;line-height:1.22;text-wrap:balance}
h3{font-family:var(--f-hd);font-weight:400;line-height:1.22}
.script{font-family:var(--f-en);color:var(--terra);font-size:22px;line-height:1}
.pin{font-size:11.5px;font-weight:800;padding:3px 10px;border-radius:20px;white-space:nowrap;display:inline-block}
.p-free{background:#eaf1ea;color:#4f7a58;border:1px solid #c6dbc9}.p-pay{background:#fdf0e4;color:#a75a25;border:1px solid #eccfaf}.p-pick{background:#fff5d6;color:#8a6a2e;border:1px solid #f0dcae}.p-ton{background:#e4eff2;color:#2f6d84;border:1px solid #c3dbe3}

/* 상단 바 */
.top{position:sticky;top:0;z-index:50;background:rgba(251,246,238,.92);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);border-bottom:1.4px solid var(--line);padding:10px 16px;display:flex;align-items:center;gap:10px}
.top .t{font-family:var(--f-hd);font-size:18px;flex:1}
.top .d{font-family:var(--f-en);color:var(--terra);font-size:15px}

/* 히어로 */
.hero{padding:22px 0 8px}
.hero h1{font-size:34px;margin:4px 0 10px}
.hero h1 em{font-style:normal;color:var(--terra);position:relative;display:inline-block}
.hero h1 em::after{content:'';position:absolute;left:-2%;right:-2%;bottom:.1em;height:.28em;z-index:-1;background:linear-gradient(90deg,rgba(217,164,65,.42),rgba(217,155,155,.42));border-radius:4px}
.hero p{color:var(--ink2);font-size:15px;margin-bottom:14px}
.shot{position:relative;margin:6px 0 14px}
.shot .fr{border-radius:52% 48% 46% 54%/48% 52% 48% 52%;overflow:hidden;border:3px solid #fff;box-shadow:0 20px 44px -22px rgba(90,60,35,.5);aspect-ratio:3/2;background:var(--cream2)}
.shot .fr img{width:100%;height:100%;object-fit:cover;display:block}
.chips{display:flex;gap:8px;flex-wrap:wrap}
.chips span{background:#fff;border:1.4px solid var(--line);border-radius:30px;padding:7px 13px;font-size:13px;font-weight:800;color:var(--sea)}
.chips span:nth-child(2){color:var(--sage)}.chips span:nth-child(3){color:var(--terra)}
.cta{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:14px 0 6px}
.cta a{display:flex;align-items:center;justify-content:center;gap:6px;text-decoration:none;font-weight:800;font-size:14.5px;padding:14px 10px;border-radius:40px;min-height:48px}
.cta a.solid{background:var(--terra);color:#fff;box-shadow:0 8px 20px -8px rgba(196,112,63,.7)}
.cta a.ghost{border:1.6px solid var(--ink);color:var(--ink)}

/* 배지 */
.badges{display:grid;grid-template-columns:1fr 1fr;gap:14px;padding:18px 0 26px;text-align:center}
.bg1{display:flex;flex-direction:column;align-items:center;gap:6px}
.bg1 .circ{width:124px;height:124px;border-radius:50%;overflow:hidden;border:2.5px solid #fff;box-shadow:0 12px 26px -14px rgba(90,60,35,.55);background:var(--cream2)}
.bg1 .circ img{width:100%;height:100%;object-fit:cover}
.bg1 .num{font-family:var(--f-num);font-weight:700;font-size:58px;line-height:.75;color:var(--terra);margin-top:6px}
.bg1 .num small{font-size:26px}
.bg1 .lb{font-size:13px;font-weight:800;color:var(--ink2)}

/* 섹션 */
.band{padding:28px 0 24px}
.band.sage{background:#eef3ec}.band.rose{background:#faf0ee}.band.paper{background:var(--paper)}
.torn{height:30px;line-height:0}.torn svg{width:100%;height:30px;display:block}
.shead{margin-bottom:16px}
.shead h2{font-size:27px}
.shead p{color:var(--ink2);font-size:14px;margin-top:6px}
.sechd{display:flex;align-items:center;gap:12px;margin:26px 0 12px}
.sechd .hp{width:78px;height:78px;border-radius:50%;flex:none;background-size:cover;background-position:center;border:2.5px solid #fff;box-shadow:0 12px 26px -16px rgba(90,60,35,.7)}
.sechd .en{font-family:var(--f-en);font-size:16px;color:var(--terra);line-height:1.1}
.sechd h3{font-size:22px;margin:1px 0 2px}
.sechd .sub{font-size:13px;color:#6b5745;line-height:1.4}

/* 카드 */
.card{background:#fff;border:1.5px solid var(--line);border-radius:18px;padding:16px;margin-bottom:12px;box-shadow:0 6px 18px -12px rgba(90,60,35,.5)}
.card.pick{border:2px solid var(--gold);background:#fffdf6}
.card .no{font-family:var(--f-en);font-size:20px;color:var(--rose)}
.card .nm{font-family:var(--f-hd);font-size:21px;line-height:1.25;margin:2px 0 2px}
.card .ship{font-size:13px;color:var(--ink2);font-weight:800;margin-bottom:8px}
.won{font-family:var(--f-num);font-weight:700;font-size:44px;line-height:.8;color:var(--sea);margin:6px 0 2px}
.won small{font-size:22px;color:var(--ink2)}
.per{font-size:13px;color:var(--ink2);font-weight:800;margin-bottom:8px}
.card ul{margin:8px 0 0 18px;font-size:14px;color:var(--ink2)}
.bd{display:inline-block;margin-top:10px;font-size:12px;font-weight:800;padding:5px 12px;border-radius:20px}
.b-pick{background:#fdf0e4;color:#a75a25;border:1px solid #eccfaf}.b-ok{background:#eaf1ea;color:#4f7a58;border:1px solid #c6dbc9}.b-hmm{background:#f8eeee;color:#a35858;border:1px solid #ebcaca}
.note{background:#fff8e8;border:1.5px solid #f0dcae;border-radius:14px;padding:12px 14px;font-size:14px;color:#8a6a2e;margin:12px 0}
.note b{color:#6f4f1c}
.warn{background:#f8efee;border:1.5px solid #ecd2cf;border-radius:14px;padding:12px 14px;font-size:14px;color:#8a4a44;margin:12px 0}
.warn b{color:#7a3a35}
.note ul,.warn ul{margin:6px 0 0 16px}

/* 접이식 */
details{background:#fff;border:1.5px solid var(--line);border-radius:16px;margin-bottom:10px;overflow:hidden}
details summary{list-style:none;cursor:pointer;padding:14px 16px;font-family:var(--f-hd);font-size:18px;display:flex;align-items:center;gap:10px;min-height:52px}
details summary::-webkit-details-marker{display:none}
details summary::after{content:'+';margin-left:auto;font-family:var(--f-num);font-size:30px;color:var(--terra);line-height:.6}
details[open] summary::after{content:'–'}
details .dbody{padding:0 16px 16px;font-size:14.5px;color:var(--ink2)}
details summary .pin{margin-left:auto}
details summary .pin + .pin{margin-left:6px}

/* 표 → 행 목록 */
.rows{display:grid;gap:6px}
.row{display:flex;justify-content:space-between;gap:10px;align-items:baseline;padding:9px 12px;background:var(--paper);border:1.2px solid var(--line);border-radius:12px;font-size:14px}
.row b.v{font-family:var(--f-num);font-size:24px;line-height:.8;color:var(--sea);white-space:nowrap}
.row.hl{background:#fff8e6;border-color:var(--gold)}
.row.sum{background:#fdf9f2;border-color:var(--ink);font-weight:800}
.row small{color:var(--ink2);font-size:12px;display:block}
.tbl{overflow-x:auto;-webkit-overflow-scrolling:touch;background:#fff;border:1.5px solid var(--line);border-radius:14px;margin:10px 0}
table{border-collapse:collapse;width:100%;font-size:13.5px;min-width:420px}
th,td{padding:8px 10px;text-align:left;border-bottom:1.2px dotted #e3d5be;vertical-align:top;white-space:nowrap}
th{font-family:var(--f-hd);font-weight:400;color:var(--ink2);border-bottom:1.6px solid var(--line)}
td.num,th.num{text-align:right}
tr.hl td{background:#fff8e6}tr.sum td{border-top:1.6px solid var(--ink);font-weight:800;background:#fdf9f2}

/* 항로 타임라인 */
.tl{list-style:none;position:relative;padding-left:26px;margin:8px 0}
.tl::before{content:'';position:absolute;left:8px;top:6px;bottom:6px;width:2px;background:repeating-linear-gradient(180deg,rgba(63,127,151,.6) 0 8px,transparent 8px 14px)}
.tl li{position:relative;padding:6px 0 10px;font-size:14.5px;color:var(--ink2)}
.tl li::before{content:'';position:absolute;left:-23px;top:12px;width:12px;height:12px;border-radius:50%;background:var(--sea);border:2px solid #fff;box-shadow:0 0 0 2px rgba(63,127,151,.3)}
.tl li b{color:var(--ink);display:block;font-size:15.5px}
.tl li .t{font-family:var(--f-en);color:var(--terra);font-size:15px;margin-right:6px}

/* 사진 카드 그리드 */
.pgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.pc{background:#fff;border:1.5px solid var(--line);border-radius:16px;overflow:hidden;cursor:pointer;display:flex;flex-direction:column;box-shadow:0 5px 16px -12px rgba(90,60,35,.55)}
.pc:active{transform:scale(.98)}
.pc img{width:100%;height:auto;aspect-ratio:16/10;object-fit:cover;display:block;background:var(--cream2)}
.pc .in{padding:10px 11px 11px;flex:1;display:flex;flex-direction:column}
.pc .nm{font-family:var(--f-hd);font-size:15.5px;line-height:1.25;margin-bottom:3px}
.pc .ds{font-size:12.5px;color:var(--ink2);line-height:1.5;flex:1}
.pc .ft{display:flex;gap:5px;flex-wrap:wrap;margin-top:7px;align-items:center}
.pc .more{font-family:var(--f-hand);font-size:15px;color:var(--terra);margin-left:auto}
.pc.best{border:2px solid var(--gold)}
.pc[hidden]{display:none}
.pc.wide{grid-column:1/-1}
.pc.wide .won{font-size:38px}
.cats{display:flex;gap:8px;overflow-x:auto;-webkit-overflow-scrolling:touch;padding:2px 0 10px;scrollbar-width:none}
.cats::-webkit-scrollbar{display:none}
.cats button{flex:none;font:inherit;font-size:13.5px;font-weight:800;color:var(--ink2);background:#fff;border:1.4px solid var(--line);padding:9px 14px;border-radius:24px;min-height:40px}
.cats button.on{border-color:var(--terra);color:var(--terra);background:#fdf3ea}
.cats button b{font-family:var(--f-num);font-size:20px;line-height:.8;margin-left:3px}

/* 기항지 */
.port{background:#fff;border:1.5px solid var(--line);border-radius:20px;overflow:hidden;margin-bottom:16px}
.port .phead{position:relative;height:190px}
.port .phead img{width:100%;height:100%;object-fit:cover;display:block}
.port .phead .pt{position:absolute;left:0;right:0;bottom:0;padding:14px 16px 12px;background:linear-gradient(transparent,rgba(40,25,15,.8));color:#fff}
.port .phead .pt .en{font-family:var(--f-en);font-size:17px;color:#ffd58a;line-height:1}
.port .phead .pt h3{font-size:26px;color:#fff;margin:2px 0}
.port .phead .pt .tm{font-size:13px;font-weight:800}
.port .pbody{padding:14px 16px 16px}
.port .pbody > p{font-size:14.5px;color:var(--ink2);margin-bottom:8px}
.port details{margin-top:10px}
.route2{list-style:none;counter-reset:r}
.route2 li{position:relative;padding:8px 0 8px 36px;border-bottom:1.2px dotted #e3d5be;font-size:14px;line-height:1.55;color:var(--ink2)}
.route2 li:last-child{border-bottom:0}
.route2 li::before{content:counter(r);counter-increment:r;position:absolute;left:0;top:9px;width:26px;height:26px;border-radius:50%;background:var(--sea);color:#fff;font-family:var(--f-hand);font-size:17px;text-align:center;line-height:26px}
.route2 li b{color:var(--ink)}
.route2 li .t{font-family:var(--f-en);color:var(--terra);font-size:14px;margin-right:6px}

/* 바텀 시트 */
.dim{position:fixed;inset:0;background:rgba(60,40,25,.5);opacity:0;pointer-events:none;transition:.25s;z-index:98}
.dim.on{opacity:1;pointer-events:auto}
.sheet{position:fixed;left:0;right:0;bottom:0;height:92vh;height:92dvh;background:var(--paper);z-index:99;border-radius:22px 22px 0 0;transform:translateY(105%);transition:.32s cubic-bezier(.2,.8,.2,1);overflow-y:auto;-webkit-overflow-scrolling:touch;box-shadow:0 -20px 50px -20px rgba(60,40,25,.5)}
.sheet.on{transform:none}
.sheet .grip{position:sticky;top:0;z-index:2;background:var(--paper);padding:10px 0 6px;text-align:center}
.sheet .grip i{display:inline-block;width:44px;height:5px;border-radius:3px;background:var(--line)}
.sheet .sclose{position:absolute;top:8px;right:12px;width:40px;height:40px;border-radius:50%;border:0;background:#fff;box-shadow:0 6px 16px -6px rgba(0,0,0,.4);font-size:22px;color:var(--ink)}
.sheet .simg{width:100%;height:56vw;max-height:360px;aspect-ratio:16/10;object-fit:cover;display:block;background:var(--cream2)}
.sheet .sbody{padding:16px 18px 40px}
.sheet .sen{font-family:var(--f-en);font-size:18px;color:var(--terra);line-height:1.1}
.sheet h3{font-size:24px;margin:2px 0 4px}
.sheet .ssub{font-size:14px;color:#6b5745;margin-bottom:10px}
.sheet .stags{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px}
.sheet .stags span{font-size:12px;font-weight:800;padding:4px 10px;border-radius:20px;background:#fff;border:1.4px solid var(--line);color:var(--ink2)}
.sheet .stags span.free{background:#eaf1ea;color:#4f7a58;border-color:#c6dbc9}.sheet .stags span.pay{background:#fdf0e4;color:#a75a25;border-color:#eccfaf}.sheet .stags span.pick{background:#fff5d6;color:#8a6a2e;border-color:#f0dcae}
.sheet p{font-size:14.5px;line-height:1.7;color:var(--ink2);margin-bottom:10px}
.sheet ul{margin:0 0 12px 18px;font-size:14px;color:var(--ink2);line-height:1.65}
.sheet .tip{background:#fff8e8;border:1.5px solid #f0dcae;border-radius:12px;padding:11px 14px;font-size:13.5px;color:#8a6a2e}
.sheet .tip b{color:#6f4f1c}
.sheet .gal{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:4px 0 12px}
.sheet .gal img{width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:8px;display:block}
.sheet table{min-width:0;font-size:13px}
.sheet .tbl{margin:8px 0 12px}
body.lock{overflow:hidden}

/* 하단 탭 */
.tabs{position:fixed;left:0;right:0;bottom:0;z-index:60;background:rgba(255,253,248,.96);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);border-top:1.4px solid var(--line);display:grid;grid-template-columns:repeat(6,1fr);padding:6px 4px calc(6px + env(safe-area-inset-bottom))}
.tabs a{text-decoration:none;color:var(--ink2);font-size:11px;font-weight:800;text-align:center;padding:4px 0;min-height:48px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;border-radius:12px}
.tabs a i{font-style:normal;font-size:18px;line-height:1}
.tabs a:active{background:var(--cream2)}
.check{list-style:none}
.check li{display:grid;grid-template-columns:22px 1fr;gap:10px;padding:8px 0;border-bottom:1.2px dotted #e3d5be;font-size:14.5px;color:var(--ink2)}
.check li:last-child{border-bottom:0}
.check li i{width:18px;height:18px;border:2px solid var(--sea);border-radius:5px;margin-top:3px}
ol.steps{margin:0 0 0 20px;font-size:14.5px;color:var(--ink2);display:grid;gap:6px}
ol.steps li::marker{color:var(--sea);font-weight:800}
footer{padding:36px 16px 30px;text-align:center;color:var(--ink2);font-size:13px;line-height:1.8}
footer .sign{font-family:var(--f-en);font-size:28px;color:var(--terra);margin-bottom:8px}
footer img{max-width:280px;margin:16px auto 0;display:block;opacity:.85}
a{color:var(--sea)}
@media (min-width:640px){.pgrid{grid-template-columns:repeat(3,1fr)}.badges{grid-template-columns:repeat(4,1fr)}}
@media (prefers-reduced-motion:reduce){.sheet,.dim{transition:none}}
'''

TORN = lambda fill: f'<div class="torn"><svg viewBox="0 0 1200 38" preserveAspectRatio="none"><path fill="{fill}" d="M0,20 C60,6 110,32 170,18 C230,4 280,30 340,17 C400,4 450,31 510,19 C570,7 620,33 680,20 C740,7 790,32 850,18 C910,4 960,30 1020,17 C1080,4 1140,28 1200,15 L1200,38 L0,38 Z"/></svg></div>'

def rows(items, cls=''):
    out = ''
    for it in items:
        c = it[2] if len(it) > 2 else ''
        out += f'<div class="row {c}"><span>{it[0]}</span><b class="v">{it[1]}</b></div>'
    return f'<div class="rows">{out}</div>'

# ───────────────────────── 본문 ─────────────────────────
P = []
P.append(f'''<div class="top"><span class="d">70th</span><span class="t">엄마 칠순 크루즈</span><span class="d">Naha 12/14</span></div>
<div class="wrap">
<div class="hero">
<div class="script">For Mom's 70th birthday · 김현순</div>
<h1>엄마 칠순<br><em>크루즈 여행</em> 2차안</h1>
<div class="shot"><div class="fr"><img data-img="{use('hero_wide',720)}" alt="MSC 벨리시마"></div></div>
<div class="chips"><span>🌊 17만 톤 · 5,655명</span><span>🌴 12월에도 낮 20도</span><span>👩‍👩‍👧 세 식구 한 방</span></div>
<p>9/18 부산 출발이 안 되면서 올해 한국 출발 대형선은 끝. 일본·대만·중국·홍콩 출발 큰 배를 다 뒤져 <b>나하(오키나와) 출발 MSC 벨리시마 12/14</b>로 거의 확정. <b>김현순</b> 어머니 · <b>정이서</b> · <b>정해민</b>, 셋이서.</p>
<div class="cta"><a class="solid" href="#ship">🚢 배 안 구경</a><a class="ghost" href="#ports">🗺 기항지 루트</a></div>
</div>
<div class="badges">
<div class="bg1"><div class="circ"><img data-img="{use('galleria_sq',300)}" alt=""></div><div class="num">96<small>m</small></div><div class="lb">LED 돔 실내 산책로</div></div>
<div class="bg1"><div class="circ"><img data-img="{use('buffet_sq',300)}" alt=""></div><div class="num">20<small>시간</small></div><div class="lb">하루 뷔페 · 100종</div></div>
<div class="bg1"><div class="circ"><img data-img="{use('theatre_sq',300)}" alt=""></div><div class="num">10<small>개</small></div><div class="lb">레스토랑 · 바 20개</div></div>
<div class="bg1"><div class="circ"><img data-img="{use('pool_sq',300)}" alt=""></div><div class="num">4<small>박 5일</small></div><div class="lb">매일 기항 · 해상일 0</div></div>
</div>
</div>''')

# 결론
P.append(TORN('#eef3ec') + '''<div class="band sage" id="pick"><div class="wrap">
<div class="shead"><div class="script">Our Pick</div><h2>결론 — 나하 벨리시마로 간다</h2><p>3명 · 항공 포함 총액. A안은 크루즈(크루즈TMK·트립닷컴)와 항공 둘 다 9/12 실제 조회값.</p></div>
<div class="card pick"><div class="no">A</div><div class="nm">12/14 나하(오키나와) 출발 4박 5일</div><div class="ship">MSC 벨리시마 · 17만 톤 · 매일 기항</div>
<div class="won">355<small>만</small></div><div class="per">내측 3인 1실 + 항공 · 1인 118만 (전날 1박 안 370만)</div>
<div class="won">416<small>만</small></div><div class="per">발코니 3인 1실 + 항공 · 1인 139만 (전날 1박 안 431만)</div>
<ul><li>인천→나하 직항 하루 7편, 1인 왕복 42만</li><li>세 식구 한 방 + 발코니 가능</li><li>일본 무비자 · 공항→항구 20분</li></ul><span class="bd b-pick">💛 거의 확정</span></div>
<details><summary>B안 · 12/8 지룽(타이베이) 출발 <span class="pin p-ton">310~340만</span></summary><div class="dbody">같은 배·같은 항로를 대만에서 탐. 내측 2인실(590,600×2) + 1인실(778,947, 1.3배) = 196만 + 팁·출국세 37만 + 항공 인천↔타이베이 75~105만. 1인 103~113만.<br>A보다 10~30만 절약 / 비행 2.5시간 + 항구까지 1시간 / 발코니 매진·3인실 없음. <b>값이 먼저면 B.</b></div></details>
<details><summary>C안 · 10/7·16 상하이 출발 스펙트럼 <span class="pin p-ton">220~300만</span></summary><div class="dbody">로얄캐리비안 16.9만 톤. 인터파크 10/7 439,894원 · 10/16 464,820원(내측 1인). 3인 크루즈 132~176만 + 팁 29만 + 항공 인천↔상하이 60~90만. 1인 74~98만.<br>가장 싸지만 중·일 갈등으로 일본 기항이 전부 <b>부산 하나</b>로 바뀜, 손님·방송 대부분 중국인. <b>싼 이유가 있다.</b></div></details>
</div></div>''')

# 공식 vs 트립닷컴
P.append(TORN('#fbf6ee') + '''<div class="wrap" id="official" style="padding-top:20px">
<div class="shead"><div class="script">Official or not?</div><h2>공식 사이트에서 사야 하는 거 아니야?</h2><p>MSC 한국 공식 사이트는 온라인 판매를 안 하고 <b>공식 파트너 여행사 10곳</b>으로 보냅니다. 유튜브 크달도 그중 하나인 크루즈TMK 예약창으로 연결. 나하 12/14 · 성인 3명으로 직접 뽑았습니다.</p></div>
<div class="card"><div class="nm">한국 · 크루즈TMK (크달 링크)</div><div class="ship">공식 파트너 · 3인 1실 총액 · 세금 포함 · 팁 별도</div>''' + rows([('디럭스 인테리어 IR1','191만'),('디럭스 발코니 파셜뷰 BP','238만'),('디럭스 발코니 BR1','252만')]) + '''<div class="per" style="margin-top:8px">판타스티카 요금제 — 선실 선택 · 일정 변경 1회 무료 · 룸서비스 무료 · 한국어 1544-3441</div></div>
<div class="card"><div class="nm">트립닷컴 · 9/12 실조회</div><div class="ship">같은 배·같은 날 · 3인 1실 총액 · 항만세 포함</div>''' + rows([('럭셔리 인사이드','192만'),('럭셔리 발코니 (일부 가림)','239만'),('럭셔리 발코니','253만')]) + '''</div>
<div class="card"><div class="nm">일본 · MSC 정규 특약점</div><div class="ship">IMA · 2인 1실 1인 · 정가 기준선</div>''' + rows([('인사이드 ¥65,980','59만'),('발코니 ¥99,800','90만')]) + '''</div>
<div class="note"><b>정리</b> — 같은 배·같은 날·같은 방이면 한국 공식 파트너(크루즈TMK)와 트립닷컴 값이 <b>1만 원 안팎으로 같습니다.</b> 그러면 남는 건 누가 챙겨주느냐 — 한국어 전화가 되고 일정 변경 1회 무료인 <b>크루즈TMK</b>. 크달 문의창에 구독자 혜택 되는지 한 줄 묻고 결제.</div>
</div>''')

# A안 상세
P.append(f'''<div class="band paper" id="a"><div class="wrap">
<div class="sechd"><div class="hp" style="background-image:url({{{{I:{use('pool',300)}}}}})"></div><div><div class="en">Plan A · Naha</div><h3>🌺 A안 상세</h3><div class="sub">12/14(월) 19:00 출항 · 12/18(금) 07:00 도착</div></div></div>
<ul class="tl">
<li><span class="t">Day 1</span><b>나하 출항 19:00</b>승선 마감 17:00 — 당일 오전 인천 비행기로 OK</li>
<li><span class="t">Day 2</span><b>이시가키 09:00~19:00</b>카비라만 · 야이마무라 · 이시가키 소고기</li>
<li><span class="t">Day 3</span><b>지룽(타이베이) 07:00~18:00</b>예류 · 지우펀 · 천등</li>
<li><span class="t">Day 4</span><b>미야코지마 08:00~18:00</b>요나하 마에하마 · 이라부 대교</li>
<li><span class="t">Day 5</span><b>나하 도착 07:00</b>하선 → 슈리성·고쿠사이도리 → 15:00 비행기</li>
</ul>
<h3 style="font-size:19px;margin:16px 0 8px">12월 출항일별 · 내측 2인1실 1인</h3>
''' + rows([('12/2 (수)','805,853'),('12/6 (일) · 두 번째 후보','610,780'),('12/10 (목)','738,587'),('12/14 (월) · 12월 최저','597,327','hl'),('12/18 (금)','725,133'),('12/22 (화) · 연말 항공 비쌈','610,780'),('12/30 (수) · 제외','2,608,595')]) + '''
<h3 style="font-size:19px;margin:18px 0 8px">12/14 · 3인 총액</h3>
<div class="tbl"><table><thead><tr><th>항목</th><th class="num">내측 3인</th><th class="num">발코니 3인</th></tr></thead><tbody>
<tr><td>크루즈 (세금 포함 · TMK)</td><td class="num">191만</td><td class="num">252만</td></tr>
<tr><td>선상팁 $18×4박×3</td><td class="num">29만</td><td class="num">29만</td></tr>
<tr><td>일본 출국세 3,000엔×3</td><td class="num">8만</td><td class="num">8만</td></tr>
<tr><td>항공 이스타 왕복 (1인 423,300)</td><td class="num">127만</td><td class="num">127만</td></tr>
<tr class="sum"><td>합계 · 당일 출발</td><td class="num">355만</td><td class="num">416만</td></tr>
<tr class="sum"><td>1인</td><td class="num">118만</td><td class="num">139만</td></tr>
<tr><td>전날 출발 + 나하 1박 (항공 -5만 · 호텔 14.6만 · 택시·저녁 6만)</td><td class="num">+15만</td><td class="num">+15만</td></tr>
<tr class="sum"><td>합계 · 전날 1박 안</td><td class="num">370만</td><td class="num">431만</td></tr>
<tr class="sum"><td>1인</td><td class="num">123만</td><td class="num">144만</td></tr></tbody></table></div>
<div class="note">355/416만은 당일 출발 기준, 전날 나하 1박 안이면 370/431만(호텔 라젠트면 -4만). 발코니 「시야 일부 가림」이면 각각 -14만.</div>
</div></div>''')

# 항공
P.append(f'''<div class="wrap" id="flight" style="padding-top:8px">
<div class="sechd"><div class="hp" style="background-image:url({{{{I:{use('skylounge',300)}}}}})"></div><div><div class="en">Flights</div><h3>✈ 한국 → 나하 비행기 전부</h3><div class="sub">트립닷컴 9/12 실조회 · 1인 편도 · 위탁 수하물 포함 · 직항만</div></div></div>
<details open><summary>12/14(월) 인천 → 나하 · 승선 마감 17:00</summary><div class="dbody">''' + rows([('대한항공 08:30→11:00 <small>여유 6시간 · 풀서비스</small>','314,000'),('진에어 09:20→11:40','245,800'),('진에어 10:10→12:35 <small>추천 · 여유 4시간</small>','210,700','hl'),('이스타 11:25→14:00 <small>최저 안전선</small>','205,100','hl'),('트리니티 11:50→14:25','205,300'),('제주항공 13:20→15:50 <small>여유 70분 · 연착 시 배 놓침</small>','186,300'),('아시아나 14:50→17:25 <small>마감 후 도착 · 불가</small>','315,300')]) + '''<p style="font-size:13px;margin-top:8px">김포·대구·청주 직항 없음. 하루 전 12/13 출발은 168,800~ + 나하 호텔 1박.</p></div></details>
<details><summary>12/18(금) 나하 → 인천 · 배 07:00 도착</summary><div class="dbody">''' + rows([('대한항공/아시아나 12:00→14:20','358,000~'),('진에어 12:40 · 13:35','253,700'),('이스타 15:00→17:50 <small>최저 · 추천</small>','218,200','hl'),('트리니티 15:25','255,670'),('제주항공 16:50','227,900'),('이스타 18:35 <small>9석 미만</small>','230,300')]) + '''</div></details>
<details><summary>조합 · 부산 출발</summary><div class="dbody">''' + rows([('진에어 10:10 + 이스타 15:00 <small>추천</small>','1인 428,900 · 3인 1,286,700','hl'),('이스타 11:25 + 이스타 15:00','1인 423,300 · 3인 1,269,900','hl'),('대한항공 왕복 풀서비스','1인 688,900 · 3인 2,066,700'),('부산 진에어 07:55 왕복','1인 404,200 · 3인 1,212,600','hl'),('부산 이스타 08:30 왕복','1인 404,500')]) + '''<div class="note" style="margin-bottom:0"><b>항공 결론</b> — 인천이면 진에어 10:10 가고 이스타 15:00 오는 조합. 크루즈 확정한 날 같이 잡기 (출발 40일 전이 제일 쌈 → 11월 초 전).</div></div></details>
<details><summary>🏨 전날 도착 안 · 12/13(일) 나하 1박 <span class="pin p-pick">+9~14만</span></summary><div class="dbody"><p style="margin-bottom:8px">당일 출발이면 집에서 새벽 6시 반. 어머니껜 <b>전날 일요일에 건너가 고쿠사이도리 저녁 → 다음날 슈리성 → 15시 느긋하게 승선</b>이 낫고, 값 차이는 3인 9~14만.</p><b style="display:block;margin:8px 0 6px">12/13(일) 인천→나하 · 1인</b>''' + rows([('진에어 09:20→11:40','187,300'),('진에어 10:10→12:35','187,300','hl'),('제주항공 13:20→15:50','190,200'),('트리니티 11:50→14:25','246,600'),('대한항공 08:30→11:00','314,000'),('아시아나 14:50→17:25','382,300')]) + '''<p style="font-size:13px;margin:6px 0 10px">일요일 진에어 187,300 — 당일 같은 편(210,700)보다 1인 23,400 쌈. 오는 편은 그대로 12/18 이스타 15:00.</p><b style="display:block;margin:8px 0 6px">나하 호텔 · 3인 1실 · 12/13 1박</b>''' + rows([('<b>호텔 JAL 시티 나하</b> <small>3인룸 · 고쿠사이도리 140m · 9.0 · 무료취소</small>','145,964','hl'),('<b>오키나와 히노데 리조트</b> <small>3인룸 · 980m · 9.5 · 무료취소 · 온천</small>','179,236','hl'),('<b>호텔 몬테레이 라 수르 나하</b> <small>코너 트윈(3인) · 480m · 9.4 · 2026년 오픈</small>','164,361'),('<b>라젠트 호텔 오키나와 나하</b> <small>디럭스 트윈(3인) · 750m · 9.0 · 2025년 오픈</small>','102,953'),('<b>오키나와 나하나 호텔 & 스파</b> <small>슈페리어 트윈(3인) · 1km · 8.7 · 무료취소</small>','103,002'),('<b>로얄파크 호텔 아이코닉 나하</b> <small>슈페리어 트윈(3인) · 750m · 9.4 · 2026년 오픈 · 수영장</small>','192,628'),('<b>호텔 그레이스리 나하</b> <small>3인룸 · 250m · 9.2 · 무료취소</small>','212,390')]) + '''<p style="font-size:13px;margin:8px 0">전부 고쿠사이도리 도보권. 공항→호텔 택시 15분(1,500엔), 호텔→크루즈터미널 택시 10~15분.</p><div class="note" style="margin-bottom:0"><b>일정</b> — 12/13 인천 10:10 → 나하 12:35 → 호텔 짐 → 마키시 시장 점심 → 고쿠사이도리·야치문 거리 → 저녁. 12/14 조식 → 슈리성 1시간 → 12:30 짐 찾아 택시 → 13:00 크루즈터미널(마감 17:00). 3인 차이: 항공 -7만 + 호텔 JAL시티 14.6만 + 택시·저녁 6만 = <b>+13.6만</b> (라젠트면 +9만).</div></div></details>
</div>''')

# 객실
DRAW = {}
cab = ''
for c in CABINS:
    DRAW[c['key']] = dict(img=use(c['img']), gal=[use(g) for g in c['gal']], en='Cabin', title=c['nm'], sub=c['sz'], tags=[('pick','추천') if c['best'] else ('free','3인 1실 가능')], body=c['body'])
    cab += f'''<div class="pc wide{' best' if c['best'] else ''}" data-open="{c['key']}" tabindex="0"><img data-img="{use(c['img'])}" alt=""><div class="in"><div class="nm">{c['nm']}</div><div class="ds">{c['sz']}</div><div class="won">{c['won']}<small>{c['unit']}</small></div><div class="ds">{c['ds']}</div><div class="ft"><span class="more">사진·정보 →</span></div></div></div>'''
P.append(f'''<div class="wrap" id="cabins" style="padding-top:8px">
<div class="sechd"><div class="hp" style="background-image:url({{{{I:{use('balcony',300)}}}}})"></div><div><div class="en">Cabins</div><h3>🛏 객실 — 누르면 사진과 정보</h3><div class="sub">3인 요금 실조회 · MSC 공식 사진</div></div></div>
<div class="pgrid">{cab}</div>
<div class="note"><b>객실 판단</b> — 추천은 <b>디럭스 발코니 BR1, 8~10층</b>. 엄마 + 작은언니 침대, 나는 소파베드. 화장실 1개 · 4박이면 감당 가능.</div>
</div>''')

# 시설
CATS = [('all','전부'),('dine','정찬·뷔페'),('spec','유료 레스토랑'),('bar','바·라운지'),('show','쇼·파티'),('play','놀거리'),('relax','수영장·스파')]
fac = ''
for i, f in enumerate(FAC):
    tags = [('free','요금 포함') if f['tag']=='free' else ('pay','유료')]
    if f.get('pick'): tags.append(('pick','엄마 추천'))
    DRAW[f'fac{i}'] = dict(img=use(f['img']), gal=[use(g) for g in f.get('gal', [])], en='On board', title=f['title'], sub=f['sub'], tags=tags, body=f['body'])
    tag = '<span class="pin p-free">포함</span>' if f['tag']=='free' else '<span class="pin p-pay">유료</span>'
    pick = '<span class="pin p-pick">엄마 추천</span>' if f.get('pick') else ''
    fac += f'''<div class="pc" data-cat="{f['cat']}" data-open="fac{i}" tabindex="0"><img data-img="{use(f['img'],420)}" alt=""><div class="in"><div class="nm">{f['nm']}</div><div class="ds">{f['ds']}</div><div class="ft">{tag}{pick}</div></div></div>'''
cat_btns = ''.join(f'<button type="button" data-cat="{k}"{" class=\"on\"" if k=="all" else ""}>{v}<b>{len(FAC) if k=="all" else sum(1 for f in FAC if f["cat"]==k)}</b></button>' for k, v in CATS)
P.append(f'''<div class="band paper" id="ship"><div class="wrap">
<div class="sechd"><div class="hp" style="background-image:url({{{{I:{use('galleria',300)}}}}})"></div><div><div class="en">On board</div><h3>🍽 배 안 시설 전부</h3><div class="sub">레스토랑 10 · 바 20 · 극장 · 수영장 · 스파 · 볼링 · F1 — MSC 공식 사진</div></div></div>
<div class="cats">{cat_btns}</div>
<div class="pgrid" id="fgrid">{fac}</div>
<div class="note"><b>요금에 든 것</b> — 정찬 4곳 · 뷔페 · 룸서비스 · 런던극장 쇼 · 돔 쇼·파티 · 수영장·자쿠지·아쿠아파크 · 헬스장 · 물·커피·차</div>
<div class="warn"><b>따로 내는 것</b> — 술·탄산·생수병 · 유료 레스토랑 5곳 · 카루셀 쇼 · 스파 · 볼링·F1·빙고 · 인터넷 · 기항지 투어 · 선상팁 $18/박 · 출국세 3,000엔. 선내 통화 미국 달러, 선실 카드로 달아두고 마지막 날 결제.</div>
</div></div>''')

# 옵션 (표 → 카드)
OPTS = [
 ('이지 음료 패키지','Easy Package','$38~48 / 1박','생맥주·병맥주, 하우스 와인·스파클링 잔, 클래식 칵테일, 탄산·주스·커피·차, AQUA 물. 하루 알코올 15잔. 유료 레스토랑 불가.','셋 중 술 드시는 분이 하루 3잔 이상이면 이득, 아니면 낱잔.'),
 ('프리미엄 엑스트라','Premium Extra','$70~85 / 1박','스페셜티 커피, 에너지드링크, 생과일 칵테일·스무디, 프리미엄 와인·스피릿·칵테일.','우리 여행엔 과함.'),
 ('무알코올 패키지','Alcohol-Free','$28~34 / 1박','스페셜티 커피·차, 탄산·에너지, 주스·스무디, 무알코올 맥주·와인·칵테일.','일반 커피·차·물은 원래 무료라 탄산·스무디를 자주 드셔야 본전.'),
 ('인터넷','Browse / Stream','4박 $40~50 / $60~80','1기기. 브라우즈(카톡·웹) / 스트림(영상).','<b>안 사도 됨</b> — 매일 기항하니 로밍·e심으로 충분.'),
 ('스페셜티 다이닝','Dining Package','1끼 $35~55 · 3끼 $100~130','웰컴 어보드(첫날) / 1끼 / 2~4끼 묶음. 부처스컷·카이토·홀라·씨파빌리온.','칠순 저녁 <b>부처스컷 1끼</b>만 사전 구매.'),
 ('스파 · 마사지','Aurea Spa','패스 $30~40 · 마사지 50분 $130~170','사우나·스팀·소금방·열탕 침대 / 발리니즈 마사지.','엄마 마사지 1회 = 칠순 선물 항목. 첫날 포트데이 할인 전단 보고 예약.'),
 ('기항지 투어 (MSC)','Excursions','3시간 $60~80 · 5시간 $90~130','버스·가이드·입장료. 배가 기다려줌.','이시가키·미야코는 택시 대절이 싸고 편함. 지룽만 MSC KEE05.'),
 ('선상팁','Service charge','$18 × 4박 = $72','객실·식당 승무원 서비스료, 자동 부과.','필수. 3인 $216 ≈ 29만.'),
]
opt = ''.join(f'<details><summary>{n} <span class="pin p-pay">{p}</span></summary><div class="dbody"><div style="font-size:12.5px;color:#a8967f;margin-bottom:6px">{e}</div><p style="margin-bottom:8px">{inc}</p><div class="note" style="margin:0">{v}</div></div></details>' for n, e, p, inc, v in OPTS)
P.append(f'''<div class="wrap" id="options" style="padding-top:8px">
<div class="sechd"><div class="hp" style="background-image:url({{{{I:{use('cerisier',300)}}}}})"></div><div><div class="en">Add-ons</div><h3>💳 살 수 있는 옵션</h3><div class="sub">MSC 공식 내용 + 가격은 아시아 사전구매가 기준 추정. 예약 후 MSC for Me 앱에서 확정</div></div></div>
{opt}
<div class="note"><b>우리 집 결론</b> — 사전 구매는 <b>부처스컷 1끼 + 엄마 마사지</b> 둘. 음료 패키지·인터넷은 안 사고, 기항지는 택시 대절 + 지룽만 MSC 투어. 추가 예산 3인 60~80만. <br><small>MSC 규정: 같은 객실 성인은 모두 같은 음료 패키지를 사야 함(한 명만 불가).</small></div>
</div>''')

# 기항지
port_html = ''
for p in PORTS:
    xc = ''
    for code, nm, dur, cat, ds, best in p['exc']:
        key = 'x_'+code; has = code in RAW
        DRAW[key] = dict(img=use(code) if has else use(p['hero']), gal=[], en=f'MSC Excursion {code}', title=nm, sub=f'{dur} · {cat} · {p["nm"]}',
                         tags=[('pay','유료 · MSC 투어'),('pick','엄마 추천')] if best else [('pay','유료 · MSC 투어')],
                         body=f'<p>{ds}</p><p><b>MSC 공식 투어 코드 {code}.</b> 가격은 로그인 후 표시(3시간 $60~80, 5시간 $90~130, 7시간 $130~180 안팎). 영어 가이드 기본. 배가 투어 귀환을 기다려 줌. 예약은 크루즈TMK 예약 완료 후 MSC for Me 앱 또는 승선 후 투어 데스크.</p><div class="tip">비슷한 코스를 택시 대절로 하면 3인 기준 절반 값. 단 출항 90분 전엔 항구에.</div>')
        img = f'<img data-img="{use(code)}" alt="">' if has else ''
        xc += f'''<div class="pc{' best' if best else ''}" data-open="{key}" tabindex="0">{img}<div class="in"><div class="nm">{nm}</div><div class="ds">{dur} · {cat}{' · <b style="color:#a75a25">엄마 추천</b>' if best else ''}</div></div></div>'''
    route = ''.join(f'<li><span class="t">{t_}</span>{txt}</li>' for t_, txt in p['route'])
    port_html += f'''<div class="port" id="port-{p['key']}">
<div class="phead"><img data-img="{use(p['hero'],720)}" alt=""><div class="pt"><div class="en">{p['en']}</div><h3>{p['nm']}</h3><div class="tm">⏱ {p['tm']}</div></div></div>
<div class="pbody"><p>{p['intro']}</p>
<details open><summary>🚕 우리끼리 루트 (엄마 걸음 기준)</summary><div class="dbody"><ol class="route2">{route}</ol><div class="note" style="margin-bottom:0">{p['tip']}</div></div></details>
<details><summary>🎫 MSC 공식 투어 {len(p['exc'])}개</summary><div class="dbody"><div class="pgrid">{xc}</div></div></details>
</div></div>'''
P.append(f'''<div class="band paper" id="ports"><div class="wrap">
<div class="sechd"><div class="hp" style="background-image:url({{{{I:{use('ISG01',300)}}}}})"></div><div><div class="en">Ports of call</div><h3>🗺 기항지 4곳</h3><div class="sub">시간표 · 우리끼리 루트 · MSC 공식 투어 39개 (msccruises.com에서 그대로)</div></div></div>
{port_html}
<div class="note"><b>공통 규칙</b> — 배는 출항 시각에 정확히 떠남. MSC 투어가 아니면 <b>출항 90분 전</b>엔 항구에. 크루즈 카드 + 여권 사본 지참(대만은 여권 지참 안내가 있을 수 있어 전날 데일리 프로그램 확인). 현금은 택시·시장용 소액만.</div>
</div></div>''')

# 뺀 배 + 확인 + 다음
P.append(TORN('#faf0ee') + '''<div class="band rose" id="others"><div class="wrap">
<div class="shead"><div class="script">Not this time</div><h2>뒤져보고 뒤로 미룬 배 9척</h2></div>
<details><summary>스펙트럼 · 홍콩 출발 <span class="pin p-ton">16.9만톤</span></summary><div class="dbody">11/16 다낭 4박 $678 · 12/13 오키나와 5박 $879 · 12/6 오키나와+타이베이 $1,196. 홍콩 항공 35~40만 → 1인 130~200만. A·B보다 비쌈.</div></details>
<details><summary>벨리시마 · 도쿄 → 지룽 편도 <span class="pin p-ton">17만톤</span></summary><div class="dbody">11/21 4박 577,147원. 값은 B와 같은데 항공을 따로 사야 함.</div></details>
<details><summary>내비게이터 · 싱가포르 <span class="pin p-ton">13.9만톤</span></summary><div class="dbody">10/29~ 4박 $771 + 항공 50~60만 → 1인 160만↑.</div></details>
<details><summary>디즈니 어드벤처 · 싱가포르 <span class="pin p-ton">20.8만톤</span></summary><div class="dbody">아이 중심 · 고가.</div></details>
<details><summary>다이아몬드 프린세스 · 도쿄 <span class="pin p-ton">11.5만톤</span></summary><div class="dbody">10~14박짜리뿐. 1인 200만↑.</div></details>
<details><summary>코스타 세레나 <span class="pin p-ton">11.4만톤</span></summary><div class="dbody">10/18 도쿄 출발 후 호주로 떠남.</div></details>
<details><summary>노르위전 제이드 · 도쿄→인천 11박 <span class="pin p-ton">9.3만톤</span></summary><div class="dbody">인천 도착이 매력이지만 11박 · 중형.</div></details>
<details><summary>아도라 매직시티 · 상하이 <span class="pin p-ton">13.5만톤</span></summary><div class="dbody">중국 내수 전용, 한국 판매 창구 없음.</div></details>
<details><summary>이스턴비너스 · 부산/포항 <span class="pin p-ton">2.6만톤</span></summary><div class="dbody">720명짜리. 3박 104~119만으로 오히려 비쌈.</div></details>
</div></div>''' + TORN('#fbf6ee') + '''<div class="wrap" id="next" style="padding-top:20px">
<div class="shead"><div class="script">Before we book</div><h2>확인할 것 · 다음 액션</h2></div>
<div class="card"><div class="nm">✅ 바로 확인</div><ul class="check">
<li><i></i><span><b>여권 3명</b> (김현순·정이서·정해민) — 2027-06-18 이후 만료</span></li>
<li><i></i><span>해민 언니 휴가 12/14(월)~12/18(금), 전날 안이면 12/13(일)부터</span></li>
<li><i></i><span>해외 결제 카드 — 전액 결제</span></li>
<li><i></i><span>엄마 12월 일정(병원 등)</span></li></ul></div>
<div class="card"><div class="nm">🚢 다음 액션</div><ol class="steps">
<li>A 확정 → 크루즈TMK(크달 링크) 나하 12/14 성인 3 · 디럭스 발코니 BR1($1,877) 또는 인테리어 IR1($1,427) 결제</li>
<li>같은 날 진에어 10:10 / 이스타 15:00 항공 결제 (3인 1,286,700원)</li>
<li>12/14 발코니 매진이면 12/6 또는 12/22 (610,780)로</li>
<li>예약 완료 후 부처스컷 1끼 + 엄마 마사지 사전 구매, 지룽 MSC 투어 예약</li></ol>
<p style="font-size:13px;color:var(--ink2);margin-top:10px">나하 출발 — <a href="https://kr.trip.com/cruises/line-73172-naha-hawaii-4night-msc-bellissima-msc/?departure=2026-12-14&locale=ko-KR">트립닷컴 line-73172</a> · 크달 — <a href="https://cdal.app/products">cdal.app</a> · 크루즈TMK 1544-3441 · 트립닷컴 1666-0060</p></div>
</div>''')

P.append(f'''<footer><div class="sign">Bon voyage, Mom</div><b>조사 2026-09-12</b> · 환율 1달러 1,340원 · 100엔 900원 · 요금은 실시간으로 바뀝니다<br>사진은 MSC 크루즈 공식 사이트의 것 — 가족 계획용<img data-img="{use('mini')}" alt=""></footer>
<nav class="tabs"><a href="#pick"><i>💛</i>결론</a><a href="#cabins"><i>🛏</i>객실</a><a href="#ship"><i>🍽</i>배 안</a><a href="#ports"><i>🗺</i>기항지</a><a href="#flight"><i>✈</i>항공</a><a href="#next"><i>✅</i>체크</a></nav>
<div class="dim" id="dim"></div>
<aside class="sheet" id="sheet" aria-hidden="true" role="dialog"><div class="grip"><i></i><button type="button" class="sclose" id="s-close" aria-label="닫기">×</button></div><img class="simg" id="s-img" alt=""><div class="sbody"><div class="sen" id="s-en"></div><h3 id="s-title"></h3><div class="ssub" id="s-sub"></div><div class="stags" id="s-tags"></div><div class="gal" id="s-gal"></div><div id="s-body"></div></div></aside>
''')

JS = '''
<script>
const IMG=__IMG__, DRAW=__DRAW__;
document.querySelectorAll('[data-img]').forEach(el=>{const k=el.getAttribute('data-img'); if(IMG[k]) el.src=IMG[k];});
document.querySelectorAll('[data-bg]').forEach(el=>{const k=el.getAttribute('data-bg'); if(IMG[k]) el.style.backgroundImage='url('+IMG[k]+')';});
const sheet=document.getElementById('sheet'), dim=document.getElementById('dim'); let last=null;
function openS(key){const d=DRAW[key]; if(!d) return; last=document.activeElement;
 document.getElementById('s-img').src=IMG[d.img]||''; document.getElementById('s-en').textContent=d.en; document.getElementById('s-title').textContent=d.title; document.getElementById('s-sub').textContent=d.sub;
 document.getElementById('s-tags').innerHTML=d.tags.map(t=>'<span class="'+t[0]+'">'+t[1]+'</span>').join('');
 const g=document.getElementById('s-gal'); g.innerHTML=d.gal.filter(k=>IMG[k]).map(k=>'<img src="'+IMG[k]+'" alt="">').join(''); g.style.display=g.innerHTML?'grid':'none';
 document.getElementById('s-body').innerHTML=d.body; sheet.scrollTop=0; sheet.classList.add('on'); dim.classList.add('on'); sheet.setAttribute('aria-hidden','false'); document.body.classList.add('lock');}
function closeS(){sheet.classList.remove('on'); dim.classList.remove('on'); sheet.setAttribute('aria-hidden','true'); document.body.classList.remove('lock'); if(last) last.focus();}
document.querySelectorAll('[data-open]').forEach(el=>{el.addEventListener('click',()=>openS(el.getAttribute('data-open'))); el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();openS(el.getAttribute('data-open'));}});});
document.getElementById('s-close').addEventListener('click',closeS); dim.addEventListener('click',closeS); document.addEventListener('keydown',e=>{if(e.key==='Escape') closeS();});
let sy=0; sheet.addEventListener('touchstart',e=>{sy=e.touches[0].clientY;},{passive:true}); sheet.addEventListener('touchend',e=>{if(sheet.scrollTop<=0 && e.changedTouches[0].clientY-sy>90) closeS();},{passive:true});
document.querySelectorAll('.cats button').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('.cats button').forEach(x=>x.classList.remove('on')); b.classList.add('on'); const c=b.getAttribute('data-cat'); document.querySelectorAll('#fgrid .pc').forEach(f=>{f.hidden=!(c==='all'||f.getAttribute('data-cat')===c);});}));
</script>'''

page = '<title>엄마 칠순 크루즈 · 모바일</title>\n<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jua&family=Dongle:wght@700&family=Gamja+Flower&family=Nothing+You+Could+Do&family=Gaegu:wght@400;700&display=swap">\n<style>' + CSS + '</style>\n' + '\n'.join(P) + JS
# {{I:key}} 배경 이미지 → data-bg 로 치환 (중복 내장 방지)
page = re.sub(r'style="background-image:url\(\{\{I:(\w+)\}\}\)"', r'data-bg="\1"', page)
page = page.replace('__IMG__', json.dumps(IMG)).replace('__DRAW__', json.dumps(DRAW, ensure_ascii=False))
open(OUT, 'w', encoding='utf-8').write(page)
print('written', len(page)//1024, 'KB, images', len(IMG))
