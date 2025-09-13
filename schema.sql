-- Entries table: holds basic metadata
-- CREATE TABLE IF NOT EXISTS entries (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Fields table: holds multilingual + media data
-- CREATE TABLE IF NOT EXISTS fields (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     entry_id INTEGER,
--     name TEXT,          -- e.g. "word", "sentence", "example", "audio"
--     language TEXT,      -- e.g. "en", "fr", "de"
--     type TEXT,          -- "text", "image", "audio", "video"
--     value TEXT,         -- text content or filepath for media
--     FOREIGN KEY(entry_id) REFERENCES entries(id)
-- );


CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name TEXT,        -- e.g. "word", "sentence", "example", "audio"
    language TEXT,    -- e.g. "en", "fr", "de"
    text_value TEXT,  -- text
    audio_path TEXT,  -- audio path
    image_path TEXT,  -- image path
    video_path TEXT   -- video path
);


CREATE TABLE IF NOT EXISTS languages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,    -- e.g. "en", "fr"
    name TEXT NOT NULL          -- e.g. "English", "French"
);

INSERT OR IGNORE INTO languages (code, name) VALUES
                ("en", "English"),
                ("fr", "French"),
                ("es", "Spanish"),
                ("de", "German"),
                ("zh", "Chinese"),
                ("ar", "Arabic");


-- Full Text Search virtual table for fast search
CREATE VIRTUAL TABLE IF NOT EXISTS fields_fts 
USING fts5(value, content='fields', content_rowid='id');
