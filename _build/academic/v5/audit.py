# Components added for the hiring-panel audit (Prompt 02). Imported by compose.py.
# Every block here renders nothing until its data exists, so nothing unconfirmed reaches the live page.
import json, os, html
H = os.path.dirname(os.path.abspath(__file__))
J = lambda n: json.load(open(os.path.join(H, n), encoding='utf-8'))
F = J('flags.json')
esc = html.escape

# ---------- D. teaching evidence (MNU Subject and Teaching Evaluation, Section B) ----------
TERMS = [  # term, modules, Muiz %, School %
    ('Term 2 2024', 'Modules not named in the report', 93.83, 84.86),
    ('Term 1 2025', 'BUS301 · MKT213 · MKT215 · MKT217', 84.17, 84.83),
    ('Term 2 2025', 'BUS107 · BUS301 · MKT217 · MKT301', 81.63, 84.58),
    ('Term 1 2026', 'MKT101 · MKT301 · MKT303 · MKT309', 87.17, 84.02),
]
NOTE = {'Term 2 2025': 'My heaviest term: four modules, two of them new to me, and 18 contact hours a week.'}
AREAS = [('Planning and preparation', 85.52, 83.94), ('Teaching and learning', 88.08, 83.54),
         ('Interaction and responsiveness', 87.92, 84.57), ('Content', 87.55, 84.16),
         ('Assessment', 89.13, 84.86), ('Resources', 88.44, 83.71)]
f5 = lambda p: round(p / 20 + 1e-9, 1)
pct = lambda v: '%.2f%%' % (v / 5 * 100)

def tag(a, b):
    a, b = f5(a), f5(b)
    if a > b: return ('up', 'Above school average')
    if a < b: return ('down', 'Below school average')
    return ('eq', 'Level with school average')

def pair(me, sc, small=False):
    m, s = f5(me), f5(sc)
    return ('<div class="eq-bars%s">' % (' sm' if small else '') +
            '<div class="eq-bar me"><span class="eq-who">Me</span><span class="eq-track"><i style="width:%s"></i></span><b>%.1f</b></div>' % (pct(m), m) +
            '<div class="eq-bar sc"><span class="eq-who">School</span><span class="eq-track"><i style="width:%s"></i></span><b>%.1f</b></div>' % (pct(s), s) +
            '</div>')

ICON = {'up': '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M6 2 11 9H1z"/></svg>',
        'down': '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M6 10 1 3h10z"/></svg>',
        'eq': '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M1 4h10v1.6H1zM1 7h10v1.6H1z"/></svg>'}

def evidence(full=True):
    if not F['evaluation_on']: return ''
    t1 = TERMS[-1]
    rows = ''
    for t, mods, me, sc in TERMS:
        k, lab = tag(me, sc)
        rows += ('<li class="eq-term"><div class="eq-tl"><b>%s</b><small>%s</small></div>%s<span class="eq-tag %s">%s%s</span>%s</li>'
                 % (t, mods, pair(me, sc), k, ICON[k], lab, ('<p class="eq-note">%s</p>' % NOTE[t]) if t in NOTE else ''))
    areas = ''
    if full:
        areas = ('<div class="eq-areas"><h3>Above the school average in all six areas, Term 1 2026<span>.</span></h3><ul>' +
                 ''.join('<li><span class="eq-an">%s</span>%s</li>' % (n, pair(a, b, True)) for n, a, b in AREAS) + '</ul></div>')
    tbl = ('<table><caption>Students’ rating of my teaching out of 5, against the Business School average</caption>'
           '<thead><tr><th scope="col">Term</th><th scope="col">Me</th><th scope="col">Business School</th><th scope="col">Comparison</th></tr></thead><tbody>' +
           ''.join('<tr><th scope="row">%s</th><td>%.1f</td><td>%.1f</td><td>%s</td></tr>' % (t, f5(me), f5(sc), tag(me, sc)[1]) for t, _, me, sc in TERMS) +
           '</tbody></table>')
    if full:
        tbl += ('<table><caption>Term 1 2026 by area, out of 5</caption><thead><tr><th scope="col">Area</th><th scope="col">Me</th><th scope="col">Business School</th></tr></thead><tbody>' +
                ''.join('<tr><th scope="row">%s</th><td>%.1f</td><td>%.1f</td></tr>' % (n, f5(a), f5(b)) for n, a, b in AREAS) + '</tbody></table>')
    return ('<div class="eq panel reveal" id="evq">'
            '<div class="eq-hero"><p class="eq-big"><b>%.1f</b> <span>out of 5</span><i class="eq-dot" aria-hidden="true"></i></p>'
            '<p class="eq-cap">Students’ rating of my teaching, %s. Business School average: %.1f.</p></div>'
            '<div class="eq-key" aria-hidden="true"><span><i class="k-me"></i>Me</span><span><i class="k-sc"></i>Business School average</span><span class="eq-axis">Scale 0 to 5</span></div>'
            '<ol class="eq-terms" aria-hidden="true">%s<li class="eq-ax"><span></span><span class="eq-ticks"><i>0</i><i>1</i><i>2</i><i>3</i><i>4</i><i>5</i></span><span></span></li></ol>%s%s'
            '<p class="src">Source: MNU Subject and Teaching Evaluation lecturer reports, Term 2 2024 to Term 1 2026. '
            'Section B, “Teaching and learning”.</p><p class="src eq-fn">Scores out of 5 are converted from MNU’s percentage scores (score ÷ 20).</p></div>'
            % (f5(t1[2]), t1[0], f5(t1[3]), rows, ('<div aria-hidden="true">' + areas + '</div>') if areas else '', '<div class="sr-only">' + tbl + '</div>'))

