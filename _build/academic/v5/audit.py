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
            '<ol class="eq-terms" aria-hidden="true">%s</ol>%s%s'
            '<p class="src">Source: MNU Subject and Teaching Evaluation lecturer reports, Term 2 2024 to Term 1 2026. '
            'Section B, “Teaching and learning”. Converted from MNU’s percentage scores (score ÷ 20).</p></div>'
            % (f5(t1[2]), t1[0], f5(t1[3]), rows, ('<div aria-hidden="true">' + areas + '</div>') if areas else '', '<div class="sr-only">' + tbl + '</div>'))

# ---------- E. student comments (render nothing until real ones exist) ----------
def comments():
    C = [c for c in J('comments.json') if c.get('comment') and c.get('name')]
    if not C: return ''
    cards = ''
    for c in C:
        first = c['name'].split()[0]
        ph = ('<img src="%s" alt="Photo of %s" width="64" height="64" loading="lazy">' % (esc(c['photo']), esc(first))) if c.get('photo') else ''
        cards += ('<figure class="cmt reveal">%s<blockquote>%s</blockquote><figcaption><b>%s</b><span>%s · %s · %s</span></figcaption></figure>'
                  % (ph, esc(c['comment']), esc(c['name']), esc(c.get('programme', '')), esc(c.get('module', '')), esc(str(c.get('year', '')))))
    return ('<div class="cmts">' + cards + '</div><p class="src">Comments from former students, shared with their permission.</p>')

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
             ('Teaching', 'Lecturer, MNU Business School, since 2024 · part-time at MI College from 2022'),
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
           'One applied project supervised to completion in 2025 (a marketing campaign designed to be implemented)' +
           ('; %s further students supervised to completion in 2026.' % F['supervision_2026_completed'] if F.get('supervision_2026_completed') else '.')]
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
