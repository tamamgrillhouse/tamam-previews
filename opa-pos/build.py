# Builds the generated previews from their sources.
# Edit the .src.html files, never the generated ones.
#     python build.py
#
#   sima.src.html            -> sima.html            (font only)
#   othoni-enarxis.src.html  -> othoni-enarxis.html  (font + the full lock-up,
#                                                     every letter its own path)
#
# The lock-up is NOT drawn here. It is read out of brand/tools/brand_geom.py,
# which is the one source of the shape (D-078). This file only breaks it into
# pieces an animation can move one at a time.
import base64
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
BRAND = pathlib.Path(r"c:/Users/SixBillion/Documents/OpaProject/brand")
FONT = BRAND / "font" / "Manrope.ttf"

sys.path.insert(0, str(BRAND / "tools"))
import brand_geom as G  # noqa: E402

INK = G.INK          # the ring and ΟΠΑ
GREEN = G.GREEN      # the exclamation and the pill
WHITE = G.WHITE      # POS on the pill
MUTED = G.MUTED      # the tagline
NIB = "#7BE8AC"      # the pen's head, launch screen only


def _glyphs(text, size, x, baseline, tracking, cls, fill):
    """One <path> per letter, already placed.

    `pathLength="100"` is what lets a stylesheet trace a letter with a dash
    without knowing how long its outline is — the numbers become percentages.
    """
    out = []
    cursor = x
    for i, ch in enumerate(text):
        d, _ = G.text_outline(ch, size, cursor, baseline, 0.0, "start")
        out.append(f'<path class="{cls} {cls}{i}" pathLength="100" d="{d}" '
                   f'fill="{fill}"/>')
        cursor += G.advance(ch) * size / G._upm + tracking
    return "".join(out)


def _pos_glyphs(h):
    """POS, one path per letter, centred in the pill exactly as brand_geom does."""
    total = G.text_width(G.PILL, h["pill_size"], h["pill_track"])
    return _glyphs(G.PILL, h["pill_size"], h["pill_cx"] - total / 2,
                   h["pill_baseline"], h["pill_track"], "pg", WHITE)


