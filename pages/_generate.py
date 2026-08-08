# -*- coding: utf-8 -*-
"""Сборка посадочных страниц: услуги, кейсы, цены, контакты, 404.

  python3 pages/_generate.py

Контент — в _content.py. Мета-теги соответствуют SEO-документу (раздел 4).
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = "https://kakestsmm.ru"

sys.path.insert(0, HERE)
from _content import PAGES, REVIEWS  # noqa: E402

TG = "https://t.me/nadya_shteinbah"

CASES = [
    ("case-cosmetology.jpg", "Instagram-аккаунт врача-косметолога", "@dr.mksimova", "Косметология",
     ["Подписчики +1 628", "Рост просмотров +74% за месяц",
      "Средний процент просмотров от неподписчиков: ~77–88%"]),
    ("case-fitness.jpg", "Instagram-аккаунт фитнес-студии", "«Боди Фитнес»", "Фитнес",
     ["Охваты +59%", "Новые пользователи в охватах +25–30%",
      "Просмотры Reels выросли до 25 000+ в неделю, рост 72%"]),
    ("case-himki.jpg", "Телеграм-канал «Афиша Химки»", "", "Мероприятия",
     ["Подписчики +500", "Цена подписчика 55 рублей", "Заказов рекламы в канале 2 в месяц"]),
    ("case-antalya.jpg", "Сайт по продаже недвижимости в Анталии", "", "Недвижимость",
     ["Быстро ведёт к заявке", "Вызывает доверие", "Удобный подбор под запрос"]),
    ("case-tarot.jpg", "Instagram-аккаунт таролога", "@lavri.n", "Образование",
     ["Подписчики +378", "Просмотры Reels +65%", "Заявки выросли на 50%, до 6 в неделю"]),
    ("case-sewing.jpg", "Instagram-аккаунт швейной школы", "", "Образование",
     ["Охваты +67%", "Просмотры Reels выросли на 84%",
      "Посещаемость профиля увеличилась на 53%"]),
]


def nav(up, active=""):
    items = [(up + "index.html", "Главная", "home"),
             (up + "index.html#services", "Услуги", "uslugi"),
             (up + "ceny.html", "Цены", "ceny"),
             (up + "keysy.html", "Кейсы", "keysy"),
             (up + "otzyvy.html", "Отзывы", "otzyvy"),
             (up + "blog/index.html", "Блог", "blog"),
             (up + "kontakty.html", "Контакты", "kontakty")]
    return "\n      ".join(
        '<a href="%s"%s>%s</a>' % (h, ' class="is-active"' if k == active else "", t)
        for h, t, k in items)


def footer(up):
    return """
<footer class="legal__foot">
  <div class="container">
    <nav class="legal__nav">
      <a href="%(up)suslugi/vedenie-socsetey.html">Ведение соцсетей</a>
      <a href="%(up)suslugi/reklama.html">Реклама</a>
      <a href="%(up)suslugi/neuroseti.html">Нейросети</a>
      <a href="%(up)suslugi/sajty.html">Создание сайтов</a>
      <a href="%(up)sceny.html">Цены</a>
      <a href="%(up)skeysy.html">Кейсы</a>
      <a href="%(up)sotzyvy.html">Отзывы</a>
      <a href="%(up)sblog/index.html">Блог</a>
      <a href="%(up)skontakty.html">Контакты</a>
    </nav>
    <nav class="legal__nav">
      <a href="%(up)slegal/privacy-policy.html">Политика обработки персональных данных</a>
      <a href="%(up)slegal/confidentiality.html">Политика конфиденциальности</a>
      <a href="%(up)slegal/terms.html">Пользовательское соглашение</a>
      <a href="%(up)slegal/cookies.html">Файлы cookie</a>
    </nav>
    <p class="legal__copy">© 2026 SMM-агентство «Как есть»</p>
  </div>
