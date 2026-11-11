/* Cost calculator — reusable component.
   Markup:
     <div class="cost-calc"></div>
   Optional: data-usd-per-aiu="0.01" (the dollar rate of one AIU; default $0.01).
   The reader picks one or more results.jsonl files. They are read in the browser and never
   uploaded. Trial records ("type": "trial-result") are grouped by variant and model. For each
   group it shows trials, passing trials (gradeResult.passed === true), ERROR trials
   (status other than "success"), total cost (trajectory.metrics.tokenUsage.cost.amount, in
   nano-AIU, a billionth of an AIU), the same in dollars, cost per passing trial, and median
   tokens. Trials with no recorded cost (bring-your-own-key runs) are counted and named.
   Load after the markup:  <script src="../assets/cost-calculator.js"></script>
   Tokens only — no hard-coded colours. */
(function () {
  var CSS =
    '.cost-calc{font-family:var(--grotesk);background:var(--paper-edge);border:1px solid var(--grid-strong);' +
    'border-left:3px solid var(--accent);padding:1.1rem 1.3rem;margin:2rem 0}' +
    '.cost-calc::before{content:"Try it · cost per passing trial";display:block;font-size:.68rem;text-transform:uppercase;' +
    'letter-spacing:.18em;color:var(--accent);margin-bottom:.7rem}' +
    '.cost-calc .cc-pick{display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;font-size:.72rem}' +
    '.cost-calc .cc-pick label{text-transform:uppercase;letter-spacing:.12em;color:var(--ink-soft);font-size:.62rem}' +
    '.cost-calc input[type=file]{max-width:100%;font-family:var(--mono);font-size:.78rem;color:var(--ink)}' +
    '.cost-calc input[type=file]::file-selector-button{font-family:var(--grotesk);font-size:.68rem;text-transform:uppercase;' +
    'letter-spacing:.12em;padding:.4rem .7rem;margin-right:.6rem;border:1px solid var(--grid-strong);border-radius:3px;' +
    'background:var(--ground);color:var(--accent);cursor:pointer}' +
    '.cost-calc input[type=file]:focus-visible{outline:2px solid var(--accent);outline-offset:2px}' +
    '.cost-calc .cc-hint{margin-top:.5rem;font-family:var(--serif);font-size:.85rem;color:var(--ink-soft)}' +
    '.cost-calc .cc-card{margin-top:1rem;padding:.8rem .9rem;border:1px solid var(--grid-strong);background:var(--ground)}' +
    '.cost-calc .cc-name{font-size:.72rem;text-transform:uppercase;letter-spacing:.12em;color:var(--accent);' +
    'margin-bottom:.6rem;overflow-wrap:anywhere}' +
    '.cost-calc .cc-name span{color:var(--ink-soft);text-transform:none;letter-spacing:0;font-family:var(--mono)}' +
    '.cost-calc dl{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.7rem 1rem;margin:0}' +
    '.cost-calc dt{font-size:.6rem;text-transform:uppercase;letter-spacing:.12em;color:var(--ink-soft)}' +
    '.cost-calc dd{margin:.15rem 0 0;font-family:var(--mono);font-size:.85rem;color:var(--ink)}' +
    '.cost-calc .cc-note{margin-top:.6rem;font-family:var(--serif);font-size:.85rem;color:var(--ink-soft)}' +
    '.cost-calc .cc-total{margin-top:1rem;font-family:var(--serif);font-size:.95rem;color:var(--ink)}' +
    '@media (max-width:520px){.cost-calc{padding:1rem}.cost-calc dl{grid-template-columns:repeat(2,minmax(0,1fr))}}';

  var NANO = 1e9;

  function injectStyle() {
    if (document.getElementById('cost-calc-style')) return;
    var s = document.createElement('style');
    s.id = 'cost-calc-style';
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  function esc(t) {
    return String(t).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function median(xs) {
    if (!xs.length) return null;
    var s = xs.slice().sort(function (a, b) { return a - b; }), m = Math.floor(s.length / 2);
    return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
  }

  function aiu(x) { return x.toFixed(2) + ' AIU'; }
  function usd(x) { return '$' + (x < 1 ? x.toFixed(3) : x.toFixed(2)); }
  function kTokens(x) { return x == null ? '—' : (x / 1000).toFixed(1) + 'k'; }

  // Read every trial record from the text of one results.jsonl file.
  function parse(text, groups, order, skipped) {
    var lines = text.split(/\r?\n/);
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i].trim();
      if (!line) continue;
      var r;
      try { r = JSON.parse(line); } catch (e) { skipped.lines++; continue; }
      if (!r || r.type !== 'trial-result') continue;
      var variant = r.variant || '(no variant)';
      var model = r.model || (r.trajectory && r.trajectory.metadata && r.trajectory.metadata.model) || '?';
      var key = variant + '\u0000' + model;
      var g = groups[key];
      if (!g) {
        g = groups[key] = { variant: variant, model: model, trials: 0, passed: 0, errors: 0,
          nano: 0, withCost: 0, tokens: [] };
        order.push(key);
      }
      g.trials++;
      if (r.status !== 'success') g.errors++;
      if (r.gradeResult && r.gradeResult.passed === true) g.passed++;
      var usage = r.trajectory && r.trajectory.metrics && r.trajectory.metrics.tokenUsage;
      if (usage) {
        if (typeof usage.totalTokens === 'number') g.tokens.push(usage.totalTokens);
        if (usage.cost && typeof usage.cost.amount === 'number' && usage.cost.unit === 'nano-aiu') {
          g.nano += usage.cost.amount;
          g.withCost++;
        }
      }
    }
  }

  function card(g, rate) {
    var total = g.nano / NANO;
    var missing = g.trials - g.withCost;
    var perPass = g.passed && g.withCost ? total / g.passed : null;
    var html = '<div class="cc-card"><div class="cc-name">' + esc(g.variant) +
      ' <span>· ' + esc(g.model) + '</span></div><dl>' +
      '<div><dt>Trials</dt><dd>' + g.trials + '</dd></div>' +
      '<div><dt>Passing</dt><dd>' + g.passed + ' of ' + g.trials + '</dd></div>' +
      '<div><dt>ERROR</dt><dd>' + g.errors + '</dd></div>' +
      '<div><dt>Total cost</dt><dd>' + (g.withCost ? aiu(total) : '—') + '</dd></div>' +
      '<div><dt>In dollars</dt><dd>' + (g.withCost ? usd(total * rate) : '—') + '</dd></div>' +
      '<div><dt>Per passing trial</dt><dd>' +
        (perPass == null ? '—' : aiu(perPass) + '<br>' + usd(perPass * rate)) + '</dd></div>' +
      '<div><dt>Median tokens</dt><dd>' + kTokens(median(g.tokens)) + '</dd></div>' +
      '</dl>';
    var notes = [];
    if (!g.passed) notes.push('No trial passed, so there is no cost per passing trial.');
    if (missing === g.trials) {
      notes.push('No cost recorded for any trial. Runs through your own provider (bring your own key) ' +
        'record tokens but no cost: multiply the tokens by your own price.');
    } else if (missing) {
      notes.push('Cost missing for ' + missing + ' of ' + g.trials + ' trials (an ERROR trial, or a run ' +
        'through your own provider), so the total covers ' + g.withCost + '.');
    }
    if (notes.length) html += '<div class="cc-note">' + notes.join(' ') + '</div>';
    return html + '</div>';
  }

  function render(root, groups, order, skipped, files) {
    var rate = parseFloat(root.dataset.usdPerAiu) || 0.01;
    var out = root.querySelector('.cc-out');
    if (!order.length) {
      out.innerHTML = '<div class="cc-note">No trial records found in ' + files +
        (files === 1 ? ' file' : ' files') + '. Pick a <code>results.jsonl</code> from a run folder.</div>';
      return;
    }
    var html = '', sum = 0, trials = 0;
    for (var i = 0; i < order.length; i++) {
      var g = groups[order[i]];
      html += card(g, rate);
      sum += g.nano; trials += g.trials;
    }
    html += '<div class="cc-total">Across ' + trials + ' trials in ' + files +
      (files === 1 ? ' file' : ' files') + ': ' + aiu(sum / NANO) + ', or ' + usd(sum / NANO * rate) +
      ' at $' + rate + ' per AIU. Judge calls are not included.</div>';
    if (skipped.lines) html += '<div class="cc-note">' + skipped.lines + ' lines could not be read and were skipped.</div>';
    out.innerHTML = html;
  }

  function build(root) {
    var id = 'cost-calc-' + Math.random().toString(36).slice(2, 8);
    root.innerHTML =
      '<div class="cc-pick"><label for="' + id + '">results.jsonl files</label>' +
      '<input id="' + id + '" type="file" multiple accept=".jsonl,.json,application/json,text/plain"></div>' +
      '<div class="cc-hint">Pick one or more <code>results.jsonl</code> files, such as one from each ' +
      'variant folder of an experiment. They are read here, in your browser; nothing is uploaded.</div>' +
      '<div class="cc-out" aria-live="polite"></div>';
    root.querySelector('input').addEventListener('change', function (ev) {
      var list = Array.prototype.slice.call(ev.target.files || []);
      if (!list.length) return;
      var groups = {}, order = [], skipped = { lines: 0 }, left = list.length;
      list.forEach(function (f) {
        var reader = new FileReader();
        reader.onload = function () { parse(String(reader.result), groups, order, skipped); done(); };
        reader.onerror = function () { skipped.lines++; done(); };
        reader.readAsText(f);
      });
      function done() { if (--left === 0) render(root, groups, order, skipped, list.length); }
    });
  }

  function init() {
    var roots = document.querySelectorAll('.cost-calc');
    if (!roots.length) return;
    injectStyle();
    roots.forEach(build);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
