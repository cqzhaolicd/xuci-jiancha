// 校验 english26q_read1_interactive.html 三数组结构
const fs = require('fs'), vm = require('vm');
const f = 'english26q_read1_interactive.html';
const h = fs.readFileSync(f, 'utf8');

function grab(decl) {
  const i = h.indexOf(decl);
  if (i < 0) throw new Error('decl not found: ' + decl);
  const j = h.indexOf('];', i + decl.length);
  let t = h.slice(i + decl.length, j).trim();
  if (t.startsWith('[')) t = t.slice(1);          // 防御双层
  return '([' + t + '])';
}
const qs = vm.runInNewContext(grab('const questions = ['));
const fc = vm.runInNewContext(grab('const flashcards = ['));
const er = vm.runInNewContext(grab('errors = ['));

console.log('questions:', qs.length, '| flashcards:', fc.length, '| errors:', er.length);
let bad = 0;
const dist = [0, 0, 0, 0];
qs.forEach((q, i) => {
  if (!q.q || !Array.isArray(q.opts)) { console.log(`  Q${i + 1} 结构异常`); bad++; return; }
  if (q.opts.length !== 4) { console.log(`  Q${i + 1} opts=${q.opts.length} 非4项`); bad++; }
  if (!(q.ans >= 0 && q.ans < q.opts.length)) { console.log(`  Q${i + 1} ans=${q.ans} 越界`); bad++; }
  else dist[q.ans]++;
  const stripped = q.opts.map(o => o.replace(/^[A-D][.、]\s*/, ''));
  if (new Set(stripped).size !== stripped.length) { console.log(`  Q${i + 1} 选项重复`); bad++; }
  if (!q.exp) { console.log(`  Q${i + 1} 缺 exp`); bad++; }
});
fc.forEach((c, i) => { if (!c.front || !c.back) { console.log(`  卡${i + 1} 缺 front/back`); bad++; } });
er.forEach((e, i) => { if (!e.title || !e.wrong || !e.right) { console.log(`  错${i + 1} 缺字段`); bad++; } });
console.log('ans 分布:', dist.join('/'), '| 最高占比:', (Math.max(...dist) / qs.length * 100).toFixed(0) + '%');
console.log('正确选项原文示例:', qs[0].opts[qs[0].ans]);
console.log(bad === 0 ? '✅ 结构全部合规' : `❌ ${bad} 项问题`);