</footer>
""" % {"up": up}


def shell(p, body, jsonld, up, active):
    url = "%s/%s" % (SITE, p["slug"])
    og = "%s/assets/og/og-main.jpg" % SITE
    return """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta name="keywords" content="%(kw)s">
<meta name="robots" content="%(robots)s">
<link rel="canonical" href="%(url)s">
<meta property="og:type" content="website">
<meta property="og:url" content="%(url)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:image" content="%(og)s">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:site_name" content="SMM-агентство «Как есть»">
<meta property="og:locale" content="ru_RU">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s">
<meta name="twitter:description" content="%(desc)s">
<meta name="twitter:image" content="%(og)s">
<meta name="theme-color" content="#2563EB">
<link rel="icon" href="%(up)sassets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="%(up)sassets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="%(up)sassets/css/style.css">
%(jsonld)s</head>
<body class="legal-page">

<header class="legal__top">
  <div class="container legal__top-in">
    <a href="%(up)sindex.html" class="logo" aria-label="Как есть — смм агентство">
      <span class="logo__mark" aria-hidden="true"><img src="%(up)sassets/img/logo-mark.svg" alt=""></span>
      <span class="logo__text"><b>КАК ЕСТЬ</b><i>СММ АГЕНТСТВО</i></span>
    </a>
    <nav class="blog__nav">
      %(nav)s
    </nav>
  </div>
</header>

%(body)s
%(footer)s
</body>
</html>
""" % {"title": html.escape(p["title"], quote=True),
       "desc": html.escape(p["description"], quote=True),
       "kw": html.escape(p["keywords"], quote=True),
       "robots": p.get("robots", "index, follow, max-image-preview:large"),
       "url": url, "og": og, "up": up, "jsonld": jsonld,
       "nav": nav(up, active), "footer": footer(up), "body": body}


def faq_html(pairs):
    if not pairs:
        return ""
    items = "\n".join(
        '      <details class="faq__item"><summary>%s</summary><p>%s</p></details>'
        % (q, a) for q, a in pairs)
    return """
  <section class="lp__faq">
    <h2>Частые вопросы</h2>
%s
  </section>
""" % items


def cases_html(up):
    cards = []
    for img, title, accent, tag, facts in CASES:
        acc = ' <em>%s</em>' % accent if accent else ""
        li = "".join("<li>%s</li>" % f for f in facts)
        cards.append("""      <article class="case case--static">
        <div class="case__media ph"><img src="%sassets/img/%s" alt="Кейс: %s" loading="lazy"></div>
        <h2>%s%s</h2>
        <ul class="case__facts">%s</ul>
        <span class="case__tag">%s</span>
      </article>""" % (up, img, title, title, acc, li, tag))
    return '    <div class="lp__cases">\n' + "\n".join(cards) + "\n    </div>\n"


def contacts_html():
    rows = [("Telegram", "https://t.me/kakestsmm", "@kakestsmm", "social-telegram.png"),
            ("WhatsApp", "https://wa.me/905518102563", "+90 551 810 25 63", "social-whatsapp.png"),
            ("ВКонтакте", "https://vk.com/id59595974", "vk.com/id59595974", "social-vk.png"),
            ("YouTube", "https://youtube.com/@kak_est_smm", "@kak_est_smm", "social-youtube.png"),
            ("TikTok", "https://www.tiktok.com/@nadya_shteinbah", "@nadya_shteinbah", "social-tiktok.png")]
    items = "\n".join(
        """      <a class="cway" href="%s" target="_blank" rel="noopener">
        <img src="assets/img/icons/%s" alt="" width="40" height="40">
        <span><b>%s</b><i>%s</i></span>
      </a>""" % (url, ico, name, handle) for name, url, handle, ico in rows)
    return """    <div class="cways">
