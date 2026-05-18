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

### `chapters`

One row per juz (30 total). Stores the surah and ayah where each juz begins and ends.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY | Juz number (1–30) |
| `chapter_no` | INTEGER | NOT NULL | Juz number (1–30) |
| `start_surah_id` | INTEGER | NOT NULL, FK → `surahs.id` | Surah where the juz begins |
| `start_ayah_no` | INTEGER | NOT NULL | Ayah number where the juz begins |
| `end_surah_id` | INTEGER | NOT NULL, FK → `surahs.id` | Surah where the juz ends |
| `end_ayah_no` | INTEGER | NOT NULL | Ayah number where the juz ends |

**Index:** `idx_chapters_no` on `chapters(chapter_no)`

---

## Relationships

```
surahs (1) ──── (many) ayahs (1) ──── (many) translations
surahs (1) ──── (many) chapters (via start_surah_id / end_surah_id)
```

---

## Row Counts

| Table | Rows |
|-------|------|
| `surahs` | 114 |
| `ayahs` | 6,236 |
| `translations` | 6,236 (Divehi) |
| `chapters` | 30 |

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

-- Juz boundaries
SELECT chapter_no, start_surah_id, start_ayah_no, end_surah_id, end_ayah_no
FROM chapters
ORDER BY chapter_no;

-- All ayahs in juz 1
SELECT a.surah_id, a.ayah_number, a.text_ar
FROM chapters c
JOIN ayahs a ON (
    a.surah_id > c.start_surah_id OR (a.surah_id = c.start_surah_id AND a.ayah_number >= c.start_ayah_no)
) AND (
    a.surah_id < c.end_surah_id OR (a.surah_id = c.end_surah_id AND a.ayah_number <= c.end_ayah_no)
)
WHERE c.chapter_no = 1
ORDER BY a.surah_id, a.ayah_number;
```
