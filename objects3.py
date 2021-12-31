from queue import SimpleQueue
from functools import lru_cache


class Street:
    def __init__(self, name, drive_time):
        self.name = name
        self.drive_time = drive_time
        self.queue = list()                 # stores cars waiting in order todo - a regular Queue? list?
        self.intersection_at_end = None     # to access the schedule
        self.cars_total = 0


class Car:
    def __init__(self, path):
        self.path = path
        self.last_position = len(path) - 1  # index of the last street
        self.current_position = 0           # index relative to the position in path
        self.next_time = 0
        self.deep_in_queue = False
        self.driving = False
        self.finished = False
        # self.certain_go = False           # todo - maybe use this? there may be situations it's certain the car can go


class Intersection:
    def __init__(self, id: int):
        self.id = id
        self.streets_in = set()


class Schedules:
    """
    Schedule is a DICTIONARY of sequences of turning the lights on and off

    schedules_dict is the "readable" form - a dictionary with items in such form for each intersection:
        - key: intersection_id
        - value: list of tuples: (street_name, duration)

    schedules_functional is the "functional" form - a dictionary of tuples representing the schedule in form
                                                            (total_time, streets_intervals)
    streets_intervals - dictionary with items in form:
                                                        street: (start_green, end_green)
    """
    def __init__(self):
        self.schedules_dict = {}
        self.schedules_functional = {}

    def add_schedule(self, intersection_id, data):
        self.schedules_dict[intersection_id] = data  # todo - doesn't need to be string

    def add_functional_schedule(self):
        """
        run after adding all schedules in "readable" form, generates "functional" schedules based on readable ones
        """
        for intersection, tuples in self.schedules_dict.items():
            street_intervals = {}
            start = 0
            for street, duration in tuples:
                street_intervals[street] = (start, start + duration - 1)
                start += duration
            self.schedules_functional[intersection] = (start, street_intervals)  # at this point start = total time

    def update_readable(self):
        """
        run to change the "readable" schedule based on changes in the "functional" one
        """
        pass  # todo - probably needed for xxx algorithm

    @lru_cache(maxsize=512)  # todo - consider what's reasonable maxsize
    def timeTillGreen(self, street: Street, time_now: int) -> int:
        """
        Given a street and the current time, check how long until the green light on that street.

        :param street: street to be checked
        :param time_now: current time of the simulation
        :return: no. of seconds until green light; 0 if it is green now
        """
        # todo - consider some optimization techniques
        #   - e.g. check if it's the only active street in the schedule
        total_time, interval_dict = self.schedules_functional[street.intersection_at_end]
        start, end = interval_dict[street]
        cycle_time = time_now % total_time  # map current time to time in the cycle
        if start <= cycle_time:
            if cycle_time <= end:
                return 0  # green now in the cycle
            else:
                # was already green in this cycle; loop over until its time for it again
                return total_time - cycle_time + start
        else:
            # it will be green still in this cycle
            return start - cycle_time

    def export(self, filename):
        with open(filename, 'w') as out_file:
            out_file.write(f'{len(self.schedules_dict.keys())}\n')  # todo - calculate how many (do we need that?)
            for intersection_id in self.schedules_dict.keys():
                out_file.write(f'{intersection_id}\n{len(self.schedules_dict[intersection_id])}\n')
                for i in self.schedules_dict[intersection_id]:
                    out_file.write(f'{i[0].name} {i[1]}\n')
