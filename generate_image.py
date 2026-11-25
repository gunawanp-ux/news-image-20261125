"""Draw the front page for Wednesday 25 November 2026.

A single 1024x1024 PNG newspaper front page: masthead, two lead stories
with original illustrations, three top stories (two illustrated, one with
a drawn gavel), forty numbered one-line briefs, a dot-matrix world map
with twelve numbered pins, and a closing markets bar. The four
illustrations in illustrations/ were generated for this entry (flat
editorial style, no text); everything else is drawn here in code with
Pillow. No network is used, so the output is fully deterministic.
"""

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "entry.png"
PICS = ROOT / "illustrations"

PAGE_W, PAGE_H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (176, 42, 32)
BLUE = (31, 78, 121)
GREY = (110, 108, 100)
PANEL = (232, 228, 216)
EDGE = (180, 175, 160)
BODY = (60, 58, 52)

FONTS = Path("/usr/share/fonts/truetype/liberation")
SERIF_B = str(FONTS / "LiberationSerif-Bold.ttf")
SERIF_R = str(FONTS / "LiberationSerif-Regular.ttf")
SANS_R = str(FONTS / "LiberationSans-Regular.ttf")
SANS_B = str(FONTS / "LiberationSans-Bold.ttf")


def face(path, size):
    return ImageFont.truetype(path, size)


def fit_lines(draw, text, fnt, width, limit):
    """Wrap text to a pixel width, keeping at most `limit` lines."""
    rows, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                rows.append(cur)
            cur = word
    if cur:
        rows.append(cur)
    return rows[:limit]


def clip_line(draw, text, fnt, width):
    """Shrink text to one line that fits, with an ellipsis when cut."""
    if draw.textlength(text, font=fnt) <= width:
        return text
    while text and draw.textlength(text + "\u2026", font=fnt) > width:
        text = text[:-1]
    return text + "\u2026"


def paste_photo(page, path, box):
    """Centre-crop a picture into `box` (x0, y0, x1, y1) and paste it."""
    pic = Image.open(path).convert("RGB")
    bw, bh = box[2] - box[0], box[3] - box[1]
    scale = max(bw / pic.width, bh / pic.height)
    nw, nh = round(pic.width * scale), round(pic.height * scale)
    pic = pic.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - bw) // 2, (nh - bh) // 2
    page.paste(pic.crop((left, top, left + bw, top + bh)), box[:2])
    ImageDraw.Draw(page).rectangle(box, outline=EDGE, width=1)


# ------------------------------------------------------------------ stories

LEADS = [
    {
        "kicker": "SPACE  \u00b7  SHENZHOU-24",
        "headline": "Pakistan's first astronaut reaches orbit as Shenzhou-24 docks with Tiangong",
        "deck": "Zeeshan Ali, 40, first foreigner aboard China's station; "
                "launched 00:18 UTC.",
        "pic": "media-generation-rocket-launch-0-037fe276-a5b6-4f4c-97c6-5c9db944f64e.png",
    },
    {
        "kicker": "MARKETS  \u00b7  ASIA",
        "headline": "Asian shares plunge again as AI rout spreads; KOSPI \u22125%, Nikkei \u22123%, Taiex \u22128%",
        "deck": "Samsung, SK Hynix \u22128%; TSMC \u22128.3%; US tariff threats "
                "add to sell-off.",
        "pic": "media-generation-market-crash-0-2f51f813-1920-4445-9089-d10daa3e2c2e.png",
    },
]

TOPS = [
    {
        "kicker": "GULF  \u00b7  HORMUZ",
        "headline": "Iran says a container ship hit a mine near Hormuz; oil jumps",
        "deck": "UKMTO confirms 3 ships hit; Brent $91.40.",
        "pic": "media-generation-oil-tanker-0-23701ea9-ca12-49ea-b926-993c1328cc15.png",
    },
    {
        "kicker": "TRADE  \u00b7  WASHINGTON",
        "headline": "US prepares to raise tariffs on China, EU and 14 others",
        "deck": "USTR to unveil probe this week.",
        "pic": "media-generation-tariffs-containers-0-e1b24046-3770-4769-a0d6-8ec713d49306.png",
    },
    {
        "kicker": "JUSTICE  \u00b7  NEW YORK",
        "headline": "US jury finds Huawei guilty of trade-secret theft and bank fraud",
        "deck": "Guilty on 10 of 12 counts; acquitted of racketeering.",
        "pic": None,
    },
]

