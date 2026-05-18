import sqlite3
from pathlib import Path
from quran_parser import parse_quran
from divehi_parser import parse_divehi, LANGUAGE, TRANSLATOR
from surahs_parser import parse_surahs
from juz_parser import parse_juz

OUTPUT_FILE = Path(__file__).parent / "output" / "quran.db"


def build_quran_db():
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(OUTPUT_FILE)
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS surahs (
            id      INTEGER PRIMARY KEY,
            name_ar TEXT NOT NULL,
            name_en TEXT NOT NULL,
            ayas    INTEGER NOT NULL,
            type    TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS ayahs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            surah_id    INTEGER NOT NULL,
            ayah_number INTEGER NOT NULL,
            text_ar     TEXT NOT NULL,
            FOREIGN KEY (surah_id) REFERENCES surahs(id)
        );

        CREATE TABLE IF NOT EXISTS translations (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            ayah_id     INTEGER NOT NULL,
            language    TEXT NOT NULL,
            translator  TEXT NOT NULL,
            text        TEXT NOT NULL,
            FOREIGN KEY (ayah_id) REFERENCES ayahs(id)
        );

        CREATE TABLE IF NOT EXISTS chapters (
            id             INTEGER PRIMARY KEY,
            chapter_no     INTEGER NOT NULL,
            start_surah_id INTEGER NOT NULL,
            start_ayah_no  INTEGER NOT NULL,
            end_surah_id   INTEGER NOT NULL,
            end_ayah_no    INTEGER NOT NULL,
            FOREIGN KEY (start_surah_id) REFERENCES surahs(id),
            FOREIGN KEY (end_surah_id)   REFERENCES surahs(id)
        );

        CREATE INDEX IF NOT EXISTS idx_ayahs_surah ON ayahs(surah_id);
        CREATE INDEX IF NOT EXISTS idx_trans_ayah  ON translations(ayah_id);
        CREATE INDEX IF NOT EXISTS idx_chapters_no ON chapters(chapter_no);
    """)

    cursor.executemany(
        "INSERT INTO surahs (id, name_ar, name_en, ayas, type) VALUES (?, ?, ?, ?, ?)",
        parse_surahs()
    )

    cursor.executemany(
        "INSERT INTO chapters (id, chapter_no, start_surah_id, start_ayah_no, end_surah_id, end_ayah_no) VALUES (?, ?, ?, ?, ?, ?)",
        parse_juz()
    )

    for sura, aya, text in parse_quran():
        cursor.execute(
            "INSERT INTO ayahs (surah_id, ayah_number, text_ar) VALUES (?, ?, ?)",
            (sura, aya, text)
        )

    for sura, aya, text in parse_divehi():
        cursor.execute("""
            INSERT INTO translations (ayah_id, language, translator, text)
            SELECT a.id, ?, ?, ?
            FROM ayahs a
            WHERE a.surah_id = ? AND a.ayah_number = ?
        """, (LANGUAGE, TRANSLATOR, text, sura, aya))

    conn.commit()
    conn.close()
    print("✅ quran.db ready — upload this to GitHub Releases")


build_quran_db()
