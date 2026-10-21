import sys
sys.path.insert(0, '/home/claude/kav/tools/site')
from build_pages import header, NAV_CSS, UTM
ROOT = '/home/claude/kav'

BASE_CSS = '''
:root{
  --bg:#1a1510; --panel:#231d15; --panel2:#2a231a; --line:#3a3023; --text:#f3ead8; --muted:#b3a68c;
  --gold:#d9a93a; --orange:#e8843a; --green:#6cc58a; --red:#e5484d; --on-gold:#1a1510;
  --display:'Bebas Neue', Impact, 'Arial Narrow', sans-serif;
  --body:'Poppins', system-ui, -apple-system, 'Segoe UI', sans-serif;
  color-scheme:dark;
}
:root[data-theme="light"]{
  --bg:#f6efe1; --panel:#fffaf0; --panel2:#f3e9d6; --line:#e0d1b4; --text:#2a2117; --muted:#6f604a;
  --gold:#a8790f; --orange:#c1621c; --green:#2d8a50; --red:#c43338; --on-gold:#fffaf0; color-scheme:light;
}
*,*::before,*::after{ box-sizing:border-box; }
html{ -webkit-text-size-adjust:100%; scroll-padding-top:120px; }
body{ margin:0; background:var(--bg); color:var(--text); font-family:var(--body); font-size:15px; line-height:1.6; }
a{ color:var(--gold); }
:focus-visible{ outline:2px solid var(--gold); outline-offset:3px; }
.icon-btn{ background:var(--panel2); color:var(--text); border:1px solid var(--line); border-radius:8px; padding:5px 10px; cursor:pointer; font:500 12px var(--body); }
.icon-btn:hover{ border-color:var(--gold); }
.wrap{ max-width:1080px; margin:0 auto; padding:36px max(16px, env(safe-area-inset-right,0px)) calc(40px + env(safe-area-inset-bottom,0px)) max(16px, env(safe-area-inset-left,0px)); display:grid; gap:44px; }
.wrap > *{ min-width:0; }
.kicker{ display:inline-block; font-size:12px; font-weight:600; letter-spacing:.08em; text-transform:uppercase; color:var(--green); border:1px solid var(--green); border-radius:20px; padding:3px 12px; margin:0 0 14px; }
h1{ font-family:var(--display); font-weight:400; font-size:clamp(44px,7.5vw,78px); line-height:.92; letter-spacing:.015em; margin:0 0 14px; text-wrap:balance; }
h1 span{ color:var(--gold); }
h2{ font-family:var(--display); font-weight:400; font-size:34px; letter-spacing:.03em; margin:0 0 6px; color:var(--gold); }
.lead{ color:var(--muted); max-width:62ch; margin:0; font-size:16px; }
.sec-lead{ color:var(--muted); margin:0 0 18px; max-width:62ch; }
.btn{ display:inline-flex; align-items:center; justify-content:center; gap:8px; border:0; border-radius:11px; padding:12px 18px; font:600 15px var(--body); cursor:pointer; text-decoration:none; }
.btn.gold{ background:var(--gold); color:var(--on-gold); }
.btn.gold:hover{ filter:brightness(1.07); }
.btn.line{ background:transparent; color:var(--text); border:1px solid var(--gold); }
.btn.line:hover{ background:color-mix(in srgb, var(--gold) 12%, transparent); }
.btn.wa{ background:#1f8f4e; color:#fff; }
.btn.green{ background:#1f8f4e; color:#fff; }
.btn.green:hover{ filter:brightness(1.1); }
.btn.ask-btn{ background:transparent; color:#3fbf73; border:1.5px solid #1f8f4e; }
.btn.ask-btn:hover{ background:color-mix(in srgb, #1f8f4e 14%, transparent); }
.btn.yt{ background:#d4190f; color:#fff; }
.card{ background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:20px; min-width:0; }
.pill{ display:inline-block; font-size:11px; font-weight:600; letter-spacing:.06em; text-transform:uppercase; padding:2px 9px; border-radius:20px; }
.pill.gold{ color:var(--on-gold); background:var(--gold); }
.pill.green{ color:var(--green); border:1px solid var(--green); }
.tbl{ overflow-x:auto; border:1px solid var(--line); border-radius:12px; background:var(--panel); }
table{ width:100%; border-collapse:collapse; min-width:640px; font-size:14px; }
th{ text-align:left; font-size:12px; font-weight:600; color:var(--gold); padding:11px 14px; border-bottom:1px solid var(--line); letter-spacing:.02em; }
td{ padding:11px 14px; border-bottom:1px solid var(--line); vertical-align:top; }
tr:last-child td{ border-bottom:0; }
td.num{ font-variant-numeric:tabular-nums; white-space:nowrap; }
details.faq{ background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:0 18px; }
details.faq + details.faq{ margin-top:10px; }
details.faq summary{ cursor:pointer; list-style:none; padding:15px 0; font-weight:600; display:flex; justify-content:space-between; gap:14px; }
details.faq summary::-webkit-details-marker{ display:none; }
details.faq summary::after{ content:"+"; color:var(--gold); font-size:20px; line-height:1; }
details.faq[open] summary::after{ content:"–"; }
details.faq p{ margin:0 0 16px; color:var(--muted); font-size:14px; }
.contact{ display:grid; grid-template-columns:minmax(0,1fr) auto; gap:18px; align-items:center; padding:20px; border-radius:14px; border:1px solid var(--line); background:var(--panel); }
@media (max-width:680px){ .contact{ grid-template-columns:1fr; } }
.contact p{ margin:0; color:var(--muted); font-size:14px; }
footer{ border-top:1px solid var(--line); padding-top:16px; display:grid; gap:8px; font-size:12px; color:var(--muted); }
@media (prefers-reduced-motion: reduce){ *{ transition:none !important; } }
'''

THEME_JS = '''<script>
(function(){
  var b = document.getElementById('themeBtn');
  function set(t){ document.documentElement.setAttribute('data-theme', t); b.textContent = t === 'light' ? 'Dark' : 'Light'; }
  try { var s = localStorage.getItem('et-dl-theme'); if (s) set(s); } catch(e){}
  b.addEventListener('click', function(){ var t = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light'; set(t); try { localStorage.setItem('et-dl-theme', t); } catch(e){} });
})();
</script>'''

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analytics import snippet as ga_snippet, lead_js as ga_lead, footer_note as ga_note

FOOTER = f'''  <footer>
    <span>© Explosive Trades · Kavi Sharma · <a href="https://www.explosivetrades.com" target="_blank" rel="noopener">www.explosivetrades.com</a></span>
    <span>Disclaimer: Explosive Trades ka content sirf education ke liye hai. Hum SEBI registered nahi hain, koi buy/sell call ya profit ki guarantee nahi dete. Trading mein capital ka risk hota hai, apni samajh se trade karein.</span>
{ga_note()}  </footer>'''

WA_BOX = lambda title, text, msg: f'''  <section class="contact" aria-label="WhatsApp">
    <div>
      <h2 style="margin-bottom:4px">{title}</h2>
      <p>{text} WhatsApp: <b style="color:var(--text)">+91 78179 40814</b></p>
    </div>
    <a class="btn wa" href="https://wa.me/917817940814?text={msg}" target="_blank" rel="noopener">WhatsApp karein</a>
  </section>'''

