# Builds pites.html out of pites.src.html — the fourteen candidate shapes for
# the pita mark, drawn where the code actually puts each one.
#
# Filled in here rather than typed into the page:
#   1. __FONT__  — Manrope, base64 (D-072).
#   2. __PIC__   — the real picture the two products share.
#   3. __PIG__   — the real meat mark, so the second mark is judged beside the
#      first and not on its own.
#   4. __CANDS__ — the fourteen glyphs, with the rectangle measured for EACH of
#      them by pictures/tools/build_assets.py: a wide taco and a tall wrap do
#      not land in the same place, and comparing them at one borrowed size
#      would be comparing something the program will never draw.
#
# Run from this folder, with the private repo beside this one:
#   python build-pites.py

import base64
import json
import pathlib

HERE = pathlib.Path(__file__).parent
APP = HERE.parents[1] / 'OpaProject' / 'app'
PITES = HERE / 'pites'


def data_uri(path: pathlib.Path, mime: str) -> str:
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()


def main() -> None:
    page = (HERE / 'pites.src.html').read_text(encoding='utf-8')

    spots = json.loads((PITES / 'spots.json').read_text(encoding='utf-8'))
    cands = {
        name: {**place, 'uri': data_uri(PITES / f'{name}.png', 'image/png')}
        for name, place in spots.items()
    }

    page = (page
            .replace('__FONT__', data_uri(APP / 'assets' / 'fonts' / 'Manrope.ttf', 'font/ttf'))
            .replace('__PIC__', data_uri(APP / 'assets' / 'library' / 'meat_souvlaki_xoirino.webp', 'image/webp'))
            .replace('__PIG__', data_uri(APP / 'assets' / 'simata' / 'xoirino.webp', 'image/webp'))
            .replace('__CANDS__', json.dumps(cands)))

    out = HERE / 'pites.html'
    out.write_text(page, encoding='utf-8')
    print(f'{out.name}: {out.stat().st_size // 1024} KB')


if __name__ == '__main__':
    main()
