# Builds the static website for The GITA Project from the e-book chapter XHTML.
# Reusable: add chapters to CHAPTERS and rerun. Output: web/*.html
import re, os

HERE = os.path.dirname(os.path.abspath(__file__))
EPUB = os.path.join(HERE, '..', 'epub_build', 'OEBPS')

# num, sanskrit, english, theme, epub filename (None = not built yet)
CHAPTERS = [
 (1,"Arjuna Viṣhāda Yoga","The Yoga of Arjuna's Despair","When Confusion Becomes the Beginning of Wisdom","ch01.xhtml"),
 (2,"Sāṅkhya Yoga","The Yoga of Knowledge","Seeing Beyond the Immediate Crisis","ch02.xhtml"),
 (3,"Karma Yoga","The Yoga of Selfless Action","Act Fully Without Being Owned by the Outcome","ch03.xhtml"),
 (4,"Jñāna Karma Sannyāsa Yoga","Knowledge and Selfless Action","How Wisdom Changes the Way We Act","ch04.xhtml"),
 (5,"Karma Sannyāsa Yoga","The Yoga of Renunciation","Renunciation Is More Than Walking Away",None),
 (6,"Dhyāna Yoga","The Yoga of Meditation","Training the Mind Without Fighting Yourself",None),
 (7,"Jñāna Vijñāna Yoga","Knowledge and Realization","Knowing About the Divine and Recognizing It",None),
 (8,"Akṣhara Brahma Yoga","The Eternal Reality","What We Remember Shapes How We Live",None),
 (9,"Rāja Vidyā Rāja Guhya Yoga","The Sovereign Knowledge","The Most Transformative Wisdom Can Be Simple",None),
 (10,"Vibhūti Yoga","Divine Manifestations","Learning to See Greatness Without Envy",None),
 (11,"Viśhvarūpa Darśhana Yoga","The Universal Form","When Reality Is Larger Than Our View",None),
 (12,"Bhakti Yoga","The Yoga of Devotion","Devotion as a Way of Living",None),
 (13,"Kṣhetra Kṣhetrajña Vibhāga Yoga","The Field and the Knower","The Body, the Mind, and the One Who Knows",None),
 (14,"Guṇatraya Vibhāga Yoga","The Three Guṇas","Understanding the Forces That Influence Us",None),
 (15,"Puruṣhottama Yoga","The Supreme Person","Remembering Our Highest Source",None),
 (16,"Daivāsura Sampad Vibhāga Yoga","Divine and Destructive Tendencies","The Qualities We Strengthen Become Who We Are",None),
 (17,"Śhraddhātraya Vibhāga Yoga","The Threefold Faith","What We Trust Shapes What We Become",None),
 (18,"Mokṣha Sannyāsa Yoga","Freedom Through Renunciation","From Confusion to Clear, Responsible Action",None),
]

# auto-detect which chapters are built in the e-book source
CHAPTERS=[(n,sk,en,th,(f"ch{n:02d}.xhtml" if os.path.exists(os.path.join(EPUB,f"ch{n:02d}.xhtml")) else fn))
          for (n,sk,en,th,fn) in CHAPTERS]

def page(num):
    return f"chapter-{num:02d}.html"

def header(active):
    nav=lambda h,l,a: f'<a href="{h}"{" aria-current=\"page\"" if a==active else ""}>{l}</a>'
    return ('<header class="site-header"><div class="bar">'
      '<a class="brand" href="index.html"><span class="dot">◆</span>&nbsp;The GITA Project<span class="dot">™</span></a>'
      '<div class="bar-right">'
      '<nav class="site-nav" id="sitenav">'
      + nav("index.html","Home","home")
      + nav("introduction.html","Introduction","intro")
      + nav("index.html#journey","Journey","journey")
      + nav("living-the-gita.html","Living the Gita","conclusion")
      + nav("appendices.html","Appendices","appendices")
      + nav("glossary.html","Glossary","glossary")
      + '</nav>'
      '<button class="themebtn" id="tt" type="button" aria-label="Toggle light or dark theme">◐ Theme</button>'
      '<button class="navtoggle" id="navtoggle" type="button" aria-label="Open menu" aria-expanded="false">☰</button>'
      '</div></div></header>')