%s
    </div>
    <div class="lp__cta">
      <h2>Написать напрямую</h2>
      <p>Отвечаем в течение рабочего дня. Разбор соцсетей — бесплатный и ни к чему не обязывает.</p>
      <a class="btn btn--lg" href="%s" target="_blank" rel="noopener">написать в Telegram</a>
    </div>
    <div class="lp__req">
      <p><b>Реквизиты.</b> Физическое лицо Штейнбах Надежда Викторовна, ИНН 190601627607,
      Россия, Республика Хакасия, г. Саяногорск, ул. Снежная, д. 5а.
      Электронная почта <a href="mailto:nadyashteinbakh@gmail.com">nadyashteinbakh@gmail.com</a>,
      телефон <a href="tel:+79950822563">+7 995 082-25-63</a>.</p>
    </div>
""" % (items, TG)



AVATAR_COLORS = ["#4B82F7", "#F2A63B", "#57B36B", "#B968D6", "#E0679A", "#3FB6C4"]


def stars():
    return ('<span class="rv__stars" aria-label="Оценка 5 из 5">'
            + '<svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true">'
              '<path d="M10 1.6l2.6 5.3 5.8.8-4.2 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8L1.6 7.7l5.8-.8z" '
              'fill="#F5A623"/></svg>' * 5 + '</span>')


def reviews_html():
    cards = []
    for i, r in enumerate(REVIEWS):
        paras = "".join("<p>%s</p>" % html.escape(t)
                        for t in r["text"].split("\n\n") if t.strip())
        reply = ""
        if r.get("reply"):
            reply = ('      <div class="rv__reply">'
                     '<b>Надежда Штейнбах</b><span>%s</span><p>%s</p></div>'
                     % (r["reply_date"], html.escape(r["reply"])))
        cards.append("""      <article class="rv">
        <header class="rv__head">
          <span class="rv__ava" style="background:%s" aria-hidden="true">%s</span>
          <span class="rv__who"><b>%s</b><time datetime="%s">%s</time></span>
          %s
        </header>
        <div class="rv__text">%s</div>
