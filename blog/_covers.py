# -*- coding: utf-8 -*-
"""Работа с обложками статей.

  python3 blog/_covers.py check     — каких обложек не хватает
  python3 blog/_covers.py fit       — привести файлы к 1200x630 JPEG
  python3 blog/_covers.py generate  — сгенерировать через Gemini (нужен GEMINI_API_KEY)

Промпты и правила именования — в blog/covers/PROMPTS.md.
"""
import base64
import json
import os
import re
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
COVERS = os.path.join(HERE, "covers")
PROMPTS_MD = os.path.join(COVERS, "PROMPTS.md")
EXTS = ("webp", "jpg", "jpeg", "png")
W, H = 1200, 630

sys.path.insert(0, HERE)
from _articles import ARTICLES  # noqa: E402

MODEL = "gemini-2.5-flash-image"
API = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % MODEL


def existing(slug):
    for ext in EXTS:
        p = os.path.join(COVERS, "%s.%s" % (slug, ext))
        if os.path.exists(p):
            return p
    return None


def read_prompts():
    """Достаёт стиль и таблицу промптов из PROMPTS.md."""
    text = open(PROMPTS_MD, encoding="utf-8").read()
    style = re.search(r"```\n(Style:.*?)\n```", text, re.S)
    style = style.group(1).strip() if style else ""
    prompts = {}
    for row in re.findall(r"^\|\s*\d+\s*\|\s*`([^`]+)`\s*\|\s*(.+?)\s*\|$", text, re.M):
        prompts[os.path.splitext(row[0])[0]] = row[1]
    return style, prompts


def cmd_check():
    missing = [a["slug"] for a in ARTICLES if not existing(a["slug"])]
    have = len(ARTICLES) - len(missing)
    print("обложек: %d из %d" % (have, len(ARTICLES)))
    for slug in missing:
        print("  нет: covers/%s.jpg" % slug)
    return 0


def cmd_fit():
    """Приводит файлы к 1200x630 JPEG: сначала кроп под пропорцию, потом размер.
    Без кропа sips растянул бы картинку — модель отдаёт 16:9, а нужно 1.905:1."""
    n = 0
    for a in ARTICLES:
        src = existing(a["slug"])
        if not src:
            continue
        dst = os.path.join(COVERS, a["slug"] + ".jpg")
        tmp = os.path.join(COVERS, "_tmp_" + a["slug"] + ".png")
        subprocess.run(["cp", src, tmp], check=False)

        out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", tmp],
                             capture_output=True, text=True)
        dims = [int(x.split(":")[1]) for x in out.stdout.strip().split("\n")[1:]]
        if len(dims) == 2:
            sw, sh = dims
            target = W / float(H)
            if sw / float(sh) > target:          # шире нужного — режем по бокам
                cw, ch = int(sh * target), sh
            else:                                # выше нужного — режем сверху и снизу
                cw, ch = sw, int(sw / target)
            subprocess.run(["sips", "-c", str(ch), str(cw), tmp],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82",
                        "-z", str(H), str(W), tmp, "--out", dst],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        os.remove(tmp)
        if src != dst and os.path.exists(src):
            os.remove(src)
        n += 1
    print("обработано файлов: %d" % n)
    return 0


def cmd_generate():
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        print("Нет GEMINI_API_KEY. Задайте переменную окружения и повторите:")
        print('  export GEMINI_API_KEY="ваш-ключ"')
        return 1

    style, prompts = read_prompts()
    todo = [a for a in ARTICLES if not existing(a["slug"])]
    if not todo:
        print("все обложки уже на месте")
        return 0

    for a in todo:
        prompt = prompts.get(a["slug"])
        if not prompt:
            print("пропуск %s: нет промпта в PROMPTS.md" % a["slug"])
            continue

        payload = json.dumps({
            "contents": [{"parts": [{"text": style + "\n\n" + prompt}]}],
            "generationConfig": {"imageConfig": {"aspectRatio": "16:9"}}
        }).encode("utf-8")
        req = urllib.request.Request(
            API, data=payload,
            headers={"Content-Type": "application/json", "x-goog-api-key": key})

        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.load(r)
        except Exception as e:                      # noqa: BLE001
            print("ошибка на %s: %s" % (a["slug"], e))
            continue

        blob = None
        for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
            if "inlineData" in part:
                blob = part["inlineData"]["data"]
                break
        if not blob:
            print("нет картинки в ответе для %s" % a["slug"])
            continue

        path = os.path.join(COVERS, a["slug"] + ".png")
        with open(path, "wb") as f:
            f.write(base64.b64decode(blob))
        print("готово: covers/%s.png" % a["slug"])

    cmd_fit()
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    sys.exit({"check": cmd_check, "fit": cmd_fit, "generate": cmd_generate}
             .get(cmd, cmd_check)())
