#!/usr/bin/env python3
"""Render the 22 November 2026 world-news front page (1024x1024 PNG).

Build-time tool only: run once here to produce entry.png. The runtime
entrypoint is main.py, which only copies entry.png (stdlib only).

Layout (fresh design, drawn from scratch with Pillow):
  masthead -> 4 lead stories -> UTC timeline -> schematic world map
  + region bars -> 6 region sections (40 stories) -> by-the-numbers footer.
Every story below was verified against reporting dated 20-22 Nov 2026;
see SOURCES.md for the source of each one.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---------------------------------------------------------------- palette
PAPER = (248, 243, 230)
INK = (25, 23, 19)
RED = (166, 28, 28)
NAVY = (29, 58, 95)
GOLD = (185, 138, 29)
GREEN = (31, 122, 51)
AMBER = (168, 106, 0)
GREY = (107, 107, 107)
LIGHT_LINE = (201, 190, 166)
OCEAN = (216, 231, 242)
LAND = (88, 108, 88)
CARD = (255, 253, 247)

REGION_COLORS = {
    "Europe": (29, 58, 95),
    "Middle East": (166, 28, 28),
    "Asia": (31, 122, 51),
    "North America": (126, 58, 140),
    "South America": (185, 106, 0),
    "Africa": (0, 122, 122),
}
VERIFY_COLORS = {"CONFIRMED": GREEN, "REPORTED": AMBER, "CLAIM": RED}

# ---------------------------------------------------------------- fonts
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)  # noqa: E731
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731
F_REG = lambda s: font("DejaVuSans.ttf", s)  # noqa: E731

# ---------------------------------------------------------------- data
# (number, region, headline, detail, verification)
LEAD = [
    (1, "Europe", "Missiles fall on Poland",
     "2 missiles, 1 drone down; NATO vows defence.",
     "CONFIRMED"),
    (2, "Middle East", "Riyadh intercepts 3 missiles",
     "3 Houthi missiles downed; 2nd strike in days.",
     "CONFIRMED"),
    (3, "South America", "M6.7 quake shakes Peru",
     "Junin, 129 km deep; felt in Lima; no deaths yet.",
     "CONFIRMED"),
    (4, "North America", "Trump vows 10% card cap",
     "Vows 10% cap with the Democratic Congress.",
     "CONFIRMED"),
]

GRID = [
    ("Europe", [
        (5, "Sparta II ablaze in Baltic",
         "16 crew evacuated; Finland says likely Ukraine.",
         "CONFIRMED"),
        (6, "COP31 talks run overtime",
         "Draft drops fossil fuels; $120bn aid target cut.",
         "CONFIRMED"),
        (7, "EU eyes Big Tech tax",
         "Brussels proposes levy on Big Tech.", "REPORTED"),
        (8, "Strikes paralyse France",
         "Sixth weekend of protests; Macron flatlines.", "REPORTED"),
        (9, "Le Pen hails Senate breakthrough",
         "National Rally enters Senate; Le Pen: historic.",
         "REPORTED"),
        (10, "US F-16 crashes in Germany",
         "US jet down on a training flight.", "REPORTED"),
        (11, "UN: 'killer robot' rules by 2028",
         "Draft autonomous-weapons rules due by 2028.",
         "CONFIRMED"),
        (12, "EU-Indonesia sign trade deal",
         "98.5% of tariffs on EU goods lifted.", "REPORTED"),
    ]),
    ("Asia", [
        (13, "World court: Myanmar guilty",
         "ICJ 9-6: genocide vs Rohingya; a first verdict.",
         "CONFIRMED"),
        (14, "Manipur liquor toll hits 16",
         "~600 in hospital; 6 arrested; methanol suspected.",
         "CONFIRMED"),
        (15, "Nepal PM visits India",
         "Balendra Shah starts two-day New Delhi visit.", "REPORTED"),
        (16, "Seoul: speed decides AI race",
         "Lee: speed is decisive in the AI race.", "REPORTED"),
        (17, "Taiwan warns Canada on China",
         "Taipei warns Ottawa over deeper Beijing ties.", "REPORTED"),
        (18, "50 garment factories shut",
         "Plants stay shut amid labour unrest.", "REPORTED"),
        (19, "Protests hit Meta in India",
         "Opposition targets Meta offices.", "REPORTED"),
        (20, "India's NSE joins top five",
         "NSE enters the world's top five bourses.",
         "REPORTED"),
    ]),
    ("North America", [
        (21, "FBI's most-wanted capo caught",
         "'El Chapo Isidro' held; 11 dead in Sinaloa.",
         "CONFIRMED"),
        (22, "SEC probes Nvidia books",
         "Shares -14% Friday, -23% in week; Nasdaq -5.6%.",
         "CONFIRMED"),
        (23, "Bayer's $7.25bn Roundup deal",
         "Payout over 21 years; $10k-$165k per person.",
         "CONFIRMED"),
        (24, "Trump threatens AI-centre tax",
         "'Tremendous tax' on overseas data centres.", "REPORTED"),
        (25, "Pentagon curbs Canada ties",
         "US curbs defence cooperation with Canada.", "REPORTED"),
        (26, "FBI probes database hack",
         "Suspected hack of US law-enforcement database.",
         "REPORTED"),
        (27, "Senate vote tests Democrats",
         "New senators face early leadership test.",
         "REPORTED"),
        (28, "Trump muzzles contractors",
         "Contractors must clear Congress replies first.",
         "REPORTED"),
        (29, "US eyes Greenland build-up",
         "Major US military expansion in Greenland.", "REPORTED"),
        (30, "Claude 'solves maths riddle'?",
         "Researcher claims maths' greatest riddle solved.",
         "CLAIM"),
    ]),
    ("Middle East", [
        (31, "Three tankers hit near Hormuz",
         "Strikes in strait; one crew member missing.",
         "CONFIRMED"),
        (32, "Four killed in Gaza",
         "Aid vehicle hit in Gaza City; 1 shot in Jabalia.",
         "CONFIRMED"),
        (33, "Bahrain site struck",
         "Iran hit industrial site, Bahrain says.",
         "REPORTED"),
        (34, "Iran to ration electricity",
         "War damage forces power rationing.", "REPORTED"),
        (35, "Iran war's record oil shock",
         "2.8bn barrels lost; largest disruption ever.",
         "CONFIRMED"),
    ]),
    ("Africa", [
        (36, "24 dead as funeral boat sinks",
         "Boat capsizes in Bayelsa; 24 rescued.", "CONFIRMED"),
        (37, "Congo politician killed",
         "Slain after defending Ebola measures.", "REPORTED"),
        (38, "Ethiopia slides back to war",
         "Fighting spreads; return to war feared.", "REPORTED"),
        (39, "Spanish troops beat migrants",
         "Soldiers filmed beating migrants in Ceuta.", "REPORTED"),
    ]),
    ("South America", [
        (40, "Storm shreds Brazil town",
         "Roofs torn off in Tupancireta; 'like a tsunami'.",
         "CONFIRMED"),
    ]),
]

REGION_COUNTS = {"Europe": 9, "Middle East": 6, "Asia": 8,
                 "North America": 11, "South America": 2, "Africa": 4}
TOTAL_STORIES = 40

# (utc label, short label) -- times verified against the reporting
TIMELINE = [
    ("FRI 05:30", "Kh-101 crosses\ninto Poland"),
    ("FRI 21:00", "Wall St: Nvidia\n-14%; Bayer deal"),
    ("FRI 22:53", "Riyadh alert;\n3 missiles down"),
    ("SAT 00:09", "M6.7 quake\nstrikes Junin"),
    ("SAT", "Sparta II ablaze\nin Gulf of Finland"),
    ("SAT", "Gaza: 4 killed;\n'Chapo Isidro' held"),
    ("SAT", "Nigeria boat toll\nreaches 24"),
    ("SUN 04:00", "COP31 final-text\ndeadline in Antalya"),
]

# Coarse dotted world map: 18 rows x 40 cols ('#' = land). Schematic only.
MAP_ROWS = [
    ".###..#######.###...........############.",
    ".####.########.###...###...##############",
    "..###.#########.....#####.###############",
    "......#######......######.##############.",
    "......#######......#####..###########...",
    ".......#####.......#####.###.#########....",
    ".......####.......#########.########.....",
    "........###.......########..##.###......",
    "...........####....#######..#..#####....",
    "...........#####...#######......###.....",
    "...........#####....######......#####...",
    "...........#####....#####.......#####...",
    "............###.....#####........####...",
    "............###......###.........###....",
    "............##.......##.................",
    "............##..........................",
    "............#...........................",
    "........................................",
]
MAP_PINS = {  # region -> (lon, lat) of its count badge
    "Europe": (15, 52), "Middle East": (47, 26), "Asia": (95, 38),
    "North America": (-100, 45), "South America": (-60, -12), "Africa": (20, 5),
}


# ---------------------------------------------------------------- helpers
def text_w(draw, s, fnt):
    return draw.textlength(s, font=fnt)


def wrap(draw, s, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = s.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if text_w(draw, trial, fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def ellipsize(draw, s, fnt, max_w):
    if text_w(draw, s, fnt) <= max_w:
        return s
    while s and text_w(draw, s + "...", fnt) > max_w:
        s = s[:-1]
    return s + "..."


def vdot(draw, x, y, status, r=4):
    draw.ellipse([x - r, y - r, x + r, y + r], fill=VERIFY_COLORS[status])

# ---------------------------------------------------------------- icons
# Twelve small pictograms, each drawn from primitives in a 40x40 box.


def _box(draw, x, y, fn, color):
    fn(draw, x, y, color)


def icon_missile(draw, x, y, color):
    draw.polygon([(x + 20, y + 2), (x + 27, y + 16), (x + 13, y + 16)], fill=color)
    draw.rectangle([x + 15, y + 16, x + 25, y + 30], fill=color)
    draw.polygon([(x + 15, y + 30), (x + 9, y + 38), (x + 15, y + 34)], fill=color)
    draw.polygon([(x + 25, y + 30), (x + 31, y + 38), (x + 25, y + 34)], fill=color)


def icon_shield(draw, x, y, color):
    draw.polygon([(x + 20, y + 3), (x + 33, y + 9), (x + 33, y + 21),
                  (x + 20, y + 37), (x + 7, y + 21), (x + 7, y + 9)], fill=color)
    draw.line([(x + 13, y + 20), (x + 18, y + 25), (x + 28, y + 13)],
              fill=PAPER, width=3)


def icon_quake(draw, x, y, color):
    pts = [(x + 2, y + 20), (x + 9, y + 20), (x + 12, y + 10), (x + 16, y + 30),
           (x + 20, y + 14), (x + 24, y + 26), (x + 27, y + 20), (x + 38, y + 20)]
    draw.line(pts, fill=color, width=3, joint="curve")
    draw.ellipse([x + 17, y + 2, x + 23, y + 8], fill=color)


def icon_card(draw, x, y, color):
    draw.rounded_rectangle([x + 3, y + 8, x + 37, y + 32], radius=4,
                           outline=color, width=3)
    draw.rectangle([x + 3, y + 14, x + 37, y + 19], fill=color)
    draw.text((x + 7, y + 22), "10%", font=F_BOLD(10), fill=color)


def icon_stars(draw, x, y, color):
    for k in range(8):
        import math
        a = math.pi * k / 4.0
        cx, cy = x + 20 + 12 * math.cos(a), y + 20 + 12 * math.sin(a)
        draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=color)
    draw.ellipse([x + 16, y + 16, x + 24, y + 24], fill=color)


def icon_flame(draw, x, y, color):
    draw.polygon([(x + 20, y + 3), (x + 30, y + 18), (x + 33, y + 27),
                  (x + 26, y + 37), (x + 14, y + 37), (x + 7, y + 27),
                  (x + 10, y + 18)], fill=color)
    draw.ellipse([x + 15, y + 22, x + 25, y + 32], fill=PAPER)


def icon_scales(draw, x, y, color):
    draw.line([(x + 20, y + 4), (x + 20, y + 34)], fill=color, width=3)
    draw.line([(x + 6, y + 10), (x + 34, y + 10)], fill=color, width=3)
    draw.polygon([(x + 6, y + 10), (x + 1, y + 22), (x + 11, y + 22)], fill=color)
    draw.polygon([(x + 34, y + 10), (x + 29, y + 22), (x + 39, y + 22)], fill=color)
    draw.line([(x + 12, y + 34), (x + 28, y + 34)], fill=color, width=3)


def icon_tower(draw, x, y, color):
    draw.rectangle([x + 6, y + 12, x + 16, y + 37], fill=color)
    draw.rectangle([x + 24, y + 4, x + 34, y + 37], fill=color)
    for yy in (16, 22, 28):
        draw.rectangle([x + 26, y + yy, x + 32, y + yy + 3], fill=PAPER)


def icon_mountain(draw, x, y, color):
    draw.polygon([(x + 2, y + 36), (x + 16, y + 10), (x + 26, y + 36)], fill=color)
    draw.polygon([(x + 16, y + 10), (x + 20, y + 17), (x + 13, y + 17)], fill=PAPER)
    draw.polygon([(x + 20, y + 36), (x + 30, y + 18), (x + 38, y + 36)], fill=color)


def icon_boat(draw, x, y, color):
    draw.polygon([(x + 6, y + 20), (x + 34, y + 20), (x + 29, y + 31),
                  (x + 11, y + 31)], fill=color)
    draw.line([(x + 20, y + 20), (x + 20, y + 5)], fill=color, width=2)
    draw.polygon([(x + 20, y + 5), (x + 20, y + 18), (x + 31, y + 18)], fill=color)
    draw.line([(x + 2, y + 36), (x + 38, y + 36)], fill=color, width=2)


def icon_globe(draw, x, y, color):
    draw.ellipse([x + 4, y + 4, x + 36, y + 36], outline=color, width=3)
    draw.ellipse([x + 14, y + 4, x + 26, y + 36], outline=color, width=2)
    draw.line([(x + 4, y + 20), (x + 36, y + 20)], fill=color, width=2)


def icon_clock(draw, x, y, color):
    draw.ellipse([x + 4, y + 4, x + 36, y + 36], outline=color, width=3)
    draw.line([(x + 20, y + 20), (x + 20, y + 10)], fill=color, width=3)
    draw.line([(x + 20, y + 20), (x + 28, y + 24)], fill=color, width=3)


LEAD_ICONS = [icon_missile, icon_shield, icon_quake, icon_card]
SECTION_ICONS = {"Europe": icon_stars, "Middle East": icon_flame,
                 "Asia": icon_scales, "North America": icon_tower,
                 "South America": icon_mountain, "Africa": icon_boat}


def draw_icon_small(canvas, fn, x, y, size, color):
    """Render a 40x40 pictogram scaled down to `size` px."""
    from PIL import Image as _Image
    tmp = _Image.new("RGBA", (40, 40), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    fn(td, 0, 0, color + (255,) if isinstance(color, tuple) and len(color) == 3
       else color)
    tmp = tmp.resize((size, size), _Image.LANCZOS)
    canvas.paste(tmp, (x, y), tmp)

# ---------------------------------------------------------------- page parts
def draw_masthead(draw):
    draw.line([(24, 12), (1000, 12)], fill=INK, width=3)
    title = "THE WORLD IN ONE PAGE"
    draw.text(((W - text_w(draw, title, F_SERIF(40))) / 2, 20), title,
              font=F_SERIF(40), fill=INK)
    draw.text((24, 66), "SUNDAY, 22 NOVEMBER 2026", font=F_BOLD(12), fill=INK)
    right = "No. 22  •  $100 PRIZE  •  FREE TO READ"
    draw.text((1000 - text_w(draw, right, F_BOLD(12)), 66), right,
              font=F_BOLD(12), fill=INK)
    draw.rectangle([24, 86, 1000, 112], fill=NAVY)
    sub = "22 November 2026  —  40 Stories, 6 Regions, One Page  —  Crossroads Edition"
    draw.text(((W - text_w(draw, sub, F_BOLD(16))) / 2, 91), sub,
              font=F_BOLD(16), fill=(255, 255, 255))
    draw.line([(24, 116), (1000, 116)], fill=INK, width=1)


def draw_lead(draw):
    y0, col_w, gap = 124, 238, 8
    for i, (num, region, head, detail, status) in enumerate(LEAD):
        x = 24 + i * (col_w + gap)
        draw.rectangle([x, y0, x + col_w, y0 + 118], fill=CARD,
                       outline=LIGHT_LINE, width=1)
        draw.rectangle([x, y0, x + col_w, y0 + 4], fill=REGION_COLORS[region])
        draw.text((x + 8, y0 + 10), "%02d" % num, font=F_BOLD(13), fill=RED)
        tag = region.upper()
        draw.text((x + col_w - 8 - text_w(draw, tag, F_BOLD(9)), y0 + 12), tag,
                  font=F_BOLD(9), fill=REGION_COLORS[region])
        LEAD_ICONS[i](draw, x + 8, y0 + 30, REGION_COLORS[region])
        for j, line in enumerate(wrap(draw, head, F_BOLD(13), col_w - 62)):
            draw.text((x + 54, y0 + 30 + j * 16), line, font=F_BOLD(13), fill=INK)
        for j, line in enumerate(wrap(draw, detail, F_REG(10), col_w - 16)[:2]):
            draw.text((x + 8, y0 + 76 + j * 13), line, font=F_REG(10), fill=INK)
        vdot(draw, x + 12, y0 + 109, status, 4)
        draw.text((x + 20, y0 + 104), status, font=F_BOLD(8),
                  fill=VERIFY_COLORS[status])


def draw_timeline(draw):
    y0 = 256
    draw.text((24, y0), "THE DAY IN UTC — ALL TIMES UTC",
              font=F_BOLD(11), fill=NAVY)
    draw.text((1000 - text_w(draw, "FRI 20 NOV  →  SUN 22 NOV", F_BOLD(10)), y0),
              "FRI 20 NOV  →  SUN 22 NOV", font=F_BOLD(10), fill=GREY)
    line_y = y0 + 34
    draw.line([(40, line_y), (984, line_y)], fill=INK, width=2)
    n = len(TIMELINE)
    for i, (when, label) in enumerate(TIMELINE):
        cx = 40 + i * (944 / (n - 1))
        draw.ellipse([cx - 5, line_y - 5, cx + 5, line_y + 5], fill=RED,
                     outline=PAPER, width=1)
        wx = min(max(cx - text_w(draw, when, F_BOLD(10)) / 2, 24),
                 1000 - text_w(draw, when, F_BOLD(10)))
        draw.text((wx, line_y - 18), when, font=F_BOLD(10), fill=RED)
        for j, part in enumerate(label.split("\n")):
            px = min(max(cx - text_w(draw, part, F_REG(9)) / 2, 24),
                     1000 - text_w(draw, part, F_REG(9)))
            draw.text((px, line_y + 10 + j * 12), part, font=F_REG(9), fill=INK)
    draw.line([(24, y0 + 62), (1000, y0 + 62)], fill=LIGHT_LINE, width=1)


def draw_map_panel(draw):
    # Left: dotted schematic world map with region count badges.
    draw.rectangle([24, 324, 330, 470], fill=CARD, outline=LIGHT_LINE, width=1)
    draw.text((34, 330), "WHERE IT HAPPENED — SCHEMATIC MAP",
              font=F_BOLD(10), fill=NAVY)
    mx, my, mw, mh = 34, 350, 286, 110
    draw.rectangle([mx, my, mx + mw, my + mh], fill=OCEAN)
    rows, cols = len(MAP_ROWS), len(MAP_ROWS[0])
    cw, ch = mw / cols, mh / rows
    for r, row in enumerate(MAP_ROWS):
        for c, ch_ in enumerate(row):
            if ch_ == "#":
                cx, cy = mx + (c + 0.5) * cw, my + (r + 0.5) * ch
                draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=LAND)
    for region, (lon, lat) in MAP_PINS.items():
        bx = mx + (lon + 180) / 360 * mw
        by = my + (90 - lat) / 180 * mh
        col = REGION_COLORS[region]
        draw.ellipse([bx - 10, by - 10, bx + 10, by + 10], fill=col,
                     outline=(255, 255, 255), width=2)
        n = str(REGION_COUNTS[region])
        draw.text((bx - text_w(draw, n, F_BOLD(10)) / 2, by - 7), n,
                  font=F_BOLD(10), fill=(255, 255, 255))
    # Right: region bars + verification legend.
    draw.text((348, 330), "6 REGIONS — 40 STORIES", font=F_BOLD(11), fill=NAVY)
    y = 352
    for region in ["Europe", "North America", "Asia", "Middle East", "Africa",
                   "South America"]:
        col = REGION_COLORS[region]
        draw.text((348, y), region, font=F_BOLD(11), fill=INK)
        bx0 = 470
        draw.rectangle([bx0, y + 1, bx0 + 300, y + 11], outline=LIGHT_LINE, width=1)
        fill_w = 300 * REGION_COUNTS[region] / 11
        draw.rectangle([bx0, y + 1, bx0 + fill_w, y + 11], fill=col)
        draw.text((782, y), str(REGION_COUNTS[region]), font=F_BOLD(12), fill=col)
        y += 16
    y += 2
    draw.text((348, y), "HOW TO READ:  ", font=F_BOLD(10), fill=INK)
    lx = 348 + text_w(draw, "HOW TO READ:  ", F_BOLD(10))
    for status, label in [("CONFIRMED", "confirmed by 2+ sources"),
                          ("REPORTED", "single report"),
                          ("CLAIM", "unverified claim")]:
        vdot(draw, lx + 5, y + 6, status, 4)
        draw.text((lx + 13, y), label, font=F_REG(10), fill=INK)
        lx += 13 + text_w(draw, label, F_REG(10)) + 22
    draw.text((348, y + 18),
              "Counts on the map match the title: 40 stories across 6 regions.",
              font=F_REG(10), fill=GREY)

# ---------------------------------------------------------------- grid + footer
def _section_height(draw, stories, hf, df, hstep, dstep, gap):
    total = 0
    for _num, head, detail, _st in stories:
        lines = wrap(draw, head, F_BOLD(hf), 268)[:2]
        total += len(lines) * hstep + dstep + gap
    return total


def _columns():
    # Reading order: Europe, Asia, North America / Middle East, Africa, S. America
    by_region = dict(GRID)
    return [
        [("Europe", by_region["Europe"]), ("South America", by_region["South America"])],
        [("Asia", by_region["Asia"]), ("Africa", by_region["Africa"])],
        [("North America", by_region["North America"]),
         ("Middle East", by_region["Middle East"])],
    ]


def draw_grid(draw, img):
    presets = [(11.5, 9.5, 13, 11, 2), (11, 9, 12, 10, 1), (10.5, 9, 12, 10, 1)]
    y_top, y_bottom = 478, 950
    chosen = None
    for hf, df, hstep, dstep, gap in presets:
        heights = []
        for col in _columns():
            h = 0
            for _region, stories in col:
                h += 26 + _section_height(draw, stories, hf, df, hstep, dstep, gap) + 6
            h += 8
            heights.append(h)
        if max(heights) <= y_bottom - y_top:
            chosen = (hf, df, hstep, dstep, gap)
            break
    if chosen is None:
        chosen = presets[-1]
    hf, df, hstep, dstep, gap = chosen
    for ci, col in enumerate(_columns()):
        x = 24 + ci * 328
        y = y_top
        for region, stories in col:
            colr = REGION_COLORS[region]
            sec_h = 26 + _section_height(draw, stories, hf, df, hstep, dstep, gap) + 6
            draw.rectangle([x, y, x + 320, y + sec_h], fill=CARD,
                           outline=LIGHT_LINE, width=1)
            draw.rectangle([x, y, x + 320, y + 24], fill=colr)
            draw_icon_small(img, SECTION_ICONS[region], x + 5, y + 4, 16,
                            (255, 255, 255))
            draw.text((x + 30, y + 5),
                      "%s  —  %d" % (region.upper(), REGION_COUNTS[region]),
                      font=F_BOLD(12), fill=(255, 255, 255))
            ry = y + 30
            for num, head, detail, status in stories:
                draw.text((x + 8, ry), "%02d" % num, font=F_BOLD(hf), fill=RED)
                lines = wrap(draw, head, F_BOLD(hf), 268)[:2]
                for j, line in enumerate(lines):
                    draw.text((x + 36, ry + j * hstep), line, font=F_BOLD(hf),
                              fill=INK)
                dy = ry + len(lines) * hstep
                draw.text((x + 36, dy),
                          ellipsize(draw, detail, F_REG(df), 272),
                          font=F_REG(df), fill=(64, 60, 52))
                vdot(draw, x + 313, ry + 5, status, 4)
                ry = dy + dstep + gap
            y += sec_h + 8


def draw_footer(draw):
    draw.line([(24, 956), (1000, 956)], fill=INK, width=2)
    stats = "40 STORIES  •  6 REGIONS  •  11 DRAWN ILLUSTRATIONS  •  3 VERIFICATION TIERS"
    draw.text(((W - text_w(draw, stats, F_BOLD(12))) / 2, 964), stats,
              font=F_BOLD(12), fill=NAVY)
    src = ("Sources: Reuters, AP, AFP, Al Jazeera, SCMP, CNN, IEA, ICJ, USGS, national "
           "authorities — every story reported 20–22 Nov 2026. Full list: SOURCES.md")
    draw.text(((W - text_w(draw, src, F_REG(9))) / 2, 982), src,
              font=F_REG(9), fill=INK)
    credit = ("THE WORLD IN ONE PAGE  •  Entry for make.fun news-image-20261122  •  "
              "Program: main.py (Python 3.13, stdlib only)  •  Image: 1024×1024 PNG")
    draw.text(((W - text_w(draw, credit, F_REG(9))) / 2, 998), credit,
              font=F_REG(9), fill=GREY)


# ---------------------------------------------------------------- main
def main():
    rows = [(r + "." * 40)[:40] for r in MAP_ROWS]
    assert len(rows) == 18, "map must have 18 rows"
    globals()["MAP_ROWS"] = rows
    all_stories = list(LEAD) + [(num, region, head, detail, status)
                                for region, ss in GRID
                                for (num, head, detail, status) in ss]
    assert len(all_stories) == TOTAL_STORIES, len(all_stories)
    assert sorted(s[0] for s in all_stories) == list(range(1, TOTAL_STORIES + 1))
    for region, want in REGION_COUNTS.items():
        got = sum(1 for s in all_stories if s[1] == region)
        assert got == want, (region, got, want)
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_lead(draw)
    draw_timeline(draw)
    draw_map_panel(draw)
    draw_grid(draw, img)
    draw_footer(draw)
    img.save(OUT, format="PNG", optimize=True)
    import hashlib
    data = open(OUT, "rb").read()
    print("wrote %s  %d bytes  sha256=%s" % (OUT, len(data),
                                             hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