def lockup():
    """The horizontal lock-up as animatable parts.

    Every piece carries a class and nothing carries an inline animation: the
    default state is the finished logo, and the CSS in the page takes it apart.

    **A group that has to move is wrapped rather than styled.** In SVG the
    `transform` attribute and the CSS `transform` property are one property, so
    an animation on `.mark` would throw away the placement written into it. The
    wrapper `.markmove` exists to be animated; `.mark` holds the geometry.
    """
    h = G.horizontal(tagline=True)
    s = h["mark_h"] / G.MARK_BOX[3]

    # --- the mark, inside its own 100-unit space -----------------------------
    mark = (
        f'<g class="markmove"><g class="mark" '
        f'transform="translate({h["mark_x"]:.4f} '
        f'{h["mark_y"]:.4f}) scale({s:.6f}) '
        f'translate({-G.MARK_BOX[0]} {-G.MARK_BOX[1]})">'
        # The ring is wrapped for the same reason the mark is: it already
        # carries a rotate, so anything that spins it has to spin the wrapper.
        f'<g class="ringmove">'
        # pathLength 100 so the dash numbers below are percentages, not lengths
        f'<circle class="ring" cx="{G.RING_CX}" cy="{G.RING_CY}" '
        f'r="{G.RING_R}" pathLength="100" fill="none" stroke="{INK}" '
        f'stroke-width="{G.RING_SW}" stroke-linecap="round" '
        f'stroke-dasharray="{100 - 100 * G.RING_GAP_DEG / 360:.2f} 100" '
        f'transform="rotate({G.RING_ROT} {G.RING_CX} {G.RING_CY})"/>'
        f'<circle class="nib" cx="{G.RING_CX}" cy="{G.RING_CY}" '
        f'r="{G.RING_R}" pathLength="100" fill="none" stroke="{NIB}" '
        f'stroke-width="{G.RING_SW}" stroke-linecap="round" '
        f'stroke-dasharray="0 100" opacity="0" '
        f'transform="rotate({G.RING_ROT} {G.RING_CX} {G.RING_CY})"/>'
        f'</g>'
        f'<rect class="mbar" x="{G.BANG_X}" y="{G.BANG_TOP}" '
        f'width="{G.BANG_W}" height="{G.BANG_BAR_H}" rx="{G.BANG_W / 2}" '
        f'fill="{GREEN}"/>'
        f'<circle class="mdot" cx="{G.BANG_X + G.BANG_W / 2}" '
        f'cy="{G.BANG_DOT_CY}" r="{G.BANG_DOT_R}" fill="{GREEN}"/>'
        f'</g></g>'
    )

    # --- ΟΠΑ -----------------------------------------------------------------
    word = _glyphs(G.WORD, h["word_size"], h["word_x"], h["baseline"],
                   h["word_track"], "wg", INK)

    # --- the word's own exclamation, split so the dot can land after the bar --
    bw, bar_h, r = G.bang_parts()
    bs = h["cap"] / G.BANG_TOTAL
    bang = (
        f'<rect class="wbar" x="{h["bang_x"]:.3f}" '
        f'y="{h["baseline"] - h["cap"]:.3f}" width="{bw * bs:.3f}" '
        f'height="{bar_h * bs:.3f}" rx="{bw * bs / 2:.3f}" fill="{GREEN}"/>'
        f'<circle class="wdot" cx="{h["bang_x"] + bw * bs / 2:.3f}" '
        f'cy="{h["baseline"] - r * bs:.3f}" r="{r * bs:.3f}" fill="{GREEN}"/>'
    )

    # --- the POS pill --------------------------------------------------------
    pill = (
        f'<g class="pill">'
        f'<rect class="pillbox" x="{h["pill_x"]:.3f}" y="{h["pill_y"]:.3f}" '
        f'width="{h["pill_w"]}" height="{h["pill_h"]}" rx="{h["pill_r"]}" '
        f'fill="{GREEN}"/>'
        f'{_pos_glyphs(h)}</g>'
    )

    # --- ΤΑΜΕΙΟ ΕΚΔΗΛΩΣΕΩΝ ---------------------------------------------------
    tag = (
        f'<text class="tag" x="{h["tag_x"]:.3f}" y="{h["tag_baseline"]:.3f}" '
        f'font-family="Manrope" font-size="{h["tag_size"]}" font-weight="700" '
        f'fill="{MUTED}" letter-spacing="{h["tag_track"]}">{G.TAG}</text>'
    )

    vb = " ".join(f"{v:.4f}" for v in h["viewbox"])
    inner = mark + f'<g class="word">{word}{bang}</g>' + pill + tag

    # --- where the mark's centre sits inside the lock-up ----------------------
    # An animation that lifts the mark to the middle of the screen needs this
    # and nothing else. Written as fractions of the box so the page never
    # carries a coordinate of its own — a banner placed by hand-written numbers
    # is exactly the fault the brand check was written to catch.
    x0, y0, w0, h0 = h["viewbox"]
    ox = (h["mark_x"] + G.mark_width(h["mark_h"]) / 2 - x0) / w0
    oy = (h["mark_y"] + h["mark_h"] / 2 - y0) / h0
    dash = 100 - 100 * G.RING_GAP_DEG / 360
    css_vars = (
        f"  /* generated by build.py from brand_geom.py - do not edit */\n"
        f"  --m-ox:{ox * 100:.3f}%;   /* the mark's centre inside the lock-up */\n"
        f"  --m-oy:{oy * 100:.3f}%;\n"
        f"  --m-dx:{(0.5 - ox) * 100:.3f}%;  /* ... to the middle of the box */\n"
        f"  --m-dy:{(0.5 - oy) * 100:.3f}%;\n"
        # In px, not bare numbers: inside an SVG one px is one user unit, and
        # stroke-dashoffset in a CSS custom property wants a length.
        f"  --ring-dash:{dash:.2f}px;   /* how much of the circle the O is */\n"
        f"  --ring-dash-neg:{-dash:.2f}px;"
    )
    return vb, inner, css_vars, h


# =============================================================================
# THE CHECK
# =============================================================================
# The lock-up was once generated correctly and then **deformed by the page's own
# stylesheet**: `transform-box: fill-box` landed on the ring, which already
# carries a `rotate(-155 36 50)`, so the rotation centre moved to the corner of
# the shape and the ring fell 53 units out of the mark. Nothing in the markup was
# wrong, so reading the markup would never have found it.
#
# So the check renders the built page's own logo — stylesheet and all — and
# subtracts it from brand/svg/logo-horizontal-dark.svg. It fails the build.
CHROME = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
OFFICIAL = BRAND / "svg" / "logo-horizontal-dark.svg"
CHECK_W, CHECK_H = 1052, 256


