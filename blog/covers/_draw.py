# -*- coding: utf-8 -*-
"""Векторные обложки статей блога.

  python3 blog/covers/_draw.py        — собрать SVG в covers/src/
  python3 blog/covers/_draw.py --png  — плюс растеризовать в covers/<slug>.jpg

Палитра и композиция общие для всех двадцати, чтобы набор читался как один.
Правится здесь: меняете фигуры — пересобираете.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")

W, H = 1200, 630
CX, CY = W / 2, 322

BLUE = "#2563EB"
BLUE_M = "#7BA0F2"
BLUE_L = "#C9DAFB"
BLUE_XL = "#E6EEFE"
GREY_D = "#A9B2C1"
GREY = "#CBD2DD"
GREY_L = "#E1E5EC"
GREY_XL = "#EFF1F5"
WHITE = "#FFFFFF"
INK = "#3A4150"

DEFS = """<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0.4" y2="1">
    <stop offset="0" stop-color="#FBFCFD"/><stop offset="1" stop-color="#E9ECF2"/>
  </linearGradient>
  <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#2563EB" stop-opacity="0.10"/>
    <stop offset="1" stop-color="#2563EB" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="blueGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#4B82F7"/><stop offset="1" stop-color="#2563EB"/>
  </linearGradient>
  <linearGradient id="glass" x1="0" y1="0" x2="0.3" y2="1">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.95"/>
    <stop offset="1" stop-color="#DDE3ED" stop-opacity="0.85"/>
  </linearGradient>
  <filter id="sh" x="-40%" y="-40%" width="180%" height="180%">
    <feDropShadow dx="0" dy="16" stdDeviation="20" flood-color="#141C2E" flood-opacity="0.11"/>
  </filter>
  <filter id="shs" x="-60%" y="-60%" width="220%" height="220%">
    <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#141C2E" flood-opacity="0.10"/>
  </filter>
  <filter id="blur"><feGaussianBlur stdDeviation="18"/></filter>