SITE = 'https://explosivetrades.github.io/free/'
def og_extra(img, title, desc, url):
    if not img: return ''
    return (f'<meta property="og:type" content="website">\n<meta property="og:site_name" content="Explosive Trades">\n'
            f'<meta property="og:url" content="{SITE}{url}">\n<meta property="og:image" content="{SITE}{img}">\n'
            f'<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            f'<meta property="og:image:alt" content="{title}">\n<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="twitter:title" content="{title}">\n<meta name="twitter:description" content="{desc}">\n'
            f'<meta name="twitter:image" content="{SITE}{img}">\n<link rel="canonical" href="{SITE}{url}">\n')

def page(path, title, desc, active, extra_css, body, bar='', og_image='', og_title='', og_url=''):
    if bar: extra_css += STICKY_CSS
    out = f'''<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="utf-8">
{ga_snippet()}<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{og_title or title}">
<meta property="og:description" content="{desc}">
{og_extra(og_image, og_title or title, desc, og_url)}<meta name="theme-color" content="#1a1510">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
<style>{BASE_CSS}{NAV_CSS}{extra_css}</style>
</head>
<body{' class="has-sticky"' if bar else ''}>
{header("../", active, '<span class="by">Prepared by Kavi Sharma</span>\n      <button class="icon-btn" id="themeBtn" type="button" aria-label="Theme badlein">Light</button>')}

<main class="wrap">
{body}
{FOOTER}
</main>
{bar}{THEME_JS}
</body>
</html>
'''
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(out)


SHEET_URL = 'https://script.google.com/macros/s/AKfycbxAMCT0OHo6qOcxxX289y_ruMwcv4OyidIx-lSvUdQR-U8Fi0a51C8v6xEcGKZwvtwA/exec'
INTERESTS = ['Trading Ka ABCD (₹49)', 'Indian Gold Market Program', 'Forex / XAUUSD Program', 'Funded Account Mastery', 'XAUUSD Swing Traders Elite', 'Complete Bundle (₹9,999)', 'Prop firm help', 'Kuch aur']
ENQ_CSS = """
.enq{ display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1.3fr); gap:24px; align-items:start; border:1.5px solid #1f8f4e; }
@media (max-width:820px){ .enq{ grid-template-columns:1fr; } }
.enq h2{ margin:0 0 6px; }
.enq .intro p{ margin:0 0 10px; color:var(--muted); font-size:14px; }
.enq .intro ul{ margin:0; padding-left:18px; color:var(--muted); font-size:13.5px; display:grid; gap:4px; }
.enq form{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }
@media (max-width:560px){ .enq form{ grid-template-columns:1fr; } }
.enq .full{ grid-column:1 / -1; }
.enq label{ display:block; font-size:13px; color:var(--muted); margin-bottom:4px; }
.enq input, .enq select, .enq textarea{ width:100%; padding:11px 12px; background:var(--bg); color:var(--text); border:1px solid var(--line); border-radius:10px; font:15px var(--body); }
.enq textarea{ min-height:76px; resize:vertical; }
.enq input:focus, .enq select:focus, .enq textarea:focus{ outline:none; border-color:var(--gold); }
.enq [aria-invalid="true"]{ border-color:var(--orange); }
.enq .send{ width:100%; padding:13px 16px; font-size:16px; }
.enq .status{ margin:0; font-size:13px; min-height:18px; color:var(--muted); }
.enq .status.err{ color:var(--orange); } .enq .status.ok{ color:var(--green); }
.enq .hp{ position:absolute; left:-9999px; width:1px; height:1px; overflow:hidden; }
"""
def enquiry(default_interest='', page_label=''):
    opts = ''.join(f'<option{" selected" if o == default_interest else ""}>{o}</option>' for o in INTERESTS)
    first = '' if default_interest else '<option value="" selected disabled>Chuniye…</option>'
    return f"""  <section class="card enq" id="query" aria-label="Query bhejein">
    <div class="intro">
      <h2>Query bhejein</h2>
      <p>Form bhariye aur "WhatsApp par bhejein" dabaiye. Aapki query seedha Kavi Sir ke WhatsApp par pahunch jayegi.</p>
      <ul><li>Kaunsa program aapke liye sahi hai</li><li>Fees, batch aur access ki jaankari</li><li>Call ka time aap khud chuniye</li></ul>
    </div>
    <form id="enqForm" novalidate>
      <div><label for="eName">Aapka naam</label><input id="eName" type="text" autocomplete="name" maxlength="60" placeholder="Jaise: Rahul Verma"></div>
      <div><label for="ePhone">WhatsApp number</label><input id="ePhone" type="tel" inputmode="tel" autocomplete="tel" maxlength="16" placeholder="98765 43210"></div>
      <div><label for="eInt">Kis cheez mein interest hai</label><select id="eInt">{first}{opts}</select></div>
      <div><label for="eTime">Call ka best time</label><select id="eTime"><option>Subah (9–12)</option><option>Dopahar (12–4)</option><option selected>Shaam (4–8)</option><option>Raat (8–10)</option></select></div>
      <div class="full"><label for="eQ">Aapka sawal (optional)</label><textarea id="eQ" maxlength="400" placeholder="Jaise: main beginner hoon, kahan se shuru karun?"></textarea></div>
      <div class="hp" aria-hidden="true"><label for="eWeb">Website</label><input id="eWeb" type="text" tabindex="-1" autocomplete="off"></div>
      <div class="full"><button class="btn wa send" type="submit">WhatsApp par bhejein</button></div>
      <p class="status full" id="eStatus" role="status" aria-live="polite"></p>
    </form>
  </section>
  <script>
  (function(){{
    var f = document.getElementById('enqForm'); if (!f) return;
    var $ = function(id){{ return document.getElementById(id); }};
    var say = function(t, c){{ var s = $('eStatus'); s.textContent = t; s.className = 'status full' + (c ? ' ' + c : ''); }};
    f.addEventListener('submit', function(e){{
      e.preventDefault();
      if ($('eWeb').value) return;
      var name = $('eName').value.trim(), raw = $('ePhone').value, d = raw.replace(/\\D/g, ''), it = $('eInt').value, tm = $('eTime').value, q = $('eQ').value.trim();
      if (d.length === 12 && d.indexOf('91') === 0) d = d.slice(2);
      $('eName').setAttribute('aria-invalid', name.length < 2); $('ePhone').setAttribute('aria-invalid', d.length < 10 || d.length > 13); $('eInt').setAttribute('aria-invalid', !it);
      if (name.length < 2) return say('Kripya apna naam daliye.', 'err');
      if (d.length < 10 || d.length > 13) return say('Kripya sahi WhatsApp number daliye.', 'err');
      if (!it) return say('Kripya interest chuniye.', 'err');
      var msg = 'Namaste Kavi Sir, I am ' + name + ' (' + d + '). I am interested in ' + it + '. Best time for a call: ' + tm + '.' + (q ? ' My question: ' + q.replace(/[.?!\\s]+$/, '') + '.' : '') + ' Please share your time for a call.';
      var url = 'https://wa.me/917817940814?text=' + encodeURIComponent(msg);
      var w = window.open(url, '_blank');
      {ga_lead('it')}
      try {{
        fetch('{SHEET_URL}', {{ method:'POST', mode:'no-cors', body: new URLSearchParams({{ name: name, phone: d, tool: 'Query · ' + it + ' · Call: ' + tm + (q ? ' · ' + q : ''), page: location.href }}) }});
      }} catch(x){{}}
      if (w) say('WhatsApp khul gaya. Message bhejne ke liye wahan Send dabaiye.', 'ok');
      else {{ say('WhatsApp kholne ke liye yahan dabaiye.', 'ok'); var a = document.createElement('a'); a.href = url; a.target = '_blank'; a.rel = 'noopener'; a.textContent = ' WhatsApp kholein →'; a.style.fontWeight = '600'; $('eStatus').appendChild(a); }}
    }});
  }})();
  </script>
"""

