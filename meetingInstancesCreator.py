import string
import json
import random
from datetime import datetime, timedelta

def generate_meeting_instance(users, meetings, order_ids):
    meeting = random.choice(meetings)
    meeting_id = meeting["meeting_id"]
    order_id = order_ids.get(meeting_id, 0) + 1
    order_ids[meeting_id] = order_id
    start_datetime = datetime.now() - timedelta(days=365)  # 1 year ago
    end_datetime = datetime.now() + timedelta(days=365)
    return {
        'meeting_id': meeting_id,
        'order_id': order_id,
        'fromdatetime':  start_datetime.isoformat(),
        'todatetime': end_datetime.isoformat()
    }

def generate_meetings_instances(users, meetings, num_meetings):
    order_ids = {}
    meetings_instances = [generate_meeting_instance(users, meetings, order_ids) for _ in range(num_meetings)]
    return meetings_instances

def write_to_json(meetings, filename):
    with open(filename, 'w') as f:
        json.dump(meetings, f, indent=4)

if __name__ == "__main__":
    with open('users.json') as f:
        users = json.load(f)

    with open('meetings.json') as f:
        meetings = json.load(f)

    num_meetings = 20  # Change this number to generate different numbers of meetings
    meetings_instances = generate_meetings_instances(users, meetings, num_meetings)
    write_to_json(meetings_instances, 'meetings_instances.json')
