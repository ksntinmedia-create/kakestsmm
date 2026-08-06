# -*- coding: utf-8 -*-
"""Сборка блога: страница-список, страницы статей, sitemap.xml.

Запуск из корня проекта:  python3 blog/_generate.py
Контент статей — в _articles.py.
"""
import os
import re
import sys
import html
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _articles import ARTICLES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "blog")
SITE = "https://kakestsmm.ru"

MONTHS = ["января", "февраля", "марта", "апреля", "мая", "июня",
          "июля", "августа", "сентября", "октября", "ноября", "декабря"]


def ru_date(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return "%d %s %d" % (d, MONTHS[m - 1], y)


def reading_time(body):
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    return max(2, round(words / 150))


def cover(slug):
    """Обложка подхватывается автоматически: covers/<slug>.<ext>.
    Файла нет — страница собирается без картинки, ничего не ломается."""
    for ext in ("webp", "jpg", "jpeg", "png"):
        name = "%s.%s" % (slug, ext)
        if os.path.exists(os.path.join(OUT, "covers", name)):
            return "covers/" + name
    return None


def nav(active=""):
    items = [
        ("../index.html", "Главная", "home"),
        ("../index.html#services", "Услуги", "services"),
        ("index.html", "Блог", "blog"),
        ("../index.html#contacts", "Контакты", "contacts"),
    ]
    return "\n      ".join(
        '<a href="%s"%s>%s</a>' % (h, ' class="is-active"' if k == active else "", t)
        for h, t, k in items
    )


def shell(title, desc, canonical, body, active="blog", jsonld="", og_type="website",
          og_image=""):
    return """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="%(canonical)s">
<meta property="og:type" content="%(og_type)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(canonical)s">
<meta property="og:site_name" content="SMM-агентство «Как есть»">
<meta property="og:locale" content="ru_RU">
%(og_image)s
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s">
<meta name="twitter:description" content="%(desc)s">
<meta name="theme-color" content="#2563EB">
<link rel="icon" href="../assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="../assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/css/style.css">
%(jsonld)s</head>
<body class="legal-page">

<header class="legal__top">
  <div class="container legal__top-in">
    <a href="../index.html" class="logo" aria-label="Как есть — смм агентство">
      <span class="logo__mark" aria-hidden="true"><img src="../assets/img/logo-mark.svg" alt=""></span>
      <span class="logo__text"><b>КАК ЕСТЬ</b><i>СММ АГЕНТСТВО</i></span>
    </a>
    <nav class="blog__nav">
      %(nav)s
    </nav>
  </div>
</header>

%(body)s

<footer class="legal__foot">
  <div class="container">
    <nav class="legal__nav">
      <a href="index.html">Блог</a>
      <a href="../legal/privacy-policy.html">Политика обработки персональных данных</a>
      <a href="../legal/confidentiality.html">Политика конфиденциальности</a>
      <a href="../legal/terms.html">Пользовательское соглашение</a>
      <a href="../legal/consent.html">Согласие на обработку ПДн</a>
      <a href="../legal/cookies.html">Файлы cookie</a>
    </nav>
    <p class="legal__copy">© 2026 SMM-агентство «Как есть»</p>
  </div>
</footer>

</body>
</html>
""" % {
        "title": html.escape(title, quote=True),
        "desc": html.escape(desc, quote=True),
        "canonical": canonical,
        "og_type": og_type,
        "og_image": og_image,
        "jsonld": jsonld,
        "nav": nav(active),
        "body": body,
    }


CTA = """
      <aside class="post__cta">
        <h2>Разберём ваш случай бесплатно</h2>
        <p>Посмотрим профиль, контент и конкурентов и назовём пять точек роста — за 20 минут и без обязательств.</p>
        <a class="btn btn--lg" href="https://t.me/nadya_shteinbah" target="_blank" rel="noopener">получить разбор</a>
      </aside>
"""


def related(current):
    """Три статьи: сначала из той же рубрики, потом любые свежие."""
    same = [a for a in ARTICLES if a["category"] == current["category"] and a["slug"] != current["slug"]]
    rest = [a for a in ARTICLES if a["category"] != current["category"]]
    picked = (same + rest)[:3]
    cards = "\n".join(
        """        <a class="rel__card" href="%s.html">
          <span class="rel__cat">%s</span>
          <span class="rel__title">%s</span>
        </a>""" % (a["slug"], a["category"], a["h1"])
        for a in picked
    )
    return """
      <section class="rel">
        <h2 class="rel__head">Читайте также</h2>
        <div class="rel__grid">
%s
        </div>
      </section>
""" % cards


def build_article(a):
    url = "%s/blog/%s.html" % (SITE, a["slug"])
    rt = reading_time(a["body"])
    cov = cover(a["slug"])

    img_json = ',\n"image":"%s/blog/%s"' % (SITE, cov) if cov else ""
    jsonld = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article",
"headline":%s,
"description":%s%s,
"datePublished":"%s","dateModified":"%s",
"author":{"@type":"Organization","name":"SMM-агентство «Как есть»"},
"publisher":{"@type":"Organization","name":"SMM-агентство «Как есть»"},
"mainEntityOfPage":{"@type":"WebPage","@id":"%s"},
"inLanguage":"ru-RU"}
</script>
""" % (
        '"%s"' % a["h1"].replace('"', "'"),
        '"%s"' % a["description"].replace('"', "'"),
        img_json,
        a["date"], a["date"], url,
    )

    hero = ""
    if cov:
        hero = ('\n    <figure class="post__cover">'
                '<img src="%s" alt="%s" width="1200" height="630"></figure>'
                % (cov, html.escape(a["h1"], quote=True)))

    body = """<main class="container post">
  <nav class="crumbs" aria-label="Навигация">
    <a href="../index.html">Главная</a>
    <span>/</span>
    <a href="index.html">Блог</a>
    <span>/</span>
    <b>%(cat)s</b>
  </nav>

  <article class="post__body">
    <p class="post__meta"><span class="post__cat">%(cat)s</span> %(date)s · %(rt)s мин чтения</p>
    <h1>%(h1)s</h1>%(hero)s
