# Обложки статей: промпты для Nano Banana

## Как пользоваться

1. Откройте Nano Banana (Gemini) и вставьте **блок стиля** — он общий для всех, чтобы
   20 обложек выглядели одним набором, а не случайной подборкой.
2. Дальше вставляйте промпт конкретной статьи.
3. Сохраните результат в эту папку под именем из колонки «файл» — строго так,
   иначе генератор не найдёт картинку.
4. Из корня проекта выполните:

```bash
python3 blog/_covers.py fit
```

Скрипт приведёт всё к 1200×630 JPEG и сожмёт под веб. Затем:

```bash
python3 blog/_generate.py
```

Обложки сами появятся в карточках, на страницах статей и в og:image для соцсетей.
Файла нет — страница просто собирается без картинки, ничего не ломается.

## Блок стиля (вставлять перед каждым промптом)

```
Style: clean minimal 3D illustration, soft studio lighting, light neutral background
(#F2F3F5 to white gradient), one accent colour — vivid blue #2563EB, matte surfaces,
soft long shadows, generous empty space, centred composition, professional and calm,
no text, no letters, no numbers, no logos, no brand marks, no human faces.
Aspect ratio 1200x630, horizontal.
```

Важно: `no text, no letters` — модели плохо рисуют кириллицу, а надписи на картинке
всё равно не индексируются. Заголовок на странице и так есть.

## Промпты

| # | Файл | Промпт |
|---|---|---|
| 1 | `kontent-plan-dlya-socsetey.jpg` | A floating 3D calendar grid with several coloured cards slotted into different days, one card highlighted in blue, small floating icons of a camera and a chat bubble nearby |
| 2 | `skolko-stoit-vedenie-socsetey.jpg` | A balance scale in soft 3D: on one side a stack of blue coins, on the other a small cluster of content blocks — a video frame, a photo, a chat bubble |
| 3 | `prodvizhenie-vkontakte.jpg` | A rounded 3D smartphone standing upright with an abstract social feed on screen, surrounded by floating blue circles representing an audience network |
| 4 | `kak-snimat-reels.jpg` | A vertical 3D video frame floating in the centre with a blue play button, small motion arcs around it, a tiny tripod and ring light beside it |
| 5 | `oformlenie-profilya.jpg` | A 3D profile card floating above a surface: round avatar placeholder, abstract bio lines, a blue action button, three small circular story highlights below |
| 6 | `targeting-vk-s-nulya.jpg` | A 3D dartboard seen at an angle with one blue dart in the centre, small floating audience segments as translucent spheres around it |
| 7 | `posevy-v-telegram.jpg` | A 3D paper plane flying upward leaving a soft blue trail, below it a row of small rounded channel cards |
| 8 | `telegram-kanal-dlya-biznesa.jpg` | A 3D chat window floating in space with stacked message bubbles, one bubble highlighted blue, small subscriber dots rising around it |
| 9 | `yandex-direct-dlya-malogo-biznesa.jpg` | A 3D search bar floating in front of a stack of result cards, the top card lifted and marked with a blue tag |
| 10 | `metriki-smm.jpg` | A minimal 3D dashboard: a rising bar chart, a circular gauge and a line graph, all in grey with one blue element |
| 11 | `voronka-prodazh-v-socsetyah.jpg` | A translucent 3D funnel with small spheres entering wide at the top and a few blue spheres exiting at the narrow bottom |
| 12 | `neiroseti-v-smm.jpg` | A glowing 3D neural node structure on the left transforming into neat content cards on the right, blue glow along the connections |
| 13 | `prodayushchie-teksty.jpg` | A 3D document card with abstract text lines, a blue cursor beam and a small paper plane lifting off the page |
| 14 | `audit-socsetey.jpg` | A 3D magnifying glass hovering over a small dashboard card, a blue checkmark and a red cross floating nearby |
| 15 | `celevaya-auditoriya.jpg` | Several translucent 3D spheres of different sizes clustered together, one group highlighted in blue and separated from the rest |
| 16 | `storis-dlya-biznesa.jpg` | A horizontal row of 3D circular story rings, the first one outlined in blue, a small vertical frame floating above them |
| 17 | `rabota-s-negativom.jpg` | Two 3D speech bubbles facing each other: one grey and jagged, one smooth and blue, a small shield between them |
| 18 | `sayt-ili-socseti.jpg` | A 3D laptop on the left and a 3D smartphone on the right connected by a blue arc, equal visual weight |
| 19 | `prodvizhenie-lokalnogo-biznesa.jpg` | A 3D map pin standing on a small circular platform with tiny abstract shop fronts around it, soft blue radius circle on the ground |
| 20 | `oshibki-v-smm.jpg` | A 3D stack of blocks slightly off balance, one block pulled out and marked blue, soft shadow underneath |

## Если хотите сгенерировать через API

Nano Banana доступна как `gemini-2.5-flash-image` в Gemini API. Скрипт-заготовка —
`blog/_covers.py`, команда `generate`: она возьмёт промпты из этого файла и разложит
результат по именам. Нужен только ключ:

```bash
export GEMINI_API_KEY="ваш-ключ"
python3 blog/_covers.py generate
```

Ключ в код не записывается и в репозиторий не попадает.
