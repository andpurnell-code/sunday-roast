/* Sunday Roast share and panel behaviour. No network calls. Testable under node (see tests). */
(function (root) {
  'use strict';

  // Replace names with roles and company terms with generic phrases, longest first.
  function applyRedactions(text, red, names, company) {
    var pairs = [];
    if (names) {
      (red.people || []).forEach(function (p) {
        pairs.push([p.name, p.role]);
        var first = p.name.split(/\s+/)[0];
        if (first.length > 2) pairs.push([first, p.role]);
      });
    }
    if (company) (red.terms || []).forEach(function (t) { pairs.push([t.term, t.generic]); });
    pairs.sort(function (a, b) { return b[0].length - a[0].length; });
    pairs.forEach(function (pr) {
      if (!pr[0]) return;
      var esc = pr[0].replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      text = text.replace(new RegExp('(^|[^\\w])' + esc + '(?![\\w])', 'gi'), function (m, pre) { return pre + pr[1]; });
    });
    return text;
  }

  function wrapLines(ctx, text, maxWidth) {
    var out = [];
    String(text).split(/\n/).forEach(function (para) {
      var words = para.split(/\s+/), line = '';
      words.forEach(function (w) {
        var test = line ? line + ' ' + w : w;
        if (ctx.measureText(test).width > maxWidth && line) { out.push(line); line = w; } else { line = test; }
      });
      out.push(line);
    });
    return out;
  }

  function init(doc) {
    var dataEl = doc.getElementById('rr-data');
    if (!dataEl) return;
    var data = JSON.parse(dataEl.textContent);
    var $ = function (id) { return doc.getElementById(id); };
    var covPanel = $('cov'), shPanel = $('share');
    var lastFocus = null;

    function openPanel(p) { lastFocus = doc.activeElement; p.hidden = false; doc.body.classList.add('lock'); var f = p.querySelector('button,textarea,input'); if (f) f.focus(); }
    function closePanel(p) { p.hidden = true; if (covPanel.hidden && shPanel.hidden) doc.body.classList.remove('lock'); if (lastFocus && lastFocus.focus) lastFocus.focus(); }
    $('open-cov').addEventListener('click', function () { openPanel(covPanel); });
    doc.querySelectorAll('[data-open-share]').forEach(function (b) { b.addEventListener('click', function () { buildPassages(); openPanel(shPanel); }); });
    doc.querySelectorAll('[data-close]').forEach(function (b) { b.addEventListener('click', function () { closePanel(b.closest('.panel')); }); });
    doc.addEventListener('keydown', function (e) { if (e.key === 'Escape') { [covPanel, shPanel].forEach(function (p) { if (!p.hidden) closePanel(p); }); } });

    // ---- share state ----
    var passages = [];
    function currentOpts() { return { names: $('opt-names').checked, company: $('opt-company').checked }; }
    function buildPassages() {
      if (passages.length) { renderPreview(); return; }
      var o = currentOpts();
      var list = [];
      if (data.share.verdict.include) list.push({ id: 'verdict', title: 'Chef’s verdict', raw: data.share.verdict.text });
      data.share.sections.forEach(function (s) { if (s.include) list.push({ id: s.key + '-' + s.index, title: s.title, raw: s.text }); });
      var host = $('passages'); host.innerHTML = '';
      passages = list.map(function (p) {
        var wrap = doc.createElement('div'); wrap.className = 'passage';
        var head = doc.createElement('label'); head.className = 'ph';
        var cb = doc.createElement('input'); cb.type = 'checkbox'; cb.checked = true; cb.id = 'inc-' + p.id;
        head.appendChild(cb); head.appendChild(doc.createTextNode(' ' + p.title));
        var ta = doc.createElement('textarea'); ta.id = 'txt-' + p.id; ta.rows = 3;
        ta.value = applyRedactions(p.raw, data.redactions, o.names, o.company);
        ta.setAttribute('aria-label', 'Edit ' + p.title);
        wrap.appendChild(head); wrap.appendChild(ta); host.appendChild(wrap);
        var st = { id: p.id, title: p.title, raw: p.raw, cb: cb, ta: ta, edited: false };
        ta.addEventListener('input', function () { st.edited = true; renderPreview(); });
        cb.addEventListener('change', renderPreview);
        return st;
      });
      renderPreview();
    }
    function reapply() {
      var o = currentOpts();
      passages.forEach(function (p) {
        p.ta.value = p.edited ? applyRedactions(p.ta.value, data.redactions, o.names, o.company)
                              : applyRedactions(p.raw, data.redactions, o.names, o.company);
      });
      renderPreview();
    }
    $('opt-names').addEventListener('change', reapply);
    $('opt-company').addEventListener('change', reapply);

    function included() { return passages.filter(function (p) { return p.cb.checked && p.ta.value.trim(); }); }
    function bodyText() {
      return included().map(function (p) { return (p.id === 'verdict' ? '' : p.title + '\n') + p.ta.value.trim(); }).join('\n\n');
    }
    function shareText() { return bodyText() + '\n\n' + data.tagline + '  sundayroast.me'; }
    function linkedInText() { return bodyText() + '\n\nMy week, roasted by a chicken. Get yours at sundayroast.me\n\n#SundayRoast'; }
    function linkedInUrl() { return 'https://www.linkedin.com/feed/?shareActive=true&text=' + encodeURIComponent(linkedInText()); }
    function renderPreview() {
      var card = $('card-body'); card.innerHTML = '';
      included().forEach(function (p) {
        var d = doc.createElement('div'); d.className = 'cp';
        if (p.id !== 'verdict') { var h = doc.createElement('h4'); h.textContent = p.title; d.appendChild(h); }
        var t = doc.createElement('p'); t.textContent = p.ta.value.trim(); d.appendChild(t); card.appendChild(d);
      });
      $('copy-src').value = shareText();
      var hit = /https?:\/\/|\b[\w.+-]+@[\w-]+\.[\w.]+\b|(^|\s)@\w+/.test($('copy-src').value);
      $('leak').hidden = !hit;
      $('li-btn').href = linkedInUrl();
    }
    function say(msg) { $('status').textContent = msg; }

    var lastCanvas = null;

    $('copy-btn').addEventListener('click', function () {
      var src = $('copy-src');
      src.value = shareText();
      function fallback() { src.hidden = false; src.focus(); src.select(); say('Copy was blocked here. The text is selected: press Ctrl+C or Cmd+C.'); }
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(src.value).then(function () { say('Share-safe text copied.'); }, fallback);
        } else { fallback(); }
      } catch (e) { fallback(); }
    });

    function gate() {
      var ok = $('review-ok').checked;
      var li = $('li-btn');
      li.setAttribute('aria-disabled', ok ? 'false' : 'true');
      li.classList.toggle('disabled', !ok);
    }
    $('review-ok').addEventListener('change', gate);
    gate();
    $('li-btn').addEventListener('click', function (e) {
      if ($('review-ok').checked) { say('LinkedIn is opening with your text filled in. Add the image if you want one.'); return; }
      e.preventDefault();
      say('Tick the box above to confirm you have reviewed the preview, then share.');
    });

    $('img-btn').addEventListener('click', function () {
      var items = included();
      if (!items.length) { say('Nothing is included yet.'); return; }
      var W = 1080, pad = 64, headH = 150, headW = Math.round(headH * 408 / 496);
      var cv = doc.createElement('canvas'), ctx = cv.getContext('2d');
      ctx.font = '30px "Figtree", system-ui, sans-serif';
      var lines = [];
      items.forEach(function (p) {
        if (p.id !== 'verdict') lines.push({ t: p.title, kind: 'h' });
        wrapLines(ctx, p.ta.value.trim(), W - pad * 2).forEach(function (l) { lines.push({ t: l, kind: 'p' }); });
        lines.push({ t: '', kind: 'gap' });
      });
      var top = pad + headH + 40;
      var H = top + lines.reduce(function (a, l) { return a + (l.kind === 'gap' ? 18 : l.kind === 'h' ? 50 : 44); }, 0) + 120;
      cv.width = W; cv.height = H; ctx = cv.getContext('2d');
      function paint(img) {
        ctx.fillStyle = '#FFFFFF'; ctx.fillRect(0, 0, W, H);
        if (img) ctx.drawImage(img, pad, pad, headW, headH);
        var tx = img ? pad + headW + 28 : pad;
        ctx.fillStyle = '#6B605B'; ctx.font = '26px "Figtree", system-ui, sans-serif'; ctx.fillText(data.week_label, tx, pad + 44);
        ctx.fillStyle = '#473628'; ctx.font = '60px "Caprasimo", Georgia, serif'; ctx.fillText('The Sunday Roast', tx, pad + 108);
        ctx.fillStyle = '#6B605B'; ctx.font = '26px "Figtree", system-ui, sans-serif'; ctx.fillText(data.tagline, tx, pad + 148);
        var y = top;
        lines.forEach(function (l) {
          if (l.kind === 'gap') { y += 18; return; }
          if (l.kind === 'h') { ctx.fillStyle = '#9C4637'; ctx.font = '600 26px "Figtree", system-ui, sans-serif'; y += 50; ctx.fillText(l.t, pad, y - 12); return; }
          ctx.fillStyle = '#302A29'; ctx.font = '30px "Figtree", system-ui, sans-serif'; y += 44; ctx.fillText(l.t, pad, y - 12);
        });
        ctx.fillStyle = '#6B605B'; ctx.font = '26px "Figtree", system-ui, sans-serif'; ctx.fillText('sundayroast.me', pad, H - 48);
        var url;
        try { url = cv.toDataURL('image/png'); } catch (e) { say('The image could not be created in this viewer.'); return; }
        lastCanvas = cv;
        $('img-out').src = url; $('img-wrap').hidden = false;
        say('Image ready below. Copy it, or press and hold (right-click) to save it.');
      }
      var logo = doc.querySelector('.logo svg');
      if (!logo) { paint(null); return; }
      var img = new Image();
      img.onload = function () { paint(img); };
      img.onerror = function () { paint(null); };
      var clone = logo.cloneNode(true); clone.setAttribute('width', '408'); clone.setAttribute('height', '496');
      img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(new XMLSerializer().serializeToString(clone));
    });

    $('img-copy').addEventListener('click', function () {
      if (!lastCanvas) { say('Make the image first.'); return; }
      try {
        lastCanvas.toBlob(function (blob) {
          try {
            navigator.clipboard.write([new ClipboardItem({ 'image/png': blob })]).then(
              function () { say('Image copied. Paste it into your LinkedIn post.'); },
              function () { say('Copy was blocked here. Press and hold (right-click) the image to save it.'); });
          } catch (e) { say('Copy was blocked here. Press and hold (right-click) the image to save it.'); }
        }, 'image/png');
      } catch (e) { say('Copy was blocked here. Press and hold (right-click) the image to save it.'); }
    });
  }

  var api = { applyRedactions: applyRedactions, wrapLines: wrapLines, init: init };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.SundayRoast = api;
  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { init(document); });
    else init(document);
  }
})(typeof window !== 'undefined' ? window : this);