# ---------- E. student comments (render nothing until real ones exist) ----------
# comments.json: one entry per former student, built for about ten. Fields:
#   who          degree only, never a name, e.g. "Bachelor of Marketing graduate"
#   modules      module codes the student took with me, e.g. ["MKT213", "MKT303"]
#   year         graduation or study year
#   theme        2-4 word tag for what the comment is about
#   pull         the strongest 20-45 words, verbatim (ellipsis allowed); shown on the card
#   full         the whole comment, verbatim, as a list of paragraphs
#   ask          optional: what they'd like more of, in a short paraphrase
#   featured     optional true: shown on the home page (keep it to 3)
#   module_quote optional {code: verbatim excerpt} for that module's page (up to 3 per module are shown)
HOME_MAX, MOD_MAX = 3, 3

def _cmts():
    C = [c for c in J('comments.json') if c.get('pull')]   # no student names are stored or shown
    for c in C:
        n = len(c['pull'].split())
        if n > 50: print('comments.json: pull quote over 50 words (%d):' % n, c['theme'])
    C.sort(key=lambda c: (not c.get('featured'), -int(c.get('year', 0))))
    return C

def _who(c):
    return '%s · %s · %s' % (esc(c['who']), ', '.join(c['modules']), c['year'])

def _card(c):
    more = ''.join('<p>%s</p>' % esc(x) for x in c['full'])
    return ('<figure class="cmt reveal" data-mods="%s"><span class="cmt-theme">%s</span><blockquote>“%s”</blockquote>'
            '<figcaption><span>%s</span></figcaption>'
            '<details class="cmt-more"><summary>Read the full comment</summary><div>%s</div></details></figure>'
            % (' '.join(c['modules']), esc(c['theme']), esc(c['pull']), _who(c), more))

def comments(full=False):
    C = _cmts()
    if not C: return ''
    note = ('<p class="src">Unedited comments from former students, given when I asked for feedback for this portfolio and shared with their permission. Names withheld.</p>')
    if not full:
        show = [c for c in C if c.get('featured')][:HOME_MAX] or C[:HOME_MAX]
        more = ('<a class="more-link" href="academic/teaching.html#comments">Read all %d comments <i data-ic="right"></i></a>' % len(C)) if len(C) > len(show) else ''
        return ('<div class="cmt-wrap"><span class="label">In their own words</span><div class="cmts">' + ''.join(map(_card, show)) +
                '</div>' + note + more + '</div>')
    mods = sorted({m for c in C for m in c['modules']})
    chips = ''
    if len(C) > 3 and len(mods) > 1:
        chips = ('<div class="cmt-filter" role="group" aria-label="Filter comments by module"><button type="button" aria-pressed="true" data-m="">All <small>%d</small></button>' % len(C) +
                 ''.join('<button type="button" aria-pressed="false" data-m="%s">%s <small>%d</small></button>' % (m, m, sum(m in c['modules'] for c in C)) for m in mods) + '</div>')
    asks = [c for c in C if c.get('ask')]
    askp = ''
    if asks:
        askp = ('<div class="panel reveal cmt-asks"><h3>What they’d like more of<span>.</span></h3><ul>' +
                ''.join('<li><span>%s</span><small>%s</small></li>' % (esc(c['ask']), ', '.join(c['modules'])) for c in asks) +
                '</ul></div>')
    return ('<div class="cmt-wrap" id="comments"><span class="label">In their own words · %d former student%s</span>' % (len(C), '' if len(C) == 1 else 's') + chips +
            '<div class="cmts cmts-all">' + ''.join(map(_card, C)) + '</div>' + note + askp + '</div>')

