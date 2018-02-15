import json


class Event(object):

    def __init__(self, event_id, timestamp, event_type, details):
        self.__event_id = event_id
        self.__timestamp = timestamp
        self.__event_type = event_type
        self.__details = details

    @property
    def event_id(self):
        return self.__event_id

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def event_type(self):
        return self.__event_type

    @property
    def details(self):
        return self.__details


def from_json(json_string):
    json_object = json.loads(json_string)
    return Event(
        event_id=json_object['eventId'],
        timestamp=json_object['timestamp'],
        event_type=json_object['eventType'],
        details=json_object['details'],
    )
