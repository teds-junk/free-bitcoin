/*
 * video-lesson motion runtime (Solarized Technical Essay).
 * Include in every scene: <script src="../_theme/vl-runtime.js" defer></script>
 *
 * Text is never revealed progressively. Motion comes only from these primitives,
 * declared as cues in <script type="application/json" id="cues">[ ... ]</script>:
 *
 *   { "type": "focus",    "target": "filter-op", "at": "1", "color": "cyan" }
 *   { "type": "focus",    "target": "none", "at": "3" }                       // clear focus
 *   { "type": "morph",    "from": "filter-op@code", "to": "filter-op@block", "at": "2+0.4" }
 *   { "type": "connect",  "from": "users@diagram", "to": "filter-op@diagram", "at": "t=1.5" }
 *   { "type": "expand",   "target": "#service", "at": "4" }
 *   { "type": "collapse", "target": "#service", "at": "6" }
 *   { "type": "scroll",   "target": "#spec", "to": "40-52", "at": "3" }       // move a file panel's window
 *
 *  at        "N" = when narration sentence N (0-based) starts; "N+0.5" = 0.5 s later; "t=4.2" = absolute;
 *            "N~word" = when that word or short phrase is spoken in sentence N (first occurrence,
 *            any case), estimated from its share of the sentence's characters
 *  duration  ms, optional (defaults: focus 350, morph 700, connect 500, expand/collapse 650;
 *            scroll 600-1800 by distance)
 *  to        scroll only: a line ("44"), a range ("40-52"), "top", or "end". A range that fits
 *            the window is centred in it; a longer one starts at the window's top.
 *  align     scroll only: "top" puts the first line of "to" at the top of the window
 *  target    a concept id (every element with data-concept="id"), "id@rep" (data-concept="id"
 *            and data-rep="rep"), or "#elementId"
 *  color     focus backing: cyan (default) | blue | yellow | green | orange | red | violet
 *  channel   focus only: independent highlight tracks (default "main")
 *  until     focus only: "N" / "t=x" when this highlight fades out
 *
 * Callouts: <p class="callout" data-anchor="filter-op">…</p> inside a .callouts column is lined up
 * with the element its data-anchor names (same syntax as a target) on every frame, follows it when
 * a file panel scrolls, is hidden while that line is outside the window, and is "lit" for as long
 * as its anchor (or the callout's own data-concept) is highlighted. No cue is needed for it.
 *
 * The renderer injects window.__VL = { duration, fps, sentences: [{ text, start, end }] } and
 * calls window.__seek(t) per frame. Every visual property is computed from t alone
 * (seekable in any order). window.__vlReady resolves after fonts load and geometry is measured.
 * Opened directly in a browser it previews in real time with ~3 s fake sentence spacing.
 */
