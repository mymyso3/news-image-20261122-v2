# 22 November 2026 — 40 Stories, 6 Regions, One Page — Crossroads Edition

[![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/mymyso3/news-image-20261122-v2/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/mymyso3/news-image-20261122-v2/reward.svg)](https://make.fun/bounty/news-image-20261122)

Entry for [news-image-20261122](https://make.fun/bounty/news-image-20261122) on make.fun: one image that sums up the world news of Sunday 22 November 2026. Free entry, $100 prize pool, top 50 paid. License: MIT (see `LICENSE`).

## The day in one image

40 verified stories across 6 regions, on one 1024×1024 front page:

- **Lead (4):** Russian missiles fall on Poland (Europe); Houthi missiles intercepted over Riyadh (Middle East); M6.7 quake in Peru (South America); Trump vows a 10% credit-card cap (North America).
- **Europe (9):** Sparta II ablaze in the Baltic; COP31 in overtime; EU Big Tech tax; France strikes; Le Pen's Senate breakthrough; F-16 crash in Germany; 'killer robot' rules by 2028; EU–Indonesia trade deal.
- **Asia (8):** ICJ rules Myanmar committed genocide vs the Rohingya (9–6); Manipur liquor toll hits 16; Nepal PM visits India; Seoul on the AI race; Taiwan warns Canada; Bangladesh factories shut; Meta protests in India; India's NSE joins the top five.
- **North America (11):** 'El Chapo Isidro' captured, 11 dead; SEC probes Nvidia; Bayer's $7.25bn Roundup deal; Trump threatens an AI-centre tax; Pentagon curbs Canada ties; FBI database hack probe; Senate vote tests Democrats; contractors muzzled; Greenland build-up; Claude 'solves maths riddle' (claim).
- **Middle East (6):** three tankers hit near Hormuz; four killed in Gaza; Bahrain site struck; Iran to ration electricity; record oil shock from the Iran war.
- **Africa (4):** 24 dead as a funeral boat sinks in Nigeria; Congo politician killed; Ethiopia slides back to war; Spanish troops beat migrants in Ceuta.
- **South America (2):** the Peru quake; a storm shreds a Brazil town.

The page also carries a UTC timeline of the day, a schematic world map with one count badge per region, region bars, and a verification mark on every story: green = confirmed by 2+ sources, amber = single report, red = unverified claim. Every story's source is listed in `SOURCES.md`.

## How it works

- `render.py` draws `entry.png` at build time with Pillow: masthead, lead cards, UTC timeline, dotted world map, six region sections, footer.
- `main.py` is the runtime entrypoint (Python 3.13, standard library only): it copies `entry.png` to the output directory. No network. Two runs write byte-identical files.

## Run

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Referral code: `gg809aec`
