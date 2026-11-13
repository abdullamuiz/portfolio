"""Compose the v5 page bodies from body.html (v4 single page) plus new fragments.
Writes v5/out/<name>.html body fragments; build5.py wraps them into full pages."""
import re, json, os
H = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(H, *a)
src = open(P('..', 'body.v4.html'), encoding='utf-8').read()
rd = lambda n: open(P(n), encoding='utf-8').read()

# ---------- facts from the CV (Muiz_Fuad_CV, Nov 2026) ----------
SCH = 'https://iocdrp.s.gy/fuad-a-m'
import sys; sys.path.insert(0, H); import audit as AU
from modtext import MODTEXT
SCHOLAR = '<a class="orcid" href="%s" target="_blank" rel="noopener"><svg class="orcid-ic" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="12" fill="#4285F4"/><path fill="#fff" d="M12 5 4.5 10.6h3.1a4.5 4.5 0 1 0 8.8 0h3.1L12 5Zm0 11.3a2.6 2.6 0 1 1 0-5.2 2.6 2.6 0 0 1 0 5.2Z"/></svg><span><b>Google Scholar</b> Fuad, A. M.</span></a>' % SCH
FIX = [
 ('<p>I came from industry. In marketing management roles I sat on the other side of the desk, interviewing graduates. The knowledge was there, but when a real question came there was no reference point, and minds went blank. So I teach students to meet that manager, and surprise them.</p>',
  '<p>I was fortunate. Asia Pacific University was set up like a business: we dressed professionally for every class and worked in teams, in spaces built like today’s co-working offices. The lecturers who met us there brought years of industry experience, and through them we saw a fragment of the real world before we stepped into it. The setting gave us the experience while the classroom gave us the theory, and we learned to use both together.</p><p>Later, in marketing management roles, I sat on the other side of the desk, interviewing graduates. The knowledge was there, but when a real question came there was no reference point, and minds went blank. So my students meet that manager in class first. I train them to walk into the real interview with an ace up their sleeve.</p>'),
 ('<span class="todo">[TODO: Google Scholar link]</span>', SCHOLAR),
 ('<span class="todo">[TODO: check Scopus / Web of Science status of both journals; state it only if true]</span>', ''),
 ('Chia, K. W. and Muiz, A. · <i style="font-style:italic">Tourism and Hospitality Research</i>, SAGE · cited 36+ times', 'Chia, K. W. and Muiz, A. · <i style="font-style:italic">Tourism and Hospitality Research</i>, 21(1), 3–14 · SAGE · cited 36 times</span><span class="pub-ix">Indexed in Scopus and Web of Science (ESCI)'),
 ('Pappayah, P. P. C. M., Muiz, A. and Jinus, D. J. · Common Ground</span><span class="todo">[TODO: confirm journal name on the CG Scholar page: Journal of Tourism and Leisure Studies, or The International Journal of Tourism and Hospitality Administration]</span>',
  'CM Pappayah, P. P., Muiz, A. and Jinus, D. J. · <i style="font-style:italic">Journal of Tourism and Leisure Studies</i>, 2(2), 11–20 · Common Ground Research Networks</span>'),
 ('https://cgscholar.com/bookstore/works/increasing-the-visibility-of-guesthouse-operation-in-the-maldives-through-emarketing?category_id=cgrn', 'https://doi.org/10.18848/2470-9336/CGP/v02i02/11-20'),
 ('<em>View on CG Scholar ↗</em>', '<em>Read via DOI ↗</em>'),
 ('<em>Read via DOI ↗</em></span>\n        </a>\n      </div>', '<em>Read via DOI ↗</em></span>\n        </a>\n      </div>\n      <p class="small pub-as reveal">Published as A. Muiz.</p>'),
 ('<span class="bk-j">Common Ground</span>', '<span class="bk-j">Journal of Tourism and Leisure Studies</span>'),
 ('<time>2011 – 2013</time><b>Senior Marketing Executive</b>', '<time>2011 – 2013</time><b>Marketing Officer</b>'),
 ('<b>Team Lead, Maldives Promotions</b><span>MATTA Fair, Kuala Lumpur · MP World Travel &amp; Tours</span>', '<b>Head of Marketing and Sales</b><span>MATTA Fair, Kuala Lumpur · MP Travel and Tours</span>'),
 ('<span class="label">Team Lead, Maldives Promotions · 2014 to 2018</span>', '<span class="label">Promoter to Head of Marketing and Sales · 2014 to 2018</span>'),
 ('I started as a junior sales host and went on to lead the sales team for Maldives packages, grouping packages by type of traveller and designing the sales conversation.',
  'I started as a promoter in 2014 and was Head of Marketing and Sales for MP Travel and Tours by 2017, grouping packages by type of traveller and designing the sales conversation.'),
 ('aria-label="Mianz College logo"></span><time>2022 – 2023</time><b>Part-time Lecturer</b><span>Mianz College</span>', 'aria-label="MI College logo"></span><time>2022 – 2024</time><b>Part-time Lecturer</b><span>MI College</span>'),
 ('I started teaching part-time at Mianz College in 2022', 'I started teaching part-time at MI College in 2022'),
 ('<h3>Mianz College</h3><p class="ink">Part-time lecturer, 2022 to 2023.</p>', '<h3>MI College</h3><p class="ink">Part-time lecturer, 2022 to 2024, for master’s and undergraduate cohorts, online and in person.</p>'),
 ('<ul class="subj"><li>Digital marketing</li><li>E-commerce</li></ul>', '<ul class="subj"><li>Digital Marketing &amp; Ecommerce · Master’s, level 500</li><li>Supply Chain Management · level 300</li><li>Introduction to Marketing and Communication · level 100</li></ul>'),
 ('\n        <span class="todo">[TODO: confirm the subjects taught there, and whether the name should read “Mianz International College”]</span>', ''),
 ('<span class="todo">[TODO: arena usage numbers (students, sessions, completion). No number is shown until supplied.]</span>', 'In two weeks (28 Oct to 11 Nov 2026), 75 of 101 enrolled students used the tools: 80 hours of practice, 7,919 practice actions and 3 full business audits. <a class="more-link" href="#class-activity">See the anonymised class activity <i data-ic="down"></i></a>'),
 ('        <article class="panel reveal" style="--rd:.08s">\n          <span class="label">Research direction · intended doctoral focus</span>\n          <h3>How small tourism enterprises in the Maldives are found, and chosen, when AI tools make the recommendation.</h3>\n          <ol class="qs">\n            <li>How visible are small Maldivian tourism businesses in AI-generated travel recommendations, compared with larger competitors?</li>\n            <li>What stops them from adapting: skills, resources, or dependence on booking platforms?</li>\n            <li>Can a simple diagnostic help owners see the gap and act on it?</li>\n          </ol>\n          <p>Working title: “From Friction to Flow”. <span class="todo">[TODO: keep or change]</span></p>\n          <p>Frameworks under consideration: technology-organisation-environment (TOE) and AI maturity, in a small-island context.</p>\n        </article>', '        <article class="panel reveal mtvo" style="--rd:.08s">\n          <span class="label">Proposed doctoral research (from 2027)</span>\n          <h3>From Rented to Owned Visibility: towards a Maldives Tourism Visibility Observatory<span>.</span></h3>\n          <p class="mtvo-status">A proposal. The observatory is what this research aims to build; the first step is a public-data pilot from January 2027.</p>\n          <p class="ink">A proposed study of how small tourism businesses in the Maldives are found and booked online, across search, booking sites, social media, review sites and AI assistants, and whether that visibility is becoming more rented from other people’s platforms or more owned.</p>\n          <ol class="mtvo-steps">\n            <li><b>Measure</b><span>Build and validate a Visibility Index that scores a property across every channel where travellers find it, including what AI assistants say about it.</span></li>\n            <li><b>Track</b><span>Apply it to the same panel of properties every month, starting from a baseline rebuilt from my 2016 guesthouse fieldwork.</span></li>\n            <li><b>Explain</b><span>Interview owners each season about why their numbers moved, and extend resource dependence theory from booking sites to algorithmic intermediaries such as AI assistants.</span></li>\n          </ol>\n          <span class="label" style="margin-top:6px">The questions it asks</span>\n          <ol class="qs">\n            <li>Can a small business’s visibility across all these channels be measured reliably, month after month?</li>\n            <li>How does that visibility change over time, and is it becoming more rented or more owned?</li>\n            <li>Which properties do AI assistants recommend, and why?</li>\n            <li>Does visibility change how much of each booking a business keeps?</li>\n          </ol>\n          <p class="small">This is proposed research: admission, supervision and ethics approval are still to come, and no results are claimed.</p>\n          <p class="small mtvo-int"><b>Declared interest:</b> I run Islandeative, whose Digital Visibility Health Check works in the same area. The research instrument and data will be kept separate from any commercial work.</p>\n          <div class="row-cta"><a class="btn" href="academic/mtvo.html">Read the research intent <i data-ic="right"></i></a><a class="btn btn--ghost" href="academic/MTVO_Research_Intent_OnePager_v0.1.pdf" download>One-page PDF <i data-ic="download"></i></a></div>\n        </article>'),
 ('<div class="panel reveal"><span class="label">Next steps · 2027</span><ul class="ticks"><li>Ethics approval and a pilot of the diagnostic</li><li>A conference abstract and a working paper</li></ul><span class="todo">[TODO: target university, supervisor, conference]</span></div>', '<div class="panel reveal"><span class="label">Next steps</span><ol class="nsteps"><li><b>Now</b><span>Prepare PhD applications to Universiti Putra Malaysia and Universiti Teknologi Malaysia.</span></li><li><b>From January 2027</b><span>Run the public-data pilot of the Maldives Tourism Visibility Observatory.</span></li><li><b>2027</b><span>Publish a working paper with an open dataset.</span></li><li><b>2027</b><span>Submit a research note to a Q1, Scopus-indexed journal, targeting <i>Information Technology &amp; Tourism</i> first and the <i>Journal of Hospitality Marketing &amp; Management</i> second.</span></li></ol></div>'),
 ('<p class="thread reveal">My first paper asked how Maldivian guesthouses could be seen online. My second mapped what it takes to run one. Today travellers increasingly ask AI tools where to stay, and small businesses don’t know whether they’re being recommended. That’s the question I want to study next.</p>',
  '<div class="res-l"><div class="thread reveal"><p>My first paper asked how Maldivian guesthouses could be seen online.</p><p>My second mapped what it takes to run one.</p><p>Today travellers increasingly ask AI tools where to stay, and small businesses don’t know whether they’re being recommended.</p><p>That’s the question I want to study next: <q>Is their visibility becoming more rented, or more owned?</q></p></div><a class="intent-prev reveal" href="academic/mtvo.html"><span class="ip-paper"><img src="img/mtvo-preview.jpg" alt="Preview of the one-page research intent, Rented to Owned Visibility" width="720" height="1019" loading="lazy"></span><span class="ip-cap"><span class="label">Research intent · one page</span><b>Rented to Owned Visibility</b><span>The study on a single page: the problem, the four questions, the path from 2016 to 2030 and what it will produce.</span><span class="more-link">Read the research intent <i data-ic="right"></i></span></span></a></div>'),
 ('"coord":"Subject coordinator, 2025",', '"coord":"Subject coordinator",'),
 ('{"c":"MKT301","n":"International Marketing","l":"Level 300","core":1,', '{"c":"MKT301","n":"International Marketing","l":"Level 300","core":1,"coord":"Subject coordinator",'),
 ('{"c":"MKT303","n":"Electronic Marketing","l":"Level 300","core":1,', '{"c":"MKT303","n":"Electronic Marketing","l":"Level 300","core":1,"coord":"Subject coordinator",'),
 ('{"c":"MKT309","n":"Brand Management","l":"Level 300","core":1,', '{"c":"MKT309","n":"Brand Management","l":"Level 300","core":1,"coord":"Subject coordinator",'),
 ('{"c":"MKT213","n":"Integrated Marketing Communication","l":"Level 200","lt":1,', '{"c":"MKT213","n":"Integrated Marketing Communication","l":"Level 200","lt":1,"coord":"Subject coordinator",'),
 ('{"c":"MKT217","n":"Advertising &amp; Promotion","l":"Level 200",', '{"c":"MKT217","n":"Advertising &amp; Promotion","l":"Level 200","coord":"Subject coordinator",'),
 ('and coordinated MKT101.', 'and coordinate six of them.'),
 ('<li><i data-ic="file"></i><b>Exam papers and validation</b>', '<li><i data-ic="layers"></i><b>Subject coordination</b><span>MKT101, MKT213, MKT217, MKT301, MKT303 and MKT309: the syllabus, learning outcomes, assessment setting, rubric moderation, Moodle course design, exam papers and tutor standardisation</span></li>\n            <li><i data-ic="file"></i><b>Exam papers and validation</b>'),
 ('<p class="spot-lead">Students use Moodle to download notes and submit work.', '<p class="spot-lead">I built the arena for first-year students: they learn best in short bursts, and the weakest student needs a way in. <a class="more-link" href="academic/teaching.html#why">Why first-years matter to me <i data-ic="right"></i></a></p>\n          <p class="spot-lead">Students use Moodle to download notes and submit work.'),
 ('<p class="creds-note reveal"><span class="todo">[TODO: confirm exact bachelor’s title; other notes say BSc Tourism and Travel Services Management]</span></p>', ''),
]
for a, b in FIX:
    assert src.count(a) == 1, a[:60]; src = src.replace(a, b)
