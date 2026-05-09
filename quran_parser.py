import re
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "quran-simple.sql"


def parse_quran() -> list[tuple[int, int, str]]:
    """Return list of (sura, aya, text) for all Arabic verses."""
    content = DATA_FILE.read_text(encoding="utf-8")
    rows = re.findall(r"\(\d+,\s*(\d+),\s*(\d+),\s*'((?:[^'\\]|\\.)*)'\)", content)
    return [(int(sura), int(aya), text.replace("\\'", "'")) for sura, aya, text in rows]
