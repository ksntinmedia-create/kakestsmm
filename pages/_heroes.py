# -*- coding: utf-8 -*-
"""Иллюстрации для страниц услуг — по одной на страницу.

  export GEMINI_API_KEY="ключ"
  python3 pages/_heroes.py

Стиль общий с обложками блога, чтобы сайт выглядел цельно. Файл уже есть —
пропускается, так что перегенерировать можно точечно: удалите нужный и запустите снова.
"""
import base64
import json
import os
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets", "img", "uslugi")
W, H = 1200, 630
API = ("https://generativelanguage.googleapis.com/v1beta/models/"
       "gemini-2.5-flash-image:generateContent")

STYLE = ("Style: clean minimal 3D illustration, soft studio lighting, light neutral "
         "background, one accent colour — vivid blue, matte surfaces, soft long shadows, "
         "generous empty space, centred composition, professional and calm, "
         "absolutely no text of any kind: no letters, no numbers, no hex colour codes, "
         "no labels, no UI captions, no logos, no brand marks, no human faces.")

HEROES = {
    "vedenie-socsetey": "Three rounded 3D content cards fanned out in a row like a deck, "
                        "the middle one vivid blue, a small soft sphere hovering above them. "
                        "Pure abstract shapes, no interface details",
    "reklama": "A matte grey 3D megaphone shape with a single vivid blue arc of sound "
               "expanding from it, a few small blue spheres drifting along the arc",
    "neuroseti": "A smooth 3D sphere that dissolves on one side into a cloud of tiny blue "
                 "particles, the other side remaining matte white and solid",
    "sajty": "Two stacked rounded 3D panels like blank screens at a slight angle, matte "
             "white, one thin vivid blue bar across the front panel. No interface, no text",
}


def fit(src, dst):
    """Кроп под пропорцию, затем размер: без кропа картинку растянуло бы."""
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", src],
                         capture_output=True, text=True)
    dims = [int(x.split(":")[1]) for x in out.stdout.strip().split("\n")[1:]]
    if len(dims) == 2:
        sw, sh = dims
        target = W / float(H)
        cw, ch = (int(sh * target), sh) if sw / float(sh) > target else (sw, int(sw / target))
        subprocess.run(["sips", "-c", str(ch), str(cw), src],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82",
                    "-z", str(H), str(W), src, "--out", dst],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    os.remove(src)


def main():
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        print('Нет GEMINI_API_KEY. export GEMINI_API_KEY="ключ" и повторите.')
        return 1

    os.makedirs(OUT, exist_ok=True)
    for slug, prompt in HEROES.items():
        dst = os.path.join(OUT, slug + ".jpg")
        if os.path.exists(dst):
            print("уже есть: %s.jpg" % slug)
            continue

        payload = json.dumps({
            "contents": [{"parts": [{"text": STYLE + "\n\n" + prompt}]}],
            "generationConfig": {"imageConfig": {"aspectRatio": "16:9"}}
        }).encode("utf-8")
        req = urllib.request.Request(
            API, data=payload,
            headers={"Content-Type": "application/json", "x-goog-api-key": key})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = json.load(r)
        except Exception as e:                       # noqa: BLE001
            print("ошибка на %s: %s" % (slug, e))
            continue

        blob = next((p["inlineData"]["data"]
                     for p in data["candidates"][0]["content"]["parts"]
                     if "inlineData" in p), None)
        if not blob:
            print("нет картинки в ответе для %s" % slug)
            continue

        tmp = os.path.join(OUT, slug + ".png")
        with open(tmp, "wb") as f:
            f.write(base64.b64decode(blob))
        fit(tmp, dst)
        print("готово: assets/img/uslugi/%s.jpg" % slug)
    return 0


if __name__ == "__main__":
    sys.exit(main())
