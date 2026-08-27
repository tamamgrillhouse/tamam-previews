# Builds plakidio-platos.html out of plakidio-platos.src.html.
#
# Two things are filled in here rather than typed into the page:
#   1. __FONT__ — Manrope, base64. The tile's whole question is how much room
#      the name has, and a system font measures differently from the one that
#      ships inside the application (D-072).
#   2. __PICS__ — three real product pictures out of app/assets/library/,
#      base64, as a JSON map from picture id to a data URI. The page shows the
#      tile at real size; a grey square would not show what a squeezed
#      photograph looks like beside a name.
#
# Run from this folder, with the private repo beside this one:
#   python build-plakidio.py

import base64
import json
import pathlib

HERE = pathlib.Path(__file__).parent
APP = HERE.parents[1] / 'OpaProject' / 'app'

PICTURES = [
    'meat_souvlaki_xoirino',
    'sweets_loukoumades',
    'meat_merida_gyro_xoirino',
]


def data_uri(path: pathlib.Path, mime: str) -> str:
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()


def main() -> None:
    page = (HERE / 'plakidio-platos.src.html').read_text(encoding='utf-8')

    font = data_uri(APP / 'assets' / 'fonts' / 'Manrope.ttf', 'font/ttf')
    pics = {
        name: data_uri(APP / 'assets' / 'library' / f'{name}.webp', 'image/webp')
        for name in PICTURES
    }

    page = page.replace('__FONT__', font).replace('__PICS__', json.dumps(pics))

    out = HERE / 'plakidio-platos.html'
    out.write_text(page, encoding='utf-8')
    print(f'{out.name}: {out.stat().st_size // 1024} KB')


if __name__ == '__main__':
    main()
