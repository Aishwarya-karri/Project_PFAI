import sqlite3
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. Bulletproof File Paths
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, '../database/pfai_engine.db')

# Create a new folder for the saved AI model
model_dir = os.path.join(current_dir, '../models')
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, 'pfai_model.pkl')

# 2. Connect to SQL and fetch the training data
print("Connecting to SQL to fetch Alumni History...")
conn = sqlite3.connect(db_path)
df = pd.read_sql_query("SELECT * FROM Alumni_History", conn)
conn.close()

# 3. Prepare the Data (Split into Features and Target)
# X = The student's stats (Inputs)
# y = The actual career they ended up in (Output)
X = df[['math_score', 'science_score', 'coding_interest', 'logic_score']]
y = df['final_career']

# 4. Train the AI Model (Random Forest Classifier)
print("Training the PFAI Machine Learning Model...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X, y)

# 5. Save the trained model to a file
joblib.dump(rf_model, model_path)
print(f"Model successfully saved to: {model_path}")

# 6. Quick AI Prediction Test
# Simulating a new student who loves coding (9/10) and logic (9/10)
test_student = [[85, 90, 9, 9]] 
prediction = rf_model.predict(test_student)

print("\n--- Testing AI Prediction ---")
print(f"A student with stats {test_student[0]} is predicted for: {prediction[0]}")