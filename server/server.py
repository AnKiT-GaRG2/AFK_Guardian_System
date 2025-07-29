# flask_server.py
from flask import Flask, jsonify
from flask_cors import CORS
import json
import os
from flask import request
from datetime import datetime

app = Flask(__name__)

CORS(app)

@app.route('/employee/<employee_id>', methods=['GET'])
def get_state_times(employee_id):
    """Returns the open, closed, and away times for a specific employee."""
    # Create a filename for storing employee data
    filename = "employee_data.json"
        
    # Check if the file exists and load data
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                employee_data = json.load(file)
            except json.JSONDecodeError:
                return jsonify({"status": "error", "message": "Invalid data format"}), 400
    else:
        return jsonify({"status": "error", "message": "No employee data found"}), 404
        
    # Check if the employee exists in the data
    if employee_id not in employee_data:
        return jsonify({"status": "error", "message": f"Employee {employee_id} not found"}), 404
        
    # Return the employee data
    return jsonify({"status": "success", "data": employee_data[employee_id]})
    
@app.route('/employee/<employee_id>', methods=['POST'])
def update_employee_data(employee_id):
    """Updates the data for a specific employee."""
    data = request.json
    
    # Create a filename for storing employee data
    filename = f"employee_data.json"
        
    # Load existing data if file exists
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                employee_data = json.load(file)
            except json.JSONDecodeError:
                employee_data = {}
    else:
        employee_data = {}
        
    # Initialize employee entry if it doesn't exist
    if employee_id not in employee_data:
        employee_data[employee_id] = {}
        
    # Add timestamp to the data
    current_time = datetime.now().isoformat()
    employee_data[employee_id][current_time] = data
        
    # Save the updated data
    with open(filename, 'w') as file:
        json.dump(employee_data, file, indent=4)
        
    return jsonify({"status": "success", "message": f"Data for employee {employee_id} updated"})

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)