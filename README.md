# quranly_mv_db

Builds a normalized SQLite database containing the complete Arabic Quran text and its official Divehi (ދިވެހި) translation, ready to ship in a mobile or web app.

## Data sources

| File | Contents |
|------|----------|
| `data/quran-simple.sql` | Tanzil Quran Text — Simple, v1.1 (CC-BY 3.0) |
| `data/dv.divehi.sql` | Divehi translation by the Office of the President of Maldives, via Tanzil.net |

## Database schema

```
surahs        id, name_ar, name_en, ayas, type
ayahs         id, surah_id, ayah_number, text_ar
translations  id, ayah_id, language, translator, text
```

`translations.language` is `"dv"` for the Divehi translation. Additional translations can be added by creating a new parser module and inserting rows in the same pattern.

## Usage

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
python main.py
```

Output: `output/quran.db` — 6,236 ayahs, 6,236 Divehi translation rows.

Upload the generated file to GitHub Releases for distribution.

## Project structure

```
.
├── data/
│   ├── quran-simple.sql   # Arabic Quran text dump
│   └── dv.divehi.sql      # Divehi translation dump
├── output/
│   └── quran.db           # generated — not committed
├── quran_parser.py
├── divehi_parser.py
└── main.py
```

## License

The Quran text and translation data are subject to their respective Tanzil.net licenses (Creative Commons Attribution 3.0). The build scripts in this repository are released under the MIT License.
