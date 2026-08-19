# Builds vivliothiki-eikones.html out of vivliothiki-eikones.src.html.
#
# Two things are filled in here rather than typed into the page:
#   1. __FONT__ — Manrope, base64. The page must show the typeface that ships
#      inside the application (D-072); a system font looks nothing like the
#      product.
#   2. __PICS__ — ten real product pictures out of app/assets/library/, base64,
#      as a JSON map from picture id to a data URI. They are the real files,
#      not stand-ins: the whole question the page asks is whether a photograph
#      of a bottle can be told apart at 40 pixels, and a grey square cannot
#      answer it.
#
# Run from this folder, with the private repo beside this one:
#   python build-vivliothiki.py

import base64
import json
import pathlib

HERE = pathlib.Path(__file__).parent
APP = HERE.parents[1] / 'OpaProject' / 'app'

PICTURES = [
    'meat_souvlaki_xoirino',
    'meat_souvlaki_kotopoulo',
    'meat_souvlaki_proveio',
    'meat_merida_gyro_xoirino',
    'meat_kebap_xoirino_merida',
    'beer_alfa_330ml_gyalini',
    'beer_alfa_500ml_koutaki',
    'beer_amstel_330ml_koutaki',
    'beer_byra_vareli_500ml',
    'beer_corona_330ml_gyalini',
]


def data_uri(path: pathlib.Path, mime: str) -> str:
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()


def main() -> None:
    page = (HERE / 'vivliothiki-eikones.src.html').read_text(encoding='utf-8')

    font = data_uri(APP / 'assets' / 'fonts' / 'Manrope.ttf', 'font/ttf')
    pics = {
        name: data_uri(APP / 'assets' / 'library' / f'{name}.webp', 'image/webp')
        for name in PICTURES
    }

    page = page.replace('__FONT__', font).replace('__PICS__', json.dumps(pics))

    out = HERE / 'vivliothiki-eikones.html'
    out.write_text(page, encoding='utf-8')
    print(f'{out.name}: {out.stat().st_size // 1024} KB')


if __name__ == '__main__':
    main()