BRIEFS = [
    "Chess: Gukesh plays White in Game 2 in Geneva today after Game 1 draw",
    'Russia accuses Ukraine of "terrorism" over ship drone attacks in Baltic and Libya',
    "Zelenskiy confirms Ukraine hit a Russian ship in the Gulf of Finland",
    "Russian strike kills two in Odesa region; Kyiv hit by drones overnight",
    "Russian assault on Zaporizhzhia kills two, injures 22",
    "Israeli strike kills Hamas internal security chief Naeem Abu Nahel in Gaza",
    "Gaza death toll reaches 74,746, WAFA says",
    "Houthi media: at least 33 killed in Saudi-led strike on al-Shariyah, near Sanaa",
    "Airstrikes hit Sanaa late Tuesday after Houthi drone attack on Riyadh tower",
    "At least eight killed in airstrikes on Houthi-held Hodeidah",
    "Yemeni military reports 697 strikes on Houthi positions; 97 fighters 'neutralised'",
    "Strike on buses and trucks kills 26 in Yemen's Lahj province",
    "Houthis will not seize Aden, Yemeni government forces say",
    "COP31 collapse leaves vulnerable nations at risk, UN warns",
    "WFP: 266 million people face acute food insecurity",
    "AIDS deaths fall to 570,000 in 2025, lowest in 20+ years, UNAIDS says",
    "England level T20 series 1\u20131; Donald smashes 85 off 32 balls vs Australia",
    "BJP and Akali Dal revive Punjab alliance; Akali Dal keeps chief minister post",
    "Nepal PM Shah wraps first state visit to India after talks with Modi",
    "Malaysia to send 6,500 Rohingya refugees back to Myanmar in December",
    "Magnitude 5.6 quake strikes eastern Nepal near Tibet border",
    "UAE bus\u2013truck crash death toll rises to 13",
    "Trump pardons turkeys Freedom and Feathers for Thanksgiving",
    "Trump awards Rudy Giuliani the Medal of Freedom",
    "CIA and ODNI suffer cybersecurity breach of unclassified data, Reuters says",
    'US envoy "not certain" military aid to Israel will end this year',
    "Fort Hood shooter Hasan seeks stay of execution set for next week",
    "Sarkozy corruption case ordered to trial; first hearing 1 April 2027",
    "Nvidia falls ~7% as Huang return rally fades; Micron \u221211%, chip index \u22128%",
    "Anthropic drops below its $83 IPO price four days after listing",
    "Dell beats earnings, lifts 2027 forecast to $202bn, $25bn buyback",
    "Sanofi agrees to buy Insmed for $41bn, pharma's biggest since 2023",
    "Dow tops 50,000 for the first time, closing at 50,019",
    'HP posts $769m profit, "prudent" guidance as memory costs bite',
    "Huang tells Nvidia staff he is in therapy, apologises in town hall",
    "Australia inflation beats forecasts in October as fuel, clothing jump",
    "Brazil cuts 2027 growth forecast to 1.8%, lifts inflation to 4.5%",
    "NATO plans early-warning aircraft deployment in Poland",
    "Workday raises full-year subscription outlook to $9.96bn",
    "Stripe valuation set to top $200bn in latest investor talks",
]

PINS = [
    (40.9, 100.3, "Jiuquan, China"),
    (37.6, 127.0, "Seoul, S. Korea"),
    (35.7, 139.7, "Tokyo, Japan"),
    (26.5, 56.3, "Strait of Hormuz"),
    (38.9, -77.0, "Washington, USA"),
    (46.2, 6.1, "Geneva, Switzerland"),
    (46.5, 30.7, "Odesa, Ukraine"),
    (31.5, 34.5, "Gaza City"),
    (15.4, 44.2, "Sanaa, Yemen"),
    (28.6, 77.2, "New Delhi, India"),
    (-28.0, 153.4, "Gold Coast, Australia"),
    (33.7, 73.1, "Islamabad, Pakistan"),
]

