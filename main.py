import json
import redis


def load_json(filename):
    with open(filename) as f:
        obj = json.load(f)
    return obj


def insert_to_redis(pipe, entity_pl, entity_name):
    for pos, entity in enumerate(entity_pl):
        for key, value in entity.items():
            if isinstance(value, list):
                value = '|'.join(value)
            pipe.hset(f'{entity_name}_{pos}', key, value)


def main():
    # Connect to Redis
    r = redis.Redis(host='localhost', port=6379, db=0)

    files = ['users.json', 'events_log.json', 'meetings.json', 'meetings_instances.json']
    content = {}
    for file in files:
        entity = file.split('.')[0]
        content[entity] = load_json(file)

    with r.pipeline() as pipe:
        for name, dictionary in content.items():
            insert_to_redis(pipe, dictionary, name)

        # Optionally, you can also create indexes for faster retrieval
        # For example, if you frequently search users by email, you can create an index like this:
        # for user in users:
        #     pipe.set('email_index:' + user['email'], user['userID'])

        pipe.execute()


if '__name__' == '__main__':
    main()
