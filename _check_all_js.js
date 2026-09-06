#!/usr/bin/env node
// Validate all interactive html JS blocks
const fs = require('fs');
const files = fs.readdirSync('.').filter(f => f.endsWith('.html') && !f.startsWith('index'));
let bad = [], totalScripts = 0, okFiles = 0;
for (const fn of files) {
  const html = fs.readFileSync(fn, 'utf8');
  const re = /<script[^>]*>([\s\S]*?)<\/script>/g;
  let m, fok = true, cnt = 0;
  while ((m = re.exec(html))) {
    cnt++;
    try { new Function(m[1]); } catch (e) { fok = false; bad.push(fn + ' :: ' + e.message); }
  }
  totalScripts += cnt;
  if (fok && cnt > 0) okFiles++;
}
console.log(`files=${files.length} okFiles=${okFiles} scripts=${totalScripts} bad=${bad.length}`);
if (bad.length) { console.log(bad.slice(0, 20).join('\n')); process.exit(1); }
