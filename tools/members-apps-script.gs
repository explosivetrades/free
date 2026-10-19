// Explosive Trades - Free tool leads + Members Research login
// Tab 1 (first tab): free tool leads.  Tab "Research Members": member accounts.

var HEADERS = ['Time', 'Name', 'WhatsApp', 'Tool', 'Page'];
var MEM = 'Research Members';
var MH = ['Joined', 'Name', 'WhatsApp', 'Plan', 'Valid till', 'Days left', 'Status', 'Last login', 'Notes', '_salt', '_hash'];
var TRIAL_DAYS = 45;
var TRIAL_PLAN = 'Free trial (45 din)';

function clean_(v) {
  v = String(v || '').slice(0, 200);
  return /^[=+\-@]/.test(v) ? "'" + v : v;
}

function doPost(e) {
  var body = null;
  try {
    var raw = e && e.postData && e.postData.contents;
    if (raw && raw.charAt(0) === '{') body = JSON.parse(raw);
  } catch (x) {}
  if (body && body.action) return json_(member_(body));
  return lead_(e);
}

function doGet() {
  return ContentService.createTextOutput('Explosive Trades endpoint is running.');
}

function lead_(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var sh = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
    if (sh.getRange(1, 1).getValue() !== 'Time') {
      sh.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]).setFontWeight('bold');
      sh.setFrozenRows(1);
    }
    var p = (e && e.parameter) || {};
    sh.appendRow([new Date(), clean_(p.name), clean_(p.phone), clean_(p.tool), clean_(p.page)]);
    return ContentService.createTextOutput('ok');
  } finally {
    lock.releaseLock();
  }
}

