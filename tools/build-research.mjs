#!/usr/bin/env node
// Explosive Trades · Members Research builder
//
// Usage:
//   node tools/build-research.mjs <macFolderCopy> <repoRoot>
//
// <macFolderCopy> is a copy of the Mac folder "Members Research":
//   1_Daily Papers/        files to publish (any type)
//   2_Clients.csv          name,password,expiry(YYYY-MM-DD),notes
//   _system/vault.json     private keys (never published), created if missing
//   _system/meta.json      optional { "<file name>": <mtimeMs> } for upload time
//
// Output (public, safe to publish):
//   <repoRoot>/research/data/index.json   file list + per-client wrapped keys
//   <repoRoot>/research/data/f/<id>.bin   AES-256-GCM encrypted files
// Updates <macFolderCopy>/_system/vault.json (copy it back to the Mac).
//
// Security model: every file has its own random key. That key is wrapped
// separately for each client whose expiry date has not passed, using a key
// derived from that client's password (PBKDF2-SHA256). Expired clients get
// no wrapped keys, so they cannot open any file after the next build.

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const [, , srcDir, repoRoot] = process.argv;
if (!srcDir || !repoRoot) { console.error('usage: build-research.mjs <macFolderCopy> <repoRoot>'); process.exit(1); }

const PAPERS = path.join(srcDir, '1_Daily Papers');
const CLIENTS = path.join(srcDir, '2_Clients.csv');
const SYS = path.join(srcDir, '_system');
const VAULT = path.join(SYS, 'vault.json');
const META = path.join(SYS, 'meta.json');
const OUT = path.join(repoRoot, 'research', 'data');
const OUT_F = path.join(OUT, 'f');
const ITER = 210000;

const b64 = (buf) => Buffer.from(buf).toString('base64');
const readJSON = (p, d) => { try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return d; } };

// Today in India (YYYY-MM-DD)
const todayIST = new Date(Date.now() + 5.5 * 3600e3).toISOString().slice(0, 10);

// ---------- vault ----------
const vault = readJSON(VAULT, null) || { v: 1, salt: b64(crypto.randomBytes(16)), files: {}, slots: {} };
vault.files ||= {}; vault.slots ||= {};
const salt = Buffer.from(vault.salt, 'base64');
const meta = readJSON(META, {});

// ---------- clients ----------
function parseCSV(text) {
  const rows = []; let row = [], cell = '', q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"' && text[i + 1] === '"') { cell += '"'; i++; } else if (c === '"') q = false; else cell += c; }
    else if (c === '"') q = true;
    else if (c === ',' || c === ';' || c === '\t') { row.push(cell); cell = ''; }
    else if (c === '\n' || c === '\r') { if (c === '\r' && text[i + 1] === '\n') i++; row.push(cell); rows.push(row); row = []; cell = ''; }
    else cell += c;
  }
  if (cell !== '' || row.length) { row.push(cell); rows.push(row); }
  return rows.map(r => r.map(x => x.trim())).filter(r => r.some(Boolean));
}
function normDate(s) {
  s = (s || '').trim();
  let m = s.match(/^(\d{4})-(\d{1,2})-(\d{1,2})$/);
  if (m) return `${m[1]}-${m[2].padStart(2, '0')}-${m[3].padStart(2, '0')}`;
  m = s.match(/^(\d{1,2})[\/.\-](\d{1,2})[\/.\-](\d{4})$/); // DD/MM/YYYY (India)
  if (m) return `${m[3]}-${m[2].padStart(2, '0')}-${m[1].padStart(2, '0')}`;
  return null;
}
const derived = new Map();
function derive(pw) {
  if (!derived.has(pw)) {
    const bits = crypto.pbkdf2Sync(pw, salt, ITER, 64, 'sha256');
    derived.set(pw, { key: bits.subarray(0, 32), id: bits.subarray(32, 48).toString('hex') });
  }
  return derived.get(pw);
}

const rows = fs.existsSync(CLIENTS) ? parseCSV(fs.readFileSync(CLIENTS, 'utf8').replace(/^﻿/, '')) : [];
const header = (rows[0] || []).map(h => h.toLowerCase());
const iName = header.findIndex(h => h.startsWith('name'));
const iPw = header.findIndex(h => h.startsWith('pass'));
const iExp = header.findIndex(h => h.startsWith('exp') || h.includes('valid'));
const clients = []; const problems = [];
rows.slice(1).forEach((r, n) => {
  const name = r[iName] || `Row ${n + 2}`, pw = r[iPw] || '', exp = normDate(r[iExp]);
  if (!pw) return;
  if (pw.length < 8) { problems.push(`${name}: password 8 characters se chhota hai, skip kiya`); return; }
  if (!exp) { problems.push(`${name}: expiry date samajh nahi aayi ("${r[iExp] || ''}"), skip kiya`); return; }
  clients.push({ name, pw, exp, active: exp >= todayIST });
});
const active = clients.filter(c => c.active);

