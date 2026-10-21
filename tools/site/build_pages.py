# Generates shared header + new pages for explosivetrades.github.io/free
import re, html, os
ROOT = '/home/claude/kav'
UTM = '?utm_source=other&amp;utm_medium=tutor-course-referral&amp;utm_campaign=course-overview-webapp'

NAV = [('', 'Free Tools', 'tools'), ('research/', '🔒 Members Login', 'research'), ('prop-firms/', 'Best Prop Firm', 'prop'),
       ('courses/', 'Learning Programs', 'courses'), ('global/', 'Global Channel', 'global')]

NAV_CSS = '''
/* ---- shared site header ---- */
.top{ position:sticky; top:0; z-index:9; background:var(--panel); border-bottom:1px solid var(--line); padding-top:env(safe-area-inset-top,0px); }
.top-in{ max-width:1180px; margin:0 auto; display:flex; align-items:center; gap:10px 18px; flex-wrap:wrap; padding:10px max(16px, env(safe-area-inset-right,0px)) 10px max(16px, env(safe-area-inset-left,0px)); }
.brand{ font-family:var(--display); font-size:24px; letter-spacing:.06em; color:var(--gold); line-height:1; text-decoration:none; white-space:nowrap; }
.nav{ display:flex; gap:2px; flex:1; min-width:0; overflow-x:auto; scrollbar-width:none; -webkit-overflow-scrolling:touch; }
.nav::-webkit-scrollbar{ display:none; }
.nav a{ white-space:nowrap; padding:7px 11px; border-radius:8px; color:var(--muted); font:500 13.5px var(--body); text-decoration:none; }
.nav a:hover{ color:var(--text); background:var(--panel2); }
.nav a[aria-current="page"]{ color:var(--gold); background:color-mix(in srgb, var(--gold) 12%, transparent); font-weight:600; }
.top-r{ display:flex; align-items:center; gap:8px; font-size:13px; color:var(--muted); }
@media (max-width:960px){ .nav{ order:3; flex-basis:100%; margin:0 -6px; flex-wrap:wrap; overflow:visible; } .nav a{ padding:6px 10px; font-size:13px; } .top-r .by{ display:none; } }
'''

def header(prefix, active, right_inner):
    links = ''.join(f'<a href="{(prefix + href) or "./"}"{" aria-current=\"page\"" if key==active else ""}>{label}</a>' for href,label,key in NAV)
    return (f'<header class="top">\n  <div class="top-in">\n    <a class="brand" href="{prefix or "./"}">Explosive Trades</a>\n'
            f'    <nav class="nav" aria-label="Main menu">{links}</nav>\n    <div class="top-r">{right_inner}</div>\n  </div>\n</header>')

def patch_existing(path, prefix, active):
    s = open(path).read()
    m = re.search(r'<header class="top">.*?</header>', s, flags=re.S)
    right = re.search(r'<div class="top-r">(.*?)</div>\s*</div>\s*</header>', m.group(0), flags=re.S)
    inner = right.group(1).strip() if right else ''
    inner = re.sub(r'\s*<a class="mem-link"[^>]*>.*?</a>', '', inner, flags=re.S)
    s = s[:m.start()] + header(prefix, active, inner) + s[m.end():]
    # replace old header css block with shared one (marker based)
    s = re.sub(r'/\* ---- shared site header ---- \*/.*?\n(?=\S)', '', s, flags=re.S)
    s = re.sub(r'\.top\{ position:sticky;[^\n]*\n', '', s)
    s = re.sub(r'\.top-in, \.wrap\{', '.wrap{', s)
    s = re.sub(r'\.top-in\{[^\n]*\n', '', s)
    s = re.sub(r'\.brand\{[^\n]*\n', '', s)
    s = re.sub(r'\.top-r\{[^\n]*\n', '', s)
    s = re.sub(r'@media \(max-width:420px\)\{ \.by\{ display:none; \} \}\n', '', s)
    s = s.replace('</style>', NAV_CSS + '</style>', 1)
    open(path, 'w').write(s)

if __name__ == '__main__':
    patch_existing(f'{ROOT}/index.html', '', 'tools')
    patch_existing(f'{ROOT}/research/index.html', '../', 'research')
    print('patched')
