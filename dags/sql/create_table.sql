CREATE TABLE IF NOT EXISTS weather_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude REAL,
    longitude REAL,
    average_temperature REAL,
    units TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);