os.makedirs(P('out'), exist_ok=True)

def sec(i):
    m = re.search(r'(  <!-- [^\n]*-->\n)?  <section class="[^"]*" id="%s">.*?\n  </section>\n' % i, src, re.S)
    assert m, i
    return m.group(0)
def rep(s, a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); return s.replace(a, b)
def cut(s, a, b):
    i = s.index(a); j = s.index(b, i) + len(b); return s[:i] + s[j:]
def grab(s, a, b):
    i = s.index(a); j = s.index(b, i) + len(b); return s[i:j]

D = json.loads(re.search(r'<script type="application/json" id="acData">(.*?)</script>', src, re.S).group(1))
for _m in D['mods']:
    if _m.get('mid'): _m['mid'][3] = ''   # B2: student comments removed until real, consented ones arrive
acdata = '<script type="application/json" id="acData">' + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + '</script>'

# ---------- module data ----------
GROUPS = [('Business concepts', ['MKT101', 'BUS107', 'BUS301']),
          ('Marketing communications', ['MKT213', 'MKT215', 'MKT217']),
          ('Strategy, brand and digital', ['MKT301', 'MKT303', 'MKT309'])]
MODS = {m['c']: m for m in D['mods']}
ORDER = [c for g in GROUPS for c in g[1]]
slug = lambda c: c.lower()
lvl = lambda m: m['l']

