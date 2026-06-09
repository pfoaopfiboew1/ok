import sqlite3

def init_db(db_path="currency_data.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL NOT NULL,
            currency_pair TEXT NOT NULL,
            average_rate REAL NOT NULL,
            std_dev REAL NOT NULL,
            source TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

def save_to_db(data, db_path="currency_data.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO rates (timestamp, currency_pair, average_rate, std_dev, source)
        VALUES (?, ?, ?, ?, ?)
    """, (data["timestamp"], data["pair"], data["average_rate"], data["std_dev"], data["source"]))
    conn.commit()
    conn.close()