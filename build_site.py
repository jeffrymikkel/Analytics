# Builds index.html from data/weekNN/grid_data.json + data/teams_fbs.json.  Usage: python3 build_site.py 6 "Sat, Oct 10"
import json, sys, html
from math import erf, sqrt
wk, date = int(sys.argv[1]), sys.argv[2]
G = json.load(open(f'data/week{wk:02d}/grid_data.json'))
T = {t['school']: t for t in json.load(open('data/teams_fbs.json'))}
def lum(h):
    h = h.lstrip('#'); r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4)); return (0.299*r + 0.587*g + 0.114*b) / 255
def col(n):
    t = T[n]; c = t.get('color') or '#444444'
    if lum(c) > 0.78: c = t.get('alternateColor') or '#444444'
    if lum(c) > 0.78: c = '#555555'
    return c
def logo(n):
    L = t = T[n].get('logos') or []
    return next((u for u in L if '/logos/128/' in u), L[0] if L else '')
def sp(x): return ('+' if x > 0 else '') + (f'{x:g}' if x else 'PK')
def cover(gap):
    if abs(gap) < 2: return 'No edge'
    return f'{min(90, round(50 * (1 + erf(abs(gap) / 13.5 / sqrt(2)))))}% to cover'
def meter(lp, rp, lc, rc):
    adv = lp - rp; mag = abs(adv); lit = mag >= 25; w = min(mag, 80) / 80 * 50; lw = adv >= 0
    fill = (lc if lw else rc) if lit else '#CBC8BD'
    left = (50 - w) if lw else 50
    rad = '9px 0 0 9px' if lw else '0 9px 9px 0'
    return f'<div class="m"><i style="left:{left}%;width:{w}%;background:{fill};border-radius:{rad}"></i><b></b></div>', lit, lw
def ordn(n): return f'{n}{"th" if 10 <= n % 100 <= 20 else {1:"st",2:"nd",3:"rd"}.get(n % 10, "th")}'
cards = []
for g in sorted(G, key=lambda x: -abs(x['gap'])):
    h, a = g['home'], g['away']; hc, ac = col(h), col(a); R = g['rows']
    spec = [('Rush offense', R[3]['op'], 'Rush defense', R[3]['dp']), ('Pass offense', R[4]['op'], 'Pass defense', R[4]['dp']),
            ('Rush defense', R[0]['dp'], 'Rush offense', R[0]['op']), ('Pass defense', R[1]['dp'], 'Pass offense', R[1]['op'])]
    rows = ''
    for lu, lp, ru, rp in spec:
        m, lit, lw = meter(lp, rp, hc, ac)
        rows += (f'<div class="r"><div><small>{html.escape(h)}</small><strong>{lu}</strong><em>{ordn(lp)} pct</em></div>{m}'
                 f'<div class="rt"><small>{html.escape(a)}</small><strong>{ru}</strong><em>{ordn(rp)} pct</em></div></div>')
    hs = g['slate_home_spread']
    if g['gap'] < 0: pk, pc = f'{a} {sp(-hs)}', ac
    else: pk, pc = f'{h} {sp(hs)}', hc
    cards.append(f'''<article><header><div class="t"><img src="{logo(h)}" alt=""><b>{html.escape(h)}</b><span>Home</span></div><div class="d">{date}</div><div class="t"><img src="{logo(a)}" alt=""><b>{html.escape(a)}</b><span>Away</span></div></header>{rows}<footer><i style="background:{pc}"></i><span>Pick</span><strong>{html.escape(pk)}</strong><u>{cover(g["gap"])}</u></footer></article>''')
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CalderVegas Week {wk}</title>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Barlow:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--bg:#F4F3EF;--card:#fff;--ink:#16140F;--mut:#6B6860;--line:#EEECE6;--track:#ECEAE3}}
@media(prefers-color-scheme:dark){{:root{{--bg:#14130F;--card:#1E1D18;--ink:#F2F0E8;--mut:#A29F94;--line:#2D2B25;--track:#2D2B25}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:Barlow,sans-serif;padding:32px 16px 48px}}
h1{{font:700 40px 'Barlow Condensed',sans-serif;margin:0 auto 4px;max-width:1220px}}.sub{{color:var(--mut);margin:0 auto 28px;max-width:1220px;font-size:14px}}
main{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,520px),1fr));gap:24px;max-width:1220px;margin:0 auto}}
article{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:24px}}
header{{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:8px;padding-bottom:16px}}
.t{{display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center}}.t img{{width:72px;height:72px;object-fit:contain}}
.t b{{font:700 24px/1 'Barlow Condensed',sans-serif}}.t span{{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--mut)}}.d{{font-size:13px;color:var(--mut);font-weight:500}}
.r{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.3fr) minmax(0,1fr);gap:12px;align-items:center;padding:12px 0;border-top:1px solid var(--line)}}
.r small{{display:block;color:var(--mut);font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:600}}.r strong{{display:block;font:700 20px/1.1 'Barlow Condensed',sans-serif}}.r em{{font-style:normal;font-size:12px;color:var(--mut)}}.rt{{text-align:right}}
.m{{position:relative;height:18px;border-radius:9px;background:var(--track)}}.m i{{position:absolute;top:0;bottom:0}}.m b{{position:absolute;left:50%;top:-4px;bottom:-4px;width:2px;margin-left:-1px;background:#B9B6AB}}
footer{{display:flex;align-items:center;gap:10px;border-top:1px solid var(--line);padding-top:16px}}footer i{{width:12px;height:12px;border-radius:6px}}
footer span{{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);font-weight:600}}footer strong{{font:700 24px/1 'Barlow Condensed',sans-serif}}footer u{{margin-left:auto;text-decoration:none;font-size:13px;font-weight:600;background:var(--bg);padding:5px 12px;border-radius:6px}}
@media(max-width:560px){{.r{{grid-template-columns:1fr 1fr}}.r .m{{grid-column:1/-1;order:3}}.t img{{width:56px;height:56px}}}}
</style></head><body><h1>CalderVegas &middot; Week {wk}</h1>
<p class="sub">Picks against the league slate lines, strongest model edge first. Meters light up in a team's color only when a unit matchup is lopsided (25+ percentile points); even matchups stay gray. Percentages are rough model estimates, not guarantees.</p>
<main>{"".join(cards)}</main></body></html>'''
open('index.html', 'w').write(page)
print('wrote index.html', len(cards), 'cards')