# ---------- HOME ----------
header = rd('header.html')
footer = rd('footer.html').replace('<span class="todo">[TODO: Google Scholar]</span>', SCHOLAR.replace('class="orcid"', 'class="orcid orcid-foot"'))
CVPDF = 'academic/Muiz_Fuad_CV.pdf'
HIDDEN = set()
def cvlinks(s):
    s = re.sub(r'<button class="(btn[^"]*?) is-todo" type="button" data-todo="CV PDF file">(.*?)</button>', lambda m: '<a class="%s" href="%s" download="Muiz_Fuad_CV.pdf">%s</a>' % (m.group(1), CVPDF, m.group(2)), s)
    s = re.sub(r'\s*<span class="todo">\[TODO: CV PDF file\]</span>', '', s)
    for t in re.findall(r'<span class="todo">(.*?)</span>', s): HIDDEN.add(re.sub('<[^>]+>', '', t))
    s = re.sub(r'\s*<span class="todo">.*?</span>', '', s)
    s = re.sub(r'<p class="src">\s*</p>|<p>\s*</p>|<p class="small">\s*</p>', '', s)
    s = re.sub(r'\s*<div class="teach"><span class="label">How I teach this</span>\s*</div>', '', s)
    s = re.sub(r'\s*<article class="panel reveal">\s*<span class="label">The revised marketing programme</span>\s*<h3>My part in the new degree</h3>\s*</article>', '', s)
    return s
s1 = sec('s1')
s1 = rep(s1, 'I teach marketing through real Maldivian businesses, and I build the tools my students learn with.',
         'I teach marketing through the experiences that built its theories.')
_ab = grab(s1, '<div class="about-text" id="aboutText">', '@@SIG2@@')
s1 = s1.replace(_ab, '<div class="about-text" id="aboutText">\n' + rd('landing_about.html') + '@@SIG2@@')
s1 = rep(s1, '<p class="intro-p">15+ years in Maldivian tourism and marketing, now in the lecture room at MNU Business School.</p>',
         '<p class="intro-p">15+ years in tourism and marketing, now in the lecture room at MNU Business School.</p>')
s1 = rep(s1, '            </div>\n            <div class="about-text" id="aboutText">', '              ' + AU.glance() + '\n            </div>\n            <div class="about-text" id="aboutText">')
s1 = rep(s1, '<a class="btn btn--ghost" href="#teach">See how I teach <i data-ic="down"></i></a>',
         '<a class="btn btn--ghost" href="#modules">See what I teach <i data-ic="down"></i></a>')
s1 = re.sub(r'\n\s*\n', '\n', s1)

teach = sec('teach')
pride_old = grab(teach, '<article class="pride reveal">', '</article>')
PRACTICE = '''      <ol class="practice reveal">
        <li><b>Start with a real case</b><span>A real business situation comes first, broken down in class.</span><a class="more-link" href="#lesson">See a lesson <i data-ic="right"></i></a></li>
        <li><b>Find the theory inside it</b><span>Students reshape the case to fit the theory behind it, and find the definitions inside the scenario.</span><a class="more-link" href="academic/teaching.html#philosophy">How I teach <i data-ic="right"></i></a></li>
        <li><b>A challenge at every level</b><span>Custom tools give every student, from those who are struggling to those who want a stretch, a challenge that fits.</span><a class="more-link" href="#tools">See the tools <i data-ic="right"></i></a></li>
      </ol>
'''
teach = teach.replace('      <!-- teaching wheel: eight principles -->', PRACTICE + '      <!-- teaching wheel: eight principles -->', 1)
PRIDE = '''<article class="pride reveal" id="delivery">
        <span class="pride-tag"><i data-ic="star"></i> Reliable delivery</span>
        <h3>Every class delivered.</h3>
        <p>By my own record, I haven’t cancelled a class since Term 1 2025, when our new dean challenged the department to get through a whole term without one. I kept it going into 2026. When a public holiday fell on a class day, I taught that class in advance, and with colleagues I set up a simple cover system so a class goes ahead whenever a free room and time slot allow.</p>
        <p>In Term 2 2025 I carried 18 contact hours a week, above my required load, and volunteered extra classes and tutorial hours so graduating students could finish that semester instead of waiting for the module to be offered again.</p>
      </article>'''
teach = teach.replace(pride_old, PRIDE)

lesson = sec('lesson')
lesson = cut(lesson, '      <div class="slots">', '</div>\n        <div class="slot reveal" style="--rd:.08s"><i data-ic="play"></i><b>Students on camera</b><span class="todo">[TODO: 2–3 captioned clips of 20–30 s, consent on file]</span></div>\n')
lesson = lesson.replace('        <div class="slides" id="slides"', AU.demo_video() + '\n        <div class="slides" id="slides"', 1)
ev = sec('evidence')
evchart = grab(ev, '      <div class="panel ev-chart reveal" id="evChart">', '</table></div></details>\n      </div>')
home_ev = rd('home_evidence.html').replace('@@EVCHART@@', AU.evidence(full=False)).replace('@@COMMENTS@@', AU.comments())
if not AU.F['evaluation_on'] and not AU.comments(): home_ev = ''
SVC_HOME = '  <section class="block" id="service">\n    <div class="wrap">\n      <div class="head wide reveal"><span class="label">Beyond the classroom</span><h2>Service and supervision<span>.</span></h2></div>\n      ' + AU.service() + '\n    </div>\n  </section>\n'

def mgroups():
    out = []
    for i, (g, cs) in enumerate(GROUPS):
        rows = ''.join('<a href="academic/modules/%s.html"><b>%s</b><span>%s%s</span><em>%s</em></a>' % (
            slug(c), c, MODS[c]['n'], ('<small>Subject coordinator</small>' if MODS[c].get('coord') else ''),
            MODS[c]['l'].replace('Level ', 'L')) for c in cs)
        out.append('<div class="mgroup reveal" style="--rd:%.2fs"><span class="label">%s</span>%s</div>' % (i * .08, g, rows))
    return '\n        '.join(out)
home_mods = rd('home_modules.html').replace('<div class="mgroups" id="mgroups"></div>', '<div class="mgroups">\n        ' + mgroups() + '\n      </div>')

res = sec('research')
res_home = cut(res, '      <div class="next">', '</div>\n      </div>\n')
res_home = rep(res_home, '<span class="label">Research</span>\n        <h2>Where the question is going<span>.</span></h2>', '<span class="label">Research</span>\n        <h2 class="big-q">What’s next? Where is the question leading?</h2>')
res_home = rep(res_home, '</p>\n    </div>\n  </section>', '</p>\n      <div class="row-cta reveal"><a class="btn btn--ghost" href="academic/research.html">Research, profiles and talks <i data-ic="right"></i></a></div>\n    </div>\n  </section>')

home = (header.replace('@@FADE@@', ' fade') + '\n<main>\n' + s1 + '\n  <section class="block atg-sec"><div class="wrap">' + AU.glance(mobile=True) + '</div></section>\n' + rd('home_story.html') + '\n' + home_mods + '\n' + teach + '\n' + AU.snapshot(rd('home_tools.html')) + '\n' +
        home_ev + '\n' + lesson + '\n' + SVC_HOME + res_home + '\n' + sec('about') + '\n' + sec('credentials') + '\n' + footer + acdata + '\n')
open(P('out', 'home.html'), 'w', encoding='utf-8').write(cvlinks(home))

# ---------- shared bits for inner pages ----------
BACK = '  <div class="backbar"><div class="wrap"><a class="btn back-home" href="academic.html"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>Back to portfolio</a></div></div>\n'
def page(name, label, title, lead, body, toc=None, crumbs=None, data=False, extra=''):
    tc = ''
    if toc: tc = '<nav class="toc" aria-label="On this page">' + ''.join('<a href="#%s">%s</a>' % t for t in toc) + '</nav>'
    cb = '<div class="crumbs">' + ' <span aria-hidden="true">/</span> '.join('<a href="%s">%s</a>' % c for c in (crumbs or [('academic.html', 'Home')])) + '</div>'
    h = (header.replace('@@FADE@@', '') + '\n<main>\n  <section class="pagehead"><div class="wrap">' + cb +
         '<span class="label">' + label + '</span><h1 class="ph-t">' + title + '<span>.</span></h1>' +
         ('<p class="ph-lead">' + lead + '</p>' if lead else '') + extra + tc + '</div></section>\n' + body + '\n' + BACK + footer + (acdata + '\n' if data else ''))
    open(P('out', name + '.html'), 'w', encoding='utf-8').write(cvlinks(h))

def block(i, label, h2, inner, intro=''):
    return ('  <section class="block" id="%s">\n    <div class="wrap">\n      <div class="head wide reveal"><span class="label">%s</span><h2>%s<span>.</span></h2>%s</div>\n%s\n    </div>\n  </section>\n'
            % (i, label, h2, ('<p>' + intro + '</p>' if intro else ''), inner))
inner = lambda s: re.search(r'<div class="wrap">\n(.*)\n    </div>\n  </section>', s, re.S).group(1)
strip_head = lambda s: re.sub(r'\s*<div class="head[^"]*">.*?</div>\n', '\n', s, count=1, flags=re.S)

# ---------- TEACHING ----------
phil = grab(teach, '<div class="phil reveal">', '</div>')
PILLARS = '''<div class="pillars">
        <div class="pillar reveal"><em>1</em><b>Real local cases</b><p>Maldivian firms like Ruka, Reethi and the SME HUB businesses, not distant examples.</p><a class="more-link" href="academic/cv.html#work">See the cases <i data-ic="right"></i></a></div>
        <div class="pillar reveal" style="--rd:.06s"><em>2</em><b>Theory to application</b><p>Every concept ends in a decision for a real business.</p><a class="more-link" href="academic/tools.html">See the tools <i data-ic="right"></i></a></div>
        <div class="pillar reveal" style="--rd:.12s"><em>3</em><b>Practise the hard question</b><p>Rehearse the manager’s question until the answer comes.</p><a class="more-link" href="academic.html#lesson">See a lesson <i data-ic="right"></i></a></div>
        <div class="pillar reveal" style="--rd:.18s"><em>4</em><b>Listen and adjust</b><p>Each term’s evaluation shapes the next.</p><a class="more-link" href="#evidence">See the evidence <i data-ic="right"></i></a></div>
      </div>
      <p class="src reveal" style="margin-top:14px">Steps 1 to 3 come from my teaching philosophy. Step 4 follows Tomáška (2025), <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC12635050/" target="_blank" rel="noopener">“Making the first moves as a university teacher”</a>, <i>EMBO Reports</i>.</p>
      <div class="row-cta reveal"><a class="btn btn--ghost" href="academic.html#teach-wheel">All eight ideas, on the teaching wheel <i data-ic="right"></i></a></div>'''
if not AU.F['evaluation_on']: PILLARS = PILLARS.replace('href="#evidence"', 'href="#outcomes"')
A101 = D['asg']['MKT101']
wb = lambda A: '<div class="wbar">' + ''.join('<span style="--w:%d">%s <b>%d</b></span>' % (x[1], x[0], x[1]) for x in A[1]) + '</div>'
ASSESS = '''<div class="assess">
        <article class="panel reveal"><span class="label">Clear from week one</span><h3>Outlines and rubrics, up front.</h3><p>In all three midterm check-ins I hold, every responding student said the subject outline arrived in the first two weeks and every assignment came with a marking rubric.</p><p class="src">Midterm Subject and Teaching Evaluations: MKT215, Term 1 2025; MKT217 and MKT301, Term 2 2025; 1 to 5 respondents each.</p></article>
        <article class="panel reveal" style="--rd:.08s"><span class="label">A mix of evidence · MKT101, %s</span><h3>Coursework, a midterm and a final.</h3>%s<p class="small">Each module’s weighting, as delivered, is on its <a href="academic/modules.html">module page</a>.</p></article>
        <article class="panel reveal"><span class="label">Setting and moderation</span><h3>Exam papers set and combined.</h3><p>I set the exam papers for four modules in Term 2 2025, and reviewed and combined the MKT101 paper with a co-lecturer’s. I have also supervised three applied projects to completion (2025 to 2026), with three in progress.</p></article>
        <article class="panel reveal" style="--rd:.08s"><span class="label">Where I want to improve</span><h3>Closing the exam gap.</h3><p>Coursework marks beat final-exam marks in all 15 cohorts with an exam, by a median of 16.4 points. The MKT101 Arena’s timed written practice is one response.</p><span class="todo">[TODO: what else you are doing about it, for example mock papers]</span></article>
      </div>
      <p class="reveal" style="margin-top:16px"><span class="todo">[TODO: for one module, a map of each learning outcome to the assessment that tests it (constructive alignment)]</span></p>''' % (A101[0], wb(A101))
cur = sec('curriculum')
cur_in = strip_head(inner(cur))
ev_in = strip_head(inner(ev))
ev_in = ev_in.replace('<details class="more-ev reveal"><summary><span>See the full teaching evidence</span><small>Student outcomes, attendance and midterm check-ins</small></summary>', '<details class="more-ev reveal" open><summary><span>Student outcomes</span><small>Pass rates, attendance and the exam gap</small></summary>')
ev_in = cut(ev_in, '      <p class="pulse reveal">', '</p>\n')
mods_sec = sec('modules')
also = grab(mods_sec, '      <div class="also">', '</div>\n      </div>\n')
# students per term now lives in the evidence charts; keep duties here
also = re.sub(r'\s*<div class="panel reveal">\s*<span class="label">Students per term</span>.*?</p>\s*</div>', '', also, count=1, flags=re.S)
also = also.replace('<div class="panel reveal" style="--rd:.08s">\n          <span class="label">Beyond the classroom</span>', '<div class="panel reveal">\n          <span class="label">Beyond the classroom</span>')
EV2 = ev_in[ev_in.index('      <div class="ev2">'):ev_in.index('      <details class="more-ev')]

slots = '''      <div class="slots">
        <div class="slot reveal"><i data-ic="play"></i><b>Teaching demo video</b><span class="todo">[TODO: 3–5 min recording of “Found, Chosen, Booked”, with captions]</span></div>
        <div class="slot reveal" style="--rd:.08s"><i data-ic="play"></i><b>Students on camera</b><span class="todo">[TODO: 2–3 captioned clips of 20–30 s, consent on file]</span></div>
      </div>'''
