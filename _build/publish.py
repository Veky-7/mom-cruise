# -*- coding: utf-8 -*-
"""완성 HTML 두 개를 docs/ 에 완전한 문서로 감싸 넣는다 (GitHub Pages 용)"""
import os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
head = ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="robots" content="noindex, nofollow">\n<meta name="theme-color" content="#fbf6ee">\n<meta name="apple-mobile-web-app-capable" content="yes">\n'
        '<meta name="apple-mobile-web-app-status-bar-style" content="default">\n<meta property="og:title" content="엄마 칠순 크루즈">\n<meta property="og:description" content="나하 출발 MSC 벨리시마 12/14 · 4박 5일 가이드북">\n')
def wrap(body):
    i = body.index('<div class="top">') if '<div class="top">' in body else body.index('<div class="wrap">')
    return head + body[:i] + '</head>\n<body>\n' + body[i:] + '\n</body>\n</html>\n'
for src, dst in [('엄마칠순_크루즈_2차안_모바일.html', 'index.html'), ('엄마칠순_크루즈_2차안.html', 'pc.html')]:
    open(os.path.join(R, 'docs', dst), 'w', encoding='utf-8').write(wrap(open(os.path.join(R, src), encoding='utf-8').read()))
    print('docs/' + dst)