# Land as coarse boxes on a 48 x 20 grid (columns 180W-180E, rows 78N-57S).
# Each box is (col0, row0, col1, row1) inclusive; drawn as dots.
LAND_BOXES = [
    (2, 1, 12, 2), (2, 3, 13, 5), (4, 6, 11, 7), (6, 8, 9, 9),
    (14, 1, 16, 2),
    (10, 10, 14, 11), (11, 12, 13, 13), (12, 14, 13, 15),
    (22, 1, 26, 2), (23, 3, 27, 4),
    (23, 7, 28, 8), (24, 9, 28, 10), (24, 11, 27, 12), (25, 13, 26, 13),
    (28, 1, 44, 2), (29, 3, 44, 5), (30, 6, 42, 7), (31, 8, 38, 8),
    (36, 9, 42, 10),
    (38, 13, 44, 14),
]

MARKETS = [
    "Dow 50,019 +0.85%",
    "S&P 500 7,201 \u22120.50%",
    "Nasdaq 23,734 \u22121.48%",
    "KOSPI \u22125.0%",
    "Nikkei \u22123.1%",
    "Brent $91.40",
    "WTI $82.05",
]


# ------------------------------------------------------------------ pictograms

def glyph(draw, kind, cx, cy, s, color=INK):
    """Draw one small pictogram centred at (cx, cy), size s."""
    u = s / 40.0

    def seg(pts, w=2):
        draw.line([(cx + x * u, cy + y * u) for x, y in pts],
                  fill=color, width=max(1, int(w * u)))

    def shape(pts, fill=color):
        draw.polygon([(cx + x * u, cy + y * u) for x, y in pts], fill=fill)

    if kind == "gavel":
        seg([(-14, 14), (10, -10)], w=4)
        seg([(2, -18), (18, -2)], w=7)
        seg([(-14, 16), (14, 16)], w=2)
    elif kind == "star":
        shape([(0, -16), (4, -5), (16, -5), (7, 2), (10, 14),
               (0, 7), (-10, 14), (-7, 2), (-16, -5), (-4, -5)])
    elif kind == "chip":
        draw.rectangle([cx - 10 * u, cy - 10 * u, cx + 10 * u, cy + 10 * u],
                       outline=color, width=max(1, int(2 * u)))
        draw.rectangle([cx - 4 * u, cy - 4 * u, cx + 4 * u, cy + 4 * u],
                       fill=color)
        for k in (-6, 0, 6):
            seg([(k, -16), (k, -10)])
            seg([(k, 10), (k, 16)])
            seg([(-16, k), (-10, k)])
            seg([(10, k), (16, k)])
    elif kind == "cross":
        shape([(-4, -16), (4, -16), (4, -4), (16, -4), (16, 4),
               (4, 4), (4, 16), (-4, 16), (-4, 4), (-16, 4), (-16, -4),
               (-4, -4)], fill=RED)
    elif kind == "flame":
        shape([(-10, 12), (-12, 0), (-4, -8), (0, -16), (6, -6),
               (12, -2), (10, 12)], fill=(214, 96, 20))
    elif kind == "ball":
        draw.ellipse([cx - 14 * u, cy - 14 * u, cx + 14 * u, cy + 14 * u],
                     outline=color, width=max(1, int(2 * u)))
        seg([(-14, 0), (14, 0)])
        draw.arc([cx - 6 * u, cy - 14 * u, cx + 6 * u, cy + 14 * u],
                 270, 90, fill=color, width=max(1, int(2 * u)))
        draw.arc([cx - 6 * u, cy - 14 * u, cx + 6 * u, cy + 14 * u],
                 90, 270, fill=color, width=max(1, int(2 * u)))


# Small pictograms on a few briefs (story number -> glyph kind).
BRIEF_GLYPHS = {7: "star", 12: "cross", 16: "flame", 22: "ball",
                34: "chip", 35: "chip"}