def btn(cls, url, label, soon):
    if url:
        return f'<a class="btn {cls}" href="{url}" target="_blank" rel="noopener">{label}</a>'
    return f'<a class="btn {cls}" aria-disabled="true">{soon}</a>'


# ======================= FEATURE SWITCHES (False = band, page pehle jaisa) =======================
FEATURES = dict(
    comparison=True,   # Learning Programs: programs comparison table
    curriculum=True,   # Learning Programs: "Andar kya hai" modules (sirf jin programs ke modules diye hain)
    sticky_bar=True,   # Phone par neeche "Ask now" bar
    next_batch=True,   # Swing Elite par next batch / seats (sirf jab NEXT_BATCH bhara ho)
)
# ---- EDIT HERE: modules per program (Kavi bhejenge) ----
CURRICULUM = {'728981': [], '690245': [], '690264': [], '692783': [], '894443': []}
# ---- EDIT HERE: Swing Elite next batch (khaali = nahi dikhega) ----
NEXT_BATCH = ''   # jaise '1 Nov 2026'
SEATS_LEFT = ''   # jaise '8'

# ======================= COURSES =======================
# ---- EDIT HERE: intro video per program (kin logon ko join karna chahiye) ----
SWING_RESULTS_PLAYLIST = ''  # unlisted YouTube playlist link
INTRO_VIDEOS = {'728981': '', '690245': '', '690264': '', '692783': '', '894443': ''}
C = lambda cid: f'https://www.explosivetrades.com/courses/{cid}{UTM}'
courses_css = '''
.path{ display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-top:18px; font-size:13px; }
.path span{ padding:5px 12px; border-radius:20px; background:var(--panel2); border:1px solid var(--line); white-space:nowrap; }
.path span.end{ border-color:var(--gold); color:var(--gold); font-weight:600; }
.path i{ color:var(--muted); font-style:normal; }
.clist{ display:grid; gap:16px; }
.course{ display:grid; grid-template-columns:auto minmax(0,1fr) minmax(0,220px); gap:20px; align-items:start; }
@media (max-width:820px){ .course{ grid-template-columns:auto minmax(0,1fr); } .course .side{ grid-column:1 / -1; } }
.course.main{ border:1.5px solid var(--gold); background:linear-gradient(160deg, color-mix(in srgb, var(--gold) 12%, var(--panel)), var(--panel) 70%); }
.course .no{ font-family:var(--display); font-size:44px; line-height:.9; color:var(--gold); }
.course h3{ margin:0 0 4px; font-size:19px; }
.course .tag{ margin:0 0 10px; color:var(--muted); font-size:14px; }
.course ul{ margin:0; padding-left:18px; font-size:14px; display:grid; gap:3px; }
.course .who{ margin:10px 0 0; font-size:13px; color:var(--muted); }
.course .who b{ color:var(--text); }
.side{ display:grid; gap:10px; align-content:start; }
.price{ font-family:var(--display); font-size:38px; line-height:1; color:var(--text); }
.price small{ font-family:var(--body); font-size:12px; color:var(--muted); display:block; margin-top:4px; letter-spacing:0; }
.side .btn{ width:100%; }
.bundle{ display:grid; grid-template-columns:minmax(0,1fr) auto; gap:18px; align-items:center; border:1px dashed var(--gold); }
@media (max-width:680px){ .bundle{ grid-template-columns:1fr; } }
.bundle p{ margin:0; color:var(--muted); font-size:14px; }
.bundle .price{ font-size:44px; color:var(--gold); }
.intro-v{ display:flex; align-items:center; gap:10px; padding:9px 11px; border:1px solid var(--line); border-radius:10px; background:var(--panel2); text-decoration:none; color:var(--text); }
a.intro-v:hover{ border-color:#d4190f; }
.intro-v .iv-ic{ flex:0 0 28px; height:28px; border-radius:7px; background:#d4190f; color:#fff; display:grid; place-items:center; font-size:12px; }
.intro-v b{ display:block; font-size:13px; line-height:1.2; }
.intro-v small{ display:block; font-size:11.5px; color:var(--muted); line-height:1.3; }
.intro-v.soon{ opacity:.75; }
.intro-v.soon .iv-ic{ background:var(--line); color:var(--muted); }
.intro-v em{ margin-left:auto; font-style:normal; font-size:11px; color:var(--muted); border:1px solid var(--line); border-radius:20px; padding:1px 8px; }
.results{ display:grid; grid-template-columns:minmax(0,1fr) auto; gap:20px; align-items:center; border:1.5px solid #d4190f; background:linear-gradient(135deg, color-mix(in srgb, #d4190f 10%, var(--panel)), var(--panel) 70%); }
@media (max-width:680px){ .results{ grid-template-columns:1fr; } }
.results p{ margin:0; color:var(--muted); font-size:14px; max-width:62ch; }
.results p.fine{ margin-top:8px; font-size:12px; }
.results .btn{ white-space:nowrap; padding:13px 20px; }
.btn[aria-disabled="true"]{ opacity:.55; pointer-events:none; }

.curr{ margin-top:12px; border:1px solid var(--line); border-radius:10px; background:var(--panel2); }
.curr summary{ cursor:pointer; padding:9px 12px; font-size:13.5px; font-weight:600; color:var(--gold); list-style:none; }
.curr summary::-webkit-details-marker{ display:none; }
.curr summary::after{ content:" +"; } .curr[open] summary::after{ content:" –"; }
.curr ol{ list-style:none; margin:0; padding:0 12px 10px; display:grid; gap:4px; font-size:13.5px; }
.curr li{ display:flex; gap:10px; } .curr li span{ color:var(--muted); font-variant-numeric:tabular-nums; }
.batch{ font-size:12.5px; color:var(--text); background:color-mix(in srgb, var(--orange) 14%, transparent); border:1px solid var(--orange); border-radius:9px; padding:6px 10px; }
.batch b{ color:var(--orange); }
tr.hl td{ background:color-mix(in srgb, var(--gold) 8%, transparent); }
.bundle-r{ display:grid; gap:10px; justify-items:end; }
@media (max-width:680px){ .bundle-r{ justify-items:start; } }
.price .ask{ font-family:var(--body); font-size:12px; font-weight:600; color:#3fbf73; text-decoration:none; letter-spacing:0; vertical-align:middle; margin-left:4px; white-space:nowrap; }
.price .ask:hover{ text-decoration:underline; }
'''
STICKY_CSS = '''
.sticky{ display:none; }
@media (max-width:900px){
  .sticky{ display:grid; grid-template-columns:auto 1fr; gap:8px; position:fixed; left:0; right:0; bottom:0; z-index:60; padding:10px max(12px, env(safe-area-inset-right,0px)) calc(10px + env(safe-area-inset-bottom,0px)) max(12px, env(safe-area-inset-left,0px)); background:var(--panel); border-top:1px solid var(--line); box-shadow:0 -6px 20px rgba(0,0,0,.25); }
  .sticky a{ text-align:center; text-decoration:none; font:600 14px var(--body); border-radius:10px; padding:11px 14px; }
  .sticky .s-q{ color:var(--text); border:1px solid var(--line); }
  .sticky .s-wa{ background:#1f8f4e; color:#fff; }
  body.has-sticky{ padding-bottom:76px; }
}
'''

def curriculum_box(cid):
    mods = CURRICULUM.get(cid) or []
    if not (FEATURES['curriculum'] and mods): return ''
    items = ''.join(f'<li><span>{i+1:02d}</span>{m}</li>' for i, m in enumerate(mods))
    return f'<details class="curr"><summary>Andar kya hai · {len(mods)} modules</summary><ol>{items}</ol></details>'

