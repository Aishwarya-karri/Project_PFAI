from flask import Flask, render_template, request
import joblib
import os
import numpy as np
import sqlite3

app = Flask(__name__)

# 1. Load your trained AI model
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, '../models/pfai_model.pkl')
rf_model = joblib.load(model_path)

# 2. Friendly role descriptions for Intermediate/12th students
ROLE_DESCRIPTIONS = {
    "Software_Developer_Trainee": "Writes core program logic, fixes bugs, and builds software modules under senior engineers.",
    "Associate_Software_Engineer": "Designs and tests basic software systems and application components in team environments.",
    "Junior_Software_Developer": "Assists with coding user features, testing script reliability, and updating existing apps.",
    "Data_Analyst_Trainee": "Inspects and organizes business numbers to spot patterns and create simple analytical reports.",
    "Associate_Data_Analyst": "Cleans data sets and builds dashboards to help managers make informed operational decisions.",
    "AI_ML_Trainee": "Helps train mathematical algorithms and process data inputs for predictive machine learning models.",
    "Junior_QA_Engineer": "Tests software products to identify glitches, bugs, and errors before they reach customers.",
    "Manual_Testing_Trainee": "Steps through software applications by hand to ensure buttons, screens, and features work properly.",
    "Automation_Testing_Trainee": "Writes automated test scripts to check software speed, reliability, and functionality.",
    "Technical_Support_Associate": "Troubleshoots hardware, network, and application issues directly for enterprise end-users.",
    "IT_Service_Desk_Associate": "Logs incoming tech incidents, troubleshoots user access, and routes complex IT issues.",
    "Application_Support_Associate": "Monitors business software to ensure zero downtime and resolves operational app errors.",
    "SQL_Developer_Trainee": "Writes database queries, organizes structured tables, and retrieves information efficiently.",
    "Database_Support_Trainee": "Monitors database health, handles routine backups, and ensures stored records remain secure.",
    "Cloud_Support_Associate": "Helps manage virtual servers and basic cloud storage setups on platforms like AWS or Azure.",
    "Cybersecurity_Analyst_Trainee": "Monitors digital traffic, identifies security alerts, and safeguards systems against attacks.",
    "Network_Support_Trainee": "Configures routers, switches, and cabling to keep company internet and internal networks stable.",
    "Business_Analyst_Trainee": "Translates business requirements into clear technical instructions for development teams.",
    "MIS_Executive": "Organizes company records and builds daily operational Excel reports for business leadership.",
    "Reporting_Analyst": "Transforms raw company numbers into clear summaries, charts, and executive KPI trackers.",
    "Associate_Consultant": "Analyzes client workflows and recommends technical tools to improve company productivity.",
    "Systems_Engineer_Trainee": "Maintains physical computer systems, operating software, and office hardware infrastructure.",
    "Programmer_Analyst_Trainee": "Codes specific functional modules while analyzing program flow and logic performance.",
    "Web_Developer_Trainee": "Builds responsive web pages, layouts, forms, and interactive site features using web tools.",
    "ERP_Support_Trainee": "Assists teams with enterprise software (like SAP or Oracle) that manages inventory and billing.",
    "Graduate_Engineer_Trainee": "Rotates across various core engineering, maintenance, and software projects to build foundational skills.",
    "IT_Operations_Associate": "Coordinates background IT workflows, system uptime checks, and routine technical procedures.",
    "Software_Support_Trainee": "Helps corporate clients install, update, and resolve errors with specialized software packages.",
    "Junior_Data_Engineer": "Builds the pipelines and cleanup scripts that transfer data safely into storage databases.",
    "Technical_Process_Associate": "Follows standardized tech procedures to enter, verify, and maintain digital enterprise records."
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    math = int(request.form['math_score'])
    science = int(request.form['science_score'])
    coding = int(request.form['coding_interest'])
    logic = int(request.form['logic_score'])
    
    probabilities = rf_model.predict_proba([[math, science, coding, logic]])[0]
    classes = rf_model.classes_
    
    top_indices = np.argsort(probabilities)[::-1][:2]
    
    role1 = classes[top_indices[0]]
    prob1 = round(probabilities[top_indices[0]] * 100)
    desc1 = ROLE_DESCRIPTIONS.get(role1, "Focuses on technical operations, data analysis, and software systems.")
    
    role2 = classes[top_indices[1]]
    prob2 = round(probabilities[top_indices[1]] * 100)
    desc2 = ROLE_DESCRIPTIONS.get(role2, "Focuses on technical operations, data analysis, and software systems.")
    
    return render_template('choose_role.html', 
                           role1=role1, prob1=prob1, desc1=desc1,
                           role2=role2, prob2=prob2, desc2=desc2)

@app.route('/roadmap', methods=['POST'])
def roadmap():
    chosen_role = request.form['chosen_role']
    degree_type = request.form['degree_type']
    
    # 3. Open the database and search for the specific roadmap
    db_path = os.path.join(current_dir, '../data/pfai_database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM roadmaps WHERE role=? AND degree_type=?", (chosen_role, degree_type))
    plan = cursor.fetchone()
    conn.close()
    
    # 4. Send the database row to the final HTML page
    return render_template('roadmap.html', role=chosen_role.replace('_', ' '), degree=degree_type, plan=plan)

if __name__ == '__main__':
    app.run(debug=True)