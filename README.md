# quranly_mv_db

Builds a normalized SQLite database containing the complete Arabic Quran text and its official Divehi (ދިވެހި) translation, ready to ship in a mobile or web app.

## Data sources

| File | Contents |
|------|----------|
| `data/quran-simple.sql` | Tanzil Quran Text — Simple, v1.1 (CC-BY 3.0) |
| `data/dv.divehi.sql` | Divehi translation by the Office of the President of Maldives, via Tanzil.net |
| `data/quran-data.js` | Surah metadata (names, ayah counts, revelation type) |
| `data/juz-to-chapter-verse-mappings.json` | Juz-to-surah/verse range mappings for all 30 juz |

## Database schema

```
surahs        id, name_ar, name_en, ayas, type
ayahs         id, surah_id, ayah_number, text_ar
translations  id, ayah_id, language, translator, text
chapters      id, chapter_no, start_surah_id, start_ayah_no, end_surah_id, end_ayah_no
```

`translations.language` is `"dv"` for the Divehi translation. Additional translations can be added by creating a new parser module and inserting rows in the same pattern.

`chapters` represents the 30 juz of the Quran. Each row records the surah and ayah where a juz begins and ends, enabling range queries by juz.

## Usage

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
python3 main.py
```

Output: `output/quran.db` — 6,236 ayahs, 6,236 Divehi translation rows, 30 juz chapters.

Upload the generated file to GitHub Releases for distribution.

## Project structure

```
.
├── data/
│   ├── quran-simple.sql                  # Arabic Quran text dump
│   ├── dv.divehi.sql                     # Divehi translation dump
│   ├── quran-data.js                     # Surah metadata
│   └── juz-to-chapter-verse-mappings.json
├── output/
│   └── quran.db                          # generated — not committed
├── quran_parser.py
├── divehi_parser.py
├── surahs_parser.py
├── juz_parser.py
└── main.py
```

## License

The Quran text and translation data are subject to their respective Tanzil.net licenses (Creative Commons Attribution 3.0). The build scripts in this repository are released under the MIT License.