def batch_box(cid):
    if not (FEATURES['next_batch'] and cid == '894443' and NEXT_BATCH): return ''
    seats = f' · <b>{SEATS_LEFT} seats bache</b>' if SEATS_LEFT else ''
    return f'<div class="batch">Next batch: <b>{NEXT_BATCH}</b>{seats}</div>'

def comparison_html():
    if not FEATURES['comparison']: return ''
    rows = [
      ('Trading Ka ABCD', '₹49', '5 saal', 'Live classes, PDFs', 'Bilkul naye'),
      ('Indian Gold Market (MCX)', '₹4,999', '3 saal', 'Videos, tests, PDFs', 'Beginner se advanced'),
      ('Forex / XAUUSD', '₹4,999', '3 saal', 'Videos, PDFs', 'Beginner se advanced'),
      ('Funded Account Mastery', '₹4,999', '3 saal', 'Videos, PDFs', 'Prop firm traders'),
      ('XAUUSD Swing Traders Elite', 'WhatsApp par poochein', 'Group membership', 'Weekend live sessions, swing setups Group Head ke saath, personal support', 'Basic knowledge zaroori'),
    ]
    tr = ''.join(f'<tr{" class=\"hl\"" if r[0].startswith("XAUUSD") else ""}><td><b>{r[0]}</b></td><td class="num">{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>' for r in rows)
    return f"""  <section aria-label="Programs comparison" id="compare">
    <h2>Programs comparison</h2>
    <p class="sec-lead">Ek nazar mein: price, access, kya milta hai aur kis level ke liye hai.</p>
    <div class="tbl"><table><thead><tr><th>Program</th><th>Price</th><th>Access</th><th>Kya milta hai</th><th>Level</th></tr></thead><tbody>{tr}</tbody></table></div>
  </section>
"""

def sticky_bar(msg='Namaste Kavi Sir, I am interested in your learning programs. Please share your time for a call.', form='#query'):
    if not FEATURES['sticky_bar']: return ''
    url = 'https://wa.me/917817940814?text=' + __import__('urllib.parse').parse.quote(msg)
    return f"""<div class="sticky" role="region" aria-label="Quick contact">
  <a class="s-q" href="{form}">Query form</a>
  <a class="s-wa" href="{url}" target="_blank" rel="noopener">💬 Ask now on WhatsApp</a>
</div>
"""

def intro_box(cid):
    url = INTRO_VIDEOS.get(cid, '')
    inner = '<span class="iv-ic" aria-hidden="true">▶</span><span><b>Intro video</b><small>Kin logon ko ye program join karna chahiye</small></span>'
    if url:
        return f'<a class="intro-v" href="{url}" target="_blank" rel="noopener">{inner}</a>'
    return f'<div class="intro-v soon">{inner}<em>Jald</em></div>'

def WA_ASK(name):
    import urllib.parse
    return 'https://wa.me/917817940814?text=' + urllib.parse.quote(f'Namaste Kavi Sir, I am interested in the {name}' + ('' if 'Program' in name else ' learning program') + '. Please share your time for a call.')

