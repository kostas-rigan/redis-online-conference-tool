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
            'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        }
        r.rpush(f'events_Log_{meeting.id}_{user.id}_1', json.dumps(event))
        print(f'User {user.name} joined the meeting {meeting.title}')
    else:
        print(f'User {user.name} is not allowed to join the meeting {meeting.title}')
     
# 2 - Function: a user leaves an active meeting instance
def user_leaves_meeting(r, user, meeting):
    cursor = 0
    first_time = True
    event_keys = set()
    while cursor or first_time:
        cursor, rd_vals = r.scan(cursor, f'event_{meeting.id}_{user.id}*')
        event_keys.update(extract_meeting_instances(rd_vals))
        if first_time:
            first_time = False
            
    last_event = unbyteify_dict(r.hgetall(event_keys[-1]))
    if last_event['event_type'] == 1:
        event = {
            'event_id': f'event_{meeting.id}_{user.id}_2',
            'userID': user.id,
            'event_type': 2,
            'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        }
        r.rpush(f'events_log_{meeting.id}_{user.id}_2', json.dumps(event))
        print(f'User {user.name} leaved the meeting {meeting.title}')
    else:
        print(f'User {user.name} was not in the meeting {meeting.title}')
        
# 3 - Function: Show meeting participants
def show_participants(r,meeting):
    cursor = 0
    first_time = True
    event_keys = set()
    while cursor or first_time:
        cursor, rd_vals = r.scan(cursor, f'event_{meeting.id}*')
        event_keys.update(extract_meeting_instances(rd_vals))
        if first_time:
            first_time = False
    
    participants = []
    for event in event_keys:
        event_res = unbyteify_dict(r.hgetall(event))
        if event_res['event_type'] == 1:
            participants.append(event_res['userID'])
        elif event_res['event_type'] == 2:
            participants.remove(event_res['userID'])
    
    return participants


# 4 - Function: show active meetings
def get_active_meetings(r: redis.StrictRedis):
    cursor = 0
    first_time = True
    meetings_keys = set()
    while cursor or first_time:
        cursor, rd_vals = r.scan(cursor, 'meetings_*')
        meetings_keys.update(extract_meeting_instances(rd_vals))
        if first_time:
            first_time = False
    meetings = []
    for meeting_key in meetings_keys:
        res = unbyteify_dict(r.hgetall(meeting_key))
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        if res['fromdatetime'] < now < res['todatetime']:
            meetings.append(res['meeting_id'])
    return meetings

# 5 - Function: when a meeting ends, all participants must leave
def participants_leave(r, meeting):
    cursor = 0
    first_time = True
    event_keys = set()
    while cursor or first_time:
        cursor, rd_vals = r.scan(cursor, f'event_{meeting.id}*')
        event_keys.update(extract_meeting_instances(rd_vals))
        if first_time:
            first_time = False
    
    for event in event_keys:
        event_res = unbyteify_dict(r.hgetall(event))
        if event_res['event_type'] == 1:
            event = {
                'event_id': f'event_{meeting.id}_{event_res['userID']}_2',
                'userID': event_res['userID'],
                'event_type': 2,
                'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            }
            r.rpush(f'events_log_{meeting.id}_{event_res['userID']}_2', json.dumps(event))
            print(f'User {event_res['userID']} leaved the meeting {meeting.title}')
            

    
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
def get_active_participants_join_times(r: redis.StrictRedis):
    active_meetings = get_active_meetings(r)
    meeting_participant_dict = {}
    for active_meeting in active_meetings:
        meeting_participant_dict[active_meeting] = []
        event_log_keys = set()
        cursor = 0
        first_time = True
        while cursor or first_time:
            cursor, values = r.scan(cursor, f'events_log_{active_meeting}_*')
            event_log_keys.update(val.decode('utf-8') for val in values)
            if first_time:
                first_time = False
        for event_log_key in event_log_keys:
            res = r.lrange(event_log_key, 0, -1)[-1].decode('utf-8')
            meeting_participant_dict[active_meeting].append(res)
    join_times_str = ''
    for meeting, event_log in meeting_participant_dict.items():
        join_times_str += f'{meeting}\n'
        if event_log:
            for event in event_log:
                event = json.loads(event)
                if event['event_type'] == 1:
                    join_times_str += f'\t{event["userID"]}: {event["timestamp"]}\n'
        else:
            join_times_str += '\tNo active participants\n'
    return join_times_str


# 9 - Function: show for an active meeting and a user his/her chat messages
def get_messages_for_meeting_and_user(r, meeting: Meeting, user: User):
    active_meetings = get_active_meetings(r)
    if meeting.id in active_meetings:
        chat_messages = get_chat_messages(r, meeting)
        user_messages = list(filter(lambda x: user.id in x, chat_messages))
        return '\n'.join(user_messages)
    else:
        return 'Meeting is not currently active!'


def main():
    # Connect to Redis
    r = redis.Redis(host='localhost', port=6379, db=0)

    content = read_jsons()

    load_redis(r, content)

    while True:
        user = User(get_random_user(content))
        meeting = Meeting(get_random_meeting(content))
        choice = input('Give your input: ')
        if choice == '1':
            user_join(r, user, meeting)
        elif choice == '2':
            user_leaves_meeting(r, user, meeting)
        elif choice == '3':
            participants = show_participants(r, meeting)
            print('The participants are:')
            for p in participants:
                print(p)
        elif choice == '4':
            meetings = get_active_meetings(r)
            print(meetings)
        elif choice == '5':
            participants_leave(r, meeting)
        elif choice == '6':
            message = generate_message()
            post_message(r, user, meeting, message)
            print(f'User {user.name} sent a message successfully!')
        elif choice == '7':
            messages = get_chat_messages(r, meeting)
            for message in messages:
                print(message)
        elif choice == '8':
            join_times = get_active_participants_join_times(r)
            print(join_times)
        elif choice == '9':
            user_messages = get_messages_for_meeting_and_user(r, meeting, user)
            print(user_messages)
        else:
            break


if __name__ == '__main__':
    main()
