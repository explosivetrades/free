"""Google Analytics (GA4) for the Explosive Trades site.

Hatana ho to: GA_ID = '' karke  `python3 tools/site/analytics.py`  aur  `python3 tools/site/new_pages.py`  chalayein.
"""
import re, os

GA_ID = 'G-G7X02GX0MT'
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Click events (sirf link ka naam aur domain/path jaata hai, kisi ka naam ya number nahi)
_EVENTS_JS = r"""
document.addEventListener('click',function(e){
  var a=e.target&&e.target.closest?e.target.closest('a'):null; if(!a||!a.href) return;
  var h=a.href, u=h.split('?')[0], t=(a.textContent||'').replace(/\s+/g,' ').trim().slice(0,80), ev=null;
  if(/wa\.me|whatsapp\.com/i.test(h)) ev='whatsapp_click';
  else if(/fundingpips|fundedelite|the5ers/i.test(h)) ev='prop_firm_click';
  else if(/explosivetrades\.com|clplily\.page\.link/i.test(h)) ev='program_click';
  else if(/youtube\.com|youtu\.be/i.test(h)) ev='youtube_click';
  else if(/t\.me\//i.test(h)) ev='telegram_click';
  else if(a.hasAttribute('download')||/\/downloads\//.test(h)) ev='tool_download';
  if(ev) gtag('event',ev,{link_text:t,link_url:u.slice(0,100),page_name:document.title.slice(0,60)});
},true);
"""

def snippet():
    if not GA_ID: return ''
    return (f'<!-- ga:start -->\n<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>\n'
            f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag(\'js\',new Date());'
            f'gtag(\'config\',\'{GA_ID}\');{_EVENTS_JS}</script>\n<!-- ga:end -->\n')

def lead_js(interest_expr):
    """JS call for a submitted query form (only interest, no personal data)."""
    if not GA_ID: return ''
    return f"if(window.gtag)gtag('event','generate_lead',{{interest:{interest_expr}}});"

NOTE = '<span class="ga-note">Site visits ginne ke liye Google Analytics use hota hai. Aapka naam ya number isme nahi jaata.</span>'

def footer_note():
    return ('    ' + NOTE + '\n') if GA_ID else ''

def patch(path):
    s = open(path).read()
    s = re.sub(r'<!-- ga:start -->.*?<!-- ga:end -->\n', '', s, flags=re.S)
    if GA_ID:
        m = re.search(r'<meta charset=[^>]*>\n', s)
        at = m.end() if m else s.index('<head>\n') + 7
        s = s[:at] + snippet() + s[at:]
    s = re.sub(r'    <span class="ga-note">.*?</span>\n', '', s)
    if GA_ID:
        s = s.replace('  </footer>', footer_note() + '  </footer>', 1)
    open(path, 'w').write(s)

if __name__ == '__main__':
    for p in ('index.html', 'research/index.html'):
        patch(os.path.join(ROOT, p))
    print('analytics', 'on' if GA_ID else 'off')
