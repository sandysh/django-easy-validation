import json

from django.http import HttpRequest
from .validators import *


class Validator:
    rules = {}
    requests = {}
    messages = {}
    validation_error = {}

    @classmethod
    def validate(cls, request, rules, messages=None):
        cls.validation_error = {}
        if isinstance(request, HttpRequest):
            cls.requests = json.loads(request.body)
        else:
            cls.validation_error['data'] = "Must be a HttpRequest object"
        if messages is None:
            messages = {}
        cls.rules = rules
        cls.messages = messages
        for item, rule in cls.rules.items():
            val_rules = rule.split("|")
            for val in val_rules:
                frags = val.split(":")
                function_name = frags[0]
                call_method = globals()[function_name]
                data = call_method(item, frags, cls.requests, cls.messages)
                name = f'{item}_{function_name}'
                if data:
                    cls.validation_error[name] = data
        return cls.validation_error

    @classmethod
    def failed(cls):
        if len(cls.validation_error) > 0:
            return True
        else:
            return False

    @classmethod
    def validated_data(cls):
        return cls.requests