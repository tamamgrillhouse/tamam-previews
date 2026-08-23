# Builds eidika.html out of eidika.src.html.
#
# Two things are filled in here rather than typed into the page:
#   1. __FONT__  — Manrope, base64. The page must show the typeface that ships
#      inside the application; a borrowed system font looks impressive on his
#      screen and nothing like the product (DEAD-ENDS.md §9).
#   2. __A1__ … __D3__ — the twelve proposal drawings. Each appears four times
#      in the page (large on white, large on dark, 36px, 36px on dark), so they
#      live here once instead of forty-eight times there.
#
# Every curve is SAMPLED INTO A POLYGON in Python rather than written as an SVG
# arc: the notch of a ticket and the scalloped rim of a coupon are the two
# shapes where an arc's sweep flag is easy to get backwards, and the mistake is
# invisible until the page is open.
#
# SECOND SET. The first four proposals were all "draw the paper" — the word on
# it, it torn, it moving, it on a badge — and the owner refused every one of
# them: «σου είπα σκέψου κάτι καινούργιο». These four start from what a person
# at a πανηγύρι already knows, not from the object in the hand.
#
#     python build-eidika.py
import base64
import math
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
FONT = pathlib.Path(r"c:\Users\SixBillion\Documents\OpaProject\brand\font\Manrope.ttf")

AMBER, AMBER_D = "#df8324", "#a95d0c"
GREEN, GREEN_D = "#2f7d4f", "#1c5433"
RED, RED_D = "#c03a2f", "#8a2119"
CREAM = "#fbf6ec"
PAPER, PAPER_S = "#f7f1e0", "#e3d8bd"       # printed paper, and its shaded side
DARKINK = "#2a2622"


def poly(points, fill, extra=""):
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polygon points="{pts}" fill="{fill}" {extra}/>'


def arc(cx, cy, r, a0, a1, n=18):
    return [(cx + r * math.cos(a), cy + r * math.sin(a))
            for a in (a0 + (a1 - a0) * i / n for i in range(n + 1))]


def card(x0, y0, x1, y1, r=6, notch=None, nr=7.5):
    """Rounded rectangle, optionally bitten by a semicircular notch top and
    bottom at x = notch — the outline that says 'ticket' with no word at all."""
    p = arc(x0 + r, y0 + r, r, math.pi, 1.5 * math.pi, 8)
    if notch:
        p.append((notch - nr, y0))
        p += arc(notch, y0, nr, math.pi, 0, 16)
        p.append((notch + nr, y0))
    p += arc(x1 - r, y0 + r, r, 1.5 * math.pi, 2 * math.pi, 8)
    p += arc(x1 - r, y1 - r, r, 0, 0.5 * math.pi, 8)
    if notch:
        p.append((notch + nr, y1))
        p += arc(notch, y1, nr, 0, -math.pi, 16)
        p.append((notch - nr, y1))
    p += arc(x0 + r, y1 - r, r, 0.5 * math.pi, math.pi, 8)
    return p


def scalloped(x0, y0, x1, y1, n=10):
    w, h = x1 - x0, y1 - y0
    px, py = w / n, h / n
    r = min(px, py) * 0.5
    p = []
    for i in range(n):
        p += arc(x0 + px * (i + 0.5), y0, r, math.pi, 0, 7)
    for i in range(n):
        p += arc(x1, y0 + py * (i + 0.5), r, -0.5 * math.pi, 0.5 * math.pi, 7)
    for i in range(n):
        p += arc(x1 - px * (i + 0.5), y1, r, 0, -math.pi, 7)
    for i in range(n):
        p += arc(x0, y1 - py * (i + 0.5), r, 0.5 * math.pi, 1.5 * math.pi, 7)
    return p


def text(s, x, y, size, fill=CREAM, track=0.06, angle=0, weight=800):
    t = (f'<text x="{x}" y="{y}" font-family="Manrope" font-weight="{weight}" '
         f'font-size="{size}" fill="{fill}" letter-spacing="{size * track:.2f}" '
         f'text-anchor="middle" dominant-baseline="central"')
    if angle:
        t += f' transform="rotate({angle} {x} {y})"'
    return t + f'>{s}</text>'


