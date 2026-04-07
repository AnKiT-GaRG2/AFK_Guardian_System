# flask_server.py
from flask import Flask, jsonify, Response, stream_with_context
from flask_cors import CORS
import json
import os
from flask import request
from datetime import datetime
import time
from policy_engine import DecisionPolicyEngine

app = Flask(__name__)

CORS(app)

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "employee_data.json")
policy_engine = DecisionPolicyEngine()


def build_employee_response(employee_records):
    return {
        "status": "success",
        "data": employee_records,
        "policy_result": policy_engine.evaluate_employee(employee_records),
    }


def load_employee_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return None
    return {}


def save_employee_data(employee_data):
    with open(DATA_FILE, 'w') as file:
        json.dump(employee_data, file, indent=4)

@app.route('/employee/<employee_id>', methods=['GET'])
def get_state_times(employee_id):
    """Returns the open, closed, and away times for a specific employee."""
    employee_data = load_employee_data()
    if employee_data is None:
        return jsonify({"status": "error", "message": "Invalid data format"}), 400
    if not employee_data:
        return jsonify({"status": "error", "message": "No employee data found"}), 404
        
    # Check if the employee exists in the data
    if employee_id not in employee_data:
        return jsonify({"status": "error", "message": f"Employee {employee_id} not found"}), 404
        
    # Return employee activity data and computed policy decision output
    return jsonify(build_employee_response(employee_data[employee_id]))
    
@app.route('/employee/<employee_id>', methods=['POST'])
def update_employee_data(employee_id):
    """Updates the data for a specific employee."""
    data = request.json

    employee_data = load_employee_data()
    if employee_data is None:
        employee_data = {}
        
    # Initialize employee entry if it doesn't exist
    if employee_id not in employee_data:
        employee_data[employee_id] = {}
        
    # Add timestamp to the data
    current_time = datetime.now().isoformat()
    employee_data[employee_id][current_time] = data

    # Save the updated data
    save_employee_data(employee_data)

    return jsonify({"status": "success", "message": f"Data for employee {employee_id} updated"})


@app.route('/employee/<employee_id>/stream', methods=['GET'])
def stream_employee_data(employee_id):
    def event_stream():
        last_mtime = None
        heartbeat_counter = 0

        while True:
            try:
                if os.path.exists(DATA_FILE):
                    current_mtime = os.path.getmtime(DATA_FILE)
                    if last_mtime is None or current_mtime != last_mtime:
                        employee_data = load_employee_data()
                        if employee_data is None:
                            payload = {"status": "error", "message": "Invalid data format"}
                        elif employee_id not in employee_data:
                            payload = {"status": "error", "message": f"Employee {employee_id} not found"}
                        else:
                            payload = build_employee_response(employee_data[employee_id])

                        yield f"data: {json.dumps(payload)}\n\n"
                        last_mtime = current_mtime

                heartbeat_counter += 1
                if heartbeat_counter >= 15:
                    yield ": heartbeat\n\n"
                    heartbeat_counter = 0

            except Exception as error:
                payload = {"status": "error", "message": str(error)}
                yield f"data: {json.dumps(payload)}\n\n"

            time.sleep(1)

    return Response(
        stream_with_context(event_stream()),
        mimetype='text/event-stream',
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)