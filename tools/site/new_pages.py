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

FOOTER = '''  <footer>
    <span>© Explosive Trades · Kavi Sharma · <a href="https://www.explosivetrades.com" target="_blank" rel="noopener">www.explosivetrades.com</a></span>
    <span>Disclaimer: Explosive Trades ka content sirf education ke liye hai. Hum SEBI registered nahi hain, koi buy/sell call ya profit ki guarantee nahi dete. Trading mein capital ka risk hota hai, apni samajh se trade karein.</span>
  </footer>'''

WA_BOX = lambda title, text, msg: f'''  <section class="contact" aria-label="WhatsApp">
    <div>
      <h2 style="margin-bottom:4px">{title}</h2>
      <p>{text} WhatsApp: <b style="color:var(--text)">+91 78179 40814</b></p>
    </div>
    <a class="btn wa" href="https://wa.me/917817940814?text={msg}" target="_blank" rel="noopener">WhatsApp karein</a>
  </section>'''

def page(path, title, desc, active, extra_css, body):
    out = f'''<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta name="theme-color" content="#1a1510">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
<style>{BASE_CSS}{NAV_CSS}{extra_css}</style>
</head>
<body>
{header("../", active, '<span class="by">Kavi Sharma · Founder</span>\n      <button class="icon-btn" id="themeBtn" type="button" aria-label="Theme badlein">Light</button>')}

<main class="wrap">
{body}
{FOOTER}
</main>
{THEME_JS}
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
      try {{
        fetch('{SHEET_URL}', {{ method:'POST', mode:'no-cors', body: new URLSearchParams({{ name: name, phone: d, tool: 'Query · ' + it + ' · Call: ' + tm + (q ? ' · ' + q : ''), page: location.href }}) }});
      }} catch(x){{}}
      if (w) say('WhatsApp khul gaya. Message bhejne ke liye wahan Send dabaiye.', 'ok');
      else {{ say('WhatsApp kholne ke liye yahan dabaiye.', 'ok'); var a = document.createElement('a'); a.href = url; a.target = '_blank'; a.rel = 'noopener'; a.textContent = ' WhatsApp kholein →'; a.style.fontWeight = '600'; $('eStatus').appendChild(a); }}
    }});
  }})();
  </script>
"""

# ======================= COURSES =======================
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
.bundle-r{ display:grid; gap:10px; justify-items:end; }
@media (max-width:680px){ .bundle-r{ justify-items:start; } }
.price .ask{ font-family:var(--body); font-size:12px; font-weight:600; color:#3fbf73; text-decoration:none; letter-spacing:0; vertical-align:middle; margin-left:4px; white-space:nowrap; }
.price .ask:hover{ text-decoration:underline; }
'''
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
        </div>
        <div class="side">
          <div class="price">{price} <a class="ask" href="{WA_ASK(name)}" target="_blank" rel="noopener">Ask now →</a><small>{price_note}</small></div>
          <a class="btn {'gold' if main else 'green'}" href="{C(cid)}" target="_blank" rel="noopener">Program details &amp; join</a>
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
    <div class="clist">
{cards}    </div>
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

  <section aria-label="FAQ">
    <h2>Learning programs se jude sawal</h2>
    <p class="sec-lead">Jo sawal sabse zyada poochhe jaate hain.</p>
{faq_html}  </section>

{enquiry()}
'''
page(f'{ROOT}/courses/index.html', 'Learning Programs · Explosive Trades',
     'Explosive Trades ke saare learning programs: Trading Ka ABCD, Indian Gold, Forex/XAUUSD, Funded Account Mastery aur XAUUSD Swing Traders Elite, FAQ ke saath.',
     'courses', courses_css + ENQ_CSS, courses_body)

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

def btn(cls, url, label, soon):
    if url:
        return f'<a class="btn {cls}" href="{url}" target="_blank" rel="noopener">{label}</a>'
    return f'<a class="btn {cls}" aria-disabled="true">{soon}</a>'

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
     'prop', prop_css + ENQ_CSS, prop_body)

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
'''
global_body = '''  <section class="hero" aria-label="Intro">
    <div>
      <p class="kicker">Our other YouTube channel</p>
      <h1>Explosive Trades <span>Global</span></h1>
      <p class="lead">An Indian trader going global, learning in public. Kavi Sharma ka English channel, duniya bhar ke traders ke liye: prop firm challenges, gold swing trading aur real results.</p>
    </div>
    <div class="card chan">
      <div class="h"><div class="logo" aria-hidden="true">ET</div><div><b>Explosive Trades Global</b><small>@ExplosiveTradesGlobal · English</small></div></div>
      <p>Naya channel hai. Abhi subscribe karein aur shuruaat se journey ka hissa banein.</p>
      <a class="btn yt" href="https://www.youtube.com/@ExplosiveTradesGlobal?sub_confirmation=1" target="_blank" rel="noopener">YouTube par subscribe karein</a>
    </div>
  </section>

  <section aria-label="Topics">
    <h2>Is channel par kya milega</h2>
    <p class="sec-lead">English mein, international traders ke liye. Koi buy/sell calls nahi, sirf process aur learning.</p>
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
      <h3>Explosive Trades Global (English)</h3>
      <p>International audience ke liye. Prop firm challenges aur gold swing trading, English mein.</p>
      <a class="btn yt" href="https://www.youtube.com/@ExplosiveTradesGlobal?sub_confirmation=1" target="_blank" rel="noopener">Global channel dekhein</a>
    </div>
  </section>
'''
page(f'{ROOT}/global/index.html', 'Explosive Trades Global',
     'Explosive Trades Global: Kavi Sharma ka English YouTube channel. Prop firm challenges, gold swing trading aur real results.',
     'global', global_css, global_body)
print('pages written')