def dots(x, y0, y1, step, r, fill):
    out, y = [], y0
    while y <= y1:
        out.append(f'<circle cx="{x}" cy="{y:.1f}" r="{r}" fill="{fill}"/>')
        y += step
    return "".join(out)


def svg(body, defs=""):
    d = f"<defs>{defs}</defs>" if defs else ""
    return f'<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">{d}{body}</svg>'


# The paper of Ν1: a warm sheet lit from the upper left, exactly the light the
# 33 food pictures are rendered under, so the tile belongs beside them.
PAPERGRAD = (f'<linearGradient id="pg" x1="0" y1="0" x2="0.6" y2="1">'
             f'<stop offset="0" stop-color="#fffdf6"/><stop offset="0.55" stop-color="{PAPER}"/>'
             f'<stop offset="1" stop-color="{PAPER_S}"/></linearGradient>'
             f'<linearGradient id="fold" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0" stop-color="#000" stop-opacity="0.16"/>'
             f'<stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>')


# ------------------------------------------------ Ν1  the real paper, our ink
def a1():
    b = '<g transform="rotate(-7 60 60)">'
    b += poly(card(6, 30, 114, 90, 5, notch=86, nr=7), "url(#pg)")
    b += f'<rect x="86" y="30" width="6" height="60" fill="url(#fold)"/>'
    b += dots(86, 39, 81, 7, 1.5, "#ffffff")
    b += (f'<rect x="12" y="36" width="66" height="48" fill="none" stroke="{AMBER}" '
          f'stroke-width="1.6"/>')
    b += (f'<rect x="14.5" y="38.5" width="61" height="43" fill="none" stroke="{AMBER}" '
          f'stroke-width="0.8"/>')
    b += text("ΕΙΣΙΤΗΡΙΟ", 45, 55, 10.5, AMBER)
    b += f'<line x1="20" y1="64" x2="70" y2="64" stroke="{AMBER}" stroke-width="0.9"/>'
    b += text("ΠΑΝΗΓΥΡΙ", 45, 72, 6, AMBER_D, track=0.22)
    b += text("247", 103, 60, 13, AMBER_D, angle=-90)
    return svg(b + "</g>", PAPERGRAD)


def a2():
    b = '<g transform="rotate(-4 60 60)">'
    b += poly(scalloped(12, 22, 108, 98), "url(#pg)")
    b += (f'<line x1="20" y1="40" x2="100" y2="40" stroke="{GREEN}" stroke-width="1.4" '
          f'stroke-dasharray="4 3.5"/>')
    b += text("ΚΟΥΠΟΝΙ", 60, 62, 13, GREEN)
    b += f'<line x1="30" y1="74" x2="90" y2="74" stroke="{GREEN}" stroke-width="1"/>'
    b += text("ΓΙΑ ΜΙΑ ΜΕΡΙΔΑ", 60, 84, 6, GREEN_D, track=0.16)
    return svg(b + "</g>", PAPERGRAD)


def a3():
    # a strip torn off the roll, curling: the shape a λαχνός actually has
    b = '<g transform="rotate(6 60 60)">'
    b += poly(card(10, 26, 110, 94, 4), "url(#pg)")
    b += f'<rect x="10" y="26" width="100" height="7" fill="url(#fold)"/>'
    b += dots(0, 0, -1, 1, 0, RED)
    for y in (34, 86):
        b += (f'<line x1="14" y1="{y}" x2="106" y2="{y}" stroke="{RED}" stroke-width="1.2" '
              f'stroke-dasharray="3 3"/>')
    b += text("ΛΑΧΝΟΣ", 60, 52, 13, RED)
    b += text("ΛΑΧΕΙΟΦΟΡΟΥ", 60, 64, 6, RED_D, track=0.2)
    b += (f'<circle cx="60" cy="76" r="7.5" fill="none" stroke="{RED}" stroke-width="1.4"/>'
          + text("7", 60, 76.5, 9, RED_D, track=0))
    return svg(b + "</g>", PAPERGRAD)