FOOTER=('<footer class="site-footer">The GITA Project™ — One\'s Own Journey Through Life · '
  'Student Handbook v1.0 · Public-Domain Edition. Verse translations: Annie Besant (1922), public domain.<br/>© 2026 <a href="https://b-temple.org/">Bharatiya Temple</a>. All rights reserved.</footer>')

THEMEJS=("(function(){var b=document.getElementById('tt'),r=document.documentElement;"
 "try{var s=localStorage.getItem('gita-theme');if(s)r.setAttribute('data-theme',s);}catch(e){}"
 "if(b)b.addEventListener('click',function(){var c=r.getAttribute('data-theme')||'dark';"
 "var n=c==='dark'?'light':'dark';"
 "r.setAttribute('data-theme',n);try{localStorage.setItem('gita-theme',n);}catch(e){}});"
 "var nt=document.getElementById('navtoggle'),nv=document.getElementById('sitenav');"
 "if(nt&&nv){nt.addEventListener('click',function(){var o=nv.classList.toggle('open');nt.setAttribute('aria-expanded',o);});"
 "nv.addEventListener('click',function(e){if(e.target.tagName==='A')nv.classList.remove('open');});}"
 "})();")

def shell(title, body, active):
    return (f'<!doctype html>\n<html lang="en" data-theme="dark">\n<head>\n<meta charset="utf-8">\n'
      f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
      f'<title>{title} — The GITA Project</title>\n'
      f'<link rel="stylesheet" href="assets/site.css">\n</head>\n<body>\n'
      f'{header(active)}\n{body}\n{FOOTER}\n<script>{THEMEJS}</script>\n</body>\n</html>\n')

def linkify(html):
    # verse header number (… · 2.47) -> external verse link
    html=re.sub(r'(<p class="vh">[^<]*?·\s*)(\d+)\.(\d+)(</p>)',
        lambda m:f'{m.group(1)}<a href="https://en.wikisource.org/wiki/Bhagavad-Gita_(Besant_4th)/Discourse_{m.group(2)}" target="_blank" rel="noopener">{m.group(2)}.{m.group(3)}</a>{m.group(4)}',
        html)
    # attribution "Bhagavad Gita X.Y" -> external verse link
    html=re.sub(r'Bhagavad Gita (\d+)\.(\d+)',
        lambda m:f'<a href="https://en.wikisource.org/wiki/Bhagavad-Gita_(Besant_4th)/Discourse_{m.group(1)}" target="_blank" rel="noopener">Bhagavad Gita {m.group(1)}.{m.group(2)}</a>',
        html)
    return html

def extract_body(fn):
    x=open(os.path.join(EPUB,fn),encoding='utf-8').read()
    m=re.search(r'<section[^>]*>(.*)</section>', x, re.S)
    body=m.group(1)
    body=body.replace(' epub:type="chapter"','')
    return body

def prevnext(num):
    meta={c[0]:c for c in CHAPTERS}
    parts=['<nav class="prevnext">']
    p=meta.get(num-1)
    if p and p[4]:
        parts.append(f'<a class="prev" href="{page(num-1)}"><span class="dir">‹ Previous</span>'
                     f'<span class="ttl">Ch {num-1} — {p[1]}</span></a>')
    else:
        parts.append('<a class="prev disabled" href="#"><span class="dir">‹ Previous</span><span class="ttl">—</span></a>')
    n=meta.get(num+1)
    if n and n[4]:
        parts.append(f'<a class="next" href="{page(num+1)}"><span class="dir">Next ›</span>'
                     f'<span class="ttl">Ch {num+1} — {n[1]}</span></a>')
    else:
        parts.append('<a class="next disabled" href="#"><span class="dir">Next ›</span>'
                     '<span class="ttl">Coming soon</span></a>')
    parts.append('</nav>')
    return '\n'.join(parts)

built=0
for num,sk,en,th,fn in CHAPTERS:
    if not fn: continue
    body=linkify(extract_body(fn))
    crumb=f'<p class="crumb"><a href="index.html">The GITA Project</a> › Week {num} · Chapter {num}</p>'
    main=f'<main class="wrap"><div class="reading">\n{crumb}\n{body}\n{prevnext(num)}\n</div></main>'
    open(os.path.join(HERE,page(num)),'w',encoding='utf-8').write(shell(f"Chapter {num}: {sk}", main, f"ch{num}"))
    built+=1

