import json
import random
import string

def generate_meeting(users):
    meeting_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    title = ''.join(random.choices(string.ascii_uppercase, k=6))
    description = ''.join(random.choices(string.ascii_uppercase, k=6))
    description = 'This meeting is about ' + description
    isPublic = random.randint(0, 1)
    audience = random.sample(users, k=random.randint(1, len(users)))  # Randomly select emails from users list
    audience_emails = [user['email'] for user in audience]  # Extract emails
    return {
        'meeting_id': meeting_id,
        'title': title,
        'description': description,
        'isPublic': isPublic,
        'audience': audience_emails
    }

def generate_meetings(users, num_meetings):
    meetings = [generate_meeting(users) for _ in range(num_meetings)]
    return meetings

def write_to_json(meetings, filename):
    with open(filename, 'w') as f:
        json.dump(meetings, f, indent=4)

if __name__ == "__main__":
    with open('users.json') as f:
        users = json.load(f)
    
    num_meetings = 7  # Change this number to generate different number of meetings
    meetings = generate_meetings(users, num_meetings)
    write_to_json(meetings, 'meetings.json')