%(text)s
%(cta)s
  </article>
%(rel)s
</main>
""" % {
        "cat": a["category"],
        "date": ru_date(a["date"]),
        "rt": rt,
        "h1": a["h1"],
        "hero": hero,
        "text": a["body"].rstrip(),
        "cta": CTA,
        "rel": related(a),
    }

    img = "%s/blog/%s" % (SITE, cov) if cov else "%s/assets/og/og-blog.jpg" % SITE
    og_image = ('<meta property="og:image" content="%s">\n'
                '<meta property="og:image:width" content="1200">\n'
                '<meta property="og:image:height" content="630">\n'
                '<meta name="twitter:image" content="%s">' % (img, img))
    page = shell(a["title"] + " | Как есть", a["description"], url, body,
                 jsonld=jsonld, og_type="article", og_image=og_image)
    with open(os.path.join(OUT, a["slug"] + ".html"), "w", encoding="utf-8") as f:
        f.write(page)


def build_index():
    cats = []
    for a in ARTICLES:
        if a["category"] not in cats:
            cats.append(a["category"])

    chips = "\n        ".join(
        '<button class="chip is-on" type="button" data-cat="all">Все</button>'
        if i == 0 else "" for i in range(1)
    )
    chips += "\n        " + "\n        ".join(
        '<button class="chip" type="button" data-cat="%s">%s</button>' % (c, c) for c in cats
    )

    posts = sorted(ARTICLES, key=lambda x: x["date"], reverse=True)
    def card(a):
        cov = cover(a["slug"])
        pic = ('\n          <span class="pcard__cover">'
               '<img src="%s" alt="" loading="lazy" width="1200" height="630"></span>'
               % cov) if cov else ""
        return """      <article class="pcard%(mod)s" data-cat="%(cat)s">
        <a class="pcard__link" href="%(slug)s.html">%(pic)s
          <span class="pcard__cat">%(cat)s</span>
          <h2 class="pcard__title">%(h1)s</h2>
          <p class="pcard__text">%(excerpt)s</p>
          <span class="pcard__meta">%(date)s · %(rt)s мин</span>
        </a>
      </article>""" % {
            "mod": " pcard--img" if cov else "",
            "cat": a["category"], "slug": a["slug"], "h1": a["h1"], "pic": pic,
            "excerpt": a["excerpt"], "date": ru_date(a["date"]),
            "rt": reading_time(a["body"]),
        }

    cards = "\n".join(card(a) for a in posts)

    items = ",".join(
        '{"@type":"ListItem","position":%d,"url":"%s/blog/%s.html"}' % (i + 1, SITE, a["slug"])
        for i, a in enumerate(posts)
    )
    jsonld = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Blog","name":"Блог SMM-агентства «Как есть»",
"url":"%s/blog/","inLanguage":"ru-RU",
"blogPost":[%s]}
</script>
""" % (SITE, items)

    body = """<main class="container blog">
  <h1>Блог о продвижении в соцсетях</h1>
  <p class="blog__lead">Разборы, инструкции и наблюдения из практики агентства: контент,
  реклама, аналитика и инструменты. Пишем то, что применяем в работе с клиентами.</p>

  <div class="chips" id="chips">
        %(chips)s
  </div>

  <div class="pgrid" id="pgrid">
%(cards)s
  </div>
  <p class="blog__empty" id="blogEmpty" hidden>В этой рубрике пока нет статей.</p>
</main>

<script>
(function () {
  var chips = document.getElementById('chips');
  var cards = document.querySelectorAll('.pcard');
  var empty = document.getElementById('blogEmpty');
  chips.addEventListener('click', function (e) {
    var btn = e.target.closest('.chip');
    if (!btn) return;
    var cat = btn.dataset.cat, shown = 0;
    chips.querySelectorAll('.chip').forEach(function (c) { c.classList.toggle('is-on', c === btn); });
    cards.forEach(function (card) {
      var ok = cat === 'all' || card.dataset.cat === cat;
      card.hidden = !ok;
      if (ok) shown++;
    });
    empty.hidden = shown > 0;
  });
})();
</script>
""" % {"chips": chips, "cards": cards}

    page = shell(
        "Блог о SMM и продвижении в соцсетях | Как есть",
        "Статьи о продвижении бизнеса в соцсетях: контент-план, таргет, Telegram, "
        "аналитика и нейросети. Практика SMM-агентства «Как есть».",
        SITE + "/blog/", body, jsonld=jsonld,
        og_image=('<meta property="og:image" content="%s/assets/og/og-blog.jpg">\n'
                  '<meta property="og:image:width" content="1200">\n'
                  '<meta property="og:image:height" content="630">\n'
                  '<meta name="twitter:image" content="%s/assets/og/og-blog.jpg">'
                  % (SITE, SITE)))
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)


def build_sitemap():
    urls = [(SITE + "/", "1.0", "weekly"), (SITE + "/blog/", "0.9", "weekly")]
    for a in sorted(ARTICLES, key=lambda x: x["date"], reverse=True):
        urls.append(("%s/blog/%s.html" % (SITE, a["slug"]), "0.7", "monthly"))
    for f in ["privacy-policy", "confidentiality", "consent", "terms", "cookies"]:
        urls.append(("%s/legal/%s.html" % (SITE, f), "0.2", "yearly"))

    today = date.today().isoformat()
    body = "\n".join(
        "  <url><loc>%s</loc><lastmod>%s</lastmod>"
        "<changefreq>%s</changefreq><priority>%s</priority></url>" % (u, today, freq, pr)
        for u, pr, freq in urls
    )
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + body + "\n</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)

    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE)


if __name__ == "__main__":
    for a in ARTICLES:
        build_article(a)
    build_index()
    build_sitemap()
    print("статей: %d, плюс index.html, sitemap.xml и robots.txt" % len(ARTICLES))
