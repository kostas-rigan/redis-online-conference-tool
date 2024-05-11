import json
import random
import string
from datetime import datetime, timedelta

def generate_event_log_entry(users, meetings, event_types):
    meeting_id = random.choice(meetings)["meeting_id"]
    user_id = random.choice(users)["userID"]  # Assume each user has a unique ID
    event_id = f'event_{meeting_id}_{user_id}_0'
    event_type = random.choice(event_types)
    timestamp = datetime.now().isoformat()  # Get the current timestamp in ISO format
    return {
        'event_id': event_id,
        'userID': user_id,
        'event_type': event_type,
        'timestamp': timestamp
    }

def generate_events_log(users, meetings, event_types, num_entries):
    events_log = [generate_event_log_entry(users, meetings, event_types) for _ in range(num_entries)]
    return events_log

def write_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    with open('users.json') as f:
        users = json.load(f)
        
    with open('meetings.json') as f:
        meetings = json.load(f)

    event_types = [1, 2, 3]  # event_type can be 1 (join_meeting), 2 (leave_meeting), 3 (timeout)
    num_entries = 100  # Change this number to generate a different number of log entries
    events_log = generate_events_log(users, meetings, event_types, num_entries)
    write_to_json(events_log, 'events_log.json')
