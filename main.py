import json
import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Load users.json
with open('users.json') as f:
    users = json.load(f)

# Load events_log.json
with open('events_log.json') as f:
    events_log = json.load(f)

# Load meetings.json
with open('meetings.json') as f:
    meetings = json.load(f)

# Load meetings_instances.json
with open('meetings_instances.json') as f:
    meetings_instances = json.load(f)

# Store users
for user in users:
    r.hset('users', user['userID'], json.dumps(user))

# Store events_log
for event in events_log:
    r.hset('events_log', event['event_id'], json.dumps(event))

# Store meetings
for meeting in meetings:
    r.hset('meetings', meeting['meetingID'], json.dumps(meeting))

# Store meetings_instances
for meeting_instance in meetings_instances:
    r.hset('meetings_instances', meeting_instance['meeting_id'], json.dumps(meeting_instance))

# Optionally, you can also create indexes for faster retrieval
# For example, if you frequently search users by email, you can create an index like this:
for user in users:
    r.set('email_index:' + user['email'], user['userID'])
