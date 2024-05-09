import redis
import random, string
from helper import *
from entities import User, Meeting
from datetime import datetime
import json
import string
import random


# 1 - Function: a user joins an active meeting instance
def user_join(r, user, meeting):
    if meeting.is_public or user.email in meeting.audience:
        event = {
            'event_id': f'{meeting.id}_{user.id}_1',
            'userID': user.id,
            'event_type': 1,
            'timestamp': datetime.now().isoformat()
        }
        r.rpush(f'eventsLog_{meeting.id}_{user.id}_1', json.dumps(event))
        print(f'User {user.name} joined the meeting {meeting.title}')
    else:
        print(f'User {user.name} is not allowed to join the meeting {meeting.title}')
     
# 2 - Function: a user leaves an active meeting instance
def user_leaves_meeting(r, user, meeting):
    if (user.email in meeting.audience) and ():
        event = {
            'event_id': ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)),
            'userID': user.id,
            'event_type': 2,
            'timestamp': datetime.now().isoformat()
        }
        r.rpush(f'eventsLog_{meeting.id}_{user.id}_1', json.dumps(event))
        print(f'User {user.name} leaved the meeting {meeting.title}')
    else:
        print(f"User {user.name} wasn't in the meeting {meeting.title}")
        
# 3 - Function: Show meeting participants
def show_participants(r,meeting):
    # Initialize cursor
    cursor = 0

    # Initialize an empty list to store the results
    events_type_1 = []

    # Partial string to match
    partial_event_id = meeting.id

    # Scan through keys matching the pattern "event_type:1:*"
    while True:
        # Scan for keys matching the pattern "event_type:1:*"
        cursor, keys = r.scan(cursor, match="event_type:1:*")
        
        # Append the keys to the events_type_1 list
        events_type_1.extend(keys)
        
        # Break the loop when the cursor is 0
        if cursor == 0:
            break

    # Now, let's filter out the keys that have event type 2
    events_type_1_no_type_2 = []

    for key in events_type_1:
        # Check if the key doesn't have event type 2
        if not r.exists(key.replace("event_type:1:", "event_type:2:")):
            events_type_1_no_type_2.append(key)

    # Now, filter keys based on partial match of event_id
    filtered_keys = [key for key in events_type_1_no_type_2 if partial_event_id in key]

    # Retrieve the values associated with the filtered keys
    event_data = []

    for key in filtered_keys:
        # Retrieve the event data
        event_data_json = r.get(key)
        # Deserialize the JSON data
        event_data_dict = json.loads(event_data_json)
        # Append the event data dictionary to the event_data list
        event_data.append(event_data_dict)

    # Now event_data contains the values of all events with event type 1 but not event type 2, and with event_id containing the partial string
    print(event_data)
    
# 6 - Function: a user posts a chat message
def post_message(r: redis.StrictRedis, user: User, meeting: Meeting, message: str):
    message_dict = {
        'user_id': user.id,
        'message': message,
        'time_posted': datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    }
    r.rpush(f'meeting_{meeting.id}_chat', json.dumps(message_dict))


# 7 - Function: show meeting’s chat messages in chronological order
def get_chat_messages(r, meeting):
    messages_dict_list = [json.loads(message) for message in r.lrange(f'meeting_{meeting.id}_chat', 0, -1)]
    messages_dict_list.sort(key=lambda d: d['time_posted'])
    messages = [f'{message["user_id"]}: {message["message"]}' for message in messages_dict_list]
    return messages


# 8 - Function: show for each active meeting when (timestamp) current participants joined
def get_active_participants_join_times(r, meeting):
    pass


# 9 - Function: show for an active meeting and a user his/her chat messages
def get_messages_for_meeting_and_user(r, meeting, user):
    pass


def main():
    # Connect to Redis
    r = redis.Redis(host='localhost', port=6379, db=0)

    content = read_jsons()

    load_redis(r, content)

    while True:
        user = User(get_random_user(content))
        meeting = Meeting(get_random_meeting(content))
        choice = input('Give your input: ')
        if choice == '6':
            message = generate_message()
            post_message(r, user, meeting, message)
            print(f'User {user.name} sent a message successfully!')
        elif choice == '7':
            messages = get_chat_messages(r, meeting)
            for message in messages:
                print(message)
        elif choice == '1':
            user_join(r, user, meeting)
        elif choice == '3':
            show_participants(r, meeting)
        else:
            break


if __name__ == '__main__':
    main()