def _shoot(html, out):
    import subprocess
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False,
                                     encoding="utf-8") as f:
        f.write(html)
        tmp = f.name
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--screenshot={out}", f"--window-size={CHECK_W},{CHECK_H}",
                    "--virtual-time-budget=4000",
                    pathlib.Path(tmp).as_uri()],
                   check=True, capture_output=True, timeout=180)
    pathlib.Path(tmp).unlink(missing_ok=True)


def _ink_box(img):
    px = img.load()
    box = [10 ** 9, 10 ** 9, -1, -1]
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = px[x, y]
            if abs(r - 18) + abs(g - 17) + abs(b - 16) < 24:
                continue
            box[0], box[1] = min(box[0], x), min(box[1], y)
            box[2], box[3] = max(box[2], x), max(box[3], y)
    return box


def check():
    import re
    import tempfile
    from PIL import Image, ImageChops

    page = (HERE / "othoni-enarxis.html").read_text(encoding="utf-8")
    style = re.search(r"<style>(.*?)</style>", page, re.S).group(1)
    svg = re.search(r'(<svg viewBox="[^"]+">.*?</svg>)', page, re.S).group(1)

    tmpdir = pathlib.Path(tempfile.mkdtemp())
    frame = ("<!doctype html><meta charset=utf-8><style>html,body{margin:0;"
             "padding:0;overflow:hidden;background:#121110}</style>")

    official = OFFICIAL.read_text(encoding="utf-8")
    official = (official.replace('width="526"', f'width="{CHECK_W}"')
                        .replace('height="128"', f'height="{CHECK_H}"'))
    _shoot(frame + official, tmpdir / "a.png")

    # the page's own logo, under the page's own stylesheet
    _shoot(f"<!doctype html><meta charset=utf-8><style>{style}"
           "html,body{margin:0;padding:0;overflow:hidden;background:#121110}"
           f".screen{{position:fixed;inset:0;width:{CHECK_W}px;height:{CHECK_H}px}}"
           "</style>"
           f'<div class="screen"><div class="splash">'
           f'<div class="logo hero" style="width:100%">{svg}</div></div></div>',
           tmpdir / "b.png")

    a = Image.open(tmpdir / "a.png").convert("RGB")
    b = Image.open(tmpdir / "b.png").convert("RGB")
    ba, bb = _ink_box(a), _ink_box(b)
    ra = (ba[2] - ba[0]) / (ba[3] - ba[1])
    rb = (bb[2] - bb[0]) / (bb[3] - bb[1])
    hist = ImageChops.difference(a, b).convert("L").histogram()
    bad = sum(hist[24:]) / (CHECK_W * CHECK_H)

    print(f"  check: shape {ra:.3f} vs {rb:.3f}   pixels differing {bad * 100:.2f}%")
    if abs(ra - rb) / ra > 0.02:
        raise SystemExit(f"FAIL: the logo in the page is the wrong shape "
                         f"({rb:.3f} against {ra:.3f} in {OFFICIAL.name}). "
                         f"Something in the stylesheet is deforming it.")
    if bad > 0.04:
        raise SystemExit(f"FAIL: {bad * 100:.1f}% of the logo disagrees with "
                         f"{OFFICIAL.name}.")


def main():
    font_b64 = base64.b64encode(FONT.read_bytes()).decode()

    src = (HERE / "sima.src.html").read_text(encoding="utf-8")
    assert "__FONT_B64__" in src, "the font placeholder is gone from sima.src.html"
    out = HERE / "sima.html"
    out.write_text(src.replace("__FONT_B64__", font_b64), encoding="utf-8")
    print(f"sima.html            {out.stat().st_size // 1024} KB")

    vb, inner, css_vars, h = lockup()
    src = (HERE / "othoni-enarxis.src.html").read_text(encoding="utf-8")
    for token in ("__FONT_B64__", "__VIEWBOX__", "__LOCKUP__", "__VARS__"):
        assert token in src, f"{token} is gone from othoni-enarxis.src.html"
    page = (src.replace("__VIEWBOX__", vb)
               .replace("__VARS__", css_vars)
               .replace("__LOCKUP__", inner)
               .replace("__FONT_B64__", font_b64))
    out = HERE / "othoni-enarxis.html"
    out.write_text(page, encoding="utf-8")
    print(f"othoni-enarxis.html  {out.stat().st_size // 1024} KB")
    print(f"  viewBox {vb}   ratio {h['viewbox'][2] / h['viewbox'][3]:.3f}")
    check()
    print("  all checks passed")


if __name__ == "__main__":
    main()
