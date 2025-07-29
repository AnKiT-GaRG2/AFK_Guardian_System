import time
import datetime
from afk_checks.window_tracker import get_active_window
from afk_checks import eye_tracker
from collections import defaultdict
from time import sleep
from collections import defaultdict
from afk_checks.voice_tracker import VoiceTracker
from afk_checks.activity_tracker import get_activity_data
import json
import requests


# Constants
AFK_THRESHOLD = 300  # seconds (5 minutes) of inactivity to be considered AFK
CHECK_INTERVAL = 1  # seconds between checks
PRINT_INTERVAL = 60  # seconds between activity reports
EMPLOYEE_ID=1

# Global variables
last_input_time = time.time()
window_time = defaultdict(float)
current_window = None
current_window_start = time.time()
afk_start_time = None
is_afk = False
total_afk_time = 0

def get_active_window_title():
    """Get the title of the currently active window."""
    monitor = get_active_window()
    return monitor
    

def check_user_activity():
    """Check Eye Movement."""
    data = eye_tracker.return_data()
    eye_tracker.reset_data()
    
    return data

def check_voice_activity(tracker):
    status = tracker.get_speaking_status()
    if(status==0):
        return "SPEAKING"
    else:
        return "NOT SPEAKING"
    
def keyboad_tracker():
    return get_activity_data()


def main():
    """Main function to run the activity monitoring."""
    print(f"Starting activity monitoring for Employee ID: {EMPLOYEE_ID}")
    print(f"AFK threshold set to {AFK_THRESHOLD} seconds")
     # Create a more flexible nested defaultdict structure
    my_map = defaultdict(lambda: {
        "time_spent": 0, 
        "activities": defaultdict(lambda: {"count": 0, "text": ""})
    })
    new_map = defaultdict(int)

    tracker = VoiceTracker()
    eye_tracker.start_eye_tracking()
    currntTime = 0

    while True:
        time.sleep(CHECK_INTERVAL)
        active_window = get_active_window_title()
        
        # ✅ Ensure "activities" key exists before accessing it
        if "activities" not in my_map[active_window]:
            my_map[active_window]["activities"] = defaultdict(int)

        # ✅ Increment time spent on the active window
        my_map[active_window]['time_spent'] += 1

        # ✅ Track user activity in new_map
        for key, value in check_user_activity().items():
            new_map[key] += int(value)  
        
        new_map[check_voice_activity(tracker)] += 1    

        for key, value in keyboad_tracker().items():
            if isinstance(value, str):  
                # Store string values in the "text" field
                my_map[active_window]["activities"][key]["text"] += value  
            else:  
                # Store numeric values in the "count" field
                my_map[active_window]["activities"][key]["count"] += int(value)


        currntTime += 1
        print(currntTime)
        if currntTime % 30 == 0:
            print(my_map)  # Print structured data
            print(new_map)  # Print new activity summary
            
            # Prepare the payload combining both maps
            payload = {
                "employee_id": EMPLOYEE_ID,
                "timestamp": datetime.datetime.now().isoformat(),
                "window_activity": dict(my_map),  # Convert defaultdict to regular dict
                "activity_summary": dict(new_map)  # Convert defaultdict to regular dict
            }
            
            # Send the data via POST request
            try:
                response = requests.post(
                    f"http://localhost:5000/employee/{EMPLOYEE_ID}",  # Replace with your actual API endpoint
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                print(f"Data sent to server. Status code: {response.status_code}")
                if response.status_code != 200:
                    print(f"Error response: {response.text}")
            except Exception as e:
                print(f"Failed to send data: {e}")
            
            # ✅ Reset maps while keeping the structure intact
            my_map = defaultdict(lambda: {
            "time_spent": 0, 
            "activities": defaultdict(lambda: {"count": 0, "text": ""})
            })
            new_map = defaultdict(int)
        

if __name__ == "__main__":
    main()