from os.path import split

import regex as re
from django.db import connection

def fromDatabase(model, db_column, item):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT {db_column} FROM {model} WHERE {db_column} = %s", [item])
        row = cursor.fetchone()
        return row

# Validation functions
def unique(item, frags, req, messages):
    if req.get(item):
        db_column = item
        model = frags[1]
        attribute = frags[0]
        required_key = item + '.unique'
        record = fromDatabase(model, db_column, req[item])
        print("record", record)
        if record:
            if required_key in messages.keys():
                return messages[required_key]
            else:
                return f'{item.title()} must be unique'

def max_character(item, frags, req, messages):
    if req.get(item):
        max_value = frags[1]
        required_key = item + '.max'
        if len(req[item]) > int(max_value):
            if required_key in messages.keys():
                return messages[required_key]
            else:
                return f'{item.title()} must not be greater than {max_value} characters'

def min_character(item, frags, req, messages):
    if req.get(item):
        min_value = frags[1]
        required_key = item + '.min'
        if len(req[item]) < int(min_value):
            if required_key in messages.keys():
                return messages[required_key]
            else:
                return f'{item.title()} must be at least {min_value} characters'

def required(item, frags, req, messages):
    if not req.get(item):
        required_key = item + '.required'
        if required_key in messages.keys():
            return messages[required_key]
        else:
            return f'{item.title()} cannot be empty'

def email(item, frags, req, messages):
    if req.get(item):
        required_key = item + '.email'
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, req[item]):
            if required_key in messages.keys():
                return messages[required_key]
            else:
                return messages.get("email", "Invalid email address")

def numeric(item, frags, req, messages):
    if req.get(item):
        required_key = item + '.numeric'
        if not str(req[item]).isnumeric():
            if required_key in messages.keys():
                return messages[required_key]
            else:
                return messages.get("numeric", f'{item.title()} should be a number')

def boolean(item, frags, req, messages):
    if req.get(item):
        required_key = item + '.boolean'
        if not isinstance(req[item], bool):
            if required_key in messages.keys():
                return messages[required_key]
            else:
                return messages.get("boolean", f'{item.title()} should be a boolean')

def string(item, frags, req, messages):
    if req.get(item):
        required_key = item + '.string'
        if not isinstance(req[item], str):
            if required_key in messages.keys():
                return messages[required_key]
            else:
                return messages.get("string", f'{item.title()} should be a string')

def uppercase(item, frags, req, messages):
    if req.get(item):
        required_key = item + '.uppercase'
        if not req[item].isupper():
            if required_key in messages.keys():
                return messages[required_key]
            else:
                return messages.get("uppercase", f'{item.title()} should be uppercase')


def is_array(item, frags, req, messages):
    if req.get(item):
        required_key = item + '.is_array'
        if not isinstance(req[item], (list, tuple)):
            if required_key in messages.keys():
                return messages[required_key]
            else:
                return messages.get("array", f'{item.title()} should be a array')

def alphanumeric(item, frags, req, messages):
    if req.get(item):
        required_key = item + '.alphanumeric'
        if not req[item].isalnum():
            if required_key in messages.keys():
                return messages[required_key]
            else:
                return messages.get("alphanumeric", f'{item.title()} should be a alphanumeric')

def lowercase(item, frags, req, messages):
    if req.get(item):
        required_key = item + '.lowercase'
        if not req[item].islower():
            if required_key in messages.keys():
                return messages[required_key]
            else:
                return messages.get("lowercase", f'{item.title()} should be a lowercase')

def between(item, frags, req, messages):
    if req.get(item):
        required_key = item + '.between'
        range = frags[1].split(",")
        if not int(range[0]) <= int(req[item]) <= int(range[1]):
            if required_key in messages.keys():
                return messages[required_key]
            else:
                return messages.get("between", f'{item.title()} should be betwee {range[0]} and {range[1]}')

def size(item, frags, req, messages):
    print(item, frags, req[item]) # size, 6
    if req.get(item):
        required_key = item + '.size'

        # check for string length
        if isinstance(req[item], str):
            if not len(req[item]) <= int(frags[1]):
                return messages.get("size", f'{item.title()} should be less than {frags[1]} characters')
        if not req[item].isnumeric():
            if required_key in messages.keys():
                return messages[required_key]
            else:
                return messages.get("size", f'{item.title()} should be a size')