# ------------------------------------------------------------------ page

def build_page():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(page)
    mx = 16

    # Masthead
    d.text((PAGE_W // 2, 10), "THE WORLD IN ONE DAY",
           font=face(SERIF_B, 46), fill=INK, anchor="ma")
    d.text((PAGE_W // 2, 60),
           "WEDNESDAY 25 NOVEMBER 2026  \u00b7  45 STORIES FROM SIX CONTINENTS",
           font=face(SANS_B, 15), fill=RED, anchor="ma")
    d.line([(mx, 84), (PAGE_W - mx, 84)], fill=INK, width=2)
    d.line([(mx, 88), (PAGE_W - mx, 88)], fill=INK, width=1)

    # Leads: two boxes with an illustration on the right of each.
    lead_y, lead_h = 96, 140
    box_w = (PAGE_W - 2 * mx - 12) // 2
    f_kick = face(SANS_B, 12)
    f_head = face(SANS_B, 18)
    f_deck = face(SANS_R, 13)
    for i, lead in enumerate(LEADS):
        x0 = mx + i * (box_w + 12)
        d.rectangle([x0, lead_y, x0 + box_w, lead_y + lead_h],
                    outline=EDGE, width=1)
        d.rectangle([x0, lead_y, x0 + box_w, lead_y + 22], fill=PANEL)
        d.text((x0 + 8, lead_y + 4), lead["kicker"], font=f_kick, fill=RED)
        img_w, img_h = 148, 106
        paste_photo(page, PICS / lead["pic"],
                    (x0 + box_w - img_w - 8, lead_y + 30,
                     x0 + box_w - 8, lead_y + 30 + img_h))
        text_w = box_w - img_w - 24
        y = lead_y + 30
        for ln in fit_lines(d, lead["headline"], f_head, text_w, 3):
            d.text((x0 + 8, y), ln, font=f_head, fill=INK)
            y += 22
        for ln in fit_lines(d, lead["deck"], f_deck, text_w, 2):
            d.text((x0 + 8, y), ln, font=f_deck, fill=BODY)
            y += 16

    # Top stories: three boxes; the first two carry illustrations,
    # the third a drawn gavel.
    top_y, top_h = 246, 104
    top_w = (PAGE_W - 2 * mx - 24) // 3
    f_thead = face(SANS_B, 14)
    f_tdeck = face(SANS_R, 11)
    for i, top in enumerate(TOPS):
        x0 = mx + i * (top_w + 12)
        d.rectangle([x0, top_y, x0 + top_w, top_y + top_h],
                    outline=EDGE, width=1)
        d.text((x0 + 8, top_y + 5), top["kicker"], font=f_kick, fill=BLUE)
        if top["pic"]:
            paste_photo(page, PICS / top["pic"],
                        (x0 + top_w - 108, top_y + 26,
                         x0 + top_w - 8, top_y + 26 + 70))
            head_w = top_w - 116
        else:
            glyph(d, "gavel", x0 + top_w - 30, top_y + 40, 36)
            head_w = top_w - 66
        y = top_y + 24
        for ln in fit_lines(d, top["headline"], f_thead, head_w, 3):
            d.text((x0 + 8, y), ln, font=f_thead, fill=INK)
            y += 17
        for ln in fit_lines(d, top["deck"], f_tdeck, head_w, 2):
            d.text((x0 + 8, y), ln, font=f_tdeck, fill=BODY)
            y += 14

    return page, d, mx


def draw_briefs(d, mx):
    """Two columns of twenty numbered one-line briefs."""
    d.line([(mx, 362), (PAGE_W - mx, 362)], fill=INK, width=2)
    d.text((mx, 368), "THE DAY IN BRIEF \u2014 40 MORE STORIES",
           font=face(SANS_B, 13), fill=INK)
    d.text((PAGE_W - mx, 368), "ALL FROM WEDNESDAY 25 NOVEMBER 2026",
           font=face(SANS_B, 11), fill=GREY, anchor="ra")
    f_num = face(SANS_B, 12)
    f_txt = face(SANS_R, 12)
    col_w = (PAGE_W - 2 * mx - 12) // 2
    for idx, text in enumerate(BRIEFS):
        col, row = idx // 20, idx % 20
        x0 = mx + col * (col_w + 12)
        y = 392 + row * 20
        num = idx + 6
        d.text((x0, y), f"{num}.", font=f_num, fill=RED)
        tx = x0 + 26
        kind = BRIEF_GLYPHS.get(num)
        if kind:
            glyph(d, kind, x0 + 34, y + 7, 15)
            tx = x0 + 46
        d.text((tx, y), clip_line(d, text, f_txt, x0 + col_w - tx),
               font=f_txt, fill=INK)


def draw_map(d, mx):
    """Dot-matrix world map with numbered pins, plus a legend."""
    map_y = 802
    d.line([(mx, map_y - 6), (PAGE_W - mx, map_y - 6)], fill=INK, width=2)
    d.text((mx, map_y), "WHERE IT HAPPENED",
           font=face(SANS_B, 13), fill=INK)
    map_x, map_w, map_h = mx, 620, 118
    map_top = map_y + 20
    cols, rows = 48, 20
    cw, ch = map_w / cols, map_h / rows
    land = [[False] * cols for _ in range(rows)]
    for c0, r0, c1, r1 in LAND_BOXES:
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                land[r][c] = True
    for r in range(rows):
        for c in range(cols):
            if land[r][c]:
                d.ellipse([map_x + c * cw + 1, map_top + r * ch + 1,
                           map_x + (c + 1) * cw - 1,
                           map_top + (r + 1) * ch - 1], fill=(90, 88, 80))
    f_pin = face(SANS_B, 9)
    for n, (lat, lon, _name) in enumerate(PINS, start=1):
        px = map_x + (lon + 180) / 7.5 * cw
        py = map_top + (78 - lat) / 6.75 * ch
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED,
                  outline=PAPER, width=1)
        d.text((px, py - 1), str(n), font=f_pin, fill=(255, 255, 255),
               anchor="mm")
    leg_x = map_x + map_w + 16
    f_leg = face(SANS_R, 12)
    for i, (_lat, _lon, name) in enumerate(PINS):
        lx = leg_x + (i // 6) * 190
        ly = map_top + 4 + (i % 6) * 20
        d.ellipse([lx, ly, lx + 14, ly + 14], fill=RED)
        d.text((lx + 7, ly + 6), str(i + 1), font=f_pin,
               fill=(255, 255, 255), anchor="mm")
        d.text((lx + 20, ly + 1), name, font=f_leg, fill=INK)


def draw_markets(d, mx):
    """Closing bar: Tuesday US closes and Wednesday Asia intraday."""
    bar_y = 946
    d.rectangle([mx, bar_y, PAGE_W - mx, bar_y + 52], fill=INK)
    d.text((mx + 10, bar_y + 6),
           "MARKETS \u2014 TUESDAY US CLOSES, WEDNESDAY ASIA INTRADAY",
           font=face(SANS_B, 12), fill=(255, 210, 90))
    f_mkt = face(SANS_R, 12)
    x = mx + 10
    y = bar_y + 26
    for item in MARKETS:
        d.text((x, y), item, font=f_mkt, fill=(240, 238, 230))
        x += d.textlength(item, font=f_mkt) + 18
    # Sparkline: KOSPI's slide across the week, top right of the bar.
    pts = [(0, 2), (18, 3), (36, 1), (54, 5), (72, 4), (90, 8), (108, 13)]
    sx, sy = PAGE_W - mx - 122, bar_y + 5
    d.line([(sx + px, sy + py) for px, py in pts],
           fill=(255, 120, 90), width=2)


def main():
    page, d, mx = build_page()
    draw_briefs(d, mx)
    draw_map(d, mx)
    draw_markets(d, mx)
    d.text((PAGE_W // 2, 1006),
           "Every story above happened or was first reported on "
           "Wednesday 25 November 2026.",
           font=face(SANS_R, 11), fill=GREY, anchor="ma")
    page.save(OUT, "PNG")
    print("wrote", OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