def course_card(no, cid, name, tagline, points, who, price, price_note, main=False, badge=''):
    pts = ''.join(f'<li>{p}</li>' for p in points)
    return f'''      <article class="card course{' main' if main else ''}">
        <div class="no">{no}</div>
        <div>
          {f'<span class="pill gold">{badge}</span>' if badge else ''}
          <h3>{name}</h3>
          <p class="tag">{tagline}</p>
          <ul>{pts}</ul>
          <p class="who"><b>Kiske liye:</b> {who}</p>
          {curriculum_box(cid)}
        </div>
        <div class="side">
          <div class="price">{price} <a class="ask" href="{WA_ASK(name)}" target="_blank" rel="noopener">Ask now →</a><small>{price_note}</small></div>
          {batch_box(cid)}
          <a class="btn {'gold' if main else 'green'}" href="{C(cid)}" target="_blank" rel="noopener">Program details &amp; join</a>
          {intro_box(cid)}
        </div>
      </article>
'''
cards = ''.join([
  course_card(1, '728981', 'Trading Ka ABCD · Complete Trading Foundation', 'Bilkul zero se trading samjhein, simple Hindi-English mein.',
    ['Trading kya hai aur aaj kyon zaroori hai', 'Win rate, probability aur basic risk management', 'Investing, swing, intraday aur scalping ka farak', 'Ek professional trader decision kaise leta hai'],
    'Jo bilkul naye hain aur aage Gold, Forex, stocks ya funded accounts mein professional trading karna chahte hain.', '₹49', '5 saal access · live classes + PDFs', badge='Yahan se shuru karein'),
  course_card(2, '690245', 'Indian Gold Market Program (MCX)', 'GoldMini aur GoldPetal mein zone-based trading, Indian exchange par.',
    ['GoldMini aur GoldPetal ki practical strategy', 'Zone-based trading system', 'Risk management', 'Real market analysis'],
    'Jo sirf Indian gold market (MCX) trade karna chahte hain, beginner se advanced tak.', '₹4,999', '3 saal access'),
  course_card(3, '690264', 'Forex / XAUUSD Program', 'International market mein Gold (XAUUSD) trading.',
    ['Zone-based, multi-timeframe strategy, news impact ke saath', 'Global market timing', 'International broker par account setup', 'Strict money management'],
    'Jo international forex brokers ke through XAUUSD trade karna chahte hain.', '₹4,999', '3 saal access'),
  course_card(4, '692783', 'Funded Account Mastery', 'Prop firm challenge pass karna aur funded account scale karna.',
    ['Challenge rules ki poori samajh', 'Prop firm ke hisaab se risk management', 'Drawdown handle karna', 'Scaling roadmap: chhote account se bade account tak'],
    'Jo apne paise ki jagah firm ke capital se trading business banana chahte hain.', '₹4,999', '3 saal access'),
  course_card(5, '894443', 'XAUUSD Swing Traders Elite', 'Har swing decision par focused support. Chhota group, personal attention.',
    ['Group Head ke saath swing setups plan aur execute karna', 'Har Saturday aur Sunday live session: market conditions aur weekly analysis', 'Trade planning, entry, risk aur position management mein seedhi madad', 'Patience, discipline aur swing trader mindset par coaching'],
    'Jinke paas basic market knowledge hai aur jo consistent, independent swing trader banna chahte hain. Bilkul naye logon ke liye nahi.', 'Elite', 'Fee aur seats ke liye WhatsApp karein', main=True, badge='Main program'),
])
faqs = [
  ('Main bilkul naya hoon. Kahan se shuru karun?', 'Pehle "Trading Ka ABCD" (₹49) karein. Usme trading ki basic samajh, risk aur probability clear ho jati hai. Phir apne market ke hisaab se Indian Gold ya Forex/XAUUSD program chuniye.'),
  ('Learning programs kis language mein hain?', 'Simple Hindi-English (Hinglish) mein, taaki har level ka trader aasani se samajh sake.'),
  ('Program ka access kitne time tak rahega?', 'Indian Gold, Forex/XAUUSD aur Funded Account Mastery ka access 3 saal ka hai. Trading Ka ABCD ka access 5 saal ka hai.'),
  ('Kya teen programs ek saath sasta milta hai?', 'Haan. Indian Gold + Forex/XAUUSD + Funded Account Mastery ka Complete Bundle ₹9,999 mein hai. Alag-alag lene par teeno ₹4,999 ke hain.'),
  ('Program kahan aur kaise dekhenge?', 'Program join karne ke baad Explosive Trades app ya website par apne account se login karke videos, PDFs aur classes dekh sakte hain.'),
  ('Swing Traders Elite baaki programs se alag kaise hai?', 'Ye recorded program se aage ka program hai: chhota group, Group Head ke saath trades ki planning, aur har weekend live sessions. Ye unke liye hai jinke paas basic knowledge pehle se hai.'),
  ('Kya program ke baad profit ki guarantee hai?', 'Nahi. Trading mein risk hota hai aur koi bhi honest teacher profit ki guarantee nahi de sakta. Hum strategy, risk management aur discipline sikhate hain. Result aapki practice aur execution par depend karta hai.'),
  ('Kya aap buy/sell calls ya tips dete hain?', 'Nahi. Explosive Trades sirf education deta hai. Hum SEBI registered nahi hain aur koi trading tips ya calls nahi dete.'),
  ('Funded account ke liye apne paise lagane padenge?', 'Prop firm ka challenge fee dena hota hai, trading capital firm deti hai. Funded Account Mastery mein sikhaya jata hai ki challenge rules ke andar kaise trade karein.'),
  ('Join karne se pehle koi sawal ho to?', 'Neeche diye WhatsApp button se message karein. Kaunsa program aapke liye sahi hai, ye hum bata denge.'),
]
faq_html = ''.join(f'''    <details class="faq"><summary>{q}</summary><p>{a}</p></details>\n''' for q,a in faqs)
courses_body = f'''  <section aria-label="Intro">
    <p class="kicker">Learning programs</p>
    <h1>Ek strategy, <span>alag markets</span></h1>
    <p class="lead">Kavi Sharma ka zone-based system, basic se professional level tak. Apne market aur level ke hisaab se learning program chuniye.</p>
    <div class="path" aria-label="Recommended order"><span>Trading Ka ABCD</span><i>→</i><span>Indian Gold</span><i>→</i><span>Forex / XAUUSD</span><i>→</i><span>Funded Account</span><i>→</i><span class="end">Swing Traders Elite</span></div>
  </section>

  <section aria-label="Learning programs">
    <h2>Saare learning programs</h2>
    <p class="sec-lead">Har program ka price, access aur kya seekhenge. "Program details &amp; join" se seedha program page khulega.</p>
    <div class="clist" style="margin-bottom:16px">
{cards}    </div>
    <section class="card results" id="swing-results" aria-label="Swing trades results">
    <div>
      <span class="pill green">Trade logic + results</span>
      <h2 style="margin:8px 0 4px">Swing Trades Results</h2>
      <p>Kavi ke swing trades, har trade ka logic, entry, management aur result. Sab ek YouTube playlist mein, jaise-jaise trades hote hain.</p>
      <p class="fine">Past results future profit ki guarantee nahi hain. Ye sirf education aur transparency ke liye share kiye jaate hain.</p>
    </div>
    {btn('yt', SWING_RESULTS_PLAYLIST, '▶ View results', '▶ Results jald')}
    </section>
  </section>

  <section class="card bundle" aria-label="Complete Bundle">
    <div>
      <span class="pill green">Save ₹4,998</span>
      <h2 style="margin:8px 0 4px">Complete Bundle</h2>
      <p>Indian Gold Market + Forex/XAUUSD + Funded Account Mastery, teeno programs ek saath. Alag-alag lene par ₹14,997.</p>
    </div>
    <div class="bundle-r">
      <div class="price">₹9,999</div>
      <a class="btn wa" href="https://wa.me/917817940814?text=Namaste%20Kavi%20Sir%2C%20I%20am%20interested%20in%20all%20learning%20programs%3A%20Complete%20Bundle%20%28Indian%20Gold%20Market%20%2B%20Forex/XAUUSD%20%2B%20Funded%20Account%20Mastery%29%20for%20%E2%82%B99%2C999.%20Please%20share%20your%20time%20for%20a%20call." target="_blank" rel="noopener">Ask now</a>
    </div>
  </section>

{comparison_html()}
  <section aria-label="FAQ">
    <h2>Learning programs se jude sawal</h2>
    <p class="sec-lead">Jo sawal sabse zyada poochhe jaate hain.</p>
{faq_html}  </section>

{enquiry()}
'''
page(f'{ROOT}/courses/index.html', 'Learning Programs · Explosive Trades',
     'Explosive Trades ke saare learning programs: Trading Ka ABCD, Indian Gold, Forex/XAUUSD, Funded Account Mastery aur XAUUSD Swing Traders Elite, FAQ ke saath.',
     'courses', courses_css + ENQ_CSS, courses_body, sticky_bar())

# ======================= PROP FIRMS =======================
# ---- EDIT HERE: prop firm list (Kavi batayenge to update) ----
PROP_FIRMS = [
  dict(name='FundingPips', note='Kavi ka main prop firm. MT5 par challenge aur alag-alag payout options.',
       model='', video='', url='https://fundingpips.com', offer='Open FundingPips &amp; get 20% offer', code='0888028d', code_label='Code'),
  dict(name='FundedElite', note='Kavi yahan bhi challenges trade karte hain.',
       model='', video='', url='https://fundedelite.com', offer='', code='AFF1265748', code_label='Code'),
  dict(name='The5ers', note='Purani aur jaani-maani firm. Kavi isme High Stakes account trade karte hain.',
       model='', video='', url='https://the5ers.com', offer='', code='', code_label=''),
]
# ---- EDIT HERE: challenge pass videos ----
CHALLENGES = [
  # dict(title='FundingPips 100K Phase 1 clear', firm='FundingPips', video='https://youtu.be/...'),
]
# ---- EDIT HERE: setup links ----
BANK_VIDEO = ''
KYC_VIDEO = ''
PAYOUTS = [
  dict(name='Rise', desc='Prop firm payouts ke liye sabse common tareeka. Rise account se paisa bank mein le sakte hain.', url='https://www.riseworks.io'),
  dict(name='Crypto (USDT)', desc='Kai firms crypto mein bhi payout deti hain. Apna wallet address dhyan se daalein.', url=''),
]

