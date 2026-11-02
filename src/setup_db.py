import sqlite3
import pandas as pd
import os

# Define paths
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, '../data/pfai_database.db')
csv_path = os.path.join(current_dir, '../data/curated_roadmap.csv')

# Connect to SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS roadmaps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT,
        degree_type TEXT,
        year_1 TEXT,
        year_2 TEXT,
        year_3 TEXT,
        year_4 TEXT
    )
''')

# Clear old data and load new CSV
cursor.execute('DELETE FROM roadmaps')
df = pd.read_csv(csv_path)
df.to_sql('roadmaps', conn, if_exists='append', index=False)

conn.commit()
conn.close()
print("Database successfully built and populated!")