WHY = """<article class="why reveal" id="why">
        <div class="why-l">
          <span class="label">Why I teach</span>
          <h3>Why first-years matter to me<span>.</span></h3>
          <ul class="why-chips"><li>Voluntary moderation · MKT101</li><li>First-year subjects · MKT101 and BUS107</li></ul>
          <a class="more-link" href="academic/tools.html#class-activity">Two weeks of class activity <i data-ic="right"></i></a>
        </div>
        <div class="why-r">
          <p class="why-lead">I give MKT101 special care. I moderate it voluntarily because it is where students first meet marketing, and a first-year subject that fails to interest them can set the tone for the rest of their degree. Students who do poorly early are the ones most likely to slacken off or leave.</p>
          <p>I know this from my own time at university. In my early years, one subject and one lecturer nearly put me off studying altogether. Then, in my second year, I met lecturers with real passion for their subjects and years of industry experience behind them. They are the reason I went on to the roles I have had, and the reason I came back to teach.</p>
          <p>After freelancing in tourism marketing and managing marketing for a resort, I could see the next step was cluster director: less creative work, more corporate decision-making, further from the people and the customers. Building my own career had stopped feeling fulfilling. I had reached the point my lecturers reached after careers of 30 years and more; it took me 15, with no shortcuts, and I am grateful for every one of them. Now I want to inspire the next group of young, enthusiastic minds to pursue the art of communicating to influence what people buy.</p>
          <p>That is why MKT101 and BUS107, the first-year subjects I teach, get my special attention. The MKT101 Arena began as a way to help these students practise case studies, because they learn best in short bursts and the weakest student needs a way in. Several versions later, I have seen it get students learning actively in short blocks and arriving at the exam better prepared.</p>
        </div>
      </article>"""
tbody = (block('philosophy', 'Teaching philosophy', 'How I teach', '      ' + phil + '\n      ' + PILLARS + '\n      ' + WHY) +
         block('assessment', 'Assessment', 'How I assess', '      ' + ASSESS) +
         block('delivery-sec', 'Delivery', 'Reliability', '      ' + PRIDE.replace(' id="delivery"', '')) +
         block('curriculum', 'Curriculum', 'Shaping what we teach', cur_in, 'MNU is developing a new marketing programme, and I keep updating the content we deliver.') +
         (block('evidence', 'Teaching evidence', 'What students say', '      ' + AU.evidence(full=True) + '\n      ' + AU.comments(full=True), 'How students rated my teaching in every term I’ve taught at MNU, against the Business School average. The good terms and the hard one.') if AU.F['evaluation_on'] or AU.comments() else '') +
         block('outcomes', 'Student outcomes', 'How my students do', EV2) +
         block('beyond', 'Beyond the classroom', 'Service and supervision', '      ' + AU.service()))
page('teaching', 'Teaching portfolio', 'Teaching', 'How I teach and assess, what students say, and the work around the classroom: curriculum, supervision, exam setting and committees.', tbody,
     toc=[('philosophy', 'Philosophy'), ('assessment', 'Assessment'), ('delivery-sec', 'Delivery'), ('curriculum', 'Curriculum')] + ([('evidence', 'Evidence')] if AU.F['evaluation_on'] else []) + [('outcomes', 'Outcomes'), ('beyond', 'Service')], data=True)

# ---------- MODULES (list) ----------
def yr_of(t): return t.split()[-1]
years = {}
for c in ORDER:
    for t in MODS[c]['terms']:
        years.setdefault(yr_of(t[0]), {}).setdefault(c, []).append(t)
def course(c, terms):
    m = MODS[c]
    chips = ''.join('<li>%s%s</li>' % (t[0], (' · <b>%d students</b>' % t[1]) if t[1] else '') for t in terms)
    role = ' · ' + m['coord'] if m.get('coord') else ''
    return ('<article class="course reveal"><a class="c-logo" href="academic/modules/%s.html" aria-label="%s, module page">%s<small>%s</small></a><div class="c-body">'
            '<h3><a href="academic/modules/%s.html">%s</a></h3><p class="c-meta">%s · %s · MNU Business School%s</p>'
            '<ul class="chips">%s</ul></div></article>'
            % (slug(c), re.sub('&amp;', 'and', m['n']), c, m['l'].replace('Level ', 'L'), slug(c), m['n'], c, lvl(m), role, chips))
lst = ''
for y in sorted(years, reverse=True):
    lst += '<div class="yr"><h2>%s<span>.</span></h2>%s</div>\n' % (y, ''.join(course(c, years[y][c]) for c in ORDER if c in years[y]))
earlier = grab(mods_sec, '      <div class="panel earlier reveal">', '</div>\n    </div>\n')
earlier = earlier.replace('</div>\n    </div>\n', '</div>\n')
earlier = earlier.replace('<span class="label">Earlier teaching</span>', '', 1)
lst += '<div class="yr"><h2>Earlier teaching<span>.</span></h2></div>\n' + earlier
mbody = '  <section class="block" id="list">\n    <div class="wrap">\n' + lst + '\n    </div>\n  </section>\n'
page('modules', 'Modules', 'Modules I teach', 'Nine undergraduate modules at MNU Business School since 2024, newest first. Each module page has its level, outcomes, assessment, the terms I taught it and what students use. Term 2 2024 isn’t listed: the evaluation report for that term doesn’t name the modules.', mbody,
     crumbs=[('academic.html', 'Home')])