// ---------------- Members ----------------
function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
function phone_(v) {
  var d = String(v || '').replace(/\D/g, '');
  if (d.length === 12 && d.indexOf('91') === 0) d = d.slice(2);
  if (d.length === 11 && d.charAt(0) === '0') d = d.slice(1);
  return d;
}
function hash_(pw, salt) {
  var s = Utilities.newBlob(salt).getBytes();
  var b = Utilities.newBlob(salt + '|' + pw).getBytes();
  for (var i = 0; i < 800; i++) b = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, b.concat(s));
  return Utilities.base64Encode(b);
}
function token_(phone) {
  var secret = PropertiesService.getScriptProperties().getProperty('SECRET');
  return Utilities.base64EncodeWebSafe(Utilities.computeHmacSha256Signature(phone, secret));
}
function ymd_(d) {
  return Utilities.formatDate(d, 'Asia/Kolkata', 'yyyy-MM-dd');
}
function memSheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(MEM);
  if (!sh) {
    sh = ss.insertSheet(MEM);
    sh.getRange(1, 1, 1, MH.length).setValues([MH]).setFontWeight('bold');
    sh.setFrozenRows(1);
    sh.getRange('C:C').setNumberFormat('@');
    sh.getRange('A:A').setNumberFormat('dd mmm yyyy');
    sh.getRange('E:E').setNumberFormat('dd mmm yyyy');
    sh.getRange('H:H').setNumberFormat('dd mmm yyyy, h:mm am/pm');
    sh.hideColumns(10, 2);
    var g = sh.getRange('G2:G1000');
    sh.setConditionalFormatRules([
      SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo('Active').setBackground('#d9f2e1').setFontColor('#1e6b3a').setRanges([g]).build(),
      SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo('Expiring').setBackground('#fde5cf').setFontColor('#9a4a12').setRanges([g]).build(),
      SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo('Expired').setBackground('#f8d7d8').setFontColor('#9b1c20').setRanges([g]).build()
    ]);
  }
  return sh;
}
function rowFormulas_(sh, r) {
  sh.getRange(r, 6).setFormula('=IF(E' + r + '="","",INT(E' + r + ')-TODAY())').setNumberFormat('0');
  sh.getRange(r, 7).setFormula('=IF(E' + r + '="","",IF(INT(E' + r + ')<TODAY(),"Expired",IF(INT(E' + r + ')-TODAY()<=7,"Expiring","Active")))');
  sh.getRange(r, 1).setNumberFormat('dd mmm yyyy');
  sh.getRange(r, 5).setNumberFormat('dd mmm yyyy');
  sh.getRange(r, 8).setNumberFormat('dd mmm yyyy, h:mm am/pm');
}
function dateOnly_(d) {
  return new Date(Utilities.formatDate(d, 'Asia/Kolkata', 'yyyy-MM-dd') + 'T00:00:00+05:30');
}
// Run once to tidy existing rows (formats + formulas)
function fixFormats() {
  var sh = memSheet_();
  for (var r = 2; r <= sh.getLastRow(); r++) {
    var e = sh.getRange(r, 5).getValue();
    if (e instanceof Date) sh.getRange(r, 5).setValue(dateOnly_(e));
    rowFormulas_(sh, r);
  }
  sh.autoResizeColumns(1, 9);
}
function findRow_(sh, phone) {
  var n = sh.getLastRow();
  if (n < 2) return 0;
  var vals = sh.getRange(2, 3, n - 1, 1).getValues();
  for (var i = 0; i < vals.length; i++) if (phone_(vals[i][0]) === phone) return i + 2;
  return 0;
}
function grant_(sh, r, phone) {
  var v = sh.getRange(r, 1, 1, 9).getValues()[0];
  var exp = v[4] instanceof Date ? ymd_(v[4]) : String(v[4] || '');
  if (!exp || exp < ymd_(new Date())) return { ok: false, code: 'expired', name: v[1], exp: exp };
  return { ok: true, name: v[1], plan: v[3], exp: exp, token: token_(phone),
           key: PropertiesService.getScriptProperties().getProperty('MASTER_KEY') };
}
function member_(b) {
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var sh = memSheet_();
    var phone = phone_(b.phone);
    if (!/^\d{10,13}$/.test(phone)) return { ok: false, code: 'phone' };
    var cache = CacheService.getScriptCache();
    var fails = Number(cache.get('f' + phone) || 0);
    if (fails >= 8) return { ok: false, code: 'locked' };
    var r = findRow_(sh, phone);
    var pw = String(b.password || '');

    if (b.action === 'signup') {
      var name = String(b.name || '').trim().slice(0, 60);
      if (name.length < 2) return { ok: false, code: 'name' };
      if (pw.length < 6) return { ok: false, code: 'short' };
      if (r) return { ok: false, code: 'exists' };
      var salt = Utilities.getUuid();
      var now = new Date();
      var exp = dateOnly_(new Date(now.getTime() + TRIAL_DAYS * 864e5));
      sh.appendRow([now, clean_(name), phone, TRIAL_PLAN, exp, '', '', now, 'Website signup', salt, hash_(pw, salt)]);
      r = sh.getLastRow();
      sh.getRange(r, 3).setNumberFormat('@').setValue(phone);
      rowFormulas_(sh, r);
      return grant_(sh, r, phone);
    }

    if (b.action === 'login') {
      if (!r) return { ok: false, code: 'nouser' };
      var saltC = sh.getRange(r, 10), hashC = sh.getRange(r, 11);
      if (!hashC.getValue()) {
        if (pw.length < 6) return { ok: false, code: 'short' };
        var s2 = Utilities.getUuid();
        saltC.setValue(s2); hashC.setValue(hash_(pw, s2));
      } else if (hash_(pw, String(saltC.getValue())) !== hashC.getValue()) {
        cache.put('f' + phone, String(fails + 1), 1800);
        return { ok: false, code: 'wrong' };
      }
      cache.remove('f' + phone);
      var g = grant_(sh, r, phone);
      if (g.ok) sh.getRange(r, 8).setValue(new Date());
      return g;
    }

    if (b.action === 'check') {
      if (!r || String(b.token || '') !== token_(phone)) return { ok: false, code: 'session' };
      return grant_(sh, r, phone);
    }
    return { ok: false, code: 'action' };
  } finally {
    lock.releaseLock();
  }
}

// One-time setup (run once from the editor, then this function can stay)
function setup() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.setSpreadsheetTimeZone('Asia/Kolkata');
  var props = PropertiesService.getScriptProperties();
  if (!props.getProperty('MASTER_KEY')) props.setProperty('MASTER_KEY', '__MASTER__');
  if (!props.getProperty('SECRET')) props.setProperty('SECRET', Utilities.getUuid() + Utilities.getUuid());
  var sh = memSheet_();
  if (!findRow_(sh, '9259595122')) {
    var salt = Utilities.getUuid();
    var exp = new Date('2026-11-19T00:00:00+05:30');
    sh.appendRow([new Date(), 'Ananya Choudhary', '9259595122', 'Paid', exp, '', '', '', '1 month - Oct 2026', salt, hash_('9259595122', salt)]);
    var r = sh.getLastRow();
    sh.getRange(r, 3).setNumberFormat('@').setValue('9259595122');
    rowFormulas_(sh, r);
  }
  Logger.log('Setup done');
}
