-- Event table

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    predicted_label INTEGER,
    confidence REAL,
    alert TEXT
);
