#!/usr/bin/env python3
"""Build the individual speaker pages (summer / linda / terry) as sibling folders
next to this repo, e.g. ../summer.keynotesunlimited.com. Joanne's page is hand-built.

Usage: python3 scripts/make_speaker_page.py [slug ...]   (default: all)
Styling is lifted from ../joanne.keynotesunlimited.com/index.html so pages match.
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent          # the landing-page repo
SITES = HERE.parent
JOANNE = SITES / "joanne.keynotesunlimited.com"
DOMAIN = "keynotesunlimited.com"


def yt(i, t):
    return (i, t)


SPEAKERS = {
    "summer": dict(
        name="Summer Jelinek", first="Summer",
        title="Summer Jelinek | Leadership Keynote Speaker",
        description="Summer Jelinek is a leadership keynote speaker, consultant, and educator with more than two decades of leadership experience. Watch her videos and hear her podcast interviews.",
        og_description="Keynotes and coaching on leadership, the M.A.G.I.C. model, and neurodivergence in the workplace. Videos, podcast interviews, and more.",
        eyebrow="Keynote Speaker &middot; Leadership",
        lead="A leadership keynote speaker, consultant, and educator with more than two decades of leadership experience at organizations including Walt Disney World, the Disney Institute, H-E-B/Central Market, and the Center for Creative Leadership.",
        hero="summer-headshot.jpg", marks=["summer-headshot.jpg", "backdrop/summer.jpg"],
        extra_imgs=["summer-book.png"],
        reel_vimeo="922495012",
        yt_heading="Popular Content from Summer&rsquo;s YouTube Channel",
        yt_channel="https://www.youtube.com/@SummerJelinek",
        videos=[yt("ZHXT1LfJE9U", "The Real ADHD Leadership Guide You&rsquo;ve Been Looking For"),
                yt("wLjn9c6nAKo", "Hybrid Workplaces Expand Opportunity but Demand Adaptability"),
                yt("bqfGDNWqxrg", "Why Your Feedback Isn&rsquo;t Working (And What To Do Instead)")],
        podcast=[("Understanding Neurodivergence, Featuring Summer Jelinek, Pt. 1", "Understanding Neurodivergence, Pt. 1"),
                 ("Understanding Neurodivergence, Featuring Summer Jelinek, Pt. 2", "Understanding Neurodivergence, Pt. 2"),
                 ("Summer Jelinek on Leadership, Pt. 1", "Summer Jelinek on Leadership")],
        about_title="About Summer",
        about="""
                <div class="card panel">
                    <h3>Why select Summer?</h3>
                    <p>Summer brings real-world hospitality industry experience, combined with humor and storytelling to her keynotes. Her goals are to:</p>
                    <ul>
                        <li>Help leaders at all levels build purpose</li>
                        <li>Ignite action</li>
                        <li>Inspire teams</li>
                        <li>Stay centered in the face of adversity</li>
                    </ul>
                    <p>She is the creator of the M.A.G.I.C. model for leadership, a practical framework addressing:</p>
                    <ul>
                        <li>Self-management</li>
                        <li>Purpose alignment</li>
                        <li>Team galvanization</li>
                        <li>Team inspiration</li>
                        <li>Chaos control</li>
                    </ul>
                    <h3>Key topics</h3>
                    <ul>
                        <li>The M.A.G.I.C. Leadership Model</li>
                        <li>Neurodivergence in the Workplace</li>
                        <li>Quality Leaders = Quality Culture</li>
                    </ul>
                </div>
                <div class="card panel">
                    <h3>Author and coach</h3>
                    <p>She is a proud neurodivergent leadership expert and PhD researcher who shares straightforward leadership truths to empower audiences and organizations to chart new paths forward. Additionally, she&rsquo;s a best-selling author.</p>
                    <img src="img/summer-book.png" alt="Unlocking the Magic of Leadership by Summer Jelinek" loading="lazy" style="display:block;max-width:220px;width:100%;height:auto;margin:6px 0 16px;border-radius:4px;box-shadow:0 4px 14px rgba(0,0,0,.25)">
                    <p>Summer provides values-based coaching that is rooted in co-creating. She understands that there are no one-size-fits-all approaches to human development. This means she works with clients on unpacking ideas and discovering what&rsquo;s next. She creates tools for each individual client and creates a judgment-free zone for self-discovery.</p>
                </div>""",
        follow=[("https://www.linkedin.com/in/summerjelinek/", "LinkedIn", "summerjelinek"),
                ("https://www.instagram.com/summerjelinek/", "Instagram", "@summerjelinek"),
                ("https://www.youtube.com/@SummerJelinek", "YouTube", "Leadership videos"),
                ("https://summerjelinek.com/", "Website", "summerjelinek.com")],
    ),
    "linda": dict(
        name="Linda Roszak Burton", first="Linda",
        title="Linda Roszak Burton | Keynote Speaker on Gratitude & Well-Being",
        description="Linda Roszak Burton is a respected authority on strengths and evidence-based leadership development, researcher, author, keynote speaker, and board-certified health and well-being coach.",
        og_description="Keynotes and coaching on gratitude, positive psychology, and evidence-based leadership development. Her TEDx talk, podcast interviews, and more.",
        eyebrow="Keynote Speaker &middot; Gratitude &amp; Well-Being",
        lead="A respected authority on strengths and evidence-based leadership development, researcher, author, keynote speaker, and board-certified health and well-being coach.",
        hero="linda-headshot.jpg", marks=["linda-headshot.jpg", "backdrop/linda.jpg"],
        extra_imgs=[],
        featured_yt=("paXMGo8cHSo", "Linda Roszak Burton TEDx talk: Gratitude, The Power to Heal the World"),
        videos=[], yt_channel=None,
        podcast=[("Developing Grateful Hearts, Featuring Linda Roszak Burton", "Developing Grateful Hearts"),
                 ("Gratitude in Chaotic Times, Featuring Linda Roszak Burton", "Gratitude in Chaotic Times"),
                 ("Post-Traumatic Growth Featuring Linda Roszak Burton", "Post-Traumatic Growth")],
        about_title="About Linda",
        about="""
                <div class="card panel">
                    <h3>Why select Linda?</h3>
                    <ul>
                        <li>Her programs are informed by the latest research and best practices in gratitude, positive psychology, and neuroscience</li>
                        <li>Her programs are designed to engage adult learners and build and broaden the applications of new knowledge</li>
                        <li>She emphasizes measurable leadership and culture performance strategies that improve how people work together and advance the well-being of employees and their organization</li>
                    </ul>
                    <p>Linda&rsquo;s keynotes reflect clients&rsquo; desired outcomes with pre-event planning to ensure cultural and program objectives are met. Some of Linda&rsquo;s recent speaking engagements include:</p>
                    <ul>
                        <li><em>The Science of Gratitude: The Positive Impact on Employees and the Organization</em></li>
                        <li><em>The Gratitude Edge: Harnessing the Science of Gratitude to Elevate Well-Being, Engagement and Partnerships</em></li>
                        <li><em>The Health and Well-Being Benefits of Gratitude</em></li>
                    </ul>
                </div>
                <div class="card panel">
                    <h3>Thought leadership</h3>
                    <p>Linda shares her subject matter expertise in a variety of ways, including:</p>
                    <ul>
                        <li>Her TEDx Talk, <em>Gratitude: The Power to Heal the World</em></li>
                        <li>Her international academic research partnerships in England and Australia</li>
                        <li>As a contributor to the <em>Wharton Healthcare Quarterly</em> feature series on gratitude since 2017</li>
                        <li>Author of <em>Gratitude Heals&reg;: A Journal for Inspiration and Guidance</em></li>
                        <li><strong>Newly released:</strong> <em>What Went Well Today?</em> A 60-day e-Journal mapping character strengths, energy and mood levels, milestones and growth</li>
                    </ul>
                    <h3>Coaching</h3>
                    <p>Linda is honored to coach esteemed leaders across industries, using strength-based and well-being coaching methodologies informed by current research and evidence-based practices in neuroscience, positive psychology, and gratitude, ensuring her work supports mission-driven cultures. Linda is an ICF-ACC Certified Executive Coach and a National Board-Certified Health and Well-Being Coach (NBC-HWC*). She holds certifications in Brain-Based Coaching from the NeuroLeadership Institute and in Positive Psychology Health and Well-Being through the College of Executive Coaching. She is a member of the Institute of Coaching at McLean Hospital/Harvard Medical School Associate.</p>
                    <p class="hint">*Linda maintains an active, nationally recognized credential, follows the NBC-HWC Code of Ethics and is HIPAA-compliant.</p>
                </div>""",
        follow=[("https://www.linkedin.com/in/lindaroszakburton", "LinkedIn", "lindaroszakburton"),
                ("https://drwcoaching.com/", "Website", "drwcoaching.com")],
    ),
    "terry": dict(
        name="Teresita &ldquo;Terry&rdquo; Britton, PCC", first="Terry",
        title="Teresita Britton, PCC | Executive Coach & Organizational Development Consultant",
        description="Teresita “Terry” Britton, PCC, is an executive coach and organizational development consultant who guides leaders and organizations through change.",
        og_description="Executive coaching, leadership program design, and culture transformation for senior leaders and enterprise teams.",
        eyebrow="Executive Coach &middot; Organizational Development",
        lead="An executive coach and organizational development consultant who guides leaders and organizations through change, with more than 20 years of experience.",
        hero="terry-headshot.jpg", marks=["terry-headshot.jpg", "backdrop/terry.jpg"],
        extra_imgs=[],
        featured_yt=("iX6jLIkvFfA", "Leadership Solutions"),
        videos=[], yt_channel=None, podcast=[],
        about_title="About Terry",
        about="""
                <div class="card panel">
                    <h3>Her experience</h3>
                    <p>For more than 20 years Terry has:</p>
                    <ul>
                        <li>Designed and facilitated leadership programs, retreats, and workshops</li>
                        <li>Coached CEOs, C-suite executives, and senior leadership teams at Fortune 500 corporations</li>
                        <li>Coached executives in federal agencies</li>
                    </ul>
                    <p>Founder of Leadership Solutions LLC, Terry designs custom development experiences for every level of the enterprise. She builds retreats and programs for an organization&rsquo;s most senior leaders to cohort-based programs for mid-level and emerging leaders. Her designs use action learning, structured projects, and peer learning so the change shows up on the job.</p>
                    <p>Change and culture are the threads through all of her work. Terry has a depth of knowledge in adaptive change. That is the kind of change no plan or restructuring can solve. It requires leaders to shift how they think and behave.</p>
                    <h3>Key topics</h3>
                    <ul>
                        <li>Leading Adaptive Change</li>
                        <li>Culture Assessment and Transformation</li>
                        <li>Leadership Operating Systems</li>
                    </ul>
                </div>
                <div class="card panel">
                    <h3>Why select Terry?</h3>
                    <ul>
                        <li>She conducts culture assessments that show leaders where culture supports or undermines strategy</li>
                        <li>She integrates belonging and inclusion into all of her programs and coaching</li>
                        <li>She facilitates leadership teams as they build their own Leadership Operating Systems, the operating rhythms that guide the enterprise</li>
                        <li>She provides tools that enable organizations to create and implement practices that sustain new behavior and turn strategy into execution</li>
                    </ul>
                    <h3>Credentials</h3>
                    <ul>
                        <li>Certificate in leadership coaching from Georgetown University</li>
                        <li>Certificate in change management from Johns Hopkins University</li>
                        <li>Certificate in the neuroscience of leadership from Harvard Medical School</li>
                        <li>Certificate in leading diversity, equity, and inclusion from Northwestern University</li>
                    </ul>
                    <p>She brings a background in finance and operations, and is certified in Hogan, Gallup Strengths, and the Leadership Circles assessments and is a Diversity and Belonging Facilitator through Culture Veritas. Additionally, Terry provides leadership program design and development. She earns recognition for her senior leader retreats and developmental programs.</p>
                </div>""",
        follow=[("https://www.linkedin.com/in/teresita-britton-8418bb179/", "LinkedIn", "Teresita Britton"),
                ("https://theleadersolution.com/", "Website", "theleadersolution.com")],
    ),
}


def card(i, t):
    return f'''                <a class="vid" href="https://www.youtube.com/watch?v={i}" data-id="{i}" target="_blank" rel="noopener">
                    <div class="thumb"><img loading="lazy" src="https://i.ytimg.com/vi/{i}/hqdefault.jpg" alt=""><span class="play">&#9654;</span></div>
                    <div class="meta"><strong>{t}</strong></div>
                </a>
'''


def build(slug, c):
    host = f"{slug}.{DOMAIN}"
    out = SITES / host
    for d in ("img", "data", "scripts", ".github/workflows"):
        (out / d).mkdir(parents=True, exist_ok=True)
    shutil.copy(JOANNE / "favicon.png", out / "favicon.png")
    shutil.copy(JOANNE / "logo.jpg", out / "logo.jpg")
    (out / "CNAME").write_text(host + "\n")
    (out / ".gitignore").write_text(".DS_Store\n")

    marks = []
    for n, src in enumerate(c["marks"], 1):
        dst = f"{slug}-{n}.jpg"
        shutil.copy(HERE / src, out / "img" / dst)
        marks.append(f"{slug}-{n}")
    for f in c.get("extra_imgs", []):
        shutil.copy(HERE / f, out / "img" / f)

    jh = (JOANNE / "index.html").read_text()
    css = re.search(r"<style>.*?</style>", jh, re.S).group(0)
    plain_name = html.unescape(re.sub(r"<[^>]+>", "", c["name"]))
    page_title = html.escape(c["title"]).replace("&amp;", "&")
    desc = html.escape(c["description"], quote=True)
    ogd = html.escape(c["og_description"], quote=True)
    head = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <meta name="description" content="{desc}">
    <meta property="og:title" content="{html.escape(c["title"], quote=True)}">
    <meta property="og:description" content="{ogd}">
    <meta property="og:image" content="https://{host}/img/{marks[0]}.jpg">
    <meta property="og:url" content="https://{host}/">
    <link rel="icon" type="image/png" href="favicon.png">
    {css}
</head>
'''
    has_pod = bool(c["podcast"])
    has_vid = bool(c.get("reel_vimeo") or c.get("featured_yt") or c["videos"])
    nav = ""
    if has_vid:
        nav += '                <a href="#videos">Videos</a>\n'
    if has_pod:
        nav += '                <a href="#podcast">Podcast</a>\n'
    nav += '                <a href="#about">About</a>\n                <a href="#follow">Follow</a>\n'
    btns = ""
    if has_vid:
        btns += f'                    <a class="btn" href="#videos">Watch {c["first"]}</a>\n'
    if has_pod:
        btns += '                    <a class="btn ghost" href="#podcast">Listen to the podcast</a>\n'
    if not btns:
        btns = '                    <a class="btn" href="#about">About ' + c["first"] + '</a>\n'

    body = f'''<body>
    <div class="watermark" aria-hidden="true"></div>

    <header class="topbar">
        <div class="wrap">
            <a class="brand" href="https://{DOMAIN}" aria-label="Keynotes and Coaching Unlimited"><img src="logo.jpg" alt="Keynotes and Coaching Unlimited"></a>
            <nav>
{nav}                <a class="back" href="https://{DOMAIN}">All speakers &rarr;</a>
            </nav>
        </div>
    </header>

    <section class="hero">
        <div class="wrap">
            <div>
                <p class="eyebrow">{c["eyebrow"]}</p>
                <h1>{c["name"]}</h1>
                <p class="lead">{c["lead"]}</p>
                <div class="btns">
{btns}                </div>
            </div>
            <div class="photo"><img src="img/{marks[0]}.jpg" alt="{html.escape(plain_name)}"></div>
        </div>
    </section>

    <main class="wrap">
'''
    if has_vid:
        body += '        <section class="block" id="videos">\n            <h2 class="title">Watch ' + c["first"] + '</h2>\n'
        if c.get("reel_vimeo"):
            body += f'''            <div class="featured">
                <div class="embed">
                    <iframe src="https://player.vimeo.com/video/{c["reel_vimeo"]}" title="{html.escape(plain_name)} speaker reel" loading="lazy" allow="fullscreen; picture-in-picture" allowfullscreen></iframe>
                </div>
            </div>
'''
        if c.get("featured_yt"):
            i, t = c["featured_yt"]
            body += f'''            <div class="featured">
                <div class="embed">
                    <iframe src="https://www.youtube-nocookie.com/embed/{i}?rel=0" title="{html.escape(t)}" loading="lazy" allow="accelerometer; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>
                </div>
            </div>
'''
        if c["videos"]:
            body += f'''
            <h3 style="margin:34px 0 14px">{c["yt_heading"]}</h3>
            <div class="vgrid">
{"".join(card(*v) for v in c["videos"])}            </div>
            <p class="hint"><a href="{c["yt_channel"]}?sub_confirmation=1" target="_blank" rel="noopener">Subscribe on YouTube</a></p>
'''
        body += "        </section>\n\n"
    if has_pod:
        body += '''        <section class="block" id="podcast">
            <h2 class="title">Podcast Interviews</h2>
            <div id="episodes"></div>
            <noscript><p class="hint">Turn on JavaScript to see the episodes.</p></noscript>
        </section>

'''
    body += f'''        <section class="block" id="about">
            <h2 class="title">{c["about_title"]}</h2>
            <div class="cols">{c["about"]}
            </div>
        </section>

        <section class="block" id="follow">
            <h2 class="title">Follow {c["first"]}</h2>
            <div class="follow">
''' + "".join(f'                <a href="{u}" target="_blank" rel="noopener"><strong>{t}</strong><span>{s}</span></a>\n' for u, t, s in c["follow"]) + f'''            </div>
        </section>
    </main>

    <footer class="site">
        <img src="logo.jpg" alt="Keynotes and Coaching Unlimited">
        <p class="cta">Let&rsquo;s talk about your needs.</p>
        <p>Pablo Jusem, Talent Connector</p>
        <p><a href="https://{DOMAIN}">{DOMAIN}</a> &middot; meet all our speakers and coaches</p>
    </footer>

    <div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Video player">
        <div class="box">
            <button class="close" id="lbclose" type="button">Close &times;</button>
            <div class="embed" id="lbembed"></div>
        </div>
    </div>

    <script>
    (function () {{
        var photos = {json.dumps(["img/%s.jpg" % m for m in marks])};
        var D = 170, box = document.querySelector('.watermark');
        function tiles() {{
            var w = window.innerWidth, h = window.innerHeight, html = '';
            var rows = Math.ceil(h / (D / 2)) + 2, cols = Math.ceil(w / D) + 2;
            for (var r = 0; r < rows; r++) for (var c = 0; c < cols; c++) {{
                var x = c * D + (r % 2 ? D / 2 : 0) - D / 2, y = r * (D / 2) - D / 2;
                html += '<span style="left:' + x + 'px;top:' + y + 'px;background-image:url(' + photos[(c * 3 + r * 5) % photos.length] + ')"></span>';
            }}
            box.innerHTML = html;
        }}
        var t; window.addEventListener('resize', function () {{ clearTimeout(t); t = setTimeout(tiles, 150); }});
        tiles();

        function esc(s) {{ return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {{ return {{ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }}[c]; }}); }}

        var lb = document.getElementById('lightbox'), lbe = document.getElementById('lbembed');
        function closeLb() {{ lb.classList.remove('open'); lbe.innerHTML = ''; }}
        document.getElementById('lbclose').addEventListener('click', closeLb);
        lb.addEventListener('click', function (e) {{ if (e.target === lb) closeLb(); }});
        document.addEventListener('keydown', function (e) {{ if (e.key === 'Escape') closeLb(); }});
        document.addEventListener('click', function (e) {{
            var a = e.target.closest('a.vid'); if (!a) return;
            e.preventDefault();
            lbe.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + a.dataset.id + '?autoplay=1&rel=0" title="Video" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>';
            lb.classList.add('open');
        }});
'''
    if has_pod:
        body += '''
        fetch('data/feeds.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }).then(function (d) {
            document.getElementById('episodes').innerHTML = ((d.podcast || {}).episodes || []).map(function (e) {
                return '<article class="card ep"><h3><a href="' + esc(e.link) + '" target="_blank" rel="noopener">' + esc(e.display) + '</a></h3></article>';
            }).join('');
        }).catch(function () {
            document.getElementById('episodes').innerHTML = '';
        });
'''
    body += "    })();\n    </script>\n</body>\n</html>\n"
    (out / "index.html").write_text(head + body)

    if has_pod:
        (out / "scripts" / "update_feeds.py").write_text(FEED_SCRIPT.replace("__PICKS__", json.dumps(c["podcast"], indent=4, ensure_ascii=False)).replace("__WHO__", plain_name))
        shutil.copy(JOANNE / ".github/workflows/update-feeds.yml", out / ".github/workflows/update-feeds.yml")
    else:
        for p in ("scripts", ".github", "data"):
            shutil.rmtree(out / p, ignore_errors=True)
    print("built", out)


FEED_SCRIPT = '''#!/usr/bin/env python3
"""Pull __WHO__'s picked podcast episodes into data/feeds.json.