def module_comment(code):
    Q = [(c, c['module_quote'][code]) for c in _cmts() if c.get('module_quote', {}).get(code)][:MOD_MAX]
    if not Q: return ''
    return ('<article class="panel reveal mt-cmt"><h2>%s<span>.</span></h2>' % ('A student remembers' if len(Q) == 1 else 'Students remember') +
            ''.join('<figure><blockquote>“%s”</blockquote><figcaption class="src">%s</figcaption></figure>' % (esc(q), _who(c)) for c, q in Q) + '</article>')

# ---------- F. tool impact rows (only numbers Muiz has signed off) ----------
def toolstats(tool):
    T = J('toolstats.json')
    if not T.get('signed_off'): return ''
    t = T['tools'].get(tool)
    if not t or not t.get('items'): return ''
    return ('<div class="tstats"><span class="label">%s · cohort use</span><ul>' % esc(t.get('name', tool.upper())) + ''.join('<li><b>%s</b><span>%s</span></li>' % (esc(a), esc(b)) for a, b in t['items']) +
            '</ul><p class="src">%s. Source: tool usage data.</p></div>' % esc(t['period']))

# ---------- C2. at a glance ----------
SCH = 'https://iocdrp.s.gy/fuad-a-m'
def glance(mobile=False):
    ev = ('4.4 out of 5 for teaching, Term 1 2026 (school average 4.2)' if F['evaluation_scale_confirmed']
          else '87 out of 100 for teaching, Term 1 2026 (school average 84)')
    items = [('Qualifications', 'MSc Global Marketing Management (Merit) · BA (Hons) Tourism Management, Asia Pacific University'),
             ('Teaching', 'Lecturer, MNU Business School, since 2024 · part-time at MI College, 2022 to 2024'),
             ('Modules', '9 taught, 6 coordinated, Level 100 to 300'),
             ('Research', '2 peer-reviewed journal articles · <a href="%s" target="_blank" rel="noopener">36 citations</a>' % SCH)]
    if F['evaluation_on']: items.append(('Student evaluation', ev))
    return ('<div class="atg%s"%s><%s class="atg-h">At a glance</%s><dl>' % ((' atg-m', '', 'h2', 'h2') if mobile else ('', ' id="glance"', 'h2', 'h2')) +
            ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % x for x in items) + '</dl></div>')

# ---------- H. service, supervision, development, referees, demo video ----------
SERVICE = ['Subject coordinator for six modules',
           'Assessment validation for coordinated subjects',
           'Peer evaluation of two colleagues’ teaching (2025)',
           'Member, MNU Business School Marketing Committee',
           'Member, MSME Awards committee (Business Centre Corporation, with MIRA, the Ministry and MNU), 2025',
           'Exam paper setting and moderation, including the combined MKT101 paper with a co-lecturer']
def service():
    sup = ['Undergraduate applied projects: learning-contract advice, progress meetings, report review and presentation coaching.',
           'Three applied projects supervised to completion (2025 to 2026), three in progress.',
           'Featured: <i>Safe Steps</i>, a child-safety campaign for a national ministry.']
    pd = J('development.json')
    out = ('<div class="svc reveal"><div class="panel"><h3>Service and academic citizenship<span>.</span></h3><ul class="ticks">' +
           ''.join('<li>%s</li>' % x for x in SERVICE) + '</ul></div>'
           '<div class="panel"><h3>Supervision<span>.</span></h3><ul class="ticks">' + ''.join('<li>%s</li>' % x for x in sup) + '</ul></div>')
    if pd:
        out += '<div class="panel"><h3>Professional development<span>.</span></h3><ul class="ticks">' + ''.join('<li>%s</li>' % esc(x) for x in pd) + '</ul></div>'
    return out + '</div>'

def referees():
    R = J('referees.json')
    if len(R) < 2: return 'Referees available on request.'
    return 'Referees: ' + '; '.join('%s, %s, %s' % (esc(r['name']), esc(r['title']), esc(r['institution'])) for r in R) + '.'

def demo_video(B=''):
    v = F.get('demo_video')
    if not v: return ''
    return ('<figure class="demo-vid reveal"><video controls preload="none" playsinline poster="%s"><source src="%s" type="video/mp4">'
            '<track kind="captions" src="%s" srclang="en" label="English" default></video>'
            '<figcaption>The full lesson, %s. Captions on.</figcaption></figure>' % (v['poster'], v['src'], v['captions'], v['length']))