# ---------- one page per module ----------
os.makedirs(P('out', 'modules'), exist_ok=True)
for k, c in enumerate(ORDER):
    m = MODS[c]
    A = D['asg'].get(c)
    terms = ''.join('<li>%s%s</li>' % (t[0], (' · <b>%d students</b>' % t[1]) if t[1] else '') for t in m['terms'])
    facts = '''<dl class="facts">
        <div><dt>Code</dt><dd>%s</dd></div>
        <div><dt>Level</dt><dd>%s</dd></div>
        <div><dt>My role</dt><dd>%s</dd></div>
      </dl>''' % (c, lvl(m), m.get('coord', 'Lecturer'))
    T = MODTEXT.get(c)
    if T and T.get('hours'):
        facts = facts.replace('</dl>', '  <div><dt>Contact</dt><dd>%s</dd></div>\n      </dl>' % T['hours'])
    left = ''
    if T:
        left = ('<article class="panel reveal mt-about"><h2>About this module<span>.</span></h2><p>%s</p>'
                '<span class="label" style="margin-top:6px">What students learn to do</span><ul class="ticks">%s</ul></article>'
                % (T['about'], ''.join('<li>%s</li>' % x for x in T['learn'])))
        fam = ''
        if T.get('family'):
            fam = '<nav class="mt-fam" aria-label="Taught as one family"><span class="label">Taught as one family</span><div>' + ''.join(
                ('<span aria-current="page"><b>%s</b> %s</span>' if f == c else '<a href="academic/modules/%s.html"><b>%s</b> %s</a>' % (slug(f), '%s', '%s')) % (f, MODS[f]['n']) for f in T['family']) + '</div></nav>'
        left += ('<article class="panel reveal mt-teach"><h2>How I teach it<span>.</span></h2>' + fam + '<span class="label">%s</span><p>%s</p><ol class="mt-steps">%s</ol><p>%s</p></article>'
                 % (T['teach_h'], T['teach_intro'], ''.join('<li>%s</li>' % x for x in T['teach_steps']), T['teach_after']))
        left += ('<article class="panel reveal mt-week"><h2>Every week<span>.</span></h2><dl class="mt-rhythm">%s</dl></article>'
                 % ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % r for r in T['rhythm']))
        left += ('<article class="panel reveal"><h2>Assessment that mirrors the real thing<span>.</span></h2><ul class="ticks">%s</ul><p class="small">%s</p></article>'
                 % (''.join('<li>%s</li>' % x for x in T['assess']), T['current']))  # About, outcomes, weekly topics and a sample activity stay hidden until the module descriptors are supplied
    right = '<article class="panel reveal"><h2>Assessment<span>.</span></h2>'
    right += ('<span class="label">As delivered, %s</span>%s' % (A[0], wb(A))) if A else ''
    right += '</article>'
    if not A: right = ''
    right += '<article class="panel reveal"><h2>Terms I taught it<span>.</span></h2><ul class="chips">%s</ul><p class="src">Student numbers from MNU workload forms, where recorded.</p></article>' % terms
    if m.get('app'):
        right += '<article class="panel reveal"><h2>What students use<span>.</span></h2><p>%s, a web app I built for this module.</p><div class="row-cta" style="margin-top:4px"><a class="btn btn--sm" href="%s" target="_blank" rel="noopener">Open it <i data-ic="upright"></i></a><a class="more-link" href="academic/tools.html">How it works <i data-ic="right"></i></a></div></article>' % (m['app'][0], m['app'][1].replace('&', '&amp;'))
    if m.get('demo'):
        right += '<article class="panel reveal"><h2>Sample lesson<span>.</span></h2><p>“Found, Chosen, Booked”, my 10-minute demonstration lesson, was built for this module.</p><a class="more-link" href="academic.html#lesson">See the lesson <i data-ic="right"></i></a></article>'
    right += AU.module_comment(c)
    if m.get('mid'):
        mi = m['mid']
        right += '<article class="panel reveal"><h2>Midterm check-in<span>.</span></h2><span class="label">%s · %d respondent%s</span><p>%s.</p></article>' % (mi[0], mi[1], 's' if mi[1] > 1 else '', mi[2])
    prv, nxt = ORDER[k - 1] if k else None, ORDER[k + 1] if k + 1 < len(ORDER) else None
    pager = '<nav class="pager" aria-label="Other modules">' + \
        ('<a href="academic/modules/%s.html"><small>← Previous</small>%s %s</a>' % (slug(prv), prv, MODS[prv]['n']) if prv else '<span></span>') + \
        ('<a href="academic/modules/%s.html"><small>Next →</small>%s %s</a>' % (slug(nxt), nxt, MODS[nxt]['n']) if nxt else '') + '</nav>'
    body = ('  <section class="block" id="module">\n    <div class="wrap">\n      ' + facts + '\n      ' + ('<div class="mp mp-mod" style="margin-top:16px"><div class="mp-col">' + left + '</div><div class="mp-col">' + right + '</div></div>' if left else '<div class="mp one" style="margin-top:16px"><div class="mp-col">' + right + '</div></div>') + '\n      ' + pager + '\n    </div>\n  </section>\n')
    grp = [g for g, cs in GROUPS if c in cs][0]
    page('modules/' + slug(c), c + ' · ' + grp, m['n'], None, body,
         crumbs=[('academic.html', 'Home'), ('academic/modules.html', 'Modules')])

# ---------- TOOLS ----------
tools = sec('tools')
arena = grab(tools, '      <article class="spot reveal" id="arena">', '      </article>\n')
_ss = grab(arena, '        <div class="spot-stats">', '        </div>\n      </article>\n')
_ts = AU.toolstats('mkt101')
arena = arena.replace(_ss, (_ts + ('<p class="small tstats-eg">For example, one student worked through almost 80% of the arena’s questions in two weeks, with more than 10 hours of active practice.</p>' if _ts else '') +
  '\n        <div class="spot-stats"><div class="panel stat-clock"><span class="label">When students practise</span><p>Students practise at every hour of the day, including late at night: activity I rarely see on Moodle.</p><div class="clock" aria-hidden="true"><i></i><span>24h</span></div></div></div>\n      </article>\n'))
more_tools = grab(tools, '      <div class="sub-head reveal"><div><span class="label">More tools</span>', '      </div>\n    </div>\n  </section>')
more_tools = more_tools[:-len('    </div>\n  </section>')]
more_tools = more_tools.replace('      <p class="tool-note reveal">', AU.toolstats('mkt301') + AU.toolstats('mkt303') + '\n      <p class="tool-note reveal">', 1)
CA_HEAD = '<div class="head wide reveal"><span class="label">Class activity · 28 October to 11 November 2026</span><h2>Two weeks in the tools<span>.</span></h2><p>' + rd('activity_lede.txt') + '</p></div>\n'
CA_BODY = rd('activity_body.html').replace('<section class="block ca" id="class-activity"><div class="wrap">', '<section class="block ca tools-ca" id="class-activity"><div class="wrap">\n' + CA_HEAD, 1)
tbody = ('  <section class="block" id="arena-sec">\n    <div class="wrap">\n' + arena + '    </div>\n  </section>\n' + CA_BODY + '\n  <section class="block" id="more-tools">\n    <div class="wrap">\n' + more_tools +
         '      <p class="tool-access reveal" style="margin-left:0">Students sign in with their student ID. Visitors and review panels can try each tool as a guest, with no account: the arenas open with the whole class leaderboard shown without names, and the audit plays a finished demo for a real guesthouse with a fictional scenario.</p>\n      <div class="row-cta guest-row reveal" style="margin-top:12px"><a class="btn btn--ghost" href="https://abdullamuizfuad.github.io/mkt101-cases/?guest=1#/" target="_blank" rel="noopener">Try MKT101 Arena as a guest <i data-ic="upright"></i></a><a class="btn btn--ghost" href="https://abdullamuizfuad.github.io/mkt301/?guest=1#/" target="_blank" rel="noopener">Try MKT301 Arena as a guest <i data-ic="upright"></i></a><a class="btn btn--ghost" href="https://abdullamuizfuad.github.io/student-audit/tool.html?demo=1" target="_blank" rel="noopener">Watch the MKT303 audit demo <i data-ic="upright"></i></a></div>\n'
         '      <div class="row-cta reveal"><a class="btn btn--ghost" href="academic.html#lesson">A lesson that uses AI search: Found, Chosen, Booked <i data-ic="right"></i></a></div>\n    </div>\n  </section>\n')
page('tools', 'Student tools', 'Tools I built for my students', 'Students asked for more practical, interactive learning. These are the web apps I’ve built for it, each for a module I teach. <span class="todo">[TODO: confirm which feedback prompted each app before linking them causally]</span>', tbody)

