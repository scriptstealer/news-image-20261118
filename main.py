"""Draw a one-page newspaper front page summing up Wednesday 18 November 2026.

The image is a broadsheet front page: a masthead, a red date band naming the
day, six story panels in a 2x3 grid (each with a small pictorial illustration,
a headline and a short sub-line), and a bottom strip with three more items.

Every story was verified against the day's reporting (OneTurn, Zark News,
Horizon, Daily Baku, FeedCast, Teh World News daily briefings for 18 Nov 2026):
  1. U.S. jets strike a Revolutionary Guard missile site on Qeshm Island;
     Iran answers with drones on Bahrain and Kuwait.
  2. Ukraine strikes the Kerch Bridge to Crimea for a second day; part of
     the road span falls into the strait.
  3. Xi Jinping and Vladimir Putin open the APEC summit in Shenzhen; a
     three-way meeting with Donald Trump is set for Thursday.
  4. Democrat Mary Peltola beats Dan Sullivan in Alaska; Democrats take a
     56-44 Senate majority, their largest since 2009.
  5. The Ebola outbreak in DR Congo passes 11,000 cases, the second-largest
     Ebola outbreak on record.
  6. Voyager 1 reaches one light-day from Earth, a distance no human-made
     object has crossed before (NASA JPL, 5:16 a.m. ET).
Bottom strip: U.S. loses measles elimination status after 26 years;
146,000 protest in France over living costs; Category 5 Cyclone Xavier
hits the Northern Cook Islands.

The drawing is fully procedural (PIL shapes and text only), no network, no
randomness, so two runs write byte-identical PNGs.
"""

import os

from PIL import Image, ImageDraw, ImageFont

PAGE_W = 1024
PAGE_H = 1024
PAPER = (248, 245, 238)
INK = (20, 20, 20)
MUTED = (58, 58, 58)
RED = (166, 25, 46)
PANEL_BORDER = (185, 178, 164)

# (headline, sub-line, band colour, illustration key)
STORIES = [
    (
        "U.S. HITS IRAN MISSILE SITE",
        "U.S. jets hit Qeshm Island; Iran fires drones at Bahrain and Kuwait",
        (123, 36, 28),
        "gulf",
    ),
    (
        "KERCH BRIDGE SPAN FALLS",
        "Ukraine strikes the Crimea link for a second day; part of the road span falls into the strait",
        (93, 109, 126),
        "bridge",
    ),
    (
        "XI, PUTIN, TRUMP TO MEET",
        "Leaders open the APEC summit in Shenzhen; a three-way meeting is set for Thursday",
        (30, 107, 92),
        "flags",
    ),
    (
        "PELTOLA FLIPS ALASKA",
        "Democrat beats Dan Sullivan; party takes a 56-44 majority, its largest since 2009",
        (46, 80, 144),
        "ballot",
    ),
    (
        "EBOLA PASSES 11,000 CASES",
        "Cases pass 11,000 in DR Congo; the second-largest Ebola outbreak on record",
        (108, 52, 131),
        "virus",
    ),
    (
        "VOYAGER 1: ONE LIGHT-DAY",
        "NASA probe crosses a distance no human-made object has reached before",
        (11, 21, 38),
        "voyager",
    ),
]

TICKER = "ALSO: U.S. loses measles-free status  ·  146,000 protest in France  ·  Cyclone Xavier hits Cook Islands"


