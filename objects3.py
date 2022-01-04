from collections import defaultdict

class Car:
    def __init__(self, path):
        self.path = path
        self.last_position = len(path) - 1  # index of the last street
        self.current_position = 0           # index relative to the position in path
        self.next_time = 0                  # timestamp on which the next action of the car happens
        self.deep_in_queue = False          # indicates if there are other cars queued in front of the car
        self.ini_deep_in_queue: bool       # indicates if the car was deep in queue at the beginning of the simulation
        self.driving = False                # indicates if the car is/was driving at the given timestamp
        self.finished = False               # indicates if the car has already reached its destination
        self.certain_go = False             # indicates if it's certain the car can go, without checking the green light

        self.entered_queue = 0              # indicates the timestamp in which the car entered the street's queue

class Intersection:
    def __init__(self, id: int):
        self.id = id
        self.streets_in = list()


class Street:
    def __init__(self, name, drive_time):
        self.name = name
        self.drive_time = drive_time
        # for now, we're trying out fixed-length queue of length cars_total + 1
        #   + 1 compensates for popCar and putCar time complexity, by harming memory complexity negligibly
        self.queue = None                   # stores cars waiting in order
        self.queue_first = 0                # index of the first car waiting in the queue
        self.queue_next = 0                 # index of the next free position in the queue
        self.init_queue_next = 0            # initial queue next index, used for cleanup of Instance.simulate()
        # todo - remember what's the next car idx for a dictionary, which serves the role of queue?
        self.intersection_at_end = None     # to access the schedule
        self.cars_total = 0
        self.requests = 0                   # total time that cars were waiting on that street

    def popCar(self, time: int = 0):
        """
        Pops the first car waiting in the queue; handles Car.deep_in_queue and Car.next_time method for the next car
        @param time: current time of the simulation; 0 by default
        """
        #self.queue[self.queue_first] = None
        self.queue_first += 1
        # if self.queue_first == self.cars_total:
        #     self.queue_first = 0
        if self.queue[self.queue_first]:
            self.queue[self.queue_first].deep_in_queue = False
            self.queue[self.queue_first].next_time = time + 1

    def putCar(self, car: Car):
        """
        Puts given car to the next free position in the queue; handles its Car.deep_in_queue and Car.driving
        @param car: car to be put in the queue
        """
        car.driving = False
        self.queue[self.queue_next] = car
        if not self.queue_next == self.queue_first:
            car.deep_in_queue = True
        self.queue_next += 1
        # if self.queue_next == self.cars_total:
        #     self.queue_next = 0


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
        self.score = 0
        #self.requests = defaultdict(lambda: 0) # maybe it will be better to store requests as fields of streets

    def add_schedule(self, intersection_id, data):
        self.schedules_dict[intersection_id] = data

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
            out_file.write(f'{len(self.schedules_dict.keys())}\n')  # fixme - change to count of intersectins WITH schedules
            for intersection_id in self.schedules_dict.keys():
                out_file.write(f'{intersection_id}\n{len(self.schedules_dict[intersection_id])}\n')
                for i in self.schedules_dict[intersection_id]:
                    out_file.write(f'{i[0].name} {i[1]}\n')
