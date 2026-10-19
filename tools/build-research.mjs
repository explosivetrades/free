#!/usr/bin/env node
// Explosive Trades · Members Research builder (v2: Google Sheet member login)
//
// Usage:
//   node tools/build-research.mjs <macFolderCopy> <repoRoot>
//
// <macFolderCopy> is a copy of the Mac folder "Members Research":
//   1_Daily Papers/        files to publish (any type)
//   _system/vault.json     private keys (never published)
//   _system/meta.json      optional { "<file name>": <mtimeMs> } for upload time
//
// Output (public, safe to publish):
//   <repoRoot>/research/data/index.json   file list, each file key wrapped with the master key
//   <repoRoot>/research/data/f/<id>.bin   AES-256-GCM encrypted files
// Updates <macFolderCopy>/_system/vault.json (copy it back to the Mac).
//
// Security model: every file has its own random key, wrapped with one master
// key. The master key is never published; the Google Apps Script member
// server (Sheet "Research Members") hands it only to members whose
// "Valid till" date has not passed. Members, trial sign-ups and expiry dates
// are managed in that Google Sheet.

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const [, , srcDir, repoRoot] = process.argv;
if (!srcDir || !repoRoot) { console.error('usage: build-research.mjs <macFolderCopy> <repoRoot>'); process.exit(1); }

const PAPERS = path.join(srcDir, '1_Daily Papers');
const SYS = path.join(srcDir, '_system');
const VAULT = path.join(SYS, 'vault.json');
const META = path.join(SYS, 'meta.json');
const OUT = path.join(repoRoot, 'research', 'data');
const OUT_F = path.join(OUT, 'f');

const b64 = (buf) => Buffer.from(buf).toString('base64');
const readJSON = (p, d) => { try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return d; } };

const vault = readJSON(VAULT, null);
if (!vault || !vault.master) { console.error('vault.json mein master key nahi mili. Builder band.'); process.exit(2); }
vault.files ||= {}; vault.wrap ||= {};
delete vault.slots; delete vault.salt;
const master = Buffer.from(vault.master, 'base64');
const meta = readJSON(META, {});

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
    for (const [k, f] of Object.entries(vault.files)) if (f.name === name) { delete vault.files[k]; delete vault.wrap[k]; }
    vault.files[id] = rec;
  }
  seen.add(rec.id);
  list.push(rec);
}
for (const id of Object.keys(vault.files)) if (!seen.has(id)) { delete vault.files[id]; delete vault.wrap[id]; }
for (const id of Object.keys(vault.wrap)) if (!seen.has(id)) delete vault.wrap[id];
for (const f of fs.readdirSync(OUT_F)) if (f.endsWith('.bin') && !seen.has(f.slice(0, -4))) fs.unlinkSync(path.join(OUT_F, f));

const out = { v: 2, built: new Date().toISOString(), files: [] };
for (const rec of list.sort((a, b) => b.time.localeCompare(a.time))) {
  let w = vault.wrap[rec.id];
  if (!w) {
    const iv = crypto.randomBytes(12);
    const c = crypto.createCipheriv('aes-256-gcm', master, iv);
    const ct = Buffer.concat([c.update(Buffer.from(rec.key, 'base64')), c.final(), c.getAuthTag()]);
    w = vault.wrap[rec.id] = { iv: b64(iv), k: b64(ct) };
  }
  out.files.push({ id: rec.id, name: rec.name, size: rec.size, time: rec.time, iv: rec.iv, w });
}

const idxPath = path.join(OUT, 'index.json');
const prev = readJSON(idxPath, null);
if (prev) { const a = { ...prev, built: '' }, b = { ...out, built: '' }; if (JSON.stringify(a) === JSON.stringify(b)) out.built = prev.built; }
fs.writeFileSync(idxPath, JSON.stringify(out, null, 1));
fs.mkdirSync(SYS, { recursive: true });
fs.writeFileSync(VAULT, JSON.stringify(vault, null, 1));

console.log(JSON.stringify({ files: list.map(f => `${f.name} (${f.time})`) }, null, 2));
