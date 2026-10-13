import sqlite3
import pandas as pd
import os

# 1. Define where your files live
db_path = '../database/pfai_engine.db'
alumni_csv_path = '../data/alumni_data.csv'
roadmap_csv_path = '../data/curated_roadmap.csv'

# Ensure the database directory exists before creating the file
os.makedirs('../database', exist_ok=True)

# 2. Connect to SQLite (This auto-creates the pfai_engine.db file)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
print("Connected to PFAI SQL Database...")

# 3. Create the SQL Tables structure
cursor.execute('''
CREATE TABLE IF NOT EXISTS Alumni_History (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    math_score INTEGER,
    science_score INTEGER,
    coding_interest INTEGER,
    logic_score INTEGER,
    final_career TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Curated_Roadmaps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT,
    skill_name TEXT,
    learning_sequence INTEGER,
    platform TEXT,
    url_link TEXT,
    why_this_platform TEXT
)
''')
print("SQL Tables created successfully...")

# 4. Load your CSV data into Pandas DataFrames
alumni_df = pd.read_csv(alumni_csv_path)
roadmap_df = pd.read_csv(roadmap_csv_path)

# 5. Insert DataFrames into the SQL database tables
# 'replace' ensures we don't get duplicate data if you run the script twice
alumni_df.to_sql('Alumni_History', conn, if_exists='replace', index=False)
roadmap_df.to_sql('Curated_Roadmaps', conn, if_exists='replace', index=False)
print("CSV Data inserted into SQL successfully!")

# 6. Run a quick test query to prove it works
print("\n--- Testing Database Fetch for Data Scientist ---")
cursor.execute("SELECT skill_name, platform FROM Curated_Roadmaps WHERE role_name='Data_Scientist'")
results = cursor.fetchall()

for row in results:
    print(f"Skill: {row[0]} -> Learn on: {row[1]}")

# 7. Close the connection securely
conn.close()