%s
      </article>""" % (AVATAR_COLORS[i % len(AVATAR_COLORS)], r["name"][0],
                       html.escape(r["name"]), r["date"], r["date_ru"],
                       stars(), paras, reply))
    return ('    <div class="rv__grid">\n' + "\n".join(cards) + "\n    </div>\n")



def hero_html(slug, up):
    """Иллюстрация для страницы услуги: assets/img/uslugi/<имя>.jpg.
    Файла нет — страница собирается без картинки."""
    if not slug.startswith("uslugi/"):
        return ""
    name = os.path.splitext(os.path.basename(slug))[0]
    rel = "assets/img/uslugi/%s.jpg" % name
    if not os.path.exists(os.path.join(ROOT, rel)):
        return ""
    return ('  <figure class="lp__hero"><img src="%s%s" alt="" width="1200" height="630" '
            'loading="lazy"></figure>\n' % (up, rel))


def build_page(p):
    depth = p["slug"].count("/")
    up = "../" * depth
    active = ("uslugi" if p["slug"].startswith("uslugi/")
              else os.path.splitext(os.path.basename(p["slug"]))[0])

    blocks = p["blocks"]
    if blocks == "__CASES__":
        blocks = cases_html(up)
    elif blocks == "__CONTACTS__":
        blocks = contacts_html()
    elif blocks == "__REVIEWS__":
        blocks = reviews_html()

    graph = [{"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Главная", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": p["h1"],
         "item": "%s/%s" % (SITE, p["slug"])}]}]
    if p.get("service"):
        graph.append({"@type": "Service", "name": p["service"],
                      "description": p["description"],
                      "provider": {"@id": SITE + "/#org"},
                      "areaServed": {"@type": "Country", "name": "Россия"},
                      "url": "%s/%s" % (SITE, p["slug"])})
    if p["slug"] == "kontakty.html":
        # Адрес и контакты машиночитаемо — Яндексу нужен геосигнал для региональности
        graph.append({
            "@type": "Organization", "@id": SITE + "/#org",
            "name": "SMM-агентство «Как есть»", "url": SITE + "/",
            "email": "nadyashteinbakh@gmail.com", "telephone": "+7-995-082-25-63",
            "address": {"@type": "PostalAddress", "addressCountry": "RU",
                        "addressRegion": "Республика Хакасия",
                        "addressLocality": "Саяногорск",
                        "streetAddress": "ул. Снежная, д. 5а"},
            "areaServed": {"@type": "Country", "name": "Россия"},
            "contactPoint": [
                {"@type": "ContactPoint", "contactType": "sales",
                 "telephone": "+7-995-082-25-63", "email": "nadyashteinbakh@gmail.com",
                 "availableLanguage": "Russian", "areaServed": "RU"}],
            "sameAs": ["https://t.me/kakestsmm", "https://vk.com/id59595974",
                       "https://youtube.com/@kak_est_smm",
                       "https://www.tiktok.com/@nadya_shteinbah"]})
    if p["slug"] == "otzyvy.html":
        graph.append({
            "@type": "Organization", "@id": SITE + "/#org",
            "name": "SMM-агентство «Как есть»", "url": SITE + "/",
            "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5",
                                "bestRating": "5", "reviewCount": len(REVIEWS)},
            "review": [{"@type": "Review",
                        "author": {"@type": "Person", "name": r["name"]},
                        "datePublished": r["date"],
                        "reviewRating": {"@type": "Rating", "ratingValue": "5",
                                         "bestRating": "5"},
                        "reviewBody": r["text"].replace("\n\n", " ")}
                       for r in REVIEWS]})
    if p.get("faq"):
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]})

    jsonld = ('<script type="application/ld+json">\n%s\n</script>\n'
              % json.dumps({"@context": "https://schema.org", "@graph": graph},
                           ensure_ascii=False, separators=(",", ":")))

    body = """<main class="container lp">
  <nav class="crumbs" aria-label="Навигация">
    <a href="%(up)sindex.html">Главная</a><span>/</span><b>%(h1)s</b>
  </nav>
  <h1>%(h1)s</h1>
  <p class="lp__lead">%(lead)s</p>
%(hero)s%(blocks)s
%(faq)s
  <section class="lp__cta">
    <h2>Разберём вашу задачу бесплатно</h2>
    <p>Посмотрим соцсети, контент и конкурентов и назовём пять точек роста — за 20 минут и без обязательств.</p>
    <a class="btn btn--lg" href="%(tg)s" target="_blank" rel="noopener">получить разбор</a>
  </section>
</main>
""" % {"up": up, "h1": p["h1"], "lead": p["lead"], "blocks": blocks,
       "hero": hero_html(p["slug"], up),
       "faq": faq_html(p.get("faq")), "tg": TG}

    out = os.path.join(ROOT, p["slug"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(shell(p, body, jsonld, up, active))


def build_404():
    p = {"slug": "404.html", "title": "Страница не найдена — SMM-агентство «Как есть»",
         "description": "Такой страницы нет. Вернитесь на главную или посмотрите услуги и блог.",
         "keywords": "", "h1": "Страница не найдена", "robots": "noindex, follow"}
    body = """<main class="container lp lp--404">
  <h1>Страница не найдена</h1>
  <p class="lp__lead">Возможно, адрес набран с ошибкой или страницу перенесли.
  Вот куда можно пойти дальше.</p>
  <div class="lp__links">
    <a href="index.html">На главную</a>
    <a href="uslugi/vedenie-socsetey.html">Ведение соцсетей</a>
    <a href="uslugi/reklama.html">Реклама</a>
    <a href="keysy.html">Кейсы</a>
    <a href="blog/index.html">Блог</a>
    <a href="kontakty.html">Контакты</a>
  </div>
</main>
"""
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(shell(p, body, "", "", ""))


if __name__ == "__main__":
    for p in PAGES:
        build_page(p)
        print("создано: %s" % p["slug"])
    build_404()
    print("создано: 404.html")
