import json
import random
import string

def generate_meeting():
    meeting_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    title = ''.join(random.choices(string.ascii_uppercase, k=6))
    description = ''.join(random.choices(string.ascii_uppercase, k=6))
    description = 'This meeting is about ' + description
    isPublic = random.randint(1, 2)
    #audience
    return {
        'meeting_id': meeting_id,
        'title': title,
        'description': description,
        'isPublic': isPublic,
        #'audience': audience
    }

def generate_meetings(num_users):
    meetings = [generate_meeting() for _ in range(num_users)]
    return meetings

def write_to_json(meetings, filename):
    with open(filename, 'w') as f:
        json.dump(meetings, f, indent=4)

if __name__ == "__main__":
    num_meetings = 4  # Change this number to generate different number of users
    meetings = generate_meetings(num_meetings)
    write_to_json(meetings, 'meetings.json')
