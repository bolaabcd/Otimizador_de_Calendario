
from datetime import datetime
from typing import List


class User:
    def __init__(self, name: str, password: str):
        self.name = name
        self.password = password

# Formato das datas: '%Y-%m-%d %H:%M:%S'
class Interval:
    def __init__(self, start: datetime, end: datetime):
        self.start = start
        self.end = end

class Schedule:
    def __init__(self, intervals: List[Interval]):
        self.intervals = intervals

class Activity:
    def __init__(self, schedules: List[Schedule], locations: List[str], people: List[str], value: float):
        self.schedules = schedules
        self.locations = locations
        self.people = people
        self.value = value