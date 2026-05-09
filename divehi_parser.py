import re
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "dv.divehi.sql"
LANGUAGE = "dv"
TRANSLATOR = "Office of the President of Maldives"


def parse_divehi() -> list[tuple[int, int, str]]:
    """Return list of (sura, aya, text) for all Divehi translation verses."""
    content = DATA_FILE.read_text(encoding="utf-8")
    rows = re.findall(r"\(\d+,\s*(\d+),\s*(\d+),\s*'((?:[^'\\]|\\.)*)'\)", content)
    return [(int(sura), int(aya), text.replace("\\'", "'")) for sura, aya, text in rows]
