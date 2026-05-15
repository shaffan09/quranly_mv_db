import re
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "quran-data.js"


def parse_surahs() -> list[tuple[int, str, str, int, str]]:
    content = DATA_FILE.read_text(encoding="utf-8")
    rows = re.findall(
        r"\[\d+,\s*(\d+),\s*\d+,\s*\d+,\s*'([^']+)',\s*\"([^\"]+)\",\s*'[^']+',\s*'([^']+)'\]",
        content
    )
    return [
        (i + 1, name_ar, tname, int(ayas), stype)
        for i, (ayas, name_ar, tname, stype) in enumerate(rows)
    ]
