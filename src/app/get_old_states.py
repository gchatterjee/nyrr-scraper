import json
from typing import Dict, Union
from s3 import read_file
from race import Race


def extract(state: dict, field: str) -> Union[str, None]:
    return state[field] if field in state.keys() else None


def create_race(state) -> Race:
    title = extract(state, "title")
    date = extract(state, "date")
    time = extract(state, "time")
    location = extract(state, "location")
    status = extract(state, "status")
    url = extract(state, "url")
    return Race(title, date, time, location, status, url)


def get_old_states(environment: str) -> Dict[str, Race]:
    states = read_file(environment)
    result = {}
    for key in states.keys():
        result[key] = create_race(states[key])
    return result
