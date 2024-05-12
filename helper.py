'''Helper functions for Redis assignment

This module contains functions that will assist the functions for an
online conference tool using Redis. It contains various functions like
reading files, inserting into Redis, generating random values for 
testing purposes etc.

'''
import json
import redis
from random import randrange
from datetime import datetime
import re


def load_json(filename: str) -> list:
    '''
    Given a JSON file, this function reads it and returns a list.

    Parameters
    ----------
    filename : str
        The file to read (can be any path)

    Returns
    -------
    list
        A list of dictionaries containing the contents of the JSON
    '''
    with open(filename) as f:
        obj = json.load(f)
    return obj


def read_jsons() -> dict:
    '''
    This functions reads all the JSON files and returns a dictionary
    containing all the entities.

    Parameters
    ----------
    None

    Returns
    -------
    dict
        A dictionary that contains a list of dictionaries for each entity.
    '''
    files = ['users.json', 'events_log.json', 'meetings.json', 'meetings_instances.json']
    content = {}
    for file in files:
        entity = file.split('.')[0]
        content[entity] = load_json(file)
    return content


def insert_to_redis(pipe: redis.StrictRedis, entity_pl: list, entity_name: str) -> None:
    '''Inserts an entity's key-value pairs into Redis

    Iterates over an entity's dictionaries, and inserts each key-value pair in
    Redis. The id is the combinations of the entity name and the position of the
    entity in the list.

    Parameters
    ----------
    pipe : redis.StrictRedis
        A redis pipeline object (subclass of StrictRedis), that will execute all
        insertions at once. It reduces the number of calls to Redis itself.
    entity_pl : list
        The list of dictionaries for the given entity
    entity_name : str
        The name of the entity

    Returns
    -------
    None

    Examples
    --------
    >>> r = redis.StrictRedis(host='localhost', port=6379)
    >>> people = [{'name': 'John', 'surname': 'Doe'},
    ...           {'name': 'Anna', 'surname': 'Smith'}]
    >>> with r.pipeline() as pipe:
    ...     insert_to_redis(pipe, people, 'person')
    '''
    for pos, entity in enumerate(entity_pl):
        for key, value in entity.items():
            if isinstance(value, list):
                value = '|'.join(value)
            pipe.hset(f'{entity_name}_{pos}', key, value)


def load_redis(r: redis.StrictRedis, content: dict) -> None:
    '''Bulk insert dictionaries into Redis

    Parameters
    ----------
    r : redis.StrictRedis
        A Redis connector object
    content : dict
        A dictionary containing the list of dictionaries to insert

    Returns
    -------
    None

    Examples
    --------
    >>> r = redis.StrictRedis(host='localhost', port=6379)
    >>> content = {'person': [{'name': 'John', 'surname': 'Doe'},
    ...                       {'name': 'Walter', 'surname': 'White'},
    ...                       {'name': 'Big', 'surname': 'Mallo'}],
    ...            'city': [{'city': 'Palo Alto', 'state': 'California'},
    ...                     {'city': 'Albuquerque', 'state': 'New Mexico'}]}
    >>> load_redis(r, content)
    '''
    with r.pipeline() as pipe:
        for name, dictionary in content.items():
            insert_to_redis(pipe, dictionary, name)

        pipe.execute()


def get_random_number(lst: list) -> int:
    '''Given a list, it generates an integer from 0 to len(list) - 1

    Parameters
    ----------
    lst : list
        Any list
    
    Returns
    -------
    int
        An integer from 0 to length of list - 1
    '''
    return randrange(len(lst))


def get_random_entity(entities: dict, entity_name: str) -> dict:
    '''Returns a random entity from the dictionary

    Selects a random entity from the dictionary. `get_random_number`
    is used to get the position of the entity to select.

    Parameters
    ----------
    entities : dict
        A dictionary of list of entities
    entity_name : str
        The name of the entity to randomly select

    Returns
    -------
    dict
        A single randomly selected entity
    '''
    entity = entities[entity_name]
    rn = get_random_number(entity)
    selection = entity[rn]
    return selection


def get_random_user(dictionary: dict) -> dict:
    '''Gets a random user using `get_random_entity` function'''
    return get_random_entity(dictionary, 'users')


def get_random_meeting(dictionary) -> dict:
    '''Gets a random meeting using `get_random_entity` function'''
    return get_random_entity(dictionary, 'meetings')


def generate_message() -> str:
    '''Generates a message using current time'''
    return f'message {datetime.now()}'


def extract_meeting_instances(vals):
    pattern = re.compile(r'^meetings_instances_\d+$')
    normal_vals = list(vals)
    if isinstance(normal_vals[-1], bytes):
        normal_vals = [val.decode('utf-8') for val in vals]
    meeting_vals = list(filter(lambda x: re.search(pattern, x), normal_vals))
    return meeting_vals


def unbyteify_dict(dct: dict):
    new_dct = {}
    for key, value in dct.items():
        nkey = key.decode('utf-8')
        nvalue = value.decode('utf-8')
        new_dct[nkey] = nvalue
    return new_dct
