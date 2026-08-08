"""Fills the font placeholder in anafora-z.src.html and writes anafora-z.html.

The typeface has to travel inside the page — a borrowed system font would look
right here and look nothing like this on the customer's tablet (DEAD-ENDS §9).
Manrope is 165 KB, so it goes in as base64 and the source keeps a placeholder,
which is what stops the edited file becoming unreadable (RULES.md §8).

    python build.py
"""

import base64
import pathlib

HERE = pathlib.Path(__file__).parent
FONT = pathlib.Path(
    r"c:\Users\SixBillion\Documents\OpaProject\app\assets\fonts\Manrope.ttf"
)

source = (HERE / "anafora-z.src.html").read_text(encoding="utf-8")
font = base64.b64encode(FONT.read_bytes()).decode("ascii")
(HERE / "anafora-z.html").write_text(
    source.replace("__FONT_MANROPE__", font), encoding="utf-8"
)
print(f"anafora-z.html written, font {len(font)} chars")
