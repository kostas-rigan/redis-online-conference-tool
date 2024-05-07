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

with r.pipeline() as pipe:
    # Store users
    for pos, user in enumerate(users):
        for key, value in user.items():
            pipe.hset(f'users_{pos}', key, value)

    # Store events_log
    for pos, event in enumerate(events_log):
        for key, value in event.items():
            pipe.hset(f'events_log_{pos}', key, value)

    # Store meetings
    for pos, meeting in enumerate(meetings):
        for key, value in meeting.items():
            if key == 'audience':
                value = '|'.join(value)
            pipe.hset(f'meetings_{pos}', key, value)

    # Store meetings_instances
    for pos, meeting_instance in enumerate(meetings_instances):
        for key, value in meeting_instance.items():
            pipe.hset(f'meetings_instances_{pos}', key, value)

    # Optionally, you can also create indexes for faster retrieval
    # For example, if you frequently search users by email, you can create an index like this:
    for user in users:
        pipe.set('email_index:' + user['email'], user['userID'])

    pipe.execute()
