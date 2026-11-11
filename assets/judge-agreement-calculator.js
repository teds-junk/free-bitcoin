/* Judge agreement calculator — reusable component.
   Markup:
     <div class="agreement-calc" data-yy="11" data-ny="1" data-yn="3" data-nn="5"></div>
   The four counts compare a judge's verdicts with your own labels on the same trials:
     data-yy  judge yes, you yes      data-yn  judge yes, you no
     data-ny  judge no,  you yes      data-nn  judge no,  you no
   Shows TPR, TNR and raw agreement (to show why agreement alone misleads).
   Load after the markup:  <script src="../assets/judge-agreement-calculator.js"></script>
   Tokens only — no hard-coded colours. */
(function () {
  var CSS =
    '.agreement-calc{font-family:var(--grotesk);background:var(--paper-edge);border:1px solid var(--grid-strong);' +
    'border-left:3px solid var(--accent);padding:1.1rem 1.3rem;margin:2rem 0}' +
    '.agreement-calc::before{content:"Try it · judge against your labels";display:block;font-size:.68rem;text-transform:uppercase;' +
    'letter-spacing:.18em;color:var(--accent);margin-bottom:.7rem}' +
    '.agreement-calc .ac-grid{display:grid;grid-template-columns:auto 1fr 1fr;gap:.4rem .6rem;align-items:center;font-size:.72rem}' +
    '.agreement-calc .ac-head{text-transform:uppercase;letter-spacing:.12em;color:var(--ink-soft);font-size:.62rem}' +
    '.agreement-calc input{width:100%;font-family:var(--mono);font-size:.85rem;padding:.35rem .5rem;border:1px solid var(--grid-strong);' +
    'border-radius:3px;background:var(--ground);color:var(--ink)}' +
    '.agreement-calc input:focus{outline:2px solid var(--accent);outline-offset:1px}' +
    '.agreement-calc .ac-out{display:grid;grid-template-columns:repeat(auto-fit,minmax(8.5rem,1fr));gap:.5rem;margin-top:1rem}' +
    '.agreement-calc .ac-stat{background:var(--ground);border:1px solid var(--grid-strong);border-radius:3px;padding:.5rem .7rem}' +
    '.agreement-calc .ac-stat span{display:block;font-size:.6rem;text-transform:uppercase;letter-spacing:.14em;color:var(--ink-soft)}' +
    '.agreement-calc .ac-stat strong{font-family:var(--mono);font-size:1.05rem;font-weight:400;color:var(--ink)}' +
    '.agreement-calc .ac-stat.good strong{color:var(--green)}.agreement-calc .ac-stat.bad strong{color:var(--red)}' +
    '.agreement-calc .ac-note{margin-top:.8rem;font-family:var(--serif);font-size:.85rem;color:var(--ink-soft)}';

  function injectStyle() {
    if (document.getElementById('agreement-calc-style')) return;
    var s = document.createElement('style');
    s.id = 'agreement-calc-style';
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  function pct(x) { return isFinite(x) ? (x * 100).toFixed(0) + '%' : '—'; }

  function cell(k, label, value) {
    return '<input type="number" min="0" data-k="' + k + '" aria-label="' + label + '" value="' + (value || 0) + '">';
  }

  function build(root) {
    var d = root.dataset;
    root.innerHTML =
      '<div class="ac-grid">' +
      '<div></div><div class="ac-head">You: yes</div><div class="ac-head">You: no</div>' +
      '<div class="ac-head">Judge: yes</div>' +
      cell('yy', 'Judge yes, you yes', d.yy) + cell('yn', 'Judge yes, you no', d.yn) +
      '<div class="ac-head">Judge: no</div>' +
      cell('ny', 'Judge no, you yes', d.ny) + cell('nn', 'Judge no, you no', d.nn) +
      '</div>' +
      '<div class="ac-out"></div><div class="ac-note"></div>';

    var inputs = root.querySelectorAll('input');
    for (var i = 0; i < inputs.length; i++) inputs[i].addEventListener('input', function () { update(root); });
    update(root);
  }

  function val(root, k) {
    var v = parseFloat(root.querySelector('input[data-k="' + k + '"]').value);
    return isFinite(v) && v >= 0 ? v : 0;
  }

  function stat(label, value, cls) {
    return '<div class="ac-stat' + (cls ? ' ' + cls : '') + '"><span>' + label + '</span><strong>' + value + '</strong></div>';
  }

  function update(root) {
    var yy = val(root, 'yy'), ny = val(root, 'ny'), yn = val(root, 'yn'), nn = val(root, 'nn');
    var tpr = yy / (yy + ny);
    var tnr = nn / (nn + yn);
    var agree = (yy + nn) / (yy + ny + yn + nn);

    var grade = function (x) { return !isFinite(x) ? '' : x >= 0.9 ? 'good' : x < 0.8 ? 'bad' : ''; };
    root.querySelector('.ac-out').innerHTML =
      stat('TPR', pct(tpr), grade(tpr)) +
      stat('TNR', pct(tnr), grade(tnr)) +
      stat('Raw agreement', pct(agree));

    var notes = [];
    if (yy + ny < 30 || nn + yn < 30) notes.push('Fewer than 30 of your labels are yes, or fewer than 30 are no: treat these rates as rough.');
    if (isFinite(agree) && isFinite(tnr) && agree >= 0.8 && tnr < 0.8) notes.push('High agreement with a low TNR: the judge is mostly saying yes.');
    root.querySelector('.ac-note').textContent =
      notes.join(' ') || 'TPR is the share of your yes labels the judge also passed. TNR is the share of your no labels it also failed.';
  }

  function init() {
    var roots = document.querySelectorAll('.agreement-calc');
    if (!roots.length) return;
    injectStyle();
    roots.forEach(build);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