# ---------------------------------------------------- Ν2  the number is the thing
def b1():
    b = poly(card(4, 20, 116, 100, 9, notch=None), AMBER)
    b += f'<circle cx="4" cy="60" r="9" fill="#ffffff" fill-opacity="0"/>'
    b += text("247", 60, 56, 44, CREAM, track=0.02)
    b += text("ΕΙΣΙΤΗΡΙΟ", 60, 87, 11, "#ffffff", track=0.14)
    return svg(b)


def b2():
    b = poly(card(4, 20, 116, 100, 9), GREEN)
    b += f'<circle cx="60" cy="55" r="26" fill="none" stroke="{CREAM}" stroke-width="3.5"/>'
    b += text("1", 60, 56, 38, CREAM, track=0)
    b += text("ΚΟΥΠΟΝΙ", 60, 87, 11, "#ffffff", track=0.14)
    return svg(b)


def b3():
    b = poly(card(4, 20, 116, 100, 9), RED)
    b += text("N°7", 60, 56, 36, CREAM, track=0.02)
    b += text("ΛΑΧΝΟΣ", 60, 87, 11, "#ffffff", track=0.14)
    return svg(b)


# -------------------------------------------- Ν3  what you buy, not what you get
def c1():
    # the gate of the πανηγύρι, with bunting: an entrance, not a piece of paper
    b = (f'<path d="M18 108 V56 a42 42 0 0 1 84 0 V108" fill="none" stroke="{AMBER}" '
         f'stroke-width="11" stroke-linecap="round"/>')
    b += (f'<path d="M18 108 V56 a42 42 0 0 1 84 0 V108" fill="none" stroke="{AMBER_D}" '
          f'stroke-width="3" stroke-linecap="round" stroke-dasharray="1 12"/>')
    for i, (x, y) in enumerate(((30, 44), (45, 32), (60, 28), (75, 32), (90, 44))):
        c = (RED, CREAM, GREEN, CREAM, RED)[i]
        b += poly([(x - 7, y - 8), (x + 7, y - 8), (x, y + 6)], c,
                  f'stroke="{AMBER_D}" stroke-width="0.8"')
    b += f'<rect x="46" y="70" width="28" height="38" rx="3" fill="{AMBER_D}"/>'
    b += text("ΕΙΣΟΔΟΣ", 60, 89, 7, CREAM, track=0.1, angle=-90)
    return svg(b)


def c2():
    # a plate and a glass with the coupon leaning on them: what the coupon buys
    b = f'<ellipse cx="52" cy="84" rx="42" ry="11" fill="{GREEN_D}"/>'
    b += f'<path d="M10 84 a42 26 0 0 1 84 0 z" fill="{GREEN}"/>'
    b += f'<ellipse cx="52" cy="58" rx="26" ry="8" fill="{GREEN_D}" opacity="0.55"/>'
    b += f'<path d="M84 40 h26 l-4 34 h-18 z" fill="{GREEN}"/>'
    b += f'<path d="M85 46 h24 l-1 9 h-22 z" fill="{CREAM}" opacity="0.85"/>'
    b += '<g transform="rotate(-12 34 46)">'
    b += poly(scalloped(10, 26, 58, 62, 6), CREAM)
    b += text("ΚΟΥΠΟΝΙ", 34, 44, 7.5, GREEN_D, track=0.08)
    b += '</g>'
    return svg(b)