# ---- extra pages (front matter, conclusion, appendices) ----
EXTRAS=[('introduction','front_04_intro.xhtml','Introduction — Before We Begin','intro'),
        ('how-to-use','front_05_howto.xhtml','How to Use This Book','howto'),
        ('living-the-gita','conclusion.xhtml','Living the Gita','conclusion'),
        ('appendices','appendices.xhtml','Appendices &amp; Resources','appendices')]
for slug,srcfile,title,active in EXTRAS:
    if not os.path.exists(os.path.join(EPUB,srcfile)): continue
    body=linkify(extract_body(srcfile))
    crumb=f'<p class="crumb"><a href="index.html">The GITA Project</a> &#8250; {title}</p>'
    main=f'<main class="wrap"><div class="reading">\n{crumb}\n{body}\n</div></main>'
    open(os.path.join(HERE,slug+'.html'),'w',encoding='utf-8').write(shell(title,main,active))

# ---- index ----
IC_BOOK=('<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
 '<path d="M16 8c-2.2-1.6-5.2-2.2-8.5-2.2V25c3.3 0 6.3.6 8.5 2.2 2.2-1.6 5.2-2.2 8.5-2.2V5.8c-3.3 0-6.3.6-8.5 2.2z"/><path d="M16 8v19.2"/></svg>')
IC_COMPASS=('<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
 '<circle cx="16" cy="16" r="11.5"/><path d="M21.5 10.5l-3 7-6.5 3 3-7z" fill="currentColor" stroke="none"/><circle cx="16" cy="16" r="1.3" fill="currentColor" stroke="none"/></svg>')
IC_LOTUS=('<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
 '<path d="M16 7c2.5 3.5 2.5 8 0 12-2.5-4-2.5-8.5 0-12z"/><path d="M16 19c-4.5-2.5-8-2-11.5.5 2 4.5 6.5 6.5 11.5 6.5"/><path d="M16 19c4.5-2.5 8-2 11.5.5-2 4.5-6.5 6.5-11.5 6.5"/></svg>')
pillars=('<h2 class="sec pillars-title">The Three Pillars</h2>'
 '<p class="pillars-sub">Every chapter moves through the same three steps.</p>'
 '<div class="pillars">'
 f'<div class="pillar"><div class="pillar-ic">{IC_BOOK}</div><div class="p-n">Pillar One</div><h3>Scripture</h3>'
 '<p>Every chapter begins with what Lord Shri Krishna teaches Arjuna — real verses, in Sanskrit and English.</p></div>'
 f'<div class="pillar"><div class="pillar-ic">{IC_COMPASS}</div><div class="p-n">Pillar Two</div><h3>Understanding Dharma</h3>'
 '<p>We learn to think through life\'s hard choices — not with slogans, but with wisdom.</p></div>'
 f'<div class="pillar"><div class="pillar-ic">{IC_LOTUS}</div><div class="p-n">Pillar Three</div><h3>Character</h3>'
 '<p>Each week develops one virtue, practised in real life until it becomes who we are.</p></div></div>')
jrows=[]
for num,sk,en,th,fn in CHAPTERS:
    if fn:
        jrows.append(f'<li><a href="{page(num)}"><span class="wk">Week {num}</span>'
                     f'<span><span class="nm">{sk}</span> — <span class="th">{th}</span></span></a></li>')
    else:
        jrows.append(f'<li><span class="soon"><span class="wk">Week {num}</span>'
                     f'<span><span class="nm">{sk}</span> — <span class="th">{th}</span> · <em>coming soon</em></span></span></li>')
