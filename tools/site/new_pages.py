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
{header("../", active, '<span class="by">Prepared by Kavi Sharma</span>\n      <button class="icon-btn" id="themeBtn" type="button" aria-label="Theme badlein">Light</button>')}

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
'''
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
          <div class="price">{price}<small>{price_note}</small></div>
          <a class="btn {'gold' if main else 'line'}" href="{C(cid)}" target="_blank" rel="noopener">Course details &amp; join</a>
        </div>
      </article>
'''
cards = ''.join([
  course_card(1, '728981', 'Trading Ka ABCD · Complete Trading Foundation', 'Bilkul zero se trading samjhein, simple Hindi-English mein.',
    ['Trading kya hai aur aaj kyon zaroori hai', 'Win rate, probability aur basic risk management', 'Investing, swing, intraday aur scalping ka farak', 'Ek professional trader decision kaise leta hai'],
    'Jo bilkul naye hain aur aage Gold, Forex, stocks ya funded accounts mein professional trading karna chahte hain.', '₹49', '5 saal access · live classes + PDFs', badge='Yahan se shuru karein'),
  course_card(2, '690245', 'Indian Gold Market Course (MCX)', 'GoldMini aur GoldPetal mein zone-based trading, Indian exchange par.',
    ['GoldMini aur GoldPetal ki practical strategy', 'Zone-based trading system', 'Risk management', 'Real market analysis'],
    'Jo sirf Indian gold market (MCX) trade karna chahte hain, beginner se advanced tak.', '₹4,999', '3 saal access'),
  course_card(3, '690264', 'Forex / XAUUSD Course', 'International market mein Gold (XAUUSD) trading.',
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
  ('Main bilkul naya hoon. Kahan se shuru karun?', 'Pehle "Trading Ka ABCD" (₹49) karein. Usme trading ki basic samajh, risk aur probability clear ho jati hai. Phir apne market ke hisaab se Indian Gold ya Forex/XAUUSD course chuniye.'),
  ('Courses kis language mein hain?', 'Simple Hindi-English (Hinglish) mein, taaki har level ka trader aasani se samajh sake.'),
  ('Course ka access kitne time tak rahega?', 'Indian Gold, Forex/XAUUSD aur Funded Account Mastery ka access 3 saal ka hai. Trading Ka ABCD ka access 5 saal ka hai.'),
  ('Kya teen courses ek saath sasta milta hai?', 'Haan. Indian Gold + Forex/XAUUSD + Funded Account Mastery ka Complete Bundle ₹9,999 mein hai. Alag-alag lene par teeno ₹4,999 ke hain.'),
  ('Course kahan aur kaise dekhenge?', 'Course join karne ke baad Explosive Trades app ya website par apne account se login karke videos, PDFs aur classes dekh sakte hain.'),
  ('Swing Traders Elite baaki courses se alag kaise hai?', 'Ye recorded course se aage ka program hai: chhota group, Group Head ke saath trades ki planning, aur har weekend live sessions. Ye unke liye hai jinke paas basic knowledge pehle se hai.'),
  ('Kya course ke baad profit ki guarantee hai?', 'Nahi. Trading mein risk hota hai aur koi bhi honest teacher profit ki guarantee nahi de sakta. Hum strategy, risk management aur discipline sikhate hain. Result aapki practice aur execution par depend karta hai.'),
  ('Kya aap buy/sell calls ya tips dete hain?', 'Nahi. Explosive Trades sirf education deta hai. Hum SEBI registered nahi hain aur koi trading tips ya calls nahi dete.'),
  ('Funded account ke liye apne paise lagane padenge?', 'Prop firm ka challenge fee dena hota hai, trading capital firm deti hai. Funded Account Mastery mein sikhaya jata hai ki challenge rules ke andar kaise trade karein.'),
  ('Course se pehle koi sawal ho to?', 'Neeche diye WhatsApp button se message karein. Kaunsa course aapke liye sahi hai, ye hum bata denge.'),
]
faq_html = ''.join(f'''    <details class="faq"><summary>{q}</summary><p>{a}</p></details>\n''' for q,a in faqs)
courses_body = f'''  <section aria-label="Intro">
    <p class="kicker">Learning courses</p>
    <h1>Ek strategy, <span>alag markets</span></h1>
    <p class="lead">Kavi Sharma ka zone-based system, basic se professional level tak. Apne market aur level ke hisaab se course chuniye.</p>
    <div class="path" aria-label="Recommended order"><span>Trading Ka ABCD</span><i>→</i><span>Indian Gold</span><i>→</i><span>Forex / XAUUSD</span><i>→</i><span>Funded Account</span><i>→</i><span class="end">Swing Traders Elite</span></div>
  </section>

  <section aria-label="Courses">
    <h2>Saare courses</h2>
    <p class="sec-lead">Har course ka price, access aur kya seekhenge. "Course details &amp; join" se seedha course page khulega.</p>
    <div class="clist">
{cards}    </div>
  </section>

  <section class="card bundle" aria-label="Complete Bundle">
    <div>
      <span class="pill green">Save ₹4,998</span>
      <h2 style="margin:8px 0 4px">Complete Bundle</h2>
      <p>Indian Gold Market + Forex/XAUUSD + Funded Account Mastery, teeno courses ek saath. Alag-alag lene par ₹14,997.</p>
    </div>
    <div class="price">₹9,999</div>
  </section>

  <section aria-label="FAQ">
    <h2>Courses se jude sawal</h2>
    <p class="sec-lead">Jo sawal sabse zyada poochhe jaate hain.</p>
{faq_html}  </section>

{WA_BOX("Kaunsa course lun?", "Apna level aur market batayein, hum sahi course suggest karenge.", "Namaste%20Kavi%20Sir%2C%20mujhe%20course%20chunne%20mein%20madad%20chahiye.")}
'''
page(f'{ROOT}/courses/index.html', 'Learning Courses · Explosive Trades',
     'Explosive Trades ke saare trading courses: Trading Ka ABCD, Indian Gold, Forex/XAUUSD, Funded Account Mastery aur XAUUSD Swing Traders Elite, FAQ ke saath.',
     'courses', courses_css, courses_body)

# ======================= PROP FIRMS =======================
prop_css = '''
.firms{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:16px; }
@media (max-width:900px){ .firms{ grid-template-columns:1fr; } }
.firm{ display:flex; flex-direction:column; gap:12px; }
.firm h3{ margin:0; font-size:20px; }
.firm .why{ margin:0; color:var(--muted); font-size:14px; }
.firm dl{ margin:0; display:grid; grid-template-columns:auto 1fr; gap:6px 12px; font-size:13.5px; }
.firm dt{ color:var(--muted); }
.firm dd{ margin:0; font-weight:600; font-variant-numeric:tabular-nums; }
.code{ display:flex; align-items:center; justify-content:space-between; gap:10px; padding:10px 12px; border:1px dashed var(--gold); border-radius:10px; background:var(--panel2); }
.code span{ font-size:12px; color:var(--muted); }
.code b{ font-family:ui-monospace, Menlo, monospace; font-size:15px; color:var(--gold); letter-spacing:.04em; }
.code button{ background:none; border:1px solid var(--line); color:var(--text); border-radius:7px; padding:4px 10px; font:500 12px var(--body); cursor:pointer; }
.firm .btn{ margin-top:auto; }
.checks{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }
@media (max-width:760px){ .checks{ grid-template-columns:1fr; } }
.checks ul{ margin:0; padding-left:18px; display:grid; gap:6px; font-size:14px; }
.checks h3{ margin:0 0 10px; font-size:16px; }
.checks .bad h3{ color:var(--red); } .checks .good h3{ color:var(--green); }
.note{ font-size:12.5px; color:var(--muted); margin:10px 0 0; }
.toast{ position:fixed; bottom:18px; left:50%; transform:translateX(-50%); background:var(--gold); color:var(--on-gold); font-weight:600; padding:8px 16px; border-radius:20px; font-size:13px; opacity:0; transition:opacity .2s; pointer-events:none; }
.toast.show{ opacity:1; }
'''
def firm(name, why, rows, code_label, code, url, btn):
    dl = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k,v in rows)
    codebox = f'<div class="code"><div><span>{code_label}</span><br><b>{code}</b></div><button type="button" data-copy="{code}">Copy</button></div>' if code else ''
    return f'''      <article class="card firm">
        <h3>{name}</h3>
        <p class="why">{why}</p>
        <dl>{dl}</dl>
        {codebox}
        <a class="btn line" href="{url}" target="_blank" rel="noopener sponsored">{btn}</a>
      </article>
'''
firms_html = ''.join([
  firm('FundingPips', 'Kavi ka main prop firm. MT5 par 2-Step challenge, aur alag-alag payout options.',
       [('Phase 1 target','8%'),('Phase 2 target','5%'),('Daily loss','5%'),('Max loss','10% (static)'),('Profit split','60% se 100%, payout cycle ke hisaab se'),('Platform','MT5, cTrader, Match-Trader')],
       'Referral code', '0888028d', 'https://fundingpips.com', 'FundingPips website kholein'),
  firm('FundedElite', 'Kavi yahan bhi challenges trade karte hain. Lite plan mein target thoda zyada, daily loss thoda kam.',
       [('Phase 1 target','8% (Lite: 10%)'),('Phase 2 target','5%'),('Daily loss','5% (Lite: 4%)'),('Max loss','8%'),('Profit split','80%'),('Platform','MT5, TradeLocker')],
       'Affiliate code', 'AFF1265748', 'https://fundedelite.com', 'FundedElite website kholein'),
  firm('The5ers', 'Purani aur jaani-maani firm. Kavi isme High Stakes 2-Step account trade karte hain.',
       [('Phase 1 target','10%'),('Phase 2 target','5%'),('Daily loss','5%'),('Max loss','10%'),('Profit split','Up to 100%'),('Platform','MT5, cTrader, TradingView')],
       '', '', 'https://the5ers.com', 'The5ers website kholein'),
])
prop_body = f'''  <section aria-label="Intro">
    <p class="kicker">Best prop firms</p>
    <h1>Prop firms jahan <span>Kavi khud trade karte hain</span></h1>
    <p class="lead">Ye wahi firms hain jinke challenges aur funded accounts Kavi Sharma khud trade karte hain. Neeche har firm ke main rules ek nazar mein, taaki aap apne trading style ke hisaab se chun sakein.</p>
  </section>

  <section aria-label="Firms">
    <h2>3 firms, ek nazar mein</h2>
    <p class="sec-lead">2-Step challenge ke standard rules (Oct 2026 tak ki public jaankari). Kharidne se pehle firm ki website par latest rules zaroor check karein.</p>
    <div class="firms">
{firms_html}    </div>
    <p class="note">Disclosure: FundingPips aur FundedElite ke codes Explosive Trades ke affiliate codes hain. Inse kharidne par Explosive Trades ko commission mil sakta hai, aapki price par iska asar nahi padta. Rules aur prices firms kabhi bhi badal sakti hain.</p>
  </section>

  <section aria-label="Comparison">
    <h2>Side-by-side comparison</h2>
    <div class="tbl">
      <table>
        <thead><tr><th>Rule</th><th>FundingPips</th><th>FundedElite</th><th>The5ers (High Stakes)</th></tr></thead>
        <tbody>
          <tr><td>Phase 1 target</td><td class="num">8%</td><td class="num">8% · Lite 10%</td><td class="num">10%</td></tr>
          <tr><td>Phase 2 target</td><td class="num">5%</td><td class="num">5%</td><td class="num">5%</td></tr>
          <tr><td>Daily loss limit</td><td class="num">5%</td><td class="num">5% · Lite 4%</td><td class="num">5%</td></tr>
          <tr><td>Max loss</td><td class="num">10%</td><td class="num">8%</td><td class="num">10%</td></tr>
          <tr><td>Profit split</td><td>60–100% (payout cycle par)</td><td>80%</td><td>Up to 100%</td></tr>
          <tr><td>Platforms</td><td>MT5, cTrader, Match-Trader</td><td>MT5, TradeLocker</td><td>MT5, cTrader, TradingView</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <section aria-label="Checklist">
    <h2>Prop firm chunne se pehle</h2>
    <p class="sec-lead">Sirf sasta challenge dekh kar firm mat chuniye. Ye cheezein pehle check karein.</p>
    <div class="checks">
      <div class="card good"><h3>✓ Ye check karein</h3><ul>
        <li>Daily loss floating loss ke saath ginta hai ya sirf closed trades par</li>
        <li>Max loss static hai ya trailing</li>
        <li>Swing trading mein weekend aur overnight trade hold karne ki permission</li>
        <li>News trading rules aur consistency rule</li>
        <li>Payout kitne din mein aur kis tareeke se milta hai</li>
        <li>Aapka platform (MT5 ya cTrader) available hai ya nahi</li>
      </ul></div>
      <div class="card bad"><h3>✕ In cheezon se bachein</h3><ul>
        <li>"Instant funding" jaise plans jinke rules itne tight hon ki pass hona lagbhag mushkil ho</li>
        <li>Bina padhe challenge kharidna. Har firm ki Terms of Service padhein.</li>
        <li>VPN ya VPS ka galat use. Kai firms isse account band kar deti hain.</li>
        <li>Ek hi trade mein poora target lene ki koshish. Daily loss limit sabse jaldi wahi todta hai.</li>
      </ul></div>
    </div>
  </section>

  <section class="card contact" aria-label="Course">
    <div>
      <h2 style="margin-bottom:4px">Challenge pass karna seekhein</h2>
      <p>Funded Account Mastery course mein challenge rules, prop firm ke hisaab se risk management, drawdown handle karna aur scaling roadmap sikhaya gaya hai.</p>
    </div>
    <a class="btn gold" href="{C('692783')}" target="_blank" rel="noopener">Course dekhein</a>
  </section>

{WA_BOX("Kaunsi firm lun?", "Apna trading style aur budget batayein, sahi firm aur plan chunne mein madad milegi.", "Namaste%20Kavi%20Sir%2C%20mujhe%20prop%20firm%20chunne%20mein%20madad%20chahiye.")}
  <div class="toast" id="toast" role="status"></div>
  <script>
  document.addEventListener('click', function(e){{
    var b = e.target.closest('[data-copy]'); if (!b) return;
    var t = document.getElementById('toast'), v = b.getAttribute('data-copy');
    var done = function(m){{ t.textContent = m; t.classList.add('show'); setTimeout(function(){{ t.classList.remove('show'); }}, 1600); }};
    (navigator.clipboard ? navigator.clipboard.writeText(v) : Promise.reject()).then(function(){{ done('Code copy ho gaya: ' + v); }}, function(){{ done('Code: ' + v); }});
  }});
  </script>
'''
page(f'{ROOT}/prop-firms/index.html', 'Best Prop Firms · Explosive Trades',
     'FundingPips, FundedElite aur The5ers: prop firms jahan Kavi Sharma khud trade karte hain. Rules comparison, codes aur checklist.',
     'prop', prop_css, prop_body)

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
