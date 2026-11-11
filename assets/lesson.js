/* teach-me shared page script. Load at the end of <body>, after course.js:
     <script src="../assets/course.js"></script>
     <script src="../assets/lesson.js"></script>

   What it does:
   - Theme toggle. The choice persists under localStorage 'teach-me-theme'.
   - Quizzes:  <div class="quiz"> … onclick="checkAnswer(this, true|false)"
   - Sorters:  <div class="sorter" data-categories="A|B|C">
                 <div class="sort-item" data-answer="A" data-why="…">Item</div></div>
   - Course map:  <nav class="course-map" data-current="3" data-root="../"></nav>
                  data-current="0" and data-root="" on the course home.
   - Video slots: <div class="lesson-video" hidden><video controls preload="metadata"></video>…</div>
                  A slot stays hidden unless its video file loads.
                  Lesson pages look for  ../videos/<page-stem>/<page-stem>.mp4
                  The course home (data-video="course") uses COURSE.video.
                  data-src on the slot overrides both.
   - Continue prompt: click to select and copy.
   - Syntax highlighting: <pre><code class="language-yaml|bash|json|javascript|diff|markdown">
                  Loads highlight.js from cdnjs (pinned, with SRI). Offline, or if the
                  CDN fails, the code stays plain. Only text is recoloured: authored
                  spans (.hl .bad .mark .gap .cm) are kept exactly where they are,
                  and the text inside .mark .gap .cm is left alone. <pre class="output">
                  is never highlighted.                                            */