# ---------- RESEARCH ----------
res_in = strip_head(inner(res))
TALKS = '''<ul class="talks">
        <li class="reveal"><time>2026</time><div><b>Found, Chosen, Booked: marketing when AI does the searching</b><p>A 10-minute demonstration lesson for Introduction to Marketing (MKT101) and Business Entrepreneurship (BUS301).</p><div class="row-cta"><a class="btn btn--sm" href="https://abdullamuizfuad.github.io/GEO-Visibility-/" target="_blank" rel="noopener">Slides <i data-ic="upright"></i></a><a class="btn btn--sm btn--ghost" href="https://abdullamuizfuad.github.io/GEO-Visibility-/demo/" target="_blank" rel="noopener">Phone simulation <i data-ic="upright"></i></a><a class="btn btn--sm btn--ghost" href="https://abdullamuizfuad.github.io/GEO-Visibility-/slides.pdf" target="_blank" rel="noopener">PDF <i data-ic="download"></i></a></div></div></li>
        <li class="reveal"><time>2016</time><div><b>Sustainable development of local island tourism</b><p>Conceptual paper, 3rd International Hospitality and Tourism Conference (IHTC).</p></div></li>
      </ul>'''
rbody = (block('direction', 'Research', 'Where the question is going', res_in) +
         block('talks', 'Talks', 'Talks and presentations', '      ' + TALKS))
page('research', 'Research', 'Research', 'Where my research has been, and the study I propose next: how small tourism businesses in the Maldives are found online, and whether that visibility is rented or owned.', rbody,
     toc=[('direction', 'Direction'), ('talks', 'Talks')])

# ---------- CV ----------
R = lambda t, d, org: '<div class="cv-row"><b>%s</b><span class="cv-d">%s</span></div><div class="cv-org">%s</div>' % (t, d, org)
UL = lambda *xs: '<ul>' + ''.join('<li>%s</li>' % x for x in xs) + '</ul>'
S = lambda t, body: '<section class="cv-sec"><h2>%s<span>.</span></h2>%s</section>' % (t, body)
CVDOC = ('<article class="cvdoc" id="cvdoc">'
 '<header class="cv-top"><p class="cv-name">Abdulla Muiz Fuad<span>.</span></p>'
 '<p class="cv-role">Lecturer in Marketing · Tourism, Digital Marketing and SME Development</p>'
 '<p class="cv-contact"><span>+960 990 2996</span><span><a href="mailto:abdullamuizfuad@gmail.com">abdullamuizfuad@gmail.com</a></span><span><a href="https://linkedin.com/in/abdullamuizfuad">linkedin.com/in/abdullamuizfuad</a></span><span><a href="https://orcid.org/0009-0003-5812-6693">ORCID 0009-0003-5812-6693</a></span><span>Malé, Maldives</span></p></header>'
 + S('Academic profile',
   '<p>Marketing academic and industry practitioner holding an MSc in Global Marketing Management and a BA (Hons) in Tourism Management, both from Asia Pacific University, Kuala Lumpur. Has taught undergraduate and master’s marketing, e-commerce and supply chain modules at MNU Business School and MI College, including subject coordination, assessment design and Applied Project supervision. Co-author of peer-reviewed research on guesthouse tourism and e-marketing in the Maldives (36 citations). Draws on over a decade of marketing and tourism industry experience (since 2011) to ground theory in local business practice.</p>'
   '<p><b>Research interests:</b> online visibility of small tourism businesses, including in AI-generated answers (generative engine optimisation); booking intermediaries and resource dependence; small island developing states (SIDS); guesthouse and SME development; e-marketing.</p>'
   '<p><b>Proposed doctoral research (from 2027):</b> “From Rented to Owned Visibility: towards a Maldives Tourism Visibility Observatory”. A proposal; the observatory is what the research aims to build, and the first step is a public-data pilot from January 2027. A proposed longitudinal study that builds and validates a multi-channel Visibility Index, applies it each month to a panel of small Maldivian tourism businesses with seasonal owner interviews, and extends resource dependence theory to algorithmic intermediaries such as AI assistants.</p>'
   '<p><b>Next steps:</b> Preparing PhD applications to UPM and UTM. From January 2027, a public-data pilot will produce a working paper with an open dataset and a research note targeting <i>Information Technology &amp; Tourism</i> (Q1, Scopus-indexed).</p>'
   '<p><b>Teaching areas:</b> Introduction to Marketing; International Marketing; Electronic Marketing; Brand Management; Business Entrepreneurship; E-commerce; Digital Marketing; Supply Chain Management.</p>')
 + S('Education',
   R('MSc Global Marketing Management', '2016 – 2018', 'Asia Pacific University · Kuala Lumpur, Malaysia') +
   R('BA (Hons) Tourism Management', '2014 – 2016', 'Asia Pacific University · Kuala Lumpur, Malaysia') +
   R('Diploma Level 4 in Tourism Management', '2012 – 2013', 'MAPS College · Malé, Maldives · Affiliate: Confederation of Tourism and Hospitality (CTH), UK') +
   R('Diploma in Human Resources Management', '2011', 'Clique College · Malé, Maldives · Affiliate: Association of Business Executives (ABE), UK') +
   R('Diploma in Business with Information Technology', '2008 – 2010', 'Asia Pacific University · Kuala Lumpur, Malaysia'))
 + S('Academic experience',
   R('Lecturer', 'Nov 2026 – present', 'MNU Business School, The Maldives National University · Malé, Maldives') + UL('Teaching and coordinating undergraduate marketing modules.') +
   R('Associate Lecturer and Subject Coordinator', 'Oct 2024 – Oct 2026', 'MNU Business School, The Maldives National University · Malé, Maldives') +
   UL('Full-time; taught and coordinated undergraduate modules: MKT101 Introduction to Marketing, MKT213 Integrated Marketing Communication, MKT217 Advertising and Promotion, MKT301 International Marketing, MKT303 Electronic Marketing and MKT309 Brand Management; also lectured Business Entrepreneurship and Maldivian Business Environment.',
      'As subject coordinator, responsible for the syllabus and learning outcomes, assessment setting and rubric moderation, exam papers and marking guides, Moodle course design, tutor standardisation, study guides and Applied Project supervision.',
      'Embedded real Maldivian business cases into course material to link theoretical frameworks to local industry practice.') +
   R('Part-time Lecturer', '2022 – 2024', 'MI College · Malé, Maldives') +
   UL('Taught Digital Marketing &amp; Ecommerce (master’s, level 500), Supply Chain Management (level 300) and Introduction to Marketing and Communication (level 100), online and in person.',
      'Revised and modernised inherited course materials to reflect current industry developments.',
      'Prepared exam papers; designed tutorials, workshops and assignments built around contemporary industry trends.'))
 + S('Publications',
   '<p><b>Google Scholar:</b> <a href="%s">%s</a></p>' % (SCH, SCH.replace('https://', '')) +
   UL('Chia, K. W., &amp; Muiz, A. (2021). The nature and challenges of guest house business in the Maldives: An exploratory study. <i>Tourism and Hospitality Research, 21</i>(1), 3–14. <a href="https://doi.org/10.1177/1467358420926688">https://doi.org/10.1177/1467358420926688</a> (cited 36 times). Indexed in Scopus and Web of Science (ESCI).',
      'CM Pappayah, P. P., Muiz, A., &amp; Jinus, D. J. (2017). Increasing the visibility of guesthouse operation in the Maldives through e-marketing. <i>Journal of Tourism and Leisure Studies, 2</i>(2), 11–20. <a href="https://doi.org/10.18848/2470-9336/CGP/v02i02/11-20">https://doi.org/10.18848/2470-9336/CGP/v02i02/11-20</a>') + '<p class="small">Published as A. Muiz.</p>')
 + S('Service and supervision', UL(*AU.SERVICE, 'Undergraduate applied projects: learning-contract advice, progress meetings, report review and presentation coaching; three supervised to completion (2025 to 2026), three in progress. Featured: Safe Steps, a child-safety campaign for a national ministry.'))
 + S('Conference presentations', UL('Presented a conceptual paper on Sustainable Development of Local Island Tourism, 3rd International Hospitality and Tourism Conference (IHTC), 2016.'))
 + S('Professional experience',
   R('Manager, SME HUB', '2024', 'Business Centre Corporation · Malé, Maldives') +
   UL('Managed an MSME business incubator (Ministry of Economic Development initiative under the MEERY Project), supporting 23 active vendors through a one-year incubation period.', 'Led digital and traditional marketing campaigns, market analysis, budgeting and partnership development.') +
   R('Sales and Marketing Manager, Maldives Business Network (MBN)', '2023 – 2024', 'Business Centre Corporation · Malé, Maldives') +
   UL('Marketed a business TV channel created to promote financial literacy; introduced web series and social media formats to reach a younger audience.', 'Led marketing strategy, market research, sales forecasting and client relations, securing key partnerships and growing advertising sales.') +
   R('Manager, Customer Relations and Clinical Operations', '2022 – 2023', 'Thiba Psychology · Malé, Maldives') +
   UL('Managed customer service and clinical staff, service workflows and process improvements; strengthened community presence through social media marketing.') +
   R('Marketing Manager', '2021 – 2022', 'Reethi Beach Resort · Baa Atoll, Maldives') +
   UL('Led the resort’s marketing function, with annual social media strategies targeting source markets including Germany and Italy.',
      'Ran a multi-tiered influencer programme (including Miss Germany 2022, Domitila Barros, on coral conservation and reef restoration), with TV, creator and print partnerships reaching European and Asian platforms such as VK, Xiaohongshu and Douyin.',
      'Improved organic search performance through blog content and high-authority travel features; tracked campaigns in Google Analytics; managed newsletters and repeat-guest email.',
      'Contributed to the website redesign (UI/UX), created new room category tiers and developed in-property events that grew F&amp;B revenue; represented the resort at international trade fairs.') +
   R('Copywriter', '2020 – 2021', 'Maldives Ports Limited · Malé, Maldives') +
   UL('Wrote web content and newsletters, published data-driven operational reports, and ran a social media campaign on MPL’s workforce.') +
   R('Head of Operations / Creative Director', '2018 – 2020', 'Blazon.Inc · Malé, Maldives') +
   UL('Led the marketing and design teams; oversaw corporate identities, in-house publications and contracted in-flight magazines; hosted two consecutive Annual Maldives Business Awards.') +
   '<div class="cv-row"><b>Earlier roles</b><span class="cv-d">2011 – 2017</span></div>' +
   UL('<b>Apprentice Layout Designer</b>, Tourism Publication Corporation Sdn. Bhd, Kuala Lumpur (2015–2017)', '<b>Cargo Officer</b>, Maldives Airports Company (2013–2014)',
      '<b>Marketing Officer</b>, Highrise Inc (2011–2013): sold advertising for Floating Asia and Visiting Guide; marketed MATATO Maldives Travel Awards and Living Expo', '<b>Marketing Associate</b>, Global Safety Associates (2011–2012)'))
 + S('Selected industry engagement',
   UL('<b>MATTA Fair, Kuala Lumpur (2014–2018):</b> progressed from promoter (2014) to Marketing Coordinator (2015) and Head of Marketing and Sales (2017) for MP Travel and Tours; led the Exhibitor Coordination Committee in 2018.',
      '<b>Events (2012–2024):</b> Maldives Business Awards 2019 (Event Manager); MATATO Maldives Travel Awards 2012 (Event Coordinator); Living Expo; MAHA Portal Launch and Vunadhaana Festival (BCC).',
      '<b>Content and strategy (2022):</b> Content Creator and Social Media Strategist for Miss Germany 2022, Domitila Barros (Maldives).',
      '<b>Volunteer:</b> 6th Global Summit on Urban Tourism (2017).'))
 + S('Referees', '<p>' + AU.referees().replace('Referees available on request.', 'Available on request.') + '</p>')
 + '<footer class="cv-sign"><span class="regards">Warm regards,</span>@@SIGCV@@<span class="cv-sign-role">Lecturer in Marketing · MNU Business School</span></footer>'
 + '</article>')