# ---------- F2. class-activity snapshot on the home tools section (figures already published on the activity page) ----------
def snapshot(tools_html):
    import re
    src = open(os.path.join(H, 'activity_body.html'), encoding='utf-8').read()
    D = json.loads(re.search(r'const DATA=(\{.*?\});?\n', src).group(1))
    C = json.loads(re.search(r'A303=(\{.*?\});\n', src).group(1))
    a, b = D['mkt101'], D['mkt301']
    used, roster = a['active'] + b['active'] + C['started'], a['roster'] + b['roster'] + C['roster']
    m3 = {d: x + y + z for d, x, y, z in C['daily']}
    days = [(x['d'], x['act'], b['daily'][i]['act'], m3.get(x['d'], 0)) for i, x in enumerate(a['daily'])]
    mx = max(sum(d[1:]) for d in days)
    peak = max(days, key=lambda d: sum(d[1:]))
    md = lambda d: '%d %s' % (int(d[8:]), ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][int(d[5:7]) - 1])
    W, Hh, n = 300, 96, len(days); bw = W / n
    cols = ['var(--cta)', 'var(--sea)', 'var(--deep)']
    bars = ''
    for i, d in enumerate(days):
        y = Hh
        for j, v in enumerate(d[1:]):
            if not v: continue
            h = v / mx * (Hh - 14); y -= h
            bars += '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="1.5" fill="%s"/>' % (i * bw + bw * .16, y, bw * .68, h, cols[j])
    pi = days.index(peak)
    spark = ('<svg class="snap-bars" viewBox="0 0 %d %d" aria-hidden="true" preserveAspectRatio="none">%s<line x1="0" y1="%d" x2="%d" y2="%d" stroke="var(--line)"/></svg>'
             '<div class="snap-axis"><span>%s</span><span>%s</span></div>' % (W, Hh, bars, Hh, W, Hh, md(days[0][0]), md(days[-1][0])))
    reach = [('MKT101 Arena', a['active'], a['roster'], 'used it', cols[0]), ('MKT301 Arena', b['active'], b['roster'], 'used it', cols[1]),
             ('MKT303 Audit', C['started'], C['roster'], 'started an audit', cols[2])]
    rows = ''.join('<li><span class="snap-n">%s</span><span class="snap-track"><i style="width:%d%%;background:%s"></i></span><b>%d<small> / %d</small></b></li>'
                   % (nm, round(x / r * 100), c, x, r) for nm, x, r, _, c in reach)
    card = ('<a class="snap panel lift reveal" href="academic/tools.html#class-activity">'
            '<div class="snap-l"><span class="label">Class activity · %s to %s 2026</span>'
            '<p class="snap-big"><b>%d</b><span> of %d students</span></p><p class="snap-cap">used a tool in two weeks</p>'
            '<ul class="snap-kpis"><li><b>%.0f h</b><span>of practice</span></li><li><b>%s</b><span>practice actions</span></li><li><b>%d</b><span>business audits submitted</span></li></ul></div>'
            '<div class="snap-m"><span class="snap-h">Activity each day</span>%s<div class="snap-leg"><span><i style="background:var(--cta)"></i>MKT101 students</span><span><i style="background:var(--sea)"></i>MKT301 students</span><span><i style="background:var(--deep)"></i>MKT303 audit steps</span></div><p class="snap-peak">Busiest day: %s, %d students practising</p></div>'
            '<div class="snap-r"><span class="snap-h">Reach by tool</span><ul class="snap-reach">%s</ul></div>'
            '<span class="snap-cta more-link">See the full class activity <i data-ic="right"></i></span>'
            '<span class="sr-only">%d of %d enrolled students used a tool between %s and %s 2026. MKT101 Arena %d of %d, MKT301 Arena %d of %d, MKT303 audit started by %d of %d. Busiest day %s.</span></a>'
            % (md(days[0][0]), md(days[-1][0]), used, roster, a['hrs'] + b['hrs'], '{:,}'.format(a['ans'] + b['ans']), C['submitted'],
               spark, md(peak[0]), sum(peak[1:]), rows,
               used, roster, md(days[0][0]), md(days[-1][0]), a['active'], a['roster'], b['active'], b['roster'], C['started'], C['roster'], md(peak[0])))
    old = re.search(r'      <p class="tool-note reveal">.*?</p>\n', tools_html, re.S)
    assert old, 'tool-note not found'
    return tools_html.replace(old.group(0), '      ' + card + '\n', 1)
