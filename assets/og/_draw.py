# -*- coding: utf-8 -*-
"""Карточки для соцсетей (Open Graph), 1200x630.

  python3 assets/og/_draw.py

Рисуются как HTML и снимаются браузером — так кириллица и шрифт сайта
выглядят точно так же, как на страницах.
"""
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
W, H = 1200, 630

CARDS = [
    ("og-main", "Ведение соцсетей,<br>реклама и сайты",
     "Показываем бренды живыми, как есть", "8 лет опыта · 50+ проектов"),
    ("og-blog", "Блог о продвижении<br>в соцсетях",
     "Разборы и инструкции из практики агентства", "20 статей · контент, реклама, аналитика"),
    ("og-legal", "Документы<br>и правовая информация",
     "Обработка персональных данных и условия работы", "kakestsmm.com"),
]

TPL = """<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;700;800&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:%(w)dpx;height:%(h)dpx;font-family:Manrope,sans-serif;
  background:linear-gradient(150deg,#FBFCFD 0%%,#E9ECF2 100%%);
  position:relative;overflow:hidden;display:flex;flex-direction:column;
  justify-content:space-between;padding:64px 72px}
.blob{position:absolute;border-radius:50%%;filter:blur(2px)}
.b1{width:520px;height:520px;right:-150px;top:-170px;background:rgba(37,99,235,.10)}
.b2{width:300px;height:300px;right:60px;bottom:-120px;background:rgba(37,99,235,.07)}
.mark{position:absolute;right:-40px;bottom:-70px;width:430px;opacity:.10}
.top{display:flex;align-items:center;gap:16px;position:relative}
.top img{width:62px;height:52px}
.brand b{display:block;font-size:30px;font-weight:800;letter-spacing:-.01em;line-height:1}
.brand i{display:block;font-style:normal;font-size:13px;font-weight:500;
  letter-spacing:.22em;color:#A5A9B0;margin-top:5px}
h1{position:relative;font-size:66px;font-weight:800;line-height:1.08;
  letter-spacing:-.02em;color:#15171C;max-width:900px}
h1 em{font-style:normal;color:#2563EB}
.sub{position:relative;font-size:27px;color:#3D4149;margin-top:20px;max-width:820px}
.foot{display:flex;align-items:center;justify-content:space-between;position:relative}
.pill{background:#2563EB;color:#fff;font-size:21px;font-weight:600;
  padding:15px 32px;border-radius:999px}
.meta{font-size:22px;color:#8B9099}
</style></head><body>
<div class="blob b1"></div><div class="blob b2"></div>
<img class="mark" src="../img/logo-mark.svg" alt="">
<div class="top">
  <img src="../img/logo-mark.svg" alt="">
  <span class="brand"><b>КАК ЕСТЬ</b><i>СММ АГЕНТСТВО</i></span>
</div>
<div>
  <h1>%(title)s</h1>
  <p class="sub">%(sub)s</p>
</div>
<div class="foot"><span class="pill">kakestsmm.com</span><span class="meta">%(meta)s</span></div>
</body></html>"""


def build():
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    for slug, title, sub, meta in CARDS:
        html_path = os.path.join(HERE, "_%s.html" % slug)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(TPL % {"w": W, "h": H, "title": title, "sub": sub, "meta": meta})

        png = os.path.join(HERE, slug + ".png")
        jpg = os.path.join(HERE, slug + ".jpg")
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=2", "--window-size=%d,%d" % (W, H),
                        "--screenshot=" + png, "--virtual-time-budget=4000",
                        "file://" + html_path],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        if os.path.exists(png):
            subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "88",
                            "-z", str(H), str(W), png, "--out", jpg],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            os.remove(png)
        os.remove(html_path)
        print("готово: assets/og/%s.jpg" % slug)


if __name__ == "__main__":
    build()
