import redis
from helper import *
from entities import User, Meeting
from datetime import datetime
import json


# 1 - Function: a user joins an active meeting instance
def user_join(r, user, meeting):
    if meeting.isPublic or user.email in meeting.audience:
        event = {
            'event_id': ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)),
            'userID': user.id,
            'event_type': 1,
            'timestamp': datetime.now().isoformat()
        }
        r.rpush(f'eventsLog_{meeting.id}_{user.id}_1', json.dumps(event))
    else:
        print(f'User {user.name} is not allowed to join the meeting {meeting.title}')


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
        else:
            break


if __name__ == '__main__':
    main()