(function () {
  'use strict';
  var DEFAULT_MS = { focus: 350, morph: 700, connect: 500, expand: 650, collapse: 650, scroll: null };
  var TYPES = Object.keys(DEFAULT_MS);
  // A scroll with no "duration" takes longer the further it goes: 500 ms + 50 ms per row, within these bounds.
  var SCROLL_MS = { base: 500, perRow: 50, min: 600, max: 1800 };

  // ---- easing: cubic-bezier(.22, 1, .36, 1) ------------------------------------
  function bezier(x1, y1, x2, y2) {
    function a(p1, p2) { return 1 - 3 * p2 + 3 * p1; }
    function b(p1, p2) { return 3 * p2 - 6 * p1; }
    function c(p1) { return 3 * p1; }
    function calc(t, p1, p2) { return ((a(p1, p2) * t + b(p1, p2)) * t + c(p1)) * t; }
    function slope(t, p1, p2) { return 3 * a(p1, p2) * t * t + 2 * b(p1, p2) * t + c(p1); }
    return function (x) {
      if (x <= 0) return 0; if (x >= 1) return 1;
      var t = x;
      for (var i = 0; i < 8; i++) { var s = slope(t, x1, x2); if (Math.abs(s) < 1e-6) break; t -= (calc(t, x1, x2) - x) / s; }
      return calc(t, y1, y2);
    };
  }
  var ease = bezier(0.22, 1, 0.36, 1);
  var easeInOut = bezier(0.65, 0, 0.35, 1); // spatial morphs: symmetric, no overshoot
  function clamp(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }
  function lerp(a, b, p) { return a + (b - a) * p; }
  // Progress of a cue at time t (0..1). Zero-duration cues are complete from their start.
  function prog(c, t) { return c.dur > 0 ? clamp((t - c.start) / c.dur) : (t >= c.start ? 1 : 0); }

  function vl() {
    if (window.__VL) return window.__VL;
    var s = []; for (var i = 0; i < 30; i++) s.push({ start: 0.6 + i * 3, end: 0.6 + i * 3 + 2.4 });
    return { duration: 30, fps: 30, sentences: s };
  }

  // First occurrence of `w` in `text` that starts a word; failing that, the first occurrence anywhere.
  function findWord(text, w) {
    var i = -1, first = -1;
    while ((i = text.indexOf(w, i + 1)) >= 0) {
      if (first < 0) first = i;
      if (i === 0 || !/[a-z0-9]/.test(text.charAt(i - 1))) return i;
    }
    return first;
  }

  // "N~word": the moment `word` is spoken in sentence N, estimated as the sentence start plus
  // the word's character offset as a share of the sentence's length. Falls back to the sentence
  // start (and says so) when the narration text is not available or does not contain the word.
  function wordTime(v, tilde) {
    var n = parseInt(v.slice(0, tilde), 10), s = vl().sentences[n];
    if (!s) return 0;
    var word = v.slice(tilde + 1).trim().toLowerCase(), text = String(s.text || '').toLowerCase();
    if (!text) { wordless.push(v); return s.start; } // reported once, in setup
    var i = word ? findWord(text, word) : -1;
    if (i < 0) { problems.push('cue at "' + v + '": "' + word + '" is not in sentence ' + n + ', so it fires at the start of that sentence'); return s.start; }
    return s.start + (i / text.length) * (s.end - s.start);
  }

  function timeOf(spec) {
    if (spec === undefined || spec === null) return 0;
    var v = String(spec).trim();
    if (v.indexOf('t=') === 0) return parseFloat(v.slice(2)) || 0;
    var tilde = v.indexOf('~');
    if (tilde > 0) return wordTime(v, tilde);
    var parts = v.split('+');
    var s = vl().sentences[parseInt(parts[0], 10)];
    return (s ? s.start : 0) + (parts[1] ? parseFloat(parts[1]) : 0);
  }

  // ---- DOM helpers -------------------------------------------------------------
  var scene, sceneRect;
  function resolve(ref) {
    if (!ref || ref === 'none') return [];
    if (ref.charAt(0) === '#') { var e = document.getElementById(ref.slice(1)); return e ? [e] : []; }
    var at = ref.indexOf('@');
    var sel = at < 0 ? '[data-concept="' + ref + '"]' : '[data-concept="' + ref.slice(0, at) + '"][data-rep="' + ref.slice(at + 1) + '"]';
    return Array.prototype.slice.call(scene.querySelectorAll(sel)).filter(function (el) { return !el.closest('.vl-transitions'); });
  }
  function rel(r, base) { return { x: r.left - base.left, y: r.top - base.top, w: r.width, h: r.height }; }
  // The element whose background a highlight sits on: the nearest box with a fill of its own, so the
  // backing is painted above that fill and below the text. Anything else is backed on the paper.
  function host(el) { return el.closest('.code, .part, .semantic-block, .quote') || scene; }

  var layers = new Map(); // host element -> highlight layer
  function layerFor(h) {
    if (!layers.has(h)) {
      if (getComputedStyle(h).position === 'static') h.style.position = 'relative';
      h.style.isolation = 'isolate';
      var l = document.createElement('div'); l.className = 'vl-hl-layer';
      l.style.cssText = 'position:absolute;inset:0;pointer-events:none;z-index:-1;';
      h.insertBefore(l, h.firstChild);
      layers.set(h, l);
    }
    return layers.get(h);
  }
  function focusColor(name, h) {
    var dark = h.classList.contains('dark') || h.closest('.scene.dark');
    var key = (name || 'cyan');
    if (dark) return 'var(--focus-dark-' + (/^(cyan|blue|yellow|green|orange|red|violet)$/.test(key) ? key : 'cyan') + ')';
    return 'var(--focus-' + key + ')';
  }

  // ---- file panels: a window of rows over a real file, moved by scroll cues ------------
  // (markup from scripts/file-panel.js). Every position below is in px from the top of the rows.
  var panels = [], panelByCode = new Map();

  function preparePanel(el) {
    var win = el.querySelector('.file-window'), code = el.querySelector('.file-code');
    if (!win || !code) return null;
    var cr = code.getBoundingClientRect(), winH = win.getBoundingClientRect().height;
    var rows = Array.prototype.map.call(code.querySelectorAll('.file-row'), function (r) {
      var b = r.getBoundingClientRect(), hid = r.getAttribute('data-hidden');
      var o = { el: r, top: b.top - cr.top, h: b.height };
      // a..b is the row's place in the file, in lines: a hidden row stands for its whole stretch.
      if (hid) { var p = hid.split('-'); o.hidden = true; o.first = +p[0]; o.last = +(p[1] || p[0]); o.a = o.first - 1; o.b = o.last; }
      else o.line = +r.getAttribute('data-line');
      return o;
    });
    for (var i = 0; i < rows.length;) { // the display rows of one wrapped line share that line
      if (rows[i].hidden) { i++; continue; }
      var j = i; while (j < rows.length && !rows[j].hidden && rows[j].line === rows[i].line) j++;
      for (var k = i; k < j; k++) { rows[k].a = rows[i].line - 1 + (k - i) / (j - i); rows[k].b = rows[i].line - 1 + (k - i + 1) / (j - i); }
      i = j;
    }
    var last = rows[rows.length - 1], contentH = last ? last.top + last.h : 0;
    // Minimap: one marker per run of shown lines, so the marked region is exactly the lines on
    // screen (a "lines hidden" row marks nothing).
    var map = el.querySelector('.file-map'), view = map && map.querySelector('.file-map-view'), runs = [];
    var bars = map ? (+map.getAttribute('data-bars') || map.querySelectorAll('i').length) : 0, per = map ? (+map.getAttribute('data-per') || 1) : 1;
    if (view) rows.forEach(function (r, n) {
      if (r.hidden) return;
      if (n && !rows[n - 1].hidden) { runs[runs.length - 1].bottom = r.top + r.h; return; }
      var mark = runs.length ? view.cloneNode(false) : view;
      if (runs.length) map.insertBefore(mark, view.nextSibling);
      runs.push({ top: r.top, bottom: r.top + r.h, el: mark });
    });
    return { el: el, name: el.id ? '#' + el.id : 'the file panel', code: code, rows: rows, winH: winH,
      rowH: rows.length ? rows[0].h : 1, max: Math.max(0, contentH - winH), cues: [], y: 0,
      runs: runs, pxPerLine: bars ? map.getBoundingClientRect().height / (bars * per) : 0 };
  }

  // Where a scroll's "to" puts the top of the window, or null if the panel does not show it.
  function scrollTarget(P, to, align) {
    var v = String(to == null ? '' : to).trim();
    if (v === 'top') return 0;
    if (v === 'end') return P.max;
    var m = /^(\d+)(?:\s*-\s*(\d+))?$/.exec(v);
    if (!m) return null;
    var a = +m[1], b = m[2] ? +m[2] : a, i0 = -1, i1 = -1;
    P.rows.forEach(function (r, i) { if (!r.hidden && r.line >= a && r.line <= b) { if (i0 < 0) i0 = i; i1 = i; } });
    if (i0 < 0 || P.rows[i0].line !== a || P.rows[i1].line !== b) return null;
    var top = P.rows[i0].top, height = P.rows[i1].top + P.rows[i1].h - top, y = top;
    // Centre a range that fits, on a whole row; a longer one starts at the top of the window.
    if (align !== 'top' && height < P.winH) y = top - Math.floor((P.winH - height) / 2 / P.rowH) * P.rowH;
    return Math.max(0, Math.min(P.max, y));
  }

  // The window's offset at time t: each scroll eases from wherever the one before had got to.
  function scrollAt(P, t) {
    var y = 0;
    for (var i = 0; i < P.cues.length; i++) {
      var c = P.cues[i]; if (t < c.start) break;
      y = lerp(c.fromY, c.toY, easeInOut(prog(c, t)));
    }
    return y;
  }

  function lineAt(P, y) { // the place in the file (in lines) that sits at offset y
    if (!P.rows.length) return 0;
    var r = P.rows[Math.max(0, Math.min(P.rows.length - 1, Math.floor(y / P.rowH)))];
    return lerp(r.a, r.b, clamp((y - r.top) / r.h));
  }

  function rowName(el) {
    var row = el.closest('.file-row'); if (!row) return 'its row';
    return row.getAttribute('data-line') ? 'line ' + row.getAttribute('data-line') : 'the hidden row ' + row.getAttribute('data-hidden');
  }

  function windowLines(P, y) { // "lines 40–51", for messages
    var vis = P.rows.filter(function (r) { return !r.hidden && r.top + r.h > y && r.top < y + P.winH; });
    return vis.length ? 'lines ' + vis[0].line + '–' + vis[vis.length - 1].line : 'no file lines';
  }

  // ---- setup: measure once, after fonts are ready ----------------------------------
  var cues = [], focusChannels = {}, morphs = [], connects = [], blocks = new Map(), problems = [];
  var callouts = [], litNow = new Set(); // notes lined up with what they annotate; elements highlighted in this frame
  var wordless = []; // "N~word" times that fell back to the sentence start for want of narration text

  function readCues() {
    var tag = document.getElementById('cues');
    if (!tag) return [];
    try { return JSON.parse(tag.textContent || '[]'); } catch (e) { problems.push('cues JSON: ' + e.message); return []; }
  }

  function setup() {
    scene = document.querySelector('.scene') || document.body;
    scene.style.isolation = 'isolate';
    sceneRect = scene.getBoundingClientRect();
    var trans = document.createElement('div'); trans.className = 'vl-transitions'; scene.appendChild(trans);
    var svgNS = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(svgNS, 'svg'); svg.setAttribute('class', 'vl-connectors');
    svg.setAttribute('width', sceneRect.width); svg.setAttribute('height', sceneRect.height);
    scene.insertBefore(svg, scene.firstChild);

    var sceneStyle = getComputedStyle(scene);
    var bandTop = sceneRect.bottom - (parseFloat(sceneStyle.paddingBottom) || 0), safeRight = sceneRect.right - (parseFloat(sceneStyle.paddingRight) || 0);
    Array.prototype.forEach.call(scene.querySelectorAll('.file-panel'), function (el) {
      var P = preparePanel(el); if (!P) return;
      panels.push(P); panelByCode.set(P.code, P);
      var b = el.getBoundingClientRect();
      if (b.bottom > bandTop + 1) problems.push(P.name + ' ends at ' + Math.round(b.bottom - sceneRect.top) + 'px, inside the caption band (it starts at ' + Math.round(bandTop - sceneRect.top) + 'px): give the panel fewer rows or put less above it');
      if (b.right > safeRight + 1) problems.push(P.name + ' runs ' + Math.round(b.right - safeRight) + 'px past the right safe margin: give the panel a smaller width');
    });

    cues = readCues().map(function (c, i) {
      c = Object.assign({}, c);
      if (TYPES.indexOf(c.type) < 0) { problems.push('cue ' + i + ': unknown type ' + c.type); return null; }
      c.start = timeOf(c.at);
      var ms = c.duration != null ? c.duration : DEFAULT_MS[c.type];
      c.dur = ms == null ? null : ms / 1000; // null: a scroll works its duration out from the distance
      c.untilT = c.until != null ? timeOf(c.until) : null;
      return c;
    }).filter(Boolean).sort(function (a, b) { return a.start - b.start; });

    cues.forEach(function (c, i) {
      if (c.type === 'focus') {
        var els = resolve(c.target);
        if (c.target !== 'none' && !els.length) problems.push('focus target not found: ' + c.target);
        c.els = els;
        c.rects = els.flatMap(function (el) {
          if (el.classList.contains('callout')) return []; // a callout is lit, not backed (renderCallouts)
          var h = host(el), hr = h.getBoundingClientRect();
          // A block highlighted as a whole is filled edge to edge, in its own shape.
          if (h === el) return [{ el: el, host: h, x: 0, y: 0, w: hr.width, h: hr.height, radius: getComputedStyle(el).borderRadius }];
          return Array.prototype.map.call(el.getClientRects(), function (r) {
            var q = rel(r, hr); return { el: el, host: h, x: q.x - 8, y: q.y - 2, w: q.w + 16, h: q.h + 4 };
          });
        });
        (focusChannels[c.channel || 'main'] = focusChannels[c.channel || 'main'] || []).push(c);
      } else if (c.type === 'morph') {
        var src = resolve(c.from)[0], dst = resolve(c.to)[0];
        if (!src || !dst) { problems.push('morph endpoints not found: ' + c.from + ' -> ' + c.to); return; }
        c.src = src; c.dst = dst; c.ends = [src, dst];
        c.srcRect = rel(src.getBoundingClientRect(), sceneRect);
        c.dstRect = rel(dst.getBoundingClientRect(), sceneRect);
        c.srcClone = cloneFor(src, c.srcRect, trans); c.dstClone = cloneFor(dst, c.dstRect, trans);
        morphs.push(c);
      } else if (c.type === 'connect') {
        var a = resolve(c.from)[0], b = resolve(c.to)[0];
        if (!a || !b) { problems.push('connect endpoints not found: ' + c.from + ' -> ' + c.to); return; }
        var A = rel(a.getBoundingClientRect(), sceneRect), B = rel(b.getBoundingClientRect(), sceneRect);
        var d = connectorPath(A, B, c.curve || 0);
        var p = document.createElementNS(svgNS, 'path'); p.setAttribute('d', d.path);
        if (c.color) p.setAttribute('class', 'c-' + c.color);
        var head = document.createElementNS(svgNS, 'path'); head.setAttribute('d', d.head);
        if (c.color) head.setAttribute('class', 'c-' + c.color);
        if (c.arrow === false) head.style.display = 'none';
        svg.appendChild(p); svg.appendChild(head);
        c.path = p; c.head = head; c.len = p.getTotalLength(); c.ends = [a, b];
        connects.push(c);
      } else if (c.type === 'scroll') {
        var pe = resolve(c.target)[0];
        var root = pe && (pe.classList.contains('file-panel') ? pe : pe.closest('.file-panel') || pe.querySelector('.file-panel'));
        var P = root && panels.filter(function (q) { return q.el === root; })[0];
        if (!P) { problems.push('scroll target is not a file panel: ' + c.target); return; }
        c.toY = scrollTarget(P, c.to, c.align);
        if (c.toY == null) { problems.push('scroll ' + c.target + ': "' + c.to + '" is not a line or range that panel shows (use a shown line, a range of them, "top", or "end")'); return; }
        c.fromY = scrollAt(P, c.start); // cues are in time order, so this is where the earlier ones leave it
        if (c.dur == null) {
          var moved = Math.abs(c.toY - c.fromY) / P.rowH;
          c.dur = moved ? Math.max(SCROLL_MS.min, Math.min(SCROLL_MS.max, SCROLL_MS.base + SCROLL_MS.perRow * moved)) / 1000 : 0;
        }
        P.cues.push(c);
      } else {
        var el = resolve(c.target)[0];
        if (!el) { problems.push(c.type + ' target not found: ' + c.target); return; }
        if (!blocks.has(el)) blocks.set(el, prepareBlock(el));
        blocks.get(el).cues.push(c);
      }
    });

    // Callouts: measure where each sits and where its anchor is, with every panel unscrolled.
    Array.prototype.forEach.call(scene.querySelectorAll('.callout'), function (el) {
      var ref = el.getAttribute('data-anchor');
      if (!ref) { problems.push('a .callout has no data-anchor: name the element it annotates (data-anchor="concept-id")'); return; }
      var anchors = resolve(ref).filter(function (a) { return a !== el; });
      if (!anchors.length) { problems.push('callout anchor not found: ' + ref); return; }
      var a = anchors[0], ar = a.getClientRects()[0] || a.getBoundingClientRect();
      var box = (el.offsetParent || el.parentElement).getBoundingClientRect(), er = el.getBoundingClientRect();
      var lh = parseFloat(getComputedStyle(el).lineHeight) || er.height;
      var root = a.closest('.file-panel'), P = root && panels.filter(function (q) { return q.el === root; })[0];
      callouts.push({ el: el, anchors: anchors, P: P || null, group: el.parentElement, h: er.height,
        base: ar.top + ar.height / 2 - box.top - lh / 2,            // callout top that centres its first line on the anchor
        rowTop: P ? ar.top - P.code.getBoundingClientRect().top : 0, rowH: ar.height });
    });

    if (wordless.length) {
      problems.push('no narration text here, so ' + wordless.length + ' cue(s) timed to a word ("' + wordless.slice(0, 3).join('", "') + (wordless.length > 3 ? '", …' : '"') +
        ') fire at the start of their sentences; preview with --video and --scene to time them to the words');
    }

    // File-panel guards, now that every scroll is known.
    cues.forEach(function (c) {
      if (c.type === 'focus' && c.rects && !wordless.length) { // placeholder times would raise false alarms
        // A highlight has to land on at least one row that is in the window. (A concept marked
        // in two distant places is fine: the other place is highlighted when a scroll brings it in.)
        panels.forEach(function (P) {
          var mine = c.rects.filter(function (r) { return r.host === P.code; });
          if (!mine.length) return;
          var T = c.start + c.dur, y = Math.round(scrollAt(P, T));
          if (mine.some(function (r) { var mid = r.y + r.h / 2; return mid > y && mid < y + P.winH; })) return;
          problems.push('focus "' + c.target + '" at ' + T.toFixed(1) + 's: ' + rowName(mine[0].el) + ' is outside the window of ' + P.name +
            ', which shows ' + windowLines(P, y) + ' then; scroll to it first');
        });
      } else if (c.ends) {
        c.ends.forEach(function (el) { // morph and connect measure their endpoints once, before any scroll
          var root = el.closest('.file-panel'), P = root && panels.filter(function (q) { return q.el === root; })[0];
          if (P && P.cues.length) problems.push(c.type + ' has an endpoint inside ' + P.name + ', which scrolls; its position is measured before any scroll, so it will be drawn in the wrong place');
        });
      }
    });
  }

  var COPY = ['font-family', 'font-size', 'font-weight', 'font-style', 'line-height', 'letter-spacing', 'color',
    'white-space', 'background-color', 'border-radius', 'padding-top', 'padding-right', 'padding-bottom', 'padding-left', 'text-align'];
  function cloneFor(el, r, layer) {
    var cs = getComputedStyle(el);
    var c = el.cloneNode(true);
    c.removeAttribute('id');
    [c].concat(Array.prototype.slice.call(c.querySelectorAll('[data-concept],[id]'))).forEach(function (n) { n.removeAttribute('data-concept'); n.removeAttribute('id'); });
    COPY.forEach(function (k) { c.style.setProperty(k, cs.getPropertyValue(k)); });
    c.style.position = 'absolute'; c.style.left = '0'; c.style.top = '0'; c.style.margin = '0';
    c.style.width = r.w + 'px'; c.style.height = r.h + 'px'; c.style.boxSizing = 'border-box';
    c.style.transformOrigin = '0 0'; c.style.display = cs.display === 'inline' ? 'inline-block' : cs.display;
    c.style.opacity = '0';
    layer.appendChild(c);
    return c;
  }

  function connectorPath(A, B, curve) {
    var ax, ay, bx, by, horiz = Math.abs((B.x + B.w / 2) - (A.x + A.w / 2)) >= Math.abs((B.y + B.h / 2) - (A.y + A.h / 2));
    if (horiz) {
      var right = B.x > A.x; ax = right ? A.x + A.w + 14 : A.x - 14; bx = right ? B.x - 14 : B.x + B.w + 14;
      ay = A.y + A.h / 2; by = B.y + B.h / 2;
    } else {
      var down = B.y > A.y; ay = down ? A.y + A.h + 12 : A.y - 12; by = down ? B.y - 12 : B.y + B.h + 12;
      ax = A.x + A.w / 2; bx = B.x + B.w / 2;
    }
    var mx = (ax + bx) / 2, my = (ay + by) / 2, k = curve * Math.hypot(bx - ax, by - ay);
    var nx = -(by - ay), ny = bx - ax, nl = Math.hypot(nx, ny) || 1;
    var cx = mx + nx / nl * k, cy = my + ny / nl * k;
    var ang = Math.atan2(by - cy, bx - cx), s = 14;
    var head = 'M' + (bx - s * Math.cos(ang - 0.45)) + ',' + (by - s * Math.sin(ang - 0.45)) + ' L' + bx + ',' + by +
      ' L' + (bx - s * Math.cos(ang + 0.45)) + ',' + (by - s * Math.sin(ang + 0.45));
    return { path: 'M' + ax + ',' + ay + ' Q' + cx + ',' + cy + ' ' + bx + ',' + by, head: head };
  }

  function prepareBlock(el) {
    var full = el.getBoundingClientRect();
    var keep = el.querySelector('.title, .label') || el;
    var k = keep.getBoundingClientRect();
    var pad = 22;
    var inset = { t: Math.max(0, k.top - full.top - pad), r: Math.max(0, full.right - k.right - pad),
      b: Math.max(0, full.bottom - k.bottom - pad), l: Math.max(0, k.left - full.left - pad) };
    var kc = { x: k.left + k.width / 2, y: k.top + k.height / 2 };
    var parts = Array.prototype.slice.call(el.querySelectorAll('.part, [data-part]')).map(function (p) {
      var r = p.getBoundingClientRect(); return { el: p, dx: kc.x - (r.left + r.width / 2), dy: kc.y - (r.top + r.height / 2) };
    });
    return { el: el, inset: inset, parts: parts, cues: [] };
  }

  // ---- per-frame evaluation (pure function of t) ------------------------------------
  var pools = new Map();
  function hlDivs(h, n) {
    var layer = layerFor(h), pool = pools.get(layer) || [];
    while (pool.length < n) { var d = document.createElement('div'); d.className = 'vl-hl'; layer.appendChild(d); pool.push(d); }
    pools.set(layer, pool);
    return pool;
  }

  function renderFocus(t) {
    var used = new Map(); // layer pool -> count used this frame
    function draw(r, color, opacity, scaleX) {
      var P = panelByCode.get(r.host); // in a file panel, a backing scrolled out of the window is not drawn
      if (P && (r.y + r.h <= P.y || r.y >= P.y + P.winH)) return;
      var pool = hlDivs(r.host, (used.get(r.host) || 0) + 1);
      var d = pool[used.get(r.host) || 0]; used.set(r.host, (used.get(r.host) || 0) + 1);
      d.style.left = r.x + 'px'; d.style.top = r.y + 'px'; d.style.width = (r.w * scaleX) + 'px'; d.style.height = r.h + 'px';
      d.style.background = focusColor(color, r.host); d.style.opacity = String(opacity); d.style.display = 'block';
      d.style.borderRadius = r.radius || '';
    }
    litNow = new Set();
    Object.keys(focusChannels).forEach(function (ch) {
      var list = focusChannels[ch], k = -1;
      for (var i = 0; i < list.length; i++) if (list[i].start <= t) k = i;
      if (k < 0) return;
      var cur = list[k], prev = k > 0 ? list[k - 1] : null;
      var p = ease(prog(cur, t));
      var prevLive = prev && prev.target !== 'none' && (prev.untilT == null || prev.untilT > cur.start);
      var fadeOut = cur.untilT != null && t >= cur.untilT ? ease(prog({ start: cur.untilT, dur: cur.dur }, t)) : 0;
      if (cur.target === 'none') {
        if (prevLive) prev.rects.forEach(function (r) { if (r.el.style.visibility !== 'hidden') draw(r, prev.color, 1 - p, 1); });
        return;
      }
      if (fadeOut < 0.5) (cur.els || []).forEach(function (el) { litNow.add(el); });
      cur.rects.forEach(function (r, i) {
        if (r.el.style.visibility === 'hidden') return; // a morph destination that hasn't arrived yet
        var from = prevLive ? prev.rects[Math.min(i, prev.rects.length - 1)] : null;
        if (from && from.host === r.host) {
          draw({ host: r.host, x: lerp(from.x, r.x, p), y: lerp(from.y, r.y, p), w: lerp(from.w, r.w, p), h: lerp(from.h, r.h, p) },
            cur.color, 1 - fadeOut, 1);
        } else {
          draw(r, cur.color, (from ? 1 : p) * (1 - fadeOut), from ? 1 : 0.6 + 0.4 * p);
        }
      });
      if (prevLive && p < 1) prev.rects.forEach(function (r, i) {
        if (r.el.style.visibility === 'hidden') return;
        if (i >= cur.rects.length || cur.rects[i].host !== r.host) draw(r, prev.color, 1 - p, 1); // crossfade leftovers
      });
    });
    pools.forEach(function (pool, layer) {
      var n = 0; used.forEach(function (count, h) { if (layers.get(h) === layer) n = count; });
      for (var i = n; i < pool.length; i++) pool[i].style.display = 'none';
    });
  }

  function place(clone, natural, box) {
    clone.style.transform = 'translate(' + box.x + 'px,' + box.y + 'px) scale(' + (box.w / natural.w) + ',' + (box.h / natural.h) + ')';
  }

  function renderMorphs(t) {
    var hiddenDst = new Set();
    morphs.forEach(function (m) { if (t < m.start + m.dur) hiddenDst.add(m.dst); });
    morphs.forEach(function (m) {
      var raw = (t - m.start) / (m.dur || 1e-6);
      if (raw > 0 && raw < 1) {
        var p = easeInOut(raw);
        var box = { x: lerp(m.srcRect.x, m.dstRect.x, p), y: lerp(m.srcRect.y, m.dstRect.y, p),
          w: lerp(m.srcRect.w, m.dstRect.w, p), h: lerp(m.srcRect.h, m.dstRect.h, p) };
        place(m.srcClone, m.srcRect, box); place(m.dstClone, m.dstRect, box);
        m.srcClone.style.opacity = String(clamp(1 - raw * 2.5));          // source text leaves quickly
        m.dstClone.style.opacity = String(clamp(0.15 + raw * 1.4));        // destination takes over early
      } else {
        m.srcClone.style.opacity = '0'; m.dstClone.style.opacity = '0';
      }
    });
    morphs.forEach(function (m) { m.dst.style.visibility = hiddenDst.has(m.dst) ? 'hidden' : ''; });
  }

  function renderConnects(t) {
    connects.forEach(function (c) {
      var p = ease(prog(c, t));
      c.path.style.strokeDasharray = c.len; c.path.style.strokeDashoffset = String(c.len * (1 - p));
      c.path.style.opacity = p > 0 ? '1' : '0';
      c.head.style.opacity = String(clamp((p - 0.85) / 0.15));
    });
  }

  function renderBlocks(t) {
    blocks.forEach(function (b) {
      var first = b.cues[0];
      var v = first && first.type === 'expand' ? 0 : 1; // expanded fraction before any cue
      b.cues.forEach(function (c) {
        if (t >= c.start) { var p = ease(prog(c, t)); v = c.type === 'expand' ? p : 1 - p; }
      });
      var q = 1 - v, i = b.inset;
      b.el.style.clipPath = q > 0 ? 'inset(' + i.t * q + 'px ' + i.r * q + 'px ' + i.b * q + 'px ' + i.l * q + 'px round 8px)' : '';
      b.parts.forEach(function (pt) {
        pt.el.style.opacity = String(v);
        pt.el.style.transform = v < 1 ? 'translate(' + pt.dx * q + 'px,' + pt.dy * q + 'px) scale(' + (0.85 + 0.15 * v) + ')' : '';
      });
    });
  }

  // File panels: slide the rows under the window, keep only the rows in it visible, and move
  // the minimap's marker to the part of the file the window is over.
  function renderPanels(t) {
    panels.forEach(function (P) {
      var y = Math.round(scrollAt(P, t)); // whole pixels: text stays crisp and frames repeat exactly
      P.y = y;
      P.code.style.transform = y ? 'translateY(' + (-y) + 'px)' : '';
      P.rows.forEach(function (r) { r.el.style.visibility = (r.top + r.h > y && r.top < y + P.winH) ? '' : 'hidden'; });
      P.runs.forEach(function (g) {
        var top = Math.max(y, g.top), bottom = Math.min(y + P.winH, g.bottom);
        if (bottom <= top) { g.el.style.display = 'none'; return; }
        var a = Math.round(lineAt(P, top) * P.pxPerLine), b = Math.round(lineAt(P, bottom) * P.pxPerLine);
        g.el.style.display = ''; g.el.style.top = a + 'px'; g.el.style.height = Math.max(2, b - a) + 'px';
      });
    });
  }

  // Callouts: each sits level with its anchor (following a scrolling panel), is hidden while the
  // anchor's row is outside the window, and is lit while the anchor or the callout is highlighted.
  // Callouts in one column never overlap: a lower one is pushed down just far enough.
  function renderCallouts() {
    var floor = new Map(); // column -> lowest y already taken
    callouts.map(function (c) {
      var y = c.base - (c.P ? c.P.y : 0);
      var seen = !c.P || (c.rowTop >= c.P.y - 1 && c.rowTop + c.rowH <= c.P.y + c.P.winH + 1);
      return { c: c, y: y, seen: seen };
    }).sort(function (a, b) { return a.y - b.y; }).forEach(function (o) {
      var c = o.c;
      c.el.style.visibility = o.seen ? '' : 'hidden';
      if (!o.seen) return;
      var min = floor.has(c.group) ? floor.get(c.group) : -Infinity, y = Math.max(Math.round(o.y), min);
      floor.set(c.group, y + c.h + 12);
      c.el.style.transform = 'translateY(' + y + 'px)';
      var lit = litNow.has(c.el) || c.anchors.some(function (a) { return litNow.has(a); });
      if (lit !== c.lit) { c.lit = lit; c.el.classList.toggle('lit', lit); }
    });
  }

  function renderAt(t) {
    renderPanels(t); // before focus: it decides which rows are in the window
    renderMorphs(t); renderFocus(t); renderConnects(t); renderBlocks(t); // morphs first: they decide what is visible
    renderCallouts();
    document.documentElement.style.setProperty('--vl-t', String(t));
    if (typeof window.onSeek === 'function') window.onSeek(t, vl());
  }

  var started = false;
  window.__vlReady = (document.fonts ? document.fonts.ready : Promise.resolve()).then(function () {
    return new Promise(function (r) { requestAnimationFrame(function () { requestAnimationFrame(r); }); });
  }).then(function () {
    setup();
    window.__vlProblems = problems;
    window.__seek = renderAt;
    renderAt(0);
    started = true;
    if (!window.__VL_RENDER) {
      var t0 = null;
      var loop = function (now) { if (t0 === null) t0 = now; renderAt(((now - t0) / 1000) % (vl().duration + 1.5)); requestAnimationFrame(loop); };
      requestAnimationFrame(loop);
    }
    return true;
  });
  window.__seek = function (t) { if (started) renderAt(t); };
})();