prop_css = """
.flist{ display:grid; gap:14px; }
.firm{ display:grid; grid-template-columns:auto minmax(0,1fr) auto; gap:18px; align-items:center; }
@media (max-width:820px){ .firm{ grid-template-columns:auto minmax(0,1fr); } .firm .acts{ grid-column:1 / -1; } }
.firm .logo{ width:52px; height:52px; border-radius:12px; background:var(--panel2); border:1px solid var(--line); display:grid; place-items:center; font-family:var(--display); font-size:22px; color:var(--gold); letter-spacing:.03em; }
.firm h3{ margin:0 0 2px; font-size:19px; }
.firm .why{ margin:0 0 8px; color:var(--muted); font-size:13.5px; }
.model{ display:inline-flex; gap:8px; align-items:center; flex-wrap:wrap; font-size:13px; }
.model span{ color:var(--muted); }
.model b{ color:var(--gold); }
.model i{ font-style:normal; color:var(--muted); }
.acts{ display:flex; gap:8px; flex-wrap:wrap; justify-content:flex-end; }
@media (max-width:820px){ .acts{ justify-content:flex-start; } }
.acts .btn{ padding:10px 14px; font-size:14px; }
.btn[aria-disabled="true"]{ opacity:.55; pointer-events:none; }
.code{ display:inline-flex; align-items:center; gap:8px; padding:6px 6px 6px 12px; border:1px dashed var(--gold); border-radius:10px; font-size:12px; color:var(--muted); }
.code b{ font-family:ui-monospace, Menlo, monospace; font-size:14px; color:var(--gold); letter-spacing:.04em; }
.code button{ background:var(--panel2); border:1px solid var(--line); color:var(--text); border-radius:7px; padding:4px 10px; font:500 12px var(--body); cursor:pointer; }
.chal{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:14px; }
@media (max-width:860px){ .chal{ grid-template-columns:1fr 1fr; } }
@media (max-width:540px){ .chal{ grid-template-columns:1fr; } }
.chal .card{ display:flex; flex-direction:column; gap:10px; }
.chal .thumb{ aspect-ratio:16/9; max-width:100%; border-radius:10px; background:linear-gradient(135deg, color-mix(in srgb, var(--gold) 18%, var(--panel2)), var(--panel2)); display:grid; place-items:center; font-family:var(--display); font-size:22px; color:var(--gold); letter-spacing:.04em; text-align:center; padding:10px; }
.chal h3{ margin:0; font-size:16px; }
.chal p{ margin:0; font-size:13px; color:var(--muted); }
.chal .btn{ margin-top:auto; }
.empty{ padding:22px; border:1px dashed var(--line); border-radius:14px; color:var(--muted); text-align:center; }
.setup{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; }
@media (max-width:720px){ .setup{ grid-template-columns:1fr; } }
.setup .card{ display:flex; flex-direction:column; gap:8px; }
.setup .k{ font-size:11px; font-weight:600; letter-spacing:.08em; text-transform:uppercase; color:var(--gold); }
.setup h3{ margin:0; font-size:17px; }
.setup p{ margin:0; font-size:13.5px; color:var(--muted); }
.setup .btn{ align-self:flex-start; margin-top:4px; padding:10px 14px; font-size:14px; }
.note{ font-size:12.5px; color:var(--muted); margin:12px 0 0; }
.toast{ position:fixed; bottom:18px; left:50%; transform:translateX(-50%); background:var(--gold); color:var(--on-gold); font-weight:600; padding:8px 16px; border-radius:20px; font-size:13px; opacity:0; transition:opacity .2s; pointer-events:none; }
.toast.show{ opacity:1; }
"""


def firm_row(f):
    model = f'<span>Best model:</span> <b>{f["model"]}</b>' if f['model'] else '<span>Best model:</span> <i>jald update hoga</i>'
    code = f'<span class="code">{f["code_label"]} <b>{f["code"]}</b><button type="button" data-copy="{f["code"]}">Copy</button></span>' if f['code'] else ''
    offer = f['offer'] or f'Open {f["name"]}'
    initials = '5%' if f['name'] == 'The5ers' else ''.join(c for c in f['name'] if c.isupper())[:2]
    return f"""      <article class="card firm">
        <div class="logo" aria-hidden="true">{initials}</div>
        <div>
          <h3>{f['name']}</h3>
          <p class="why">{f['note']}</p>
          <div class="model">{model} {code}</div>
        </div>
        <div class="acts">
          {btn('yt', f['video'], '▶ Deep analysis video', '▶ Analysis video jald')}
          <a class="btn gold" href="{f['url']}" target="_blank" rel="noopener sponsored">{offer}</a>
        </div>
      </article>
"""
firms_html = ''.join(firm_row(f) for f in PROP_FIRMS)

if CHALLENGES:
    chal_html = '<div class="chal">' + ''.join(f"""
      <div class="card"><div class="thumb">{c['firm']}</div><h3>{c['title']}</h3>{btn('yt', c['video'], '▶ Video dekhein', 'Video jald')}</div>""" for c in CHALLENGES) + '\n    </div>'
else:
    chal_html = '<div class="empty">Challenge videos jald yahan aayenge. Tab tak YouTube channel par latest videos dekhein.<br><br><a class="btn yt" href="https://www.youtube.com/@explosivetrades?sub_confirmation=1" target="_blank" rel="noopener">YouTube channel kholein</a></div>'

pay_html = ''.join(f"""      <div class="card"><span class="k">Payout</span><h3>{x['name']}</h3><p>{x['desc']}</p>{btn('line', x['url'], f"{x['name']} kholein", 'Link jald')}</div>
""" for x in PAYOUTS)

prop_body = f"""  <section aria-label="Intro">
    <p class="kicker">Best prop firms</p>
    <h1>Prop firms jahan <span>Kavi khud trade karte hain</span></h1>
    <p class="lead">Har firm ka deep analysis video, Kavi ka chuna hua best model, aur seedha offer link. Firm chunne se pehle analysis video zaroor dekhein.</p>
  </section>

  <section aria-label="Prop firm list">
    <h2>Prop firm list</h2>
    <p class="sec-lead">Analysis video dekhein, phir firm ki website par jaakar latest rules check karein.</p>
    <div class="flist">
{firms_html}    </div>
    <p class="note">Disclosure: kuch links aur codes Explosive Trades ke affiliate links hain. Inse kharidne par Explosive Trades ko commission mil sakta hai, aapki price par iska asar nahi padta. Rules, offers aur prices firms kabhi bhi badal sakti hain.</p>
  </section>

  <section aria-label="Challenges">
    <h2>Challenges live clear karte hue</h2>
    <p class="sec-lead">Kavi challenges khud lete hain aur clear karke dikhate hain. Har video mein planning, risk aur execution poori dikhti hai.</p>
    {chal_html}
  </section>

  <section class="card contact" aria-label="Program">
    <div>
      <h2 style="margin-bottom:4px">Challenge pass karna seekhein</h2>
      <p>Funded Account Mastery program mein challenge rules, prop firm ke hisaab se risk management, drawdown handle karna aur scaling roadmap sikhaya gaya hai.</p>
    </div>
    <a class="btn gold" href="{C('692783')}" target="_blank" rel="noopener">Program dekhein</a>
  </section>

  <section aria-label="Setup">
    <h2>Prop firm ke liye required setup</h2>
    <p class="sec-lead">Challenge kharidne se pehle ye cheezein ready rakhein, taaki payout ke time koi dikkat na ho.</p>
    <div class="setup">
      <div class="card"><span class="k">Bank</span><h3>Best bank account</h3><p>Payout ka paisa India mein lene ke liye kaunsa bank account sahi rahega, is video mein samjhaya gaya hai.</p>{btn('yt', BANK_VIDEO, '▶ Video dekhein', '▶ Video jald')}</div>
{pay_html}      <div class="card"><span class="k">Platform</span><h3>MT5 trading platform</h3><p>Zyadatar prop firms MT5 deti hain. Login details firm ke dashboard mein milte hain.</p><a class="btn line" href="https://www.metatrader5.com/en/download" target="_blank" rel="noopener">MT5 download karein</a></div>
      <div class="card"><span class="k">KYC</span><h3>Documents ready rakhein</h3><p>Funded account aur payout ke time ID proof aur address proof ki KYC hoti hai. Naam har jagah same rakhein.</p>{btn('yt', KYC_VIDEO, '▶ Video dekhein', '▶ Video jald')}</div>
    </div>
  </section>

{enquiry('Prop firm help')}
  <div class="toast" id="toast" role="status"></div>
  <script>
  document.addEventListener('click', function(e){{
    var b = e.target.closest('[data-copy]'); if (!b) return;
    var t = document.getElementById('toast'), v = b.getAttribute('data-copy');
    var done = function(m){{ t.textContent = m; t.classList.add('show'); setTimeout(function(){{ t.classList.remove('show'); }}, 1600); }};
    (navigator.clipboard ? navigator.clipboard.writeText(v) : Promise.reject()).then(function(){{ done('Code copy ho gaya: ' + v); }}, function(){{ done('Code: ' + v); }});
  }});
  </script>
"""
page(f'{ROOT}/prop-firms/index.html', 'Best Prop Firms · Explosive Trades',
     'Prop firms jahan Kavi Sharma khud trade karte hain: deep analysis videos, best model, offers, live challenges aur payout setup.',
     'prop', prop_css + ENQ_CSS, prop_body,
     sticky_bar('Namaste Kavi Sir, I need help with prop firm challenges. Please share your time for a call.'))

