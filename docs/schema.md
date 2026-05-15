# quran.db — Database Schema

SQLite database file: `quran.db`

---

## Tables

### `surahs`

Metadata for each of the 114 surahs.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY | Surah number (1–114) |
| `name_ar` | TEXT | NOT NULL | Arabic name |
| `name_en` | TEXT | NOT NULL | Romanized transliteration (e.g. `"Al-Faatiha"`) |
| `ayas` | INTEGER | NOT NULL | Total number of ayahs in this surah |
| `type` | TEXT | NOT NULL | `"Meccan"` or `"Medinan"` |

---

### `ayahs`

Arabic text for every ayah (Tanzil Quran Simple text, v1.1).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Internal row ID |
| `surah_id` | INTEGER | NOT NULL, FK → `surahs.id` | Surah number |
| `ayah_number` | INTEGER | NOT NULL | Ayah position within the surah |
| `text_ar` | TEXT | NOT NULL | Arabic ayah text |

**Index:** `idx_ayahs_surah` on `ayahs(surah_id)`

---

### `translations`

One row per ayah per translation. Currently contains Divehi only.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Internal row ID |
| `ayah_id` | INTEGER | NOT NULL, FK → `ayahs.id` | References `ayahs.id` |
| `language` | TEXT | NOT NULL | BCP-47 language code — currently `"dv"` (Divehi) |
| `translator` | TEXT | NOT NULL | `"Office of the President of Maldives"` |
| `text` | TEXT | NOT NULL | Translated ayah text |

**Index:** `idx_trans_ayah` on `translations(ayah_id)`

---

## Relationships

```
surahs (1) ──── (many) ayahs (1) ──── (many) translations
```

---

## Row Counts

| Table | Rows |
|-------|------|
| `surahs` | 114 |
| `ayahs` | 6,236 |
| `translations` | 6,236 (Divehi) |

---

## Example Queries

```sql
-- List all surahs with type
SELECT id, name_ar, name_en, ayas, type FROM surahs ORDER BY id;

-- Ayah with its Divehi translation
SELECT a.surah_id, a.ayah_number, a.text_ar, t.text AS text_dv
FROM ayahs a
JOIN translations t ON t.ayah_id = a.id
WHERE a.surah_id = 1 AND a.ayah_number = 1;

-- All translations for a given ayah
SELECT t.language, t.translator, t.text
FROM translations t
JOIN ayahs a ON a.id = t.ayah_id
WHERE a.surah_id = 2 AND a.ayah_number = 255;

-- All ayahs in a surah with Divehi translation
SELECT a.ayah_number, a.text_ar, t.text AS text_dv
FROM ayahs a
LEFT JOIN translations t ON t.ayah_id = a.id AND t.language = 'dv'
WHERE a.surah_id = 1
ORDER BY a.ayah_number;
```
