# Builds teleiose.html out of teleiose.src.html.
#
# Two things are filled in here rather than typed into the page:
#   1. __FONT__ — Manrope, base64. The page must show the typeface that ships
#      inside the application (D-072); a system font looks nothing like the
#      product, and this page is judged on how a tile reads across a stand.
#   2. __PICS__ — the twenty product pictures the mock grid draws, base64, as a
#      JSON map from picture id to a data URI. They are the real files: the
#      question the page asks is whether a photograph that has been greyed and
#      faded still reads as "sold out" at a glance, and a grey square cannot
#      answer it.
#
# The pictures are re-encoded at 128 px — twice the 64 the tile draws them at,
# so a high-density screen still has pixels to spend. The originals total 2.8 MB
# and would make a 4 MB page for no visible gain; what is being judged here is
# the treatment over the photograph, not the photograph.
#
# Run from this folder, with the private repo beside this one:
#   python build-teleiose.py

import base64
import io
import json
import pathlib

from PIL import Image

HERE = pathlib.Path(__file__).parent
APP = HERE.parents[1] / 'OpaProject' / 'app'

# The same twenty, in the same order, as the grid in teleiose.src.html.
PICTURES = [
    'meat_souvlaki_xoirino',
    'meat_souvlaki_kotopoulo',
    'meat_brizola_xoirini',
    'meat_loukaniko_xoriatiko',
    'meat_merida_gyro_xoirino',
    'meat_kotopoulo_miso',
    'meat_souvlaki_proveio',
    'meat_kebap_xoirino_merida',
    'sides_patates_tiganites',
    'sides_tzatziki',
    'sides_xoriatiki_salata',
    'sides_patatosalata',
    'sides_psomi',
    'soft_nero_500ml',
    'soft_coca_cola_330ml_koutaki',
    'soft_anthrakoyxo_nero_330ml',
    'beer_alfa_500ml_gyalini',
    'beer_amstel_330ml_gyalini',
    'wine_krasi_kokkino_xyma_250ml',
    'sweets_pagoto',
]

SIDE = 128


def data_uri(path: pathlib.Path, mime: str) -> str:
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()


def picture_uri(path: pathlib.Path) -> str:
    with Image.open(path) as img:
        img = img.convert('RGBA')
        img.thumbnail((SIDE, SIDE), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format='WEBP', quality=88, method=6)
    return 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode()


def main() -> None:
    page = (HERE / 'teleiose.src.html').read_text(encoding='utf-8')

    font = data_uri(APP / 'assets' / 'fonts' / 'Manrope.ttf', 'font/ttf')
    pics = {
        name: picture_uri(APP / 'assets' / 'library' / f'{name}.webp')
        for name in PICTURES
    }

    page = page.replace('__FONT__', font).replace('__PICS__', json.dumps(pics))
    if '__FONT__' in page or '__PICS__' in page:
        raise SystemExit('a placeholder was left behind')

    out = HERE / 'teleiose.html'
    out.write_text(page, encoding='utf-8')
    print(f'{out.name}: {out.stat().st_size // 1024} KB, {len(pics)} pictures')


if __name__ == '__main__':
    main()