// ---------- files ----------
fs.mkdirSync(OUT_F, { recursive: true });
const names = fs.existsSync(PAPERS) ? fs.readdirSync(PAPERS).filter(f => !f.startsWith('.') && fs.statSync(path.join(PAPERS, f)).isFile()) : [];
const seen = new Set();
const list = [];
for (const name of names) {
  const full = path.join(PAPERS, name);
  const data = fs.readFileSync(full);
  const hash = crypto.createHash('sha256').update(data).digest('hex');
  let rec = Object.values(vault.files).find(f => f.name === name && f.hash === hash);
  if (!rec) {
    const id = crypto.randomBytes(9).toString('base64url');
    const key = crypto.randomBytes(32), iv = crypto.randomBytes(12);
    const c = crypto.createCipheriv('aes-256-gcm', key, iv);
    const ct = Buffer.concat([c.update(data), c.final(), c.getAuthTag()]);
    fs.writeFileSync(path.join(OUT_F, id + '.bin'), ct);
    const mt = Number(meta[name]) || fs.statSync(full).mtimeMs || Date.now();
    rec = { id, name, hash, size: data.length, key: b64(key), iv: b64(iv), time: new Date(mt).toISOString() };
    // a replaced file (same name, new content) drops the old version
    for (const [k, f] of Object.entries(vault.files)) if (f.name === name) { delete vault.files[k]; delete vault.slots[k]; }
    vault.files[id] = rec;
  }
  seen.add(rec.id);
  list.push(rec);
}
// files removed from the Mac folder are removed from the site
for (const id of Object.keys(vault.files)) if (!seen.has(id)) { delete vault.files[id]; delete vault.slots[id]; }
for (const f of fs.readdirSync(OUT_F)) if (f.endsWith('.bin') && !seen.has(f.slice(0, -4))) fs.unlinkSync(path.join(OUT_F, f));

// ---------- wrap keys for active clients ----------
const out = { v: 1, salt: vault.salt, iter: ITER, built: new Date().toISOString(), clients: {}, files: [] };
for (const c of active) out.clients[derive(c.pw).id] = { exp: c.exp };
for (const rec of list.sort((a, b) => b.time.localeCompare(a.time))) {
  vault.slots[rec.id] ||= {};
  const slots = {};
  for (const c of active) {
    const { key, id } = derive(c.pw);
    let s = vault.slots[rec.id][id];
    if (!s) {
      const iv = crypto.randomBytes(12);
      const w = crypto.createCipheriv('aes-256-gcm', key, iv);
      const ct = Buffer.concat([w.update(Buffer.from(rec.key, 'base64')), w.final(), w.getAuthTag()]);
      s = vault.slots[rec.id][id] = { iv: b64(iv), k: b64(ct) };
    }
    slots[id] = s;
  }
  // forget slots of clients who are no longer active
  for (const id of Object.keys(vault.slots[rec.id])) if (!slots[id]) delete vault.slots[rec.id][id];
  out.files.push({ id: rec.id, name: rec.name, size: rec.size, time: rec.time, iv: rec.iv, slots });
}

// keep "built" stable when nothing else changed, so no empty commits
const idxPath = path.join(OUT, 'index.json');
const prev = readJSON(idxPath, null);
if (prev) { const a = { ...prev, built: '' }, b = { ...out, built: '' }; if (JSON.stringify(a) === JSON.stringify(b)) out.built = prev.built; }
fs.writeFileSync(idxPath, JSON.stringify(out, null, 1));
fs.mkdirSync(SYS, { recursive: true });
fs.writeFileSync(VAULT, JSON.stringify(vault, null, 1));

// ---------- private clients dashboard (Mac only, never published) ----------
const tpl = path.join(path.dirname(new URL(import.meta.url).pathname), 'clients-dashboard.html');
if (fs.existsSync(tpl)) {
  const iNote = header.findIndex(h => h.startsWith('note'));
  const all = rows.slice(1).map(r => ({ name: r[iName] || '', pw: r[iPw] || '', exp: normDate(r[iExp]) || (r[iExp] || ''), note: iNote >= 0 ? (r[iNote] || '') : '' })).filter(c => c.name || c.pw);
  const data = JSON.stringify({ built: new Date().toISOString(), papers: list.length, lastPaper: list[0] ? list[0].time : null, clients: all }).replace(/</g, '\\u003c');
  fs.writeFileSync(path.join(srcDir, '4_Clients Dashboard.html'), fs.readFileSync(tpl, 'utf8').replace('/*__DATA__*/null', data));
}

console.log(JSON.stringify({
  today: todayIST,
  files: list.map(f => f.name),
  activeClients: active.map(c => `${c.name} (till ${c.exp})`),
  expiredClients: clients.filter(c => !c.active).map(c => `${c.name} (expired ${c.exp})`),
  problems
}, null, 2));