</defs>"""


def rr(x, y, w, h, r, fill, extra=""):
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s" %s/>'
            % (x, y, w, h, r, fill, extra))


def ci(cx, cy, r, fill, extra=""):
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" %s/>' % (cx, cy, r, fill, extra)


def floor_shadow(cx, cy, rx, ry=None, op=0.13):
    ry = ry or rx * 0.16
    return ('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#8A93A6" '
            'opacity="%.2f" filter="url(#blur)"/>' % (cx, cy, rx, ry, op))


# ---------------------------------------------------------------- сюжеты

def calendar():
    """Контент-план: календарная сетка, одна ячейка выделена."""
    x, y, w, h = CX - 250, CY - 165, 500, 330
    s = [floor_shadow(CX, y + h + 26, 230),
         rr(x, y, w, h, 30, WHITE, 'filter="url(#sh)"'),
         rr(x, y, w, 62, 30, BLUE_XL),
         rr(x, y + 40, w, 22, 0, BLUE_XL)]
    for i in range(3):
        s.append(ci(x + 40 + i * 26, y + 31, 7, BLUE_L))
    cw, ch, gap = 54, 44, 12
    ox, oy = x + 36, y + 88
    hot = (2, 1)
    warm = [(0, 0), (4, 2), (6, 1)]
    for r in range(4):
        for c in range(7):
            cx0, cy0 = ox + c * (cw + gap), oy + r * (ch + gap)
            if (c, r) == hot:
                s.append(rr(cx0, cy0 - 6, cw, ch + 12, 12, "url(#blueGrad)", 'filter="url(#shs)"'))
            elif (c, r) in warm:
                s.append(rr(cx0, cy0, cw, ch, 11, BLUE_L))
            else:
                s.append(rr(cx0, cy0, cw, ch, 11, GREY_XL))
    # плавающие карточки
    s.append(rr(x + w - 74, y - 54, 132, 92, 22, WHITE, 'filter="url(#sh)"'))
    s.append(rr(x + w - 52, y - 30, 60, 9, 5, BLUE))
    s.append(rr(x + w - 52, y - 12, 88, 9, 5, GREY_L))
    s.append(rr(x + w - 52, y + 6, 70, 9, 5, GREY_L))
    s.append(rr(x - 78, y + h - 90, 118, 84, 22, WHITE, 'filter="url(#sh)"'))
    s.append(ci(x - 40, y + h - 56, 15, BLUE_L))
    s.append(rr(x - 62, y + h - 32, 74, 9, 5, GREY_L))
    return "".join(s)


def scales():
    """Стоимость: весы, монеты против контента."""
    beam_y = CY - 118
    plate_y = CY + 62
    s = [floor_shadow(CX, CY + 196, 210)]
    s.append(rr(CX - 15, beam_y, 30, 262, 15, GREY))
    s.append(rr(CX - 96, CY + 152, 192, 30, 15, GREY_D))
    for side in (-1, 1):
        px = CX + side * 218
        s.append('<path d="M %d %d L %d %d" stroke="%s" stroke-width="5"/>'
                 % (px, beam_y + 14, px, plate_y - 6, GREY))
        s.append('<path d="M %d %d q 0 62 84 62 q 84 0 84 -62 z" fill="%s" filter="url(#shs)"/>'
                 % (px - 84, plate_y, GREY_L))
    s.append(rr(CX - 236, beam_y - 13, 472, 26, 13, "url(#blueGrad)", 'filter="url(#shs)"'))
    s.append(ci(CX, beam_y, 27, WHITE, 'filter="url(#shs)"'))
    s.append(ci(CX, beam_y, 12, BLUE))
    for i in range(4):
        s.append('<ellipse cx="%d" cy="%d" rx="52" ry="15" fill="%s"/>'
                 % (CX - 218, plate_y - 14 - i * 24, BLUE if i == 3 else BLUE_M))
    cards = [(-70, -104, 58, 58), (2, -92, 52, 46), (-32, -40, 66, 34)]
    for i, (dx, dy, w, h) in enumerate(cards):
        s.append(rr(CX + 218 + dx, plate_y + dy, w, h, 12, WHITE, 'filter="url(#shs)"'))
        if i == 0:
            s.append('<path d="M %d %d l 24 15 l -24 15 z" fill="%s"/>'
                     % (CX + 218 + dx + 20, plate_y + dy + 14, BLUE))
        elif i == 1:
            s.append(ci(CX + 218 + dx + 26, plate_y + dy + 23, 12, BLUE_L))
        else:
            s.append(rr(CX + 218 + dx + 12, plate_y + dy + 13, 42, 8, 4, GREY_L))
    return "".join(s)


def phone_feed():
    """ВКонтакте: телефон и сеть аудитории."""
    x, y, w, h = CX - 118, CY - 210, 236, 420
    s = [floor_shadow(CX, y + h + 22, 170)]
    for i, (dx, dy, r) in enumerate([(-300, -110, 30), (-250, 90, 22), (300, -130, 26),
                                     (270, 60, 34), (-330, 10, 16), (330, -20, 18)]):
        s.append(ci(CX + dx, CY + dy, r, BLUE_L if i % 2 else BLUE_XL))
        s.append('<path d="M %d %d Q %d %d %d %d" stroke="%s" stroke-width="3" fill="none" opacity="0.55"/>'
                 % (CX + dx, CY + dy, CX + dx * 0.5, CY + dy * 0.4, CX + (110 if dx > 0 else -110), CY, BLUE_M))
    s.append(rr(x, y, w, h, 34, "#2B303B", 'filter="url(#sh)"'))
    s.append(rr(x + 9, y + 9, w - 18, h - 18, 27, WHITE))
    s.append(rr(x + 88, y + 18, 60, 10, 5, "#2B303B"))
    s.append(rr(x + 26, y + 44, 60, 60, 30, BLUE_L))
    s.append(rr(x + 96, y + 56, 96, 12, 6, GREY))
    s.append(rr(x + 96, y + 78, 66, 12, 6, GREY_L))
    s.append(rr(x + 26, y + 122, w - 52, 96, 16, GREY_XL))
    s.append('<path d="M %d %d l 26 15 l -26 15 z" fill="%s"/>' % (x + 100, y + 155, BLUE))
    s.append(rr(x + 26, y + 234, w - 52, 42, 14, "url(#blueGrad)"))
    for i in range(3):
        s.append(rr(x + 26, y + 296 + i * 26, (w - 52) * (0.9 - i * 0.2), 12, 6, GREY_L))
    return "".join(s)


def reels():
    """Reels: вертикальный кадр с кнопкой play и дуги движения."""
    x, y, w, h = CX - 105, CY - 190, 210, 372
    s = [floor_shadow(CX, y + h + 20, 150)]
    for i, r in enumerate((250, 300, 350)):
        s.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="3" '
                 'opacity="%.2f" stroke-dasharray="14 22"/>' % (CX, CY, r, BLUE_M, 0.5 - i * 0.13))
    s.append(rr(x, y, w, h, 26, WHITE, 'filter="url(#sh)"'))
    s.append(rr(x + 12, y + 12, w - 24, h - 24, 18, BLUE_XL))
    s.append(ci(CX, CY - 10, 52, WHITE, 'filter="url(#shs)"'))
    s.append('<path d="M %d %d l 44 26 l -44 26 z" fill="%s"/>' % (CX - 16, CY - 36, BLUE))
    s.append(rr(x + 34, y + h - 74, w - 68, 12, 6, GREY_L))
    s.append(rr(x + 34, y + h - 52, (w - 68) * 0.6, 12, 6, GREY_L))
    for i, (dx, dy, r) in enumerate([(-268, -140, 26), (268, 132, 22), (-250, 150, 18), (256, -160, 30)]):
        s.append(ci(CX + dx, CY + dy, r, BLUE_L if i % 2 else BLUE_XL))
    return "".join(s)


def profile():
    """Упаковка профиля: карточка с аватаром, кнопкой и хайлайтами."""
    x, y, w, h = CX - 260, CY - 175, 520, 350
    s = [floor_shadow(CX, y + h + 26, 235),
         rr(x, y, w, h, 30, WHITE, 'filter="url(#sh)"'),
         rr(x, y, w, 96, 30, BLUE_XL), rr(x, y + 66, w, 30, 0, BLUE_XL),
         ci(x + 96, y + 96, 54, WHITE), ci(x + 96, y + 96, 44, BLUE_L)]
    s.append(rr(x + 170, y + 118, 190, 16, 8, GREY))
    s.append(rr(x + 170, y + 146, 130, 13, 6, GREY_L))
    s.append(rr(x + 170, y + 172, 168, 13, 6, GREY_L))
    s.append(rr(x + 42, y + 208, 214, 46, 23, "url(#blueGrad)", 'filter="url(#shs)"'))
    s.append(rr(x + 274, y + 208, 204, 46, 23, GREY_XL))
    for i in range(4):
        cxx = x + 78 + i * 108
        s.append(ci(cxx, y + 300, 34, WHITE, 'filter="url(#shs)"'))
        s.append(ci(cxx, y + 300, 27, BLUE_L if i == 0 else GREY_L))
    return "".join(s)


def target():
    """Таргет: мишень с дротиком и сегменты аудитории."""
    s = [floor_shadow(CX, CY + 190, 190)]
    for i, (r, c) in enumerate([(168, GREY_L), (128, BLUE_XL), (88, BLUE_L), (48, BLUE_M)]):
        s.append(ci(CX, CY, r, c, 'filter="url(#sh)"' if i == 0 else ""))
    s.append(ci(CX, CY, 20, BLUE))
    s.append('<path d="M %d %d L %d %d" stroke="%s" stroke-width="13" stroke-linecap="round"/>'
             % (CX + 8, CY - 8, CX + 190, CY - 178, "#2B303B"))
    s.append('<path d="M %d %d l 46 -14 l -14 46 z" fill="%s"/>' % (CX + 156, CY - 158, BLUE))
    s.append(ci(CX + 6, CY - 6, 13, "#2B303B"))
    for dx, dy, r in [(-330, -120, 30), (-300, 120, 22), (330, 130, 26), (-360, 0, 16), (300, -170, 18)]:
        s.append(ci(CX + dx, CY + dy, r, BLUE_XL))
    return "".join(s)


def plane():
    """Посевы: бумажный самолётик и каналы."""
    s = [floor_shadow(CX + 40, CY + 190, 200)]
    s.append('<path d="M %d %d Q %d %d %d %d" stroke="%s" stroke-width="7" fill="none" '
             'stroke-linecap="round" stroke-dasharray="2 26" opacity="0.7"/>'
             % (CX - 380, CY + 150, CX - 140, CY + 120, CX - 40, CY - 40, BLUE_M))
    px, py = CX + 60, CY - 90
    s.append('<path d="M %d %d L %d %d L %d %d Z" fill="%s" filter="url(#sh)"/>'
             % (px - 130, py + 60, px + 130, py - 70, px + 10, py + 120, BLUE))
    s.append('<path d="M %d %d L %d %d L %d %d Z" fill="%s"/>'
             % (px - 130, py + 60, px + 130, py - 70, px + 6, py + 46, BLUE_M))
    for i in range(4):
        bx = CX - 330 + i * 178
        s.append(rr(bx, CY + 112, 150, 84, 20, WHITE, 'filter="url(#shs)"'))
        s.append(ci(bx + 32, CY + 148, 18, BLUE_L if i == 1 else GREY_L))
        s.append(rr(bx + 60, CY + 134, 68, 11, 6, GREY_L))
        s.append(rr(bx + 60, CY + 154, 46, 11, 6, GREY_XL))
    return "".join(s)


def chat():
    """Телеграм-канал: стопка сообщений и растущие подписчики."""
    s = [floor_shadow(CX, CY + 200, 210)]
    boxes = [(-210, -160, 330, 78, GREY_XL), (-150, -66, 400, 92, WHITE),
             (-210, 40, 300, 78, BLUE_XL), (-90, 138, 330, 86, WHITE)]
    for i, (dx, dy, w, h, fill) in enumerate(boxes):
        x, y = CX + dx, CY + dy
        s.append(rr(x, y, w, h, 22, fill, 'filter="url(#shs)"'))
        if i == 3:
            s.append(rr(x, y, w, h, 22, "url(#blueGrad)", 'filter="url(#sh)"'))
            s.append(rr(x + 26, y + 26, w * 0.62, 12, 6, WHITE, 'opacity="0.9"'))
            s.append(rr(x + 26, y + 48, w * 0.4, 12, 6, WHITE, 'opacity="0.6"'))
        else:
            s.append(rr(x + 26, y + 22, w * 0.6, 12, 6, GREY))
            s.append(rr(x + 26, y + 44, w * 0.38, 12, 6, GREY_L))
    for i, (dx, dy, r) in enumerate([(300, -180, 20), (350, -100, 14), (270, -60, 26), (360, 30, 18)]):
        s.append(ci(CX + dx, CY + dy, r, BLUE_M if i % 2 else BLUE_L))
    return "".join(s)


def search():
    """Директ: поисковая строка и выдача, верхняя карточка с меткой."""
    x, y, w = CX - 300, CY - 200, 600
    s = [floor_shadow(CX, CY + 210, 240)]
    s.append(rr(x, y, w, 74, 37, WHITE, 'filter="url(#sh)"'))
    s.append(ci(x + 44, y + 37, 17, "none", 'stroke="%s" stroke-width="6"' % BLUE))
    s.append('<path d="M %d %d l 18 18" stroke="%s" stroke-width="6" stroke-linecap="round"/>'
             % (x + 56, y + 49, BLUE))
    s.append(rr(x + 84, y + 30, 250, 14, 7, GREY_L))
    s.append(rr(x + w - 118, y + 18, 96, 38, 19, "url(#blueGrad)"))
    top = y + 100
    s.append(rr(x - 16, top, w + 32, 96, 24, WHITE, 'filter="url(#sh)"'))
    s.append(rr(x + 6, top + 24, 66, 26, 13, BLUE))
    s.append(rr(x + 86, top + 28, 220, 16, 8, GREY))
    s.append(rr(x + 6, top + 60, 380, 12, 6, GREY_L))
    for i in range(2):
        yy = top + 122 + i * 92
        s.append(rr(x, yy, w, 78, 22, GREY_XL))
        s.append(rr(x + 24, yy + 20, 200, 14, 7, GREY))
        s.append(rr(x + 24, yy + 46, 330, 11, 6, GREY_L))
    return "".join(s)


def dashboard():
    """Метрики: столбцы, шкала и линия."""
    x, y, w, h = CX - 290, CY - 175, 580, 350
    s = [floor_shadow(CX, y + h + 24, 250),
         rr(x, y, w, h, 30, WHITE, 'filter="url(#sh)"')]
    bx, by = x + 44, y + 250
    for i, hh in enumerate((70, 108, 86, 148, 196)):
        s.append(rr(bx + i * 56, by - hh, 36, hh, 12, BLUE if i == 4 else GREY_L))
    s.append('<path d="M %d %d L %d %d L %d %d L %d %d" fill="none" stroke="%s" '
             'stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
             % (bx + 6, by - 96, bx + 62, by - 130, bx + 118, by - 110, bx + 230, by - 214, BLUE_M))
    gx, gy = x + w - 128, y + 128
    s.append('<path d="M %d %d a 74 74 0 1 1 %d 0" fill="none" stroke="%s" stroke-width="20" '
             'stroke-linecap="round"/>' % (gx - 74, gy, 148, GREY_L))
    s.append('<path d="M %d %d a 74 74 0 0 1 %d %d" fill="none" stroke="%s" stroke-width="20" '
             'stroke-linecap="round"/>' % (gx - 74, gy, 116, -46, BLUE))
    s.append(rr(gx - 56, y + 232, 112, 14, 7, GREY_L))
    s.append(rr(gx - 40, y + 258, 80, 14, 7, GREY_XL))
    return "".join(s)


def funnel():
    """Воронка: шары входят широко, выходят узко."""
    s = [floor_shadow(CX, CY + 210, 170)]
    s.append('<path d="M %d %d L %d %d L %d %d L %d %d Z" fill="%s" filter="url(#sh)"/>'
             % (CX - 230, CY - 150, CX + 230, CY - 150, CX + 58, CY + 120, CX - 58, CY + 120, BLUE_XL))
    s.append('<path d="M %d %d L %d %d L %d %d L %d %d Z" fill="none" stroke="%s" '
             'stroke-width="5" stroke-linejoin="round"/>'
             % (CX - 230, CY - 150, CX + 230, CY - 150, CX + 58, CY + 120, CX - 58, CY + 120, BLUE_M))
    s.append('<ellipse cx="%d" cy="%d" rx="230" ry="26" fill="%s"/>' % (CX, CY - 150, BLUE_L))
    for dx, dy, r, c in [(-150, -196, 26, GREY), (-52, -224, 20, GREY_D), (58, -200, 30, GREY),
                         (160, -226, 22, GREY_D), (-108, -108, 22, BLUE_L), (10, -80, 26, BLUE_M),
                         (110, -110, 18, BLUE_L), (-30, 6, 22, BLUE_M)]:
        s.append(ci(CX + dx, CY + dy, r, c))
    for i, (dx, dy, r) in enumerate([(-6, 168, 24), (44, 218, 18), (-56, 222, 14)]):
        s.append(ci(CX + dx, CY + dy, r, BLUE, 'filter="url(#shs)"'))
    return "".join(s)


def neural():
    """Нейросети: узлы превращаются в карточки контента."""
    s = [floor_shadow(CX, CY + 200, 230)]
    nodes = [(-330, -110), (-360, 20), (-300, 130), (-190, -160), (-210, 60), (-170, 170)]
    for a in nodes:
        for b in nodes:
            if a is not b and abs(a[0] - b[0]) < 200:
                s.append('<path d="M %d %d L %d %d" stroke="%s" stroke-width="2.5" opacity="0.5"/>'
                         % (CX + a[0], CY + a[1], CX + b[0], CY + b[1], BLUE_M))
    for i, (dx, dy) in enumerate(nodes):
        s.append(ci(CX + dx, CY + dy, 22 if i % 2 else 16, BLUE if i in (1, 3) else BLUE_L))
    for i in range(3):
        s.append('<path d="M %d %d Q %d %d %d %d" stroke="%s" stroke-width="4" fill="none" '
                 'opacity="0.7" stroke-dasharray="3 16" stroke-linecap="round"/>'
                 % (CX - 140, CY - 60 + i * 90, CX - 20, CY - 40 + i * 70, CX + 90, CY - 130 + i * 118, BLUE_M))
    for i in range(3):
        y = CY - 170 + i * 122
        s.append(rr(CX + 120, y, 280, 100, 24, WHITE, 'filter="url(#sh)"'))
        s.append(rr(CX + 144, y + 24, 64, 52, 14, BLUE_L if i == 1 else GREY_XL))
        s.append(rr(CX + 224, y + 30, 150, 13, 7, GREY))
        s.append(rr(CX + 224, y + 54, 106, 13, 7, GREY_L))
    return "".join(s)


def document():
    """Тексты: лист, курсор и улетающий самолётик."""
    x, y, w, h = CX - 210, CY - 190, 400, 380
    s = [floor_shadow(CX - 20, y + h + 22, 200),
         rr(x, y, w, h, 26, WHITE, 'filter="url(#sh)"')]
    widths = (0.72, 0.9, 0.55, 0.84, 0.66, 0.42)
    for i, k in enumerate(widths):
        s.append(rr(x + 40, y + 56 + i * 42, (w - 80) * k, 15, 8, GREY_L if i else GREY))
    s.append(rr(x + 40, y + 56 + 6 * 42, 190, 44, 22, "url(#blueGrad)"))
    s.append(rr(x + 250, y + 140, 5, 60, 3, BLUE))
    px, py = CX + 250, CY - 150
    s.append('<path d="M %d %d L %d %d L %d %d Z" fill="%s" filter="url(#shs)"/>'
             % (px - 78, py + 36, px + 78, py - 42, px + 6, py + 72, BLUE))
    s.append('<path d="M %d %d L %d %d L %d %d Z" fill="%s"/>'
             % (px - 78, py + 36, px + 78, py - 42, px + 4, py + 28, BLUE_M))
    s.append('<path d="M %d %d Q %d %d %d %d" stroke="%s" stroke-width="5" fill="none" '
             'stroke-dasharray="2 20" stroke-linecap="round" opacity="0.65"/>'
             % (CX + 120, CY + 120, CX + 200, CY + 40, px - 40, py + 90, BLUE_M))
    return "".join(s)


def audit():
    """Аудит: лупа над карточкой, галочка и крестик."""
    x, y, w, h = CX - 250, CY - 150, 470, 300
    s = [floor_shadow(CX, y + h + 24, 220),
         rr(x, y, w, h, 28, WHITE, 'filter="url(#sh)"')]
    by = y + 220
    for i, hh in enumerate((60, 110, 78, 140)):
        s.append(rr(x + 44 + i * 62, by - hh, 40, hh, 12, BLUE_L if i == 3 else GREY_L))
    s.append(rr(x + 300, y + 60, 130, 14, 7, GREY))
    s.append(rr(x + 300, y + 88, 96, 14, 7, GREY_L))
    gx, gy, r = CX + 130, CY + 40, 96
    s.append('<path d="M %d %d l 78 78" stroke="#2B303B" stroke-width="26" stroke-linecap="round"/>'
             % (gx + 58, gy + 58))
    s.append(ci(gx, gy, r, "#FFFFFF", 'opacity="0.55"'))
    s.append(ci(gx, gy, r, "none", 'stroke="%s" stroke-width="16"' % BLUE))
    s.append(ci(CX - 280, CY - 190, 40, WHITE, 'filter="url(#shs)"'))
    s.append('<path d="M %d %d l 14 15 l 26 -30" stroke="%s" stroke-width="9" fill="none" '
             'stroke-linecap="round" stroke-linejoin="round"/>' % (CX - 298, CY - 190, BLUE))
    s.append(ci(CX + 300, CY - 210, 34, WHITE, 'filter="url(#shs)"'))
    s.append('<path d="M %d %d l 26 26 M %d %d l -26 26" stroke="%s" stroke-width="8" '
             'stroke-linecap="round"/>' % (CX + 287, CY - 223, CX + 313, CY - 223, GREY_D))
    return "".join(s)


def audience():
    """Аудитория: группы сфер, одна выделена."""
    s = [floor_shadow(CX, CY + 210, 250)]
    grey = [(-330, -80, 34), (-250, 30, 26), (-300, 130, 20), (-180, -140, 24),
            (250, -120, 30), (330, -10, 24), (280, 110, 34), (350, 150, 18),
            (-60, -210, 22), (60, -200, 16)]
    for dx, dy, r in grey:
        s.append(ci(CX + dx, CY + dy, r, GREY))
    s.append(ci(CX - 10, CY + 40, 168, BLUE_XL))
    blue = [(-80, -20, 40), (10, 30, 52), (-90, 90, 32), (70, -50, 26), (60, 118, 22)]
    for i, (dx, dy, r) in enumerate(blue):
        s.append(ci(CX + dx, CY + dy, r, BLUE if i == 1 else BLUE_M, 'filter="url(#shs)"'))
    return "".join(s)


def stories():
    """Сторис: ряд кружков и вертикальный кадр."""
    s = [floor_shadow(CX, CY + 200, 250)]
    for i in range(5):
        cx0 = CX - 300 + i * 150
        s.append(ci(cx0, CY + 90, 62, WHITE, 'filter="url(#shs)"'))
        s.append(ci(cx0, CY + 90, 62, "none",
                    'stroke="%s" stroke-width="7"' % (BLUE if i == 0 else GREY_L)))
        s.append(ci(cx0, CY + 90, 46, BLUE_L if i == 0 else GREY_XL))
    x, y, w, h = CX - 96, CY - 230, 192, 250
    s.append(rr(x, y, w, h, 24, WHITE, 'filter="url(#sh)"'))
    s.append(rr(x + 12, y + 12, w - 24, h - 24, 16, BLUE_XL))
    for i in range(3):
        s.append(rr(x + 22 + i * 54, y + 24, 44, 8, 4, BLUE if i == 0 else GREY_L))
    s.append(ci(CX, CY - 118, 34, WHITE))
    s.append('<path d="M %d %d l 28 17 l -28 17 z" fill="%s"/>' % (CX - 10, CY - 135, BLUE))
    return "".join(s)


def shield():
    """Негатив: два облака реплик и щит между ними."""
    s = [floor_shadow(CX, CY + 200, 230)]
    s.append('<path d="M %d %d h 250 a 26 26 0 0 1 26 26 v 120 a 26 26 0 0 1 -26 26 h -190 '
             'l -50 46 v -46 h -10 a 26 26 0 0 1 -26 -26 v -120 a 26 26 0 0 1 26 -26 z" '
             'fill="%s" filter="url(#shs)"/>' % (CX - 400, CY - 150, GREY_L))
    for i in range(3):
        s.append(rr(CX - 366, CY - 112 + i * 32, 190 - i * 44, 13, 7, GREY_D, 'opacity="0.65"'))
    s.append('<path d="M %d %d h -250 a 26 26 0 0 0 -26 26 v 120 a 26 26 0 0 0 26 26 h 190 '
             'l 50 46 v -46 h 10 a 26 26 0 0 0 26 -26 v -120 a 26 26 0 0 0 -26 -26 z" '
             'fill="url(#blueGrad)" filter="url(#sh)"/>' % (CX + 400, CY - 30))
    for i in range(3):
        s.append(rr(CX + 176, CY + 8 + i * 32, 190 - i * 44, 13, 7, WHITE, 'opacity="0.85"'))
    s.append('<path d="M %d %d l 74 26 v 66 q 0 62 -74 92 q -74 -30 -74 -92 v -66 z" '
             'fill="%s" filter="url(#sh)"/>' % (CX, CY - 116, WHITE))
    s.append('<path d="M %d %d l 20 21 l 38 -42" stroke="%s" stroke-width="12" fill="none" '
             'stroke-linecap="round" stroke-linejoin="round"/>' % (CX - 30, CY - 4, BLUE))
    return "".join(s)


def laptop_phone():
    """Сайт или соцсети: ноутбук и телефон, связанные дугой."""
    s = [floor_shadow(CX - 190, CY + 180, 230), floor_shadow(CX + 240, CY + 180, 120)]
    s.append('<path d="M %d %d Q %d %d %d %d" stroke="%s" stroke-width="7" fill="none" '
             'stroke-dasharray="3 22" stroke-linecap="round" opacity="0.75"/>'
             % (CX - 190, CY - 150, CX + 30, CY - 268, CX + 244, CY - 130, BLUE))
    x, y, w, h = CX - 350, CY - 130, 330, 210
    s.append(rr(x, y, w, h, 18, "#2B303B", 'filter="url(#sh)"'))
    s.append(rr(x + 12, y + 12, w - 24, h - 34, 10, WHITE))
    s.append(rr(x + 30, y + 30, 130, 12, 6, BLUE))
    for i in range(3):
        s.append(rr(x + 30, y + 56 + i * 24, (w - 60) * (0.9 - i * 0.22), 11, 6, GREY_L))
    s.append(rr(x + 30, y + 132, 96, 26, 13, "url(#blueGrad)"))
    s.append(rr(x - 40, y + h, w + 80, 20, 10, GREY_D))
    px, py, pw, ph = CX + 180, CY - 150, 128, 250
    s.append(rr(px, py, pw, ph, 24, "#2B303B", 'filter="url(#sh)"'))
    s.append(rr(px + 8, py + 8, pw - 16, ph - 16, 18, WHITE))
    s.append(rr(px + 22, py + 26, 84, 84, 14, BLUE_L))
    for i in range(3):
        s.append(rr(px + 22, py + 126 + i * 22, (pw - 44) * (1 - i * 0.25), 10, 5, GREY_L))
    s.append(rr(px + 22, py + 200, 84, 24, 12, "url(#blueGrad)"))
    return "".join(s)


def geo():
    """Локальный бизнес: булавка на площадке и радиус."""
    s = [floor_shadow(CX, CY + 200, 260)]
    s.append('<ellipse cx="%d" cy="%d" rx="330" ry="118" fill="%s" opacity="0.55"/>' % (CX, CY + 120, BLUE_XL))
    s.append('<ellipse cx="%d" cy="%d" rx="330" ry="118" fill="none" stroke="%s" '
             'stroke-width="4" stroke-dasharray="14 18" opacity="0.8"/>' % (CX, CY + 120, BLUE_M))
    s.append('<ellipse cx="%d" cy="%d" rx="190" ry="66" fill="%s"/>' % (CX, CY + 120, BLUE_L))
    for dx, scale in [(-292, 0.95), (274, 1.0), (-172, 0.72), (162, 0.76)]:
        w, h = 104 * scale, 96 * scale
        bx, by = CX + dx - w / 2, CY + 96 - h
        s.append(rr(bx, by, w, h, 13, WHITE, 'filter="url(#shs)"'))
        s.append(rr(bx, by, w, 20 * scale, 13, GREY_L))
        s.append(rr(bx, by + 14 * scale, w, 8 * scale, 0, GREY_L))
        s.append(rr(bx + w * 0.22, by + h * 0.5, w * 0.56, h * 0.4, 6, GREY_XL))
    # булавка одной фигурой: голова плюс остриё
    s.append('<path d="M %d %d C %d %d %d %d %d %d A 84 84 0 1 1 %d %d C %d %d %d %d %d %d Z" '
             'fill="url(#blueGrad)" filter="url(#sh)"/>'
             % (CX, CY + 84, CX - 32, CY + 14, CX - 84, CY - 18, CX - 84, CY - 72,
                CX + 84, CY - 72, CX + 84, CY - 18, CX + 32, CY + 14, CX, CY + 84))
    s.append(ci(CX, CY - 72, 34, WHITE))
    return "".join(s)


def blocks():
    """Ошибки: стопка блоков, один выдвинут."""
    s = [floor_shadow(CX, CY + 208, 210)]
    bw, bh = 300, 62
    for i in range(5):
        y = CY + 150 - i * (bh + 12)
        if i == 2:
            s.append(rr(CX - bw / 2 + 130, y, bw, bh, 16, "url(#blueGrad)", 'filter="url(#sh)"'))
            s.append(rr(CX - bw / 2 + 160, y + 24, 120, 14, 7, WHITE, 'opacity="0.75"'))
        else:
            s.append(rr(CX - bw / 2 + (i * 6 - 12), y, bw, bh, 16, WHITE, 'filter="url(#shs)"'))
            s.append(rr(CX - bw / 2 + (i * 6 - 12) + 28, y + 24, 150 - i * 16, 14, 7, GREY_L))
    s.append(ci(CX - 300, CY - 150, 34, WHITE, 'filter="url(#shs)"'))
    s.append('<path d="M %d %d l 24 24 M %d %d l -24 24" stroke="%s" stroke-width="8" '
             'stroke-linecap="round"/>' % (CX - 312, CY - 162, CX - 288, CY - 162, GREY_D))
    return "".join(s)


COVERS = {
    "kontent-plan-dlya-socsetey": calendar,
    "skolko-stoit-vedenie-socsetey": scales,
    "prodvizhenie-vkontakte": phone_feed,
    "kak-snimat-reels": reels,
    "oformlenie-profilya": profile,
    "targeting-vk-s-nulya": target,
    "posevy-v-telegram": plane,
    "telegram-kanal-dlya-biznesa": chat,
    "yandex-direct-dlya-malogo-biznesa": search,
    "metriki-smm": dashboard,
    "voronka-prodazh-v-socsetyah": funnel,
    "neiroseti-v-smm": neural,
    "prodayushchie-teksty": document,
    "audit-socsetey": audit,
    "celevaya-auditoriya": audience,
    "storis-dlya-biznesa": stories,
    "rabota-s-negativom": shield,
    "sayt-ili-socseti": laptop_phone,
    "prodvizhenie-lokalnogo-biznesa": geo,
    "oshibki-v-smm": blocks,
}


def build():
    os.makedirs(SRC, exist_ok=True)
    for slug, fn in COVERS.items():
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
               'viewBox="0 0 %d %d">%s'
               '<rect width="%d" height="%d" fill="url(#bg)"/>'
               '<circle cx="%d" cy="%d" r="420" fill="url(#glow)"/>'
               '%s</svg>' % (W, H, W, H, DEFS, W, H, CX, CY, fn()))
        with open(os.path.join(SRC, slug + ".svg"), "w", encoding="utf-8") as f:
            f.write(svg)
    print("SVG собрано: %d в covers/src/" % len(COVERS))


def rasterize():
    """SVG -> JPEG 1200x630: браузером, потому что sips формат не понимает."""
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if not os.path.exists(chrome):
        print("Chrome не найден, растеризация пропущена")
        return
    for slug in COVERS:
        svg = os.path.join(SRC, slug + ".svg")
        png = os.path.join(HERE, slug + ".png")
        jpg = os.path.join(HERE, slug + ".jpg")
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=2", "--window-size=%d,%d" % (W, H),
                        "--screenshot=" + png, "--virtual-time-budget=2000", "file://" + svg],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        if os.path.exists(png):
            subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "84",
                            "-z", str(H), str(W), png, "--out", jpg],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            os.remove(png)
    print("растеризовано: %d в covers/" % len(COVERS))


if __name__ == "__main__":
    build()
    if "--png" in sys.argv:
        rasterize()
