import redis
from helper import *
from entities import User, Meeting


# 6 - Function: a user posts a chat message
def post_message(user, meeting, message):
    pass


# 7 - Function: show meeting’s chat messages in chronological order
def get_chat_messages(meeting):
    pass


# 8 - Function: show for each active meeting when (timestamp) current participants joined
def get_active_participants_join_times(meeting):
    pass


# 9 - Function: show for an active meeting and a user his/her chat messages
def get_messages_for_meeting_and_user(meeting, user):
    pass


def main():
    # Connect to Redis
    r = redis.Redis(host='localhost', port=6379, db=0)

    content = read_jsons()

    load_redis(r, content)

    user = User(get_random_user(content))
    meeting = Meeting(get_random_meeting(content))
    message = generate_message()
    post_message(user, meeting, message)


if __name__ == '__main__':
    main()