Run on a schedule by .github/workflows/update-feeds.yml. Standard library only.
Each pick is [exact feed title, title to display on the page].
"""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

PODCAST_FEED = "https://media.rss.com/smiklespeaks/feed.xml"
PICKED_EPISODES = __PICKS__
OUT = Path(__file__).resolve().parent.parent / "data" / "feeds.json"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "keynotesunlimited-feed-bot/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def podcast():
    ch = ET.fromstring(fetch(PODCAST_FEED)).find("channel")
    items = {it.findtext("title"): it for it in ch.findall("item")}
    missing = [t for t, _ in PICKED_EPISODES if t not in items]
    if missing:
        raise RuntimeError(f"picked episodes not in feed: {missing}")
    return {"episodes": [
        {"title": t, "display": shown, "link": items[t].findtext("link")}
        for t, shown in PICKED_EPISODES
    ]}


def main():
    try:
        data = {"podcast": podcast()}
    except Exception as exc:  # keep the previous file if the feed is down
        print("podcast feed failed:", exc, file=sys.stderr)
        sys.exit(1)
    OUT.parent.mkdir(exist_ok=True)
    if OUT.exists():
        old = json.loads(OUT.read_text())
        old.pop("updated", None)
        if old == data:
            print("no changes")
            return
    data["updated"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\\n")
    print(f"wrote {OUT}: {len(data['podcast']['episodes'])} episodes")


if __name__ == "__main__":
    main()
'''

if __name__ == "__main__":
    which = sys.argv[1:] or list(SPEAKERS)
    for s in which:
        build(s, SPEAKERS[s])
        if SPEAKERS[s]["podcast"]:
            import subprocess
            subprocess.run([sys.executable, str(SITES / f"{s}.{DOMAIN}" / "scripts" / "update_feeds.py")], check=True)
