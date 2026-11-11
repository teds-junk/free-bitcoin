/* Range calculator — reusable component.
   Markup:
     <div class="range-calc" data-before-pass="3" data-before-n="9"
          data-after-pass="9" data-after-n="9"></div>
   For a count of passes out of trials, before and after a change, shows each pass rate with
   its 95% range (the Wilson interval, which behaves at small counts) and says whether the two
   ranges overlap.
   Load after the markup:  <script src="../assets/range-calculator.js"></script>
   Tokens only — no hard-coded colours. */
(function () {
  var CSS =
    '.range-calc{font-family:var(--grotesk);background:var(--paper-edge);border:1px solid var(--grid-strong);' +
    'border-left:3px solid var(--accent);padding:1.1rem 1.3rem;margin:2rem 0}' +
    '.range-calc::before{content:"Try it · the range around a count";display:block;font-size:.68rem;text-transform:uppercase;' +
    'letter-spacing:.18em;color:var(--accent);margin-bottom:.7rem}' +
    '.range-calc .rc-row{display:grid;grid-template-columns:4.5rem 4.5rem auto 4.5rem 1fr;gap:.5rem;align-items:center;' +
    'font-size:.72rem;margin-bottom:.5rem}' +
    '.range-calc .rc-head{text-transform:uppercase;letter-spacing:.12em;color:var(--ink-soft);font-size:.62rem}' +
    '.range-calc input{width:100%;font-family:var(--mono);font-size:.85rem;padding:.35rem .5rem;border:1px solid var(--grid-strong);' +
    'border-radius:3px;background:var(--ground);color:var(--ink)}' +
    '.range-calc input:focus{outline:2px solid var(--accent);outline-offset:1px}' +
    '.range-calc .rc-out{font-family:var(--mono);font-size:.85rem;color:var(--ink)}' +
    '.range-calc .rc-verdict{margin-top:.8rem;font-family:var(--serif);font-size:.95rem;color:var(--ink)}' +
    '.range-calc .rc-note{margin-top:.4rem;font-family:var(--serif);font-size:.85rem;color:var(--ink-soft)}' +
    '@media (max-width:520px){.range-calc .rc-row{grid-template-columns:4rem 3.5rem auto 3.5rem;}' +
    '.range-calc .rc-out{grid-column:1 / -1}}';

  function injectStyle() {
    if (document.getElementById('range-calc-style')) return;
    var s = document.createElement('style');
    s.id = 'range-calc-style';
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  // 95% Wilson interval for x passes out of n trials.
  function wilson(x, n) {
    var z = 1.96, p = x / n, d = 1 + z * z / n;
    var c = (p + z * z / (2 * n)) / d;
    var h = z * Math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d;
    return [Math.max(0, c - h), Math.min(1, c + h)];
  }

  function pct(x) { return Math.round(x * 100) + '%'; }

  function row(label, key, pass, n) {
    return '<div class="rc-row"><div class="rc-head">' + label + '</div>' +
      '<input type="number" min="0" data-k="' + key + '-pass" aria-label="' + label + ': trials passed" value="' + pass + '">' +
      '<div>of</div>' +
      '<input type="number" min="1" data-k="' + key + '-n" aria-label="' + label + ': trials run" value="' + n + '">' +
      '<div class="rc-out" data-out="' + key + '"></div></div>';
  }

  function build(root) {
    var d = root.dataset;
    root.innerHTML =
      row('Before', 'before', d.beforePass || 0, d.beforeN || 1) +
      row('After', 'after', d.afterPass || 0, d.afterN || 1) +
      '<div class="rc-verdict"></div><div class="rc-note"></div>';
    var inputs = root.querySelectorAll('input');
    for (var i = 0; i < inputs.length; i++) inputs[i].addEventListener('input', function () { update(root); });
    update(root);
  }

  function read(root, key) {
    var x = parseFloat(root.querySelector('input[data-k="' + key + '-pass"]').value);
    var n = parseFloat(root.querySelector('input[data-k="' + key + '-n"]').value);
    if (!isFinite(x) || !isFinite(n) || n < 1 || x < 0 || x > n) return null;
    var w = wilson(x, n);
    return { rate: x / n, lo: w[0], hi: w[1] };
  }

  function update(root) {
    var b = read(root, 'before'), a = read(root, 'after');
    var show = function (key, r) {
      root.querySelector('[data-out="' + key + '"]').textContent =
        r ? pct(r.rate) + ', range ' + pct(r.lo) + ' to ' + pct(r.hi) : 'passed cannot exceed trials';
    };
    show('before', b); show('after', a);
    var verdict = root.querySelector('.rc-verdict'), note = root.querySelector('.rc-note');
    if (!a || !b) { verdict.textContent = ''; note.textContent = ''; return; }
    var apart = a.lo > b.hi || b.lo > a.hi;
    verdict.textContent = apart
      ? 'The ranges do not overlap. This result supports a real change.'
      : 'The ranges overlap. This result does not show a change.';
    note.textContent = apart
      ? 'Ranges that stay apart are a cautious test: a difference this clear is unlikely to be chance.'
      : 'Overlapping ranges do not prove there is no change. They mean these trials cannot tell. More trials narrow both ranges.';
  }

  function init() {
    var roots = document.querySelectorAll('.range-calc');
    if (!roots.length) return;
    injectStyle();
    roots.forEach(build);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