def c3():
    # the prize and the drum: a λαχνός is a chance at something, never a paper
    b = f'<rect x="16" y="52" width="56" height="46" rx="4" fill="{RED}"/>'
    b += f'<rect x="12" y="42" width="64" height="14" rx="4" fill="{RED_D}"/>'
    b += f'<rect x="38" y="42" width="12" height="56" fill="{CREAM}"/>'
    b += (f'<path d="M44 42 c-14 -4 -18 -18 -6 -18 c8 0 10 10 6 18 z" fill="{CREAM}"/>'
          f'<path d="M44 42 c14 -4 18 -18 6 -18 c-8 0 -10 10 -6 18 z" fill="{CREAM}"/>')
    b += f'<circle cx="92" cy="76" r="24" fill="{RED_D}"/>'
    b += f'<circle cx="92" cy="76" r="15" fill="{CREAM}"/>'
    b += text("7", 92, 77, 17, RED_D, track=0)
    return svg(b)


# ------------------------------------------------------- Ν4  the association's stamp
def stamp(colour, dark, word, glyph, seed):
    """A round rubber stamp: outer ring, inner ring, the word across the middle.
    The ink is pressed unevenly — a few gaps in the rings — which is what keeps
    it from reading as a flat program icon."""
    b = f'<g transform="rotate({seed} 60 60)">'
    b += (f'<circle cx="60" cy="60" r="54" fill="none" stroke="{colour}" stroke-width="7" '
          f'stroke-dasharray="150 6 90 5 60 4" opacity="0.92"/>')
    b += (f'<circle cx="60" cy="60" r="43" fill="none" stroke="{colour}" stroke-width="2.6" '
          f'stroke-dasharray="120 5 70 4"/>')
    b += f'<rect x="17" y="47" width="86" height="26" fill="{colour}" rx="2"/>'
    b += text(word, 60, 60.5, 13.5, CREAM, track=0.05)
    b += glyph
    b += (f'<circle cx="60" cy="60" r="54" fill="none" stroke="#ffffff" stroke-width="2" '
          f'stroke-dasharray="2 26" opacity="0.55"/>')
    return svg(b + "</g>")


def d1():
    g = (f'<g fill="{AMBER}"><circle cx="60" cy="33" r="4"/>'
         f'<circle cx="46" cy="36" r="2.6"/><circle cx="74" cy="36" r="2.6"/></g>')
    g += poly(card(40, 78, 80, 94, 3, notch=70, nr=4), AMBER)
    return stamp(AMBER, AMBER_D, "ΕΙΣΙΤΗΡΙΟ", g, -6)


def d2():
    g = poly(scalloped(44, 24, 76, 44, 5), GREEN)
    g += (f'<g stroke="{GREEN}" stroke-width="3" fill="none" stroke-linecap="round">'
          f'<line x1="50" y1="80" x2="70" y2="94"/><line x1="70" y1="80" x2="50" y2="94"/>'
          f'<circle cx="48" cy="96" r="3"/><circle cx="72" cy="96" r="3"/></g>')
    return stamp(GREEN, GREEN_D, "ΚΟΥΠΟΝΙ", g, 5)


def d3():
    g = f'<circle cx="60" cy="34" r="11" fill="none" stroke="{RED}" stroke-width="3"/>'
    g += text("7", 60, 34.5, 11, RED, track=0)
    g += (f'<path d="M46 92 L60 78 L74 92" fill="none" stroke="{RED}" stroke-width="3.4" '
          f'stroke-linecap="round"/>')
    return stamp(RED, RED_D, "ΛΑΧΝΟΣ", g, -4)


TILES = {"A1": a1, "A2": a2, "A3": a3, "B1": b1, "B2": b2, "B3": b3,
         "C1": c1, "C2": c2, "C3": c3, "D1": d1, "D2": d2, "D3": d3}


def main():
    page = (HERE / "eidika.src.html").read_text(encoding="utf-8")
    page = page.replace("__FONT__", base64.b64encode(FONT.read_bytes()).decode())
    for key, fn in TILES.items():
        page = page.replace(f"__{key}__", fn())
    out = HERE / "eidika.html"
    out.write_text(page, encoding="utf-8")
    left = [k for k in TILES if f"__{k}__" in page]
    print(f"wrote {out} ({len(page) // 1024} KB)" + (f" — LEFT OVER {left}" if left else ""))


if __name__ == "__main__":
    main()