# Social profiles (link khaali = button nahi dikhega)
SOCIAL = [
  ('YouTube Global', 'https://www.youtube.com/@ExplosiveTradesGlobal', 'yt'),
  ('YouTube Hindi', 'https://www.youtube.com/@explosivetrades', 'yt'),
  ('Instagram', 'https://www.instagram.com/kavisharma.trader', 'ig'),
  ('Facebook', 'https://www.facebook.com/kavisharma.trader', 'fb'),
  ('Telegram', 'https://t.me/FullPotentialMode', 'tg'),
]
_ICON = {
  'yt': '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12a31 31 0 0 0 .5 4.8 3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1c.4-1.6.5-3.2.5-4.8s-.1-3.2-.5-4.8ZM9.8 15.1V8.9l5.6 3.1-5.6 3.1Z"/></svg>',
  'ig': '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 7.3a4.7 4.7 0 1 0 0 9.4 4.7 4.7 0 0 0 0-9.4Zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6Zm6-7.9a1.1 1.1 0 1 1-2.2 0 1.1 1.1 0 0 1 2.2 0ZM21.4 8.2c-.1-1.5-.4-2.8-1.5-3.9s-2.4-1.4-3.9-1.5C14.5 2.7 9.5 2.7 8 2.8c-1.5.1-2.8.4-3.9 1.5S2.7 6.7 2.6 8.2c-.1 1.5-.1 6.5 0 8 .1 1.5.4 2.8 1.5 3.9s2.4 1.4 3.9 1.5c1.5.1 6.5.1 8 0 1.5-.1 2.8-.4 3.9-1.5s1.4-2.4 1.5-3.9c.1-1.5.1-6.5 0-8Zm-2 9.6a3 3 0 0 1-1.7 1.7c-1.2.5-4 .4-5.3.4s-4.1.1-5.3-.4a3 3 0 0 1-1.7-1.7c-.5-1.2-.4-4-.4-5.3s-.1-4.1.4-5.3a3 3 0 0 1 1.7-1.7c1.2-.5 4-.4 5.3-.4s4.1-.1 5.3.4a3 3 0 0 1 1.7 1.7c.5 1.2.4 4 .4 5.3s.1 4.1-.4 5.3Z"/></svg>',
  'fb': '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.3v7A10 10 0 0 0 22 12Z"/></svg>',
  'tg': '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M21.9 4.3 18.7 19.4c-.2 1.1-.9 1.3-1.8.8l-4.9-3.6-2.4 2.3c-.3.3-.5.5-1 .5l.3-5 9.1-8.2c.4-.4-.1-.6-.6-.2L6.2 13 1.4 11.5c-1-.3-1.1-1 .2-1.5L20.5 2.7c.9-.3 1.7.2 1.4 1.6Z"/></svg>',
}
def social_row():
    items = ''.join(f'<a class="soc soc-{k}" href="{u}" target="_blank" rel="noopener">{_ICON[k]}<span>{n}</span></a>' for n, u, k in SOCIAL if u)
    if not items: return ''
    return '      <div class="follow"><p class="follow-h">Journey follow karein</p><div class="socs">' + items + '</div></div>\n'
SOCIAL_CSS = """
.follow{ margin-top:16px; }
.follow-h{ margin:0 0 8px !important; font-size:12.5px; font-weight:600; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); }
.socs{ display:flex; flex-wrap:wrap; gap:8px; }
.soc{ display:inline-flex; align-items:center; gap:8px; padding:8px 13px; border-radius:999px; border:1px solid var(--line); background:var(--panel2); color:var(--text); text-decoration:none; font-size:13.5px; font-weight:500; }
.soc svg{ width:17px; height:17px; flex:none; }
.soc:hover{ border-color:var(--gold); }
.soc-yt svg{ color:#ff3b30; } .soc-ig svg{ color:#e1306c; } .soc-fb svg{ color:#1877f2; } .soc-tg svg{ color:#2aabee; }
"""

