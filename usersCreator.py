import json
import random
import string

def generate_user():
    user_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    name = ''.join(random.choices(string.ascii_uppercase, k=6))
    age = random.randint(18, 70)
    gender = random.choice(['Male', 'Female'])
    email = f"{name.lower()}@teamsEmail.com"
    return {
        'userID': user_id,
        'name': name,
        'age': age,
        'gender': gender,
        'email': email
    }

def generate_users(num_users):
    users = [generate_user() for _ in range(num_users)]
    return users

def write_to_json(users, filename):
    with open(filename, 'w') as f:
        json.dump(users, f, indent=4)

if __name__ == "__main__":
    num_users = 10  # Change this number to generate different number of users
    users = generate_users(num_users)
    write_to_json(users, 'users.json')