open(P('out', 'cvdoc.html'), 'w', encoding='utf-8').write(CVDOC)
CVTOP = ('<div class="cv-bar reveal"><span class="small">Updated November 2026</span><a class="btn" href="academic/Muiz_Fuad_CV.pdf" download="Muiz_Fuad_CV.pdf">Download PDF <i data-ic="download"></i></a></div>\n      <div class="reveal">' + CVDOC + '</div>')
work = sec('work')
work_in = strip_head(inner(work))
cred_in = strip_head(inner(sec('credentials')))
cbody = ('  <section class="block cv-first" id="cv-file">\n    <div class="wrap">\n      ' + CVTOP + '\n    </div>\n  </section>\n' +
         block('work', 'Practice', 'From industry to classroom', work_in, 'The work I bring into the classroom.') +
         block('credentials', 'Credentials', 'Certificates', cred_in, 'Tap one to see the certificate.'))
CVTL = [('2011', 'Marketing Officer', 'Highrise Inc.', 0), ('2014', 'Head of Marketing and Sales', 'MATTA Fair, Kuala Lumpur', 0),
        ('2018', 'Head of Operations', 'Blazon Inc.', 0), ('2020', 'Copywriter', 'Maldives Ports Limited', 0),
        ('2021', 'Marketing Manager', 'Reethi Beach Resort', 0), ('2022', 'Part-time Lecturer', 'MI College', 1),
        ('2023', 'Sales and Marketing Manager', 'Maldives Business Network TV', 0), ('2024', 'Manager, SME HUB', 'Business Centre Corporation', 0),
        ('2024', 'Lecturer', 'MNU Business School · now', 1)]
CVTL_HTML = ('<div class="cvtl reveal"><div class="cvtl-key" aria-hidden="true"><span><i></i>Industry</span><span><i class="t"></i>Teaching</span></div>'
             '<ol aria-label="Career timeline, 2011 to now">' + ''.join('<li class="%s"><time>%s</time><b>%s</b><span>%s</span></li>' % ('t' if t else '', y, r, o) for y, r, o, t in CVTL) + '</ol></div>')
page('cv', 'Curriculum vitae', 'From the industry floor to the lecture room', 'Fifteen years in tourism and marketing, then the lecture room. The full CV, the industry work I teach from, and my certificates.', cbody,
     toc=[('cv-file', 'Full CV'), ('work', 'Industry work'), ('credentials', 'Certificates')], extra=CVTL_HTML)
# ---------- CLASS ACTIVITY ----------
page('activity', 'Student tools · Class activity', 'Two weeks in the student tools', rd('activity_lede.txt'), rd('activity_body.html'),
     crumbs=[('academic.html', 'Home'), ('academic/tools.html', 'Student tools')])
print('composed', sorted(os.listdir(P('out'))), len(os.listdir(P('out', 'modules'))))
open(P('out', 'hidden.txt'), 'w', encoding='utf-8').write('\n'.join(sorted(HIDDEN)) + '\n')
