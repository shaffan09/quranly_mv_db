import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "juz-to-chapter-verse-mappings.json"


def parse_juz() -> list[tuple[int, int, int, int, int, int]]:
    data = json.loads(DATA_FILE.read_text())
    rows = []
    for juz_str, surahs in data.items():
        juz_no = int(juz_str)
        sorted_surahs = sorted(surahs.items(), key=lambda x: int(x[0]))
        start_surah = int(sorted_surahs[0][0])
        start_ayah = int(sorted_surahs[0][1].split("-")[0])
        end_surah = int(sorted_surahs[-1][0])
        end_ayah = int(sorted_surahs[-1][1].split("-")[1])
        rows.append((juz_no, juz_no, start_surah, start_ayah, end_surah, end_ayah))
    return rows