# ======================= GLOBAL CHANNEL =======================
global_css = '''
.hero{ display:grid; grid-template-columns:minmax(0,1.3fr) minmax(0,1fr); gap:24px; align-items:center; }
@media (max-width:820px){ .hero{ grid-template-columns:1fr; } }
.chan{ display:grid; gap:14px; justify-items:start; border:1.5px solid var(--gold); }
.chan .h{ display:flex; align-items:center; gap:14px; }
.chan .logo{ width:56px; height:56px; border-radius:50%; background:var(--gold); color:var(--on-gold); display:grid; place-items:center; font-family:var(--display); font-size:24px; letter-spacing:.04em; }
.chan b{ display:block; font-size:18px; }
.chan small{ color:var(--muted); }
.chan p{ margin:0; color:var(--muted); font-size:14px; }
.topics{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:14px; }
@media (max-width:820px){ .topics{ grid-template-columns:1fr 1fr; } }
@media (max-width:520px){ .topics{ grid-template-columns:1fr; } }
.topics .card b{ display:block; margin-bottom:4px; }
.topics .card p{ margin:0; font-size:13.5px; color:var(--muted); }
.two{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }
@media (max-width:720px){ .two{ grid-template-columns:1fr; } }
.two h3{ margin:0 0 6px; font-size:17px; }
.two p{ margin:0 0 12px; color:var(--muted); font-size:14px; }
.me{ display:grid; grid-template-columns:minmax(0,300px) minmax(0,1fr); gap:28px; align-items:start; }
.me figure{ padding-top:46px; }
@media (max-width:760px){ .me figure{ padding-top:0; } }
@media (max-width:760px){ .me{ grid-template-columns:1fr; gap:18px; } }
.me figure{ margin:0; position:relative; }
.me img{ display:block; width:100%; max-width:300px; aspect-ratio:1/1; object-fit:cover; border-radius:18px; border:2px solid var(--gold); box-shadow:0 18px 40px rgba(0,0,0,.35); }
@media (max-width:760px){ .me img{ max-width:220px; } }
.me figcaption{ margin-top:10px; font-size:13px; color:var(--muted); }
.me figcaption b{ color:var(--text); display:block; font-size:15px; }
.me h2{ margin-top:0; }
.me p{ color:var(--muted); margin:0 0 12px; }
.me p strong{ color:var(--text); font-weight:600; }
.me .tagline{ font-family:var(--display); color:var(--gold); font-size:22px; letter-spacing:.04em; margin:-4px 0 14px; line-height:1.2; }
.goal{ background:var(--panel2); border:1px solid var(--line); border-left:3px solid var(--gold); border-radius:12px; padding:14px 16px; margin:4px 0 6px; }
.goal .goal-h{ margin:0 0 10px; color:var(--text); font-weight:600; font-size:14px; text-transform:uppercase; letter-spacing:.08em; }
.goal ol{ list-style:none; margin:0; padding:0; display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:10px; counter-reset:g; }
@media (max-width:620px){ .goal ol{ grid-template-columns:1fr; } }
.goal li{ counter-increment:g; position:relative; padding:10px 12px 10px 44px; background:var(--panel); border:1px solid var(--line); border-radius:10px; }
.goal li::before{ content:counter(g); position:absolute; left:12px; top:10px; width:22px; height:22px; border-radius:50%; background:var(--gold); color:var(--on-gold); font-size:12px; font-weight:700; display:grid; place-items:center; }
.goal li b{ display:block; color:var(--gold); font-size:14.5px; }
.goal li span{ display:block; font-size:13px; color:var(--muted); line-height:1.45; }
.goal li em{ display:block; font-style:normal; font-weight:600; color:var(--text); font-size:13.5px; line-height:1.35; margin:2px 0 4px; }
.goal-q{ margin:14px 0 0 !important; font-size:14.5px; color:var(--text) !important; font-style:italic; }
.goal-cta{ display:flex; flex-wrap:wrap; gap:10px; margin-top:12px; }
.goal-cta .btn{ font-size:14px; }
.stats{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:10px; margin:16px 0 4px; }
@media (max-width:520px){ .stats{ grid-template-columns:1fr 1fr; } }
.stats div{ background:var(--panel2); border:1px solid var(--line); border-radius:12px; padding:10px 12px; }
.stats b{ display:block; font-family:var(--display); color:var(--gold); font-size:26px; line-height:1.1; letter-spacing:.02em; }
.stats span{ font-size:12.5px; color:var(--muted); }
'''
global_body = '''  <section class="hero" aria-label="Intro">
    <div>
      <p class="kicker">Our other YouTube channel</p>
      <h1>Explosive Trades <span>Global</span></h1>
      <p class="lead">An Indian trader going global, learning in public. Kavi Sharma ka Hindi + English channel, India aur duniya bhar ke traders ke liye: prop firm challenges, gold swing trading aur real results.</p>
    </div>
    <div class="card chan">
      <div class="h"><div class="logo" aria-hidden="true">ET</div><div><b>Explosive Trades Global</b><small>@ExplosiveTradesGlobal · Hindi + English</small></div></div>
      <p>Naya channel hai. Abhi subscribe karein aur shuruaat se journey ka hissa banein.</p>
      <a class="btn yt" href="https://www.youtube.com/@ExplosiveTradesGlobal?sub_confirmation=1" target="_blank" rel="noopener">YouTube par subscribe karein</a>
    </div>
  </section>

  <section class="me" aria-label="About Kavi Sharma">
    <figure>
      <img src="img/kavi-sharma.jpg" alt="Kavi Sharma, founder of Explosive Trades" width="300" height="300" loading="lazy">
      <figcaption><b>Kavi Sharma</b>Gold &amp; Forex Trader · Mentor · India</figcaption>
    </figure>
    <div>
      <p class="kicker">Meet your mentor</p>
      <h2>Namaste, main Kavi Sharma hoon</h2>
      <p class="tagline">Trade the world. Invest in gold. Build passive income.</p>
      <p>Main ek <strong>full-time Gold &amp; Forex trader</strong> hoon aur pichhle <strong>5 saal</strong> se XAUUSD aur major forex pairs trade kar raha hoon. Mera focus zone-based, multi-timeframe <strong>swing trading</strong> par hai, aur main <strong>FundingPips, FundedElite aur The5ers</strong> ke funded accounts par khud trade karta hoon.</p>
      <p>B.Tech (ECE) ke baad maine UPSC ki taiyari sirf YouTube aur Google se ki. Wahin economics padhte hue markets mein dilchaspi bani, aur yahin se mera financial education ka safar shuru hua.</p>
      <p>Explosive Trades par main wahi sikhata hoon jo khud follow karta hoon: process, risk management aur discipline. <strong>Explosive Trades Global</strong> par yahi journey ab Hindi aur English dono mein, duniya bhar ke traders ke saath.</p>
      <div class="goal" aria-label="Mera goal">
        <p class="goal-h">Mera goal, aur aapke liye raasta</p>
        <ol>
          <li><b>Earn</b><em>Prop firm ke capital se trade karo</em><span>Funded accounts par trading, sirf challenge fee lagakar. Apna bada paisa daav par lagaye bina.</span></li>
          <li><b>Reinvest</b><em>Kamai ko gold mein badlo</em><span>Har payout ka ek hissa Indian market ke gold products mein, taaki paisa bhi aapke liye kaam kare.</span></li>
          <li><b>Passive income</b><em>Aisa system jo lambe samay tak chale</em><span>Trading, reinvesting aur discipline milkar ek aisa system banaye jo saalon tak income de.</span></li>
        </ol>
        <p class="goal-q">“Main ye safar public mein kar raha hoon: har step, har result. Aap bhi saath chaliye.”</p>
        <div class="goal-cta">
          <a class="btn yt" href="https://www.youtube.com/@ExplosiveTradesGlobal?sub_confirmation=1" target="_blank" rel="noopener">▶ Journey follow karein</a>
          <a class="btn green" href="../courses/">Ye system seekhein →</a>
        </div>
      </div>
      <div class="stats">
        <div><b>5+</b><span>saal trading</span></div>
        <div><b>90K+</b><span>YouTube traders</span></div>
        <div><b>700+</b><span>community members</span></div>
        <div><b>3</b><span>prop firms</span></div>
      </div>
@@SOCIAL@@    </div>
  </section>

  <section aria-label="Topics">
    <h2>Is channel par kya milega</h2>
    <p class="sec-lead">Hindi aur English dono mein, India aur international traders ke liye. Koi buy/sell calls nahi, sirf process aur learning.</p>
    <div class="topics">
      <div class="card"><b>Prop firm challenges</b><p>Challenge ki planning se payout tak, step by step aur live.</p></div>
      <div class="card"><b>Gold swing trading</b><p>XAUUSD par zone-based, multi-timeframe swing approach.</p></div>
      <div class="card"><b>Real results</b><p>Apne trades, wins aur losses, bina editing ke.</p></div>
      <div class="card"><b>Risk management</b><p>Account bachane ke rules jo funded accounts mein kaam aate hain.</p></div>
      <div class="card"><b>Global markets</b><p>Alag-alag deshon ke markets aur unke rules ke hisaab se trading.</p></div>
      <div class="card"><b>Learning in public</b><p>Ek Indian trader ki global journey, jaise-jaise aage badhti hai.</p></div>
    </div>
  </section>

  <section class="two" aria-label="Both channels">
    <div class="card">
      <h3>Explosive Trades (Hindi)</h3>
      <p>Main channel, 90,000+ traders. Gold, Forex, prop firms aur Indian market, Hinglish mein.</p>
      <a class="btn line" href="https://www.youtube.com/@explosivetrades?sub_confirmation=1" target="_blank" rel="noopener">Main channel dekhein</a>
    </div>
    <div class="card">
      <h3>Explosive Trades Global (Hindi + English)</h3>
      <p>India aur international audience ke liye. Prop firm challenges aur gold swing trading, Hindi aur English dono mein.</p>
      <a class="btn yt" href="https://www.youtube.com/@ExplosiveTradesGlobal?sub_confirmation=1" target="_blank" rel="noopener">Global channel dekhein</a>
    </div>
  </section>
'''
global_body = global_body.replace('@@SOCIAL@@', social_row())
page(f'{ROOT}/global/index.html', 'Explosive Trades Global',
     'Explosive Trades Global: Kavi Sharma ka Hindi + English YouTube channel. Prop firm challenges, gold swing trading aur real results.',
     'global', global_css + SOCIAL_CSS, global_body,
     og_image='global/img/og-global-2.jpg', og_title='Explosive Trades Global · Kavi Sharma', og_url='global/')
print('pages written')