def find_font(bold, serif):
    """Return a path to a DejaVu font, trying the usual locations."""
    base = "DejaVuSerif" if serif else "DejaVuSans"
    name = base + ("-Bold" if bold else "") + ".ttf"
    candidates = [
        os.path.join("/usr/share/fonts/truetype/dejavu", name),
        os.path.join("/usr/share/fonts/dejavu", name),
        os.path.join("/usr/local/share/fonts", name),
        name,
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def font(bold, serif, size):
    path = find_font(bold, serif)
    if path is not None:
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_width):
    """Split text into lines that fit max_width, by whole words."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def star_points(cx, cy, r_outer, r_inner, points=5, rotation=-90):
    """Points of a star polygon centred at (cx, cy)."""
    import math

    pts = []
    for i in range(points * 2):
        r = r_outer if i % 2 == 0 else r_inner
        angle = math.radians(rotation + i * 180.0 / points)
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return pts


def draw_gulf(draw, x, y, w, h):
    """Jet, explosion burst and Gulf waves."""
    cx = x + w // 2
    cy = y + h // 2
    # explosion starburst, left of centre
    bx, by = x + w // 4, cy + 12
    draw.polygon(star_points(bx, by, 52, 22, 8), fill=(255, 176, 32))
    draw.polygon(star_points(bx, by, 30, 13, 8), fill=(255, 92, 32))
    draw.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(255, 236, 170))
    # fighter jet in light grey, upper right, flying right: pointed nose,
    # fuselage, swept main wing, tail fin and canopy
    jx, jy = x + w - 190, y + 18
    draw.polygon([(jx, jy + 12), (jx + 150, jy + 12), (jx + 178, jy + 18),
                  (jx + 150, jy + 24), (jx, jy + 24)], fill=(214, 214, 214))
    draw.polygon([(jx + 52, jy + 12), (jx + 84, jy - 14), (jx + 108, jy + 12)],
                 fill=(214, 214, 214))
    draw.polygon([(jx + 58, jy + 24), (jx + 84, jy + 44), (jx + 112, jy + 24)],
                 fill=(214, 214, 214))
    draw.polygon([(jx + 8, jy + 12), (jx + 26, jy - 10), (jx + 44, jy + 12)],
                 fill=(214, 214, 214))
    draw.ellipse([jx + 96, jy + 8, jx + 124, jy + 14], fill=(120, 120, 120))
    # sea waves along the bottom
    for i, wy in enumerate((y + h - 26, y + h - 14)):
        for k in range(6):
            wx = x + 18 + k * 80
            draw.arc([wx, wy - 8, wx + 56, wy + 8], 180, 360,
                     fill=(214, 234, 248), width=4)


def draw_bridge(draw, x, y, w, h):
    """A bridge with its right span broken and fallen into the strait."""
    deck_y = y + 34
    # water
    draw.rectangle([x, y + h - 34, x + w, y + h], fill=(36, 84, 120))
    for k in range(5):
        wx = x + 20 + k * 92
        draw.arc([wx, y + h - 26, wx + 60, y + h - 10], 180, 360,
                 fill=(214, 234, 248), width=4)
    # left arch holding the deck
    draw.arc([x + 30, deck_y - 6, x + 190, deck_y + 74], 180, 360,
             fill=(226, 226, 226), width=10)
    # intact left deck
    draw.rectangle([x + 16, deck_y, x + 250, deck_y + 16], fill=(226, 226, 226))
    # support pillar on the left
    draw.rectangle([x + 96, deck_y + 16, x + 112, y + h - 34], fill=(200, 200, 200))
    # broken right deck, tilted down into the water
    draw.polygon([(x + 252, deck_y), (x + 452, deck_y + 66),
                  (x + 452, deck_y + 82), (x + 252, deck_y + 16)],
                 fill=(226, 226, 226))
    # burst at the break point
    bx, by = x + 252, deck_y + 8
    draw.polygon(star_points(bx, by, 26, 11, 8), fill=(255, 176, 32))
    draw.polygon(star_points(bx, by, 14, 6, 8), fill=(255, 92, 32))


def draw_flags(draw, x, y, w, h):
    """Three flags on poles: China, Russia, United States."""
    pole_y = y + 18
    pole_h = 66
    flags = [
        ("china", (206, 32, 41)),
        ("russia", None),
        ("usa", None),
    ]
    for i, (kind, colour) in enumerate(flags):
        fx = x + 52 + i * 152
        # pole
        draw.line([fx, pole_y, fx, pole_y + pole_h], fill=(240, 240, 240), width=4)
        fw, fh = 104, 52
        if kind == "china":
            draw.rectangle([fx, pole_y, fx + fw, pole_y + fh], fill=colour)
            draw.polygon(star_points(fx + 24, pole_y + 24, 13, 5, 5),
                         fill=(255, 222, 0))
        elif kind == "russia":
            draw.rectangle([fx, pole_y, fx + fw, pole_y + 17], fill=(255, 255, 255))
            draw.rectangle([fx, pole_y + 17, fx + fw, pole_y + 35],
                           fill=(0, 57, 166))
            draw.rectangle([fx, pole_y + 35, fx + fw, pole_y + 52],
                           fill=(213, 0, 50))
        else:
            for s in range(7):
                colour = (179, 25, 66) if s % 2 == 0 else (255, 255, 255)
                draw.rectangle([fx, pole_y + s * 7, fx + fw, pole_y + s * 7 + 7],
                               fill=colour)
            draw.rectangle([fx, pole_y, fx + 42, pole_y + 28], fill=(10, 49, 97))
            for sy in range(3):
                for sx in range(4):
                    draw.ellipse([fx + 5 + sx * 10, pole_y + 4 + sy * 9,
                                  fx + 9 + sx * 10, pole_y + 8 + sy * 9],
                                 fill=(255, 255, 255))


def draw_ballot(draw, x, y, w, h):
    """A ballot box with a slip going in and a big check mark."""
    bx, by = x + 62, y + 26
    # ballot slip sliding into the slot
    draw.polygon([(bx + 52, by - 6), (bx + 108, by - 6), (bx + 96, by + 34),
                  (bx + 40, by + 34)], fill=(255, 255, 255))
    draw.line([bx + 60, by + 10, bx + 96, by + 10], fill=(120, 120, 120), width=3)
    draw.line([bx + 58, by + 20, bx + 94, by + 20], fill=(120, 120, 120), width=3)
    # box
    draw.rectangle([bx, by + 34, bx + 148, by + 88], fill=(226, 226, 226))
    draw.rectangle([bx - 8, by + 26, bx + 156, by + 40], fill=(255, 255, 255))
    draw.rectangle([bx + 48, by + 31, bx + 100, by + 35], fill=(30, 30, 30))
    # big check mark, right side
    cx, cy = x + w - 128, y + 58
    draw.line([cx, cy + 6, cx + 34, cy + 38], fill=(46, 160, 67), width=16)
    draw.line([cx + 34, cy + 38, cx + 92, cy - 30], fill=(46, 160, 67), width=16)


def draw_virus(draw, x, y, w, h):
    """A spiky virus cell, centred."""
    import math

    cx, cy = x + w // 2, y + h // 2
    for i in range(12):
        angle = math.radians(i * 30)
        x1 = cx + 34 * math.cos(angle)
        y1 = cy + 34 * math.sin(angle)
        x2 = cx + 52 * math.cos(angle)
        y2 = cy + 52 * math.sin(angle)
        draw.line([x1, y1, x2, y2], fill=(255, 214, 102), width=5)
        draw.ellipse([x2 - 6, y2 - 6, x2 + 6, y2 + 6], fill=(255, 214, 102))
    draw.ellipse([cx - 36, cy - 36, cx + 36, cy + 36], fill=(255, 214, 102))
    draw.ellipse([cx - 22, cy - 14, cx - 8, cy + 0], fill=(108, 52, 131))
    draw.ellipse([cx + 6, cy + 6, cx + 20, cy + 20], fill=(108, 52, 131))
    draw.ellipse([cx - 2, cy - 26, cx + 12, cy - 12], fill=(108, 52, 131))


def draw_voyager(draw, x, y, w, h):
    """A spacecraft dish and body among stars, with a bright sun."""
    # stars at fixed positions
    stars = [(x + 40, y + 20), (x + 120, y + 14), (x + 220, y + 26),
             (x + 320, y + 16), (x + 430, y + 30), (x + 70, y + 88),
             (x + 180, y + 96), (x + 400, y + 84), (x + 460, y + 56),
             (x + 260, y + 12)]
    for sx, sy in stars:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    # sun, left
    sx, sy = x + 44, y + 58
    draw.polygon(star_points(sx, sy, 26, 11, 8), fill=(255, 214, 64))
    draw.ellipse([sx - 12, sy - 12, sx + 12, sy + 12], fill=(255, 236, 170))
    # spacecraft, centre-right and fully inside the band: a parabolic dish
    # (bowl opening up-left), a feed arm to a small feed, and a body
    dx, dy = x + 190, y + 30
    draw.pieslice([dx, dy, dx + 120, dy + 80], 0, 180, fill=(240, 240, 240))
    draw.line([dx + 60, dy + 40, dx + 60, dy + 8], fill=(240, 240, 240),
              width=5)
    draw.ellipse([dx + 52, dy, dx + 68, dy + 16], fill=(255, 214, 64))
    draw.line([dx + 96, dy + 62, dx + 150, dy + 84], fill=(240, 240, 240),
              width=6)
    draw.rectangle([dx + 146, dy + 72, dx + 196, dy + 96], fill=(200, 200, 200))
    draw.line([dx + 196, dy + 84, dx + 224, dy + 68], fill=(240, 240, 240),
              width=4)
    draw.ellipse([dx + 220, dy + 62, dx + 232, dy + 74], fill=(255, 214, 64))


ILLUSTRATIONS = {
    "gulf": draw_gulf,
    "bridge": draw_bridge,
    "flags": draw_flags,
    "ballot": draw_ballot,
    "virus": draw_virus,
    "voyager": draw_voyager,
}


def draw_panel(draw, px, py, pw, ph, headline, sub, band_colour, key):
    """One story panel: coloured illustration band, headline, sub-line."""
    draw.rectangle([px, py, px + pw, py + ph], fill=(255, 255, 255),
                   outline=PANEL_BORDER, width=2)
    band_h = 116
    draw.rectangle([px + 2, py + 2, px + pw - 2, py + band_h], fill=band_colour)
    ILLUSTRATIONS[key](draw, px + 2, py + 2, pw - 4, band_h - 2)
    pad = 18
    inner_w = pw - pad * 2
    head_fnt = font(True, False, 26)
    sub_fnt = font(False, False, 18)
    head_lines = wrap(draw, headline, head_fnt, inner_w)
    ty = py + band_h + 14
    for line in head_lines[:2]:
        draw.text((px + pad, ty), line, font=head_fnt, fill=INK)
        ty += 34
    ty += 4
    for line in wrap(draw, sub, sub_fnt, inner_w)[:2]:
        draw.text((px + pad, ty), line, font=sub_fnt, fill=MUTED)
        ty += 24


def build_page():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(img)
    # masthead
    title_fnt = font(True, True, 62)
    title = "THE WORLD TODAY"
    tw = draw.textlength(title, font=title_fnt)
    draw.text(((PAGE_W - tw) / 2, 10), title, font=title_fnt, fill=INK)
    draw.line([16, 80, PAGE_W - 16, 80], fill=INK, width=3)
    # date band
    draw.rectangle([16, 88, PAGE_W - 16, 126], fill=RED)
    date_fnt = font(True, False, 30)
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    dw = draw.textlength(date, font=date_fnt)
    draw.text(((PAGE_W - dw) / 2, 92), date, font=date_fnt, fill=(255, 255, 255))
    # story grid: 2 columns x 3 rows
    margin = 16
    gutter_x = 16
    gutter_y = 12
    panel_w = (PAGE_W - margin * 2 - gutter_x) // 2
    panel_h = 262
    top = 138
    for i, (headline, sub, colour, key) in enumerate(STORIES):
        col = i % 2
        row = i // 2
        px = margin + col * (panel_w + gutter_x)
        py = top + row * (panel_h + gutter_y)
        draw_panel(draw, px, py, panel_w, panel_h, headline, sub, colour, key)
    # bottom ticker strip
    strip_y = 960
    draw.rectangle([16, strip_y, PAGE_W - 16, strip_y + 48], fill=(31, 41, 55))
    tick_fnt = font(False, False, 17)
    tw = draw.textlength(TICKER, font=tick_fnt)
    draw.text(((PAGE_W - tw) / 2, strip_y + 14), TICKER, font=tick_fnt,
              fill=(255, 255, 255))
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    page = build_page()
    page.save(os.path.join(out_dir, "entry.png"), format="PNG")


if __name__ == "__main__":
    main()
