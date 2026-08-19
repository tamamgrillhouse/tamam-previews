# Builds pita-simadi.html out of pita-simadi.src.html.
#
# Four things are filled in here rather than typed into the page:
#   1. __FONT__  — Manrope, base64. The page must show the typeface that ships
#      inside the application (D-072).
#   2. __PICS__  — the four real product pictures out of app/assets/library/.
#      The whole question is whether two tiles sharing ONE file can be told
#      apart, so a stand-in square cannot answer it.
#   3. __MARKS__ — the two real meat marks out of app/assets/simata/, black on
#      transparent, recoloured by the page the way the tile recolours them.
#   4. __PITA__  — the candidate pita glyph, Icons8 `fluency-systems-filled`
#      icon `burrito`, fetched the same way the four animals were
#      (`pictures/simata/SOURCE.md`). It is a STAND-IN for the shape: if a road
#      is chosen, the glyph itself gets its own comparison, as the four did.
#
# Run from this folder, with the private repo beside this one:
#   python build-pita-simadi.py

import base64
import json
import pathlib

HERE = pathlib.Path(__file__).parent
APP = HERE.parents[1] / 'OpaProject' / 'app'

PICTURES = [
    'meat_souvlaki_xoirino',
    'meat_souvlaki_kotopoulo',
    'meat_merida_gyro_xoirino',
    'meat_merida_gyro_kotopoulo',
]

MARKS = ['xoirino', 'kotopoulo']


def data_uri(path: pathlib.Path, mime: str) -> str:
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()


def main() -> None:
    page = (HERE / 'pita-simadi.src.html').read_text(encoding='utf-8')

    font = data_uri(APP / 'assets' / 'fonts' / 'Manrope.ttf', 'font/ttf')
    pics = {
        name: data_uri(APP / 'assets' / 'library' / f'{name}.webp', 'image/webp')
        for name in PICTURES
    }
    marks = {
        name: data_uri(APP / 'assets' / 'simata' / f'{name}.webp', 'image/webp')
        for name in MARKS
    }
    pita = data_uri(HERE / 'pita-ypopsifia.png', 'image/png')

    page = (page
            .replace('__FONT__', font)
            .replace('__PICS__', json.dumps(pics))
            .replace('__MARKS__', json.dumps(marks))
            .replace('__PITA__', pita))

    out = HERE / 'pita-simadi.html'
    out.write_text(page, encoding='utf-8')
    print(f'{out.name}: {out.stat().st_size // 1024} KB')


if __name__ == '__main__':
    main()
