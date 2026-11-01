// DOM-level test of the report page (needs jsdom: npm install jsdom, or set NODE_PATH).
// Usage: node dom_test.js <report.html>
// Exits 0 on success, 77 when jsdom is not installed (treated as a skip), 1 on failure.
let JSDOM;
try { ({ JSDOM } = require('jsdom')); } catch (e) { console.log('SKIP: jsdom not installed'); process.exit(77); }
const fs = require('fs');
const html = '<!doctype html><html><head></head><body>' + fs.readFileSync(process.argv[2], 'utf8') + '</body></html>';
const dom = new JSDOM(html, { runScripts: 'dangerously', pretendToBeVisual: true });
const w = dom.window, d = w.document;
let failed = 0;
function ok(cond, msg) { if (!cond) { failed++; console.log('FAIL', msg); } else { console.log('ok  ', msg); } }
function fire(el, type) { el.dispatchEvent(new w.Event(type, { bubbles: true })); }

setTimeout(() => {
  const share = d.getElementById('share'), cov = d.getElementById('cov');
  ok(share.hidden && cov.hidden, 'panels start closed');

  d.getElementById('open-cov').click();
  ok(!cov.hidden, 'coverage panel opens');
  d.dispatchEvent(new w.KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
  ok(cov.hidden, 'Escape closes the coverage panel');

  d.getElementById('open-share').click();
  ok(!share.hidden, 'share panel opens');
  const areas = [...d.querySelectorAll('#passages textarea')];
  ok(areas.length >= 2, 'passages are listed (' + areas.length + ')');
  const dataEl = JSON.parse(d.getElementById('rr-data').textContent);
  const names = dataEl.redactions.people.map(p => p.name).concat(dataEl.redactions.terms.map(t => t.term));
  ok(areas.every(a => names.every(n => !a.value.toLowerCase().includes(n.toLowerCase()))), 'no names or company terms in default share text');

  // edit a passage to include a name and a company term, with redaction switched off then on
  const first = areas[0];
  d.getElementById('opt-names').checked = false; fire(d.getElementById('opt-names'), 'change');
  first.value = 'Priya Shah moved Acme Ledger.'; fire(first, 'input');
  ok(d.getElementById('copy-src').value.includes('Priya Shah'), 'with names allowed, the edit shows in the preview text');
  d.getElementById('opt-names').checked = true; fire(d.getElementById('opt-names'), 'change');
  d.getElementById('opt-company').checked = true; fire(d.getElementById('opt-company'), 'change');
  ok(!first.value.includes('Priya') && !first.value.includes('Acme Ledger'), 'switching redaction on rewrites an edited passage');

  // exclude a passage
  const before = d.getElementById('copy-src').value;
  const cb = d.querySelectorAll('#passages input[type=checkbox]')[1];
  cb.checked = false; fire(cb, 'change');
  ok(d.getElementById('copy-src').value.length < before.length, 'unticking a passage removes it from the share text');

  // leak warning
  first.value = 'See https://example.com'; fire(first, 'input');
  ok(!d.getElementById('leak').hidden, 'a link in the text raises the warning');
  first.value = 'Fine.'; fire(first, 'input');
  ok(d.getElementById('leak').hidden, 'the warning clears when the link is gone');

  // evidence is not in the share preview
  const card = d.getElementById('card').textContent;
  ok(!/How Chef knows|Directly observed|Slack:/i.test(card), 'share preview carries no evidence');
  ok(!d.querySelector('#card svg'), 'share preview has no mascot illustration');

  // LinkedIn: gated by the review box, opens the composer with the share-safe text only
  const li = d.getElementById('li-btn'), rev = d.getElementById('review-ok');
  ok(li.getAttribute('aria-disabled') === 'true', 'LinkedIn button starts disabled until the preview is confirmed');
  let prevented = false;
  const ev = new w.MouseEvent('click', { bubbles: true, cancelable: true });
  li.addEventListener('click', e => { prevented = e.defaultPrevented || prevented; }, true);
  li.dispatchEvent(ev);
  ok(ev.defaultPrevented, 'clicking before confirming does not open LinkedIn');
  rev.checked = true; fire(rev, 'change');
  ok(li.getAttribute('aria-disabled') === 'false', 'confirming enables LinkedIn');
  const href = li.getAttribute('href');
  ok(/^https:\/\/www\.linkedin\.com\/feed\/\?shareActive=true&text=/.test(href), 'LinkedIn link opens the post composer');
  const sent = decodeURIComponent(href.split('text=')[1]);
  ok(sent.includes('#SundayRoast') && sent.includes('sundayroast.me'), 'LinkedIn text carries the tag and the site');
  ok(!/Priya|Acme Ledger|example\.com|How Chef knows/.test(sent), 'LinkedIn text has no names, company terms, links or evidence');
  ok(li.getAttribute('target') === '_blank' && /noopener/.test(li.getAttribute('rel')), 'LinkedIn opens in a new tab safely');
  first.value = 'Edited line for LinkedIn.'; fire(first, 'input');
  ok(decodeURIComponent(li.getAttribute('href').split('text=')[1]).includes('Edited line for LinkedIn.'), 'editing a passage updates the LinkedIn text');
  ok(d.getElementById('img-copy') && d.getElementById('img-btn') && d.getElementById('copy-btn'), 'copy text, make image and copy image controls exist');

  // private page features
  ok(d.querySelectorAll('details.how').length >= 3, 'evidence disclosures are present');
  ok(![...d.querySelectorAll('details.how')].some(x => x.open), 'disclosures are collapsed by default');
  ok(!/Not on the menu/i.test(d.body.textContent), 'no Not on the menu section');

  console.log(failed ? failed + ' failure(s)' : 'all DOM checks passed');
  process.exit(failed ? 1 : 0);
}, 150);