home=(f'<main class="wrap">'
 f'<section class="cover-hero">'
 f'<p class="ch-eyebrow">Student Handbook · Public-Domain Edition</p>'
 f'<h1 class="ch-title">The GITA Project™</h1>'
 f'<p class="ch-sub">One\'s Own Journey Through Life</p>'
 f'<img class="ch-art" src="images/cover.jpg" alt="Lord Shri Krishna blesses Arjuna in the golden chariot at sunrise on the field of Kurukshetra."/>'
 f'<p class="ch-tagline">Timeless wisdom for the choices you face right now.</p>'
 f'<p class="ch-hook">Five thousand years old — and it still speaks your language. Climb into the chariot beside Arjuna as Lord Shri Krishna turns <span class="hl">fear</span> into <span class="hl">clarity</span>, with real answers for the things you actually face: courage, friendship, failure, and doing what is <em>right</em>.</p>'
 f'<div class="ch-chips"><span class="chip">18 Chapters</span><span class="chip">18 Virtues</span><span class="chip">One Journey</span></div>'
 f'<div class="ch-cta"><a class="dl-btn dl-btn-lg" href="The_GITA_Project.epub" download>&#8681;&nbsp; Download the e-book</a> <a class="ch-read" href="introduction.html">Start reading &#8250;</a></div>'
 f'</section>'
 f'{pillars}'
 f'<h2 class="sec" id="journey">The 18-Week Journey</h2>'
 f'<p class="journey-lead">New here? <strong>Begin with the Introduction</strong> — it sets up everything that follows.</p>'
 f'<ul class="journey">'
 f'<li><a class="start-here" href="introduction.html"><span class="wk">Start here</span><span><span class="nm">Introduction — Before We Begin</span> — <span class="th">Why this journey matters, what the Bhagavad Gita is, the Three Pillars, and the Court of Dharma. <em>Read this first.</em></span></span></a></li>'
 f'<li><a class="start-here" href="how-to-use.html"><span class="wk">Then</span><span><span class="nm">How to Use This Book</span> — <span class="th">The weekly rhythm, the journey at a glance, and the student covenant.</span></span></a></li>'
 f'{"".join(jrows)}</ul>'
 f'<h2 class="sec">Also in this book</h2>'
 f'<ul class="journey">'
 f'<li><a href="living-the-gita.html"><span class="wk">Part III</span><span><span class="nm">Living the Gita</span> — <span class="th">looking back, the character compass, a lifelong practice</span></span></a></li>'
 f'<li><a href="appendices.html"><span class="wk">Part IV</span><span><span class="nm">Appendices &amp; Resources</span> — <span class="th">glossary, verse index, tracker, references</span></span></a></li>'
 f'<li><a href="glossary.html"><span class="wk">Ref</span><span><span class="nm">Glossary</span> — <span class="th">key Sanskrit terms</span></span></a></li>'
 f'</ul>'
 f'</main>')
open(os.path.join(HERE,'index.html'),'w',encoding='utf-8').write(shell("Home", home, "home"))

# ---- glossary ----
terms=[
 ("Ātman","The eternal Self. Our true spiritual identity beyond the physical body and mind."),
 ("Bhagavad Gita","“The Song of the Lord.” A timeless dialogue between Lord Shri Krishna and Arjuna within the Mahābhārata."),
 ("Bhakti","Loving devotion expressed through faith, gratitude, service, and remembrance of the Divine."),
 ("Brahman","The Supreme Eternal Reality."),
 ("Dharma","The eternal principle of right responsibility and conduct appropriate to one's situation. Our task is to understand it and live by it."),
 ("Guṇas","The three qualities of nature — sattva (clarity), rajas (activity), tamas (inertia). Changing influences, never fixed labels for people."),
 ("Guru","One who removes ignorance through knowledge and wisdom."),
 ("Jñāna","Knowledge that transforms understanding."),
 ("Karma","Action and its consequences."),
 ("Karma Yoga","Performing one's responsibilities according to Dharma, without selfish attachment to results."),
 ("Kurukshetra","“The land of the Kurus.” In this book, also every situation where Dharma must be understood and lived."),
 ("Moksha","Freedom from ignorance and realization of one's eternal relationship with the Divine."),
 ("Samatvam","Evenness of mind in success and failure — the balance the Gita calls Yoga (2.48)."),
 ("Swa-dharma","One's own authentic duty or path (3.35)."),
 ("Yoga","The path connecting our lives with the Divine through wisdom, action, devotion, and self-mastery."),
]
gl='<main class="wrap"><div class="reading"><p class="kicker">Appendix</p><h1 class="title" style="font-family:var(--serif)">Glossary</h1>'
gl+='<p class="eng">Key Sanskrit terms from the journey.</p><div class="glossary-grid">'
for t,d in terms: gl+=f'<div class="gloss"><span class="gterm">{t}</span><span class="gdef">{d}</span></div>'
gl+='</div></div></main>'
open(os.path.join(HERE,'glossary.html'),'w',encoding='utf-8').write(shell("Glossary", gl, "glossary"))

print(f"Built {built} chapter pages + index.html + glossary.html")