(function () {
  function resolvedTheme() {
    var explicit = document.documentElement.getAttribute('data-theme');
    if (explicit) return explicit;
    return matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function syncToggle() {
    var btn = document.querySelector('button.theme-toggle');
    if (!btn) return;
    var dark = resolvedTheme() === 'dark';
    var icon = btn.querySelector('.theme-toggle-icon');
    var label = btn.querySelector('.theme-toggle-label');
    if (icon) icon.textContent = dark ? '☀' : '☾';
    if (label) label.textContent = dark ? 'Light' : 'Dark';
    btn.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
  }

  window.toggleTheme = function () {
    var next = resolvedTheme() === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem('teach-me-theme', next); } catch (e) {}
    syncToggle();
  };

  window.checkAnswer = function (btn, correct) {
    var quiz = btn.closest('.quiz');
    var buttons = quiz.querySelectorAll('.quiz-options button');
    buttons.forEach(function (b) { b.disabled = true; b.classList.remove('correct', 'incorrect'); });
    btn.classList.add(correct ? 'correct' : 'incorrect');
    quiz.querySelectorAll('.quiz-feedback').forEach(function (f) { f.classList.remove('visible'); });
    var feedback = quiz.querySelector('.quiz-feedback.' + (correct ? 'correct' : 'incorrect'));
    if (feedback) feedback.classList.add('visible');
  };

  function updateSorterScore(sorter) {
    var items = sorter.querySelectorAll('.sort-item');
    var answered = sorter.querySelectorAll('.sort-item[data-result]');
    var right = sorter.querySelectorAll('.sort-item[data-result="correct"]');
    var score = sorter.querySelector('.sort-score');
    if (!score) return;
    score.textContent = answered.length === items.length
      ? right.length + ' of ' + items.length + ' correct'
      : answered.length + ' of ' + items.length + ' answered';
  }

  function initSorters() {
    document.querySelectorAll('.sorter').forEach(function (sorter) {
      var cats = (sorter.getAttribute('data-categories') || '').split('|');
      sorter.querySelectorAll('.sort-item').forEach(function (item) {
        var row = document.createElement('div');
        row.className = 'sort-buttons';
        cats.forEach(function (cat) {
          var b = document.createElement('button');
          b.type = 'button';
          b.textContent = cat;
          b.addEventListener('click', function () {
            var answer = item.getAttribute('data-answer');
            var ok = cat === answer;
            row.querySelectorAll('button').forEach(function (x) {
              x.disabled = true;
              if (x.textContent === answer) x.classList.add('correct');
            });
            if (!ok) b.classList.add('incorrect');
            item.setAttribute('data-result', ok ? 'correct' : 'incorrect');
            var fb = document.createElement('div');
            fb.className = 'sort-feedback ' + (ok ? 'correct' : 'incorrect');
            fb.textContent = (ok ? 'Correct. ' : 'Not quite: ' + answer + '. ') + (item.getAttribute('data-why') || '');
            item.appendChild(fb);
            updateSorterScore(sorter);
          });
          row.appendChild(b);
        });
        item.appendChild(row);
      });
      var score = document.createElement('div');
      score.className = 'sort-score';
      sorter.appendChild(score);
      updateSorterScore(sorter);
    });
  }

  function escapeHtml(text) {
    return String(text == null ? '' : text)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  /* The page's path back to the workspace root. data-root="" is a valid
     value (the course home), so test for the attribute, not its truthiness. */
  function rootOf(el) {
    return el && el.hasAttribute('data-root') ? el.getAttribute('data-root') : '../';
  }

  function initCourseMap() {
    var nav = document.querySelector('.course-map');
    var course = window.COURSE;
    if (!nav || !course || !course.lessons) return;
    var current = parseInt(nav.getAttribute('data-current') || '0', 10);
    var root = rootOf(nav);
    var isHome = root === '';
    // On the course home the map is the page's main content: a plain section
    // with a heading. On lesson pages it is a collapsed aside at the foot.
    var html = isHome
      ? '<h2 id="course-map">Course map</h2>'
      : '<details><summary>Course map · ' + course.lessons.length + ' lessons</summary>';
    if (isHome) nav.classList.add('course-map-home');

    // Consecutive lessons that share a "part" label are grouped under it.
    var groups = [];
    course.lessons.forEach(function (lesson) {
      var part = lesson.part || '';
      var last = groups[groups.length - 1];
      if (!last || last.part !== part) groups.push({ part: part, lessons: [lesson] });
      else last.lessons.push(lesson);
    });
    groups.forEach(function (group) {
      html += '<div class="course-part">';
      if (group.part) html += '<div class="course-part-title">' + escapeHtml(group.part) + '</div>';
      html += '<ol>';
      group.lessons.forEach(function (lesson) {
        var cls = lesson.n === current ? 'current' : (current && lesson.n < current ? 'done' : '');
        html += '<li value="' + lesson.n + '"' + (cls ? ' class="' + cls + '"' : '') +
          (lesson.n === current ? ' aria-current="page"' : '') + '>' +
          '<a href="' + root + 'lessons/' + encodeURI(lesson.file) + '">' + escapeHtml(lesson.title) + '</a>';
        if (lesson.win) html += '<span class="course-win">' + escapeHtml(lesson.win) + '</span>';
        html += '</li>';
      });
      html += '</ol></div>';
    });

    if (course.references && course.references.length) {
      html += '<div class="course-part course-refs"><div class="course-part-title">Reference</div>';
      if (isHome) html += '<p class="course-refs-note">Not part of the lesson sequence. These sheets ' +
        'stand on their own: keep them open while you work on your own skills, long after the course.</p>';
      html += '<ul>';
      course.references.forEach(function (ref) {
        html += '<li><a href="' + root + 'reference/' + encodeURI(ref.file) + '">' + escapeHtml(ref.title) + '</a></li>';
      });
      html += '</ul>';
      if (course.downloads && course.downloads.length) {
        html += '<div class="course-downloads-title">Optional extras: the skills behind this course</div><ul class="course-downloads">';
        course.downloads.forEach(function (dl) {
          html += '<li><a href="' + root + encodeURI(dl.file) + '" download>' + escapeHtml(dl.title) +
            '</a> <span class="course-download-size">zip · ' + escapeHtml(dl.size) + '</span>' +
            (dl.note ? '<span class="course-win">' + escapeHtml(dl.note) + '</span>' : '') + '</li>';
        });
        html += '</ul>';
      }
      html += '</div>';
    }
    if (!isHome) html += '<p><a href="' + root + 'index.html">Course home</a></p></details>';
    nav.innerHTML = html;
  }

  /* Home button: on every page except the course home, a link back to it,
     fixed just below the theme toggle and styled to match it. */
  function initHomeButton() {
    var nav = document.querySelector('.course-map');
    var root = nav ? rootOf(nav) : '../';
    if (root === '') return;
    var link = document.createElement('a');
    link.className = 'theme-toggle home-button';
    link.href = root + 'index.html';
    link.setAttribute('aria-label', 'Course home');
    link.innerHTML = '<span class="theme-toggle-icon" aria-hidden="true">⌂</span>' +
      '<span class="theme-toggle-label">Home</span>';
    var toggle = document.querySelector('button.theme-toggle');
    if (toggle) toggle.insertAdjacentElement('afterend', link);
    else document.body.insertBefore(link, document.body.firstChild);
  }

  function minutesLabel(seconds) {
    var minutes = Math.max(1, Math.round(seconds / 60));
    if (minutes < 60) return minutes + ' min';
    return Math.floor(minutes / 60) + ' h ' + (minutes % 60) + ' min';
  }

  function videoSourceFor(slot) {
    var explicit = slot.getAttribute('data-src');
    if (explicit) return explicit;
    if (slot.getAttribute('data-video') === 'course') {
      var course = window.COURSE;
      if (!course || !course.video) return '';
      return /^https?:/.test(course.video) ? course.video : rootOf(slot) + course.video;
    }
    var file = decodeURIComponent(location.pathname.split('/').pop() || '');
    var stem = file.replace(/\.html?$/i, '');
    if (!stem || stem === 'index') return '';
    return '../videos/' + stem + '/' + stem + '.mp4';
  }

  function initVideoSlots() {
    document.querySelectorAll('.lesson-video').forEach(function (slot) {
      var video = slot.querySelector('video');
      var src = videoSourceFor(slot);
      if (!video || !src) return;
      video.addEventListener('loadedmetadata', function () {
        slot.hidden = false;
        // A slot wrapped in a .video-section (heading + note) shows with it.
        var section = slot.closest('.video-section');
        if (section) section.hidden = false;
        var length = slot.querySelector('.lesson-video-length');
        if (length && isFinite(video.duration)) length.textContent = minutesLabel(video.duration);
      });
      // Use the poster only if it exists, so a missing image never shows as broken.
      var course = window.COURSE;
      var posterSrc = slot.getAttribute('data-video') === 'course' && course && course.videoPoster
        ? rootOf(slot) + course.videoPoster
        : src.replace(/[^/]+$/, 'poster.png');
      var probe = new Image();
      probe.onload = function () { video.poster = posterSrc; };
      probe.src = posterSrc;
      video.src = src;
    });
  }

  function initContinuePrompt() {
    document.querySelectorAll('.continue-prompt').forEach(function (el) {
      el.addEventListener('click', function () {
        var range = document.createRange();
        range.selectNodeContents(el);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        try { navigator.clipboard.writeText(el.textContent.trim()); } catch (e) {}
      });
    });
  }

  /* ── Syntax highlighting ──────────────────────────────────── */
  var HLJS_BASE = 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/';
  var HLJS_SRI = 'sha384-F/bZzf7p3Joyp5psL90p/p89AZJsndkSoGwRpXcZhleCWhd8SnRuoYo4d0yirjJp';
  var OPAQUE = '.mark, .gap, .cm';

  function loadScript(src, integrity, done) {
    var s = document.createElement('script');
    s.src = src;
    if (integrity) s.integrity = integrity;
    s.crossOrigin = 'anonymous';
    s.referrerPolicy = 'no-referrer';
    s.onload = function () { done(true); };
    s.onerror = function () { done(false); };
    document.head.appendChild(s);
  }

  function languageOf(code) {
    var m = /(?:^|\s)language-([\w-]+)/.exec(code.className);
    return m ? m[1] : '';
  }

  /* highlight.js's markdown grammar does not know YAML front matter, so a
     markdown block that opens with --- … --- has that part highlighted as YAML. */
  function highlightSource(hljs, source, lang) {
    var opts = function (l) { return { language: l, ignoreIllegals: true }; };
    if (lang === 'markdown' && hljs.getLanguage('yaml')) {
      var fm = /^---\n[\s\S]*?\n---(?:\n|$)/.exec(source);
      if (fm) return hljs.highlight(fm[0], opts('yaml')).value +
        hljs.highlight(source.slice(fm[0].length), opts('markdown')).value;
    }
    return hljs.highlight(source, opts(lang)).value;
  }

  /* Highlight the text, then pour the coloured result back into the block's own
     text nodes, so every authored span survives untouched. */
  function highlightBlock(hljs, code, lang) {
    var nodes = [];
    var walker = document.createTreeWalker(code, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        var o = n.parentElement && n.parentElement.closest(OPAQUE);
        return o && code.contains(o) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      }
    });
    while (walker.nextNode()) nodes.push(walker.currentNode);
    var source = nodes.map(function (n) { return n.nodeValue; }).join('');
    if (!source.trim()) return;

    var tpl = document.createElement('template');
    tpl.innerHTML = highlightSource(hljs, source, lang);
    var segs = [];
    (function flatten(node, cls) {
      node.childNodes.forEach(function (c) {
        if (c.nodeType === 3) segs.push({ text: c.nodeValue, cls: cls });
        else if (c.nodeType === 1) flatten(c, c.className || cls);
      });
    })(tpl.content, '');
    if (segs.map(function (s) { return s.text; }).join('') !== source) return;

    var si = 0, so = 0;
    var frags = nodes.map(function (n) {
      var frag = document.createDocumentFragment();
      var left = n.nodeValue.length;
      while (left > 0) {
        var seg = segs[si];
        var take = Math.min(left, seg.text.length - so);
        var piece = seg.text.substr(so, take);
        if (seg.cls) {
          var span = document.createElement('span');
          span.className = seg.cls;
          span.textContent = piece;
          frag.appendChild(span);
        } else {
          frag.appendChild(document.createTextNode(piece));
        }
        left -= take; so += take;
        if (so === seg.text.length) { si++; so = 0; }
      }
      return frag;
    });
    nodes.forEach(function (n, i) { n.parentNode.replaceChild(frags[i], n); });
  }

  function initHighlighting() {
    var blocks = Array.prototype.filter.call(
      document.querySelectorAll('pre:not(.output) > code[class*="language-"]'),
      function (code) { return languageOf(code); });
    if (!blocks.length) return;
    function run() {
      var hljs = window.hljs;
      if (!hljs) return;
      blocks.forEach(function (code) {
        var lang = languageOf(code);
        if (!hljs.getLanguage(lang) || code.hasAttribute('data-highlighted')) return;
        try { highlightBlock(hljs, code, lang); code.setAttribute('data-highlighted', lang); } catch (e) {}
      });
    }
    if (window.hljs) run();
    else loadScript(HLJS_BASE + 'highlight.min.js', HLJS_SRI, function (ok) { if (ok) run(); });
  }

  function init() {
    syncToggle();
    initHighlighting();
    matchMedia('(prefers-color-scheme: dark)').addEventListener('change', syncToggle);
    initSorters();
    initCourseMap();
    initHomeButton();
    initVideoSlots();
    initContinuePrompt();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
