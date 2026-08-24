const fs = require('fs');
const path = require('path');

const files = [];
for (let i = 1; i <= 10; i++) files.push(`/home/administrator/xuci-jiancha/english8_u${i}_interactive.html`);

let allOk = true;

for (const f of files) {
  const html = fs.readFileSync(f, 'utf8');
  const errs = [];

  // 1. JS syntax check on every <script> block
  const scriptRe = /<script>([\s\S]*?)<\/script>/g;
  let m, nScripts = 0;
  while ((m = scriptRe.exec(html)) !== null) {
    nScripts++;
    try { new Function(m[1]); } catch (e) { errs.push('JS SYNTAX: ' + e.message); }
  }
  if (nScripts < 2) errs.push('expected >=2 script blocks, got ' + nScripts);

  // 2. div balance
  const open = (html.match(/<div[\s>]/g) || []).length;
  const close = (html.match(/<\/div>/g) || []).length;
  if (open !== close) errs.push(`DIV imbalance: ${open} open vs ${close} close`);

  // 3. questions array integrity
  let arr = null;
  const qs = html.indexOf('const questions=[');
  const qe = html.indexOf('const flashcards=', qs);
  if (qs < 0 || qe < 0) { errs.push('questions array markers missing'); }
  else {
    arr = eval(html.slice(qs + 'const questions='.length, qe).trim());
    if (arr.length !== 8) errs.push('questions count = ' + arr.length);
    arr.forEach((q, i) => {
      if (!q.q || !Array.isArray(q.opts) || q.opts.length !== 4) errs.push(`Q${i + 1}: opts not 4`);
      if (!(Number.isInteger(q.ans) && q.ans >= 0 && q.ans <= 3)) errs.push(`Q${i + 1}: bad ans ${q.ans}`);
      if (!q.exp) errs.push(`Q${i + 1}: missing exp`);
    });
  }

  // 4. flashcards + errors arrays parse
  const fs2 = html.indexOf('const flashcards=[');
  const fe = html.indexOf('const errors=', fs2);
  const fl = eval(html.slice(fs2 + 'const flashcards='.length, fe).trim());
  if (fl.length < 8) errs.push('flashcards count = ' + fl.length);
  const es = html.indexOf('const errors=[');
  const ee = html.indexOf('let curQ=0', es);
  const er = eval(html.slice(es + 'const errors='.length, ee).trim());
  if (er.length < 4) errs.push('errors count = ' + er.length);

  // 5. theme + title + key replaced
  if (!html.includes('--primary:#2980b9')) errs.push('theme color not replaced');
  if (html.includes('--primary:#e74c3c')) errs.push('old red theme var still present');
  if (!html.includes('quiz_progress_english8_u')) errs.push('progress key not replaced');
  if (html.includes('勾股定理')) errs.push('old template subject still present');

  const status = errs.length === 0 ? 'PASS' : 'FAIL';
  if (errs.length) allOk = false;
  console.log(`${status} ${path.basename(f)} | scripts=${nScripts} div=${open}/${close} q=${arr ? arr.length : '?'} fc=${fl.length} er=${er.length}`);
  errs.forEach(e => console.log('   - ' + e));
}

console.log(allOk ? '\nALL FILES VALID' : '\nVALIDATION FAILED');
process.exit(allOk ? 0 : 1);
