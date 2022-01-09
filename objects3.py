
class Car:
    def __init__(self, path):
        self.path = path
        self.last_position = len(path) - 1  # index of the last street
        self.current_position = 0           # index relative to the position in path
        self.next_time = 0                  # timestamp on which the next action of the car happens
        self.deep_in_queue = False          # indicates if there are other cars queued in front of the car
        self.ini_deep_in_queue: bool        # indicates if the car was deep in queue at the beginning of the simulation
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
        self.queue_first += 1
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


class Schedules:
    """
    Schedule is a DICTIONARY of sequences of turning the lights on and off
    - schedules_dict is the "readable" form - a dictionary with items in such form for each intersection:
        - key: intersection_id
        - value: list of tuples: (street, duration)
    - schedules_functional is the "functional" form - a dictionary of tuples representing the schedule in form
                                                            (total_time, streets_intervals)
        - streets_intervals - dictionary with items in form:
                                                            street: (start_green, end_green)
    """
    def __init__(self):
        self.schedules_dict = {}
        self.schedules_functional = {}
        self.score = 0
        # self.requests = defaultdict(lambda: 0)  # todo - maybe it will be better to store requests as fields of streets

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
        run to change the readable schedule based on changes in the functional one
        """
        self.schedules_dict = {}
        for intersection, intervals_tuple in self.schedules_functional.items():
            total_time, streets_intervals = intervals_tuple
            if total_time:
                street_time = []
                for street, time_intervals in streets_intervals.items():
                    street_time.append((street, time_intervals[1] - time_intervals[0] + 1))
                self.schedules_dict[intersection] = street_time

    def order_initqueue_first(self):
        """
        Orders streets in each intersection based on their init_queue_next;

        i.e. makes the streets with higher number of initial cars in the queue appear first in the schedule cycle

        @return: ordered Schedule, based on this schedule
        """
        schedules = Schedules()
        for intersection_id, streets_tuples_list in self.schedules_dict.items():
            priority_queue_values = set()
            priority_queue_items = dict()
            for street, duration in streets_tuples_list:
                if street.init_queue_next not in priority_queue_values:
                    # create list, add to values
                    priority_queue_items[street.init_queue_next] = list()
                    priority_queue_values.add(street.init_queue_next)
                priority_queue_items[street.init_queue_next].append((street, duration))

            data = list()
            while len(priority_queue_values):
                value = max(priority_queue_values)
                priority_queue_values.discard(value)
                items_list = priority_queue_items[value]
                for item in items_list:
                    data.append(item)
            if len(data):  # may be redundant
                schedules.add_schedule(intersection_id, data)

        schedules.add_functional_schedule()
        return schedules

    def timeTillGreen(self, street: Street, time_now: int) -> int:
        """
        Given a street and the current time, check how long until the green light on that street.

        :param street: street to be checked
        :param time_now: current time of the simulation
        :return: no. of seconds until green light; 0 if it is green now
        """
        # todo - optimize
        try:
            total_time, interval_dict = self.schedules_functional[street.intersection_at_end]
            start, end = interval_dict[street]
        except KeyError:
            return -1  # if a street not specified, it means it's blocked
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

    def export(self):
        count = 0
        for total_time, streets_intervals in self.schedules_functional.values():
            if total_time:
                count += 1

        print(f'{count}\n')
        for intersection_id in self.schedules_dict.keys():
            print(f'{intersection_id}\n{len(self.schedules_dict[intersection_id])}\n')
            for i in self.schedules_dict[intersection_id]:
                print(f'{i[0].name} {i[1]}\n')

    def exportToFile(self, filename):
        count = 0
        for total_time, streets_intervals in self.schedules_functional.values():
            if total_time:
                count += 1
        with open(filename, 'w') as out_file:
            out_file.write(f'{count}\n')
            for intersection_id in self.schedules_dict.keys():
                out_file.write(f'{intersection_id}\n{len(self.schedules_dict[intersection_id])}\n')
                for i in self.schedules_dict[intersection_id]:
                    out_file.write(f'{i[0].name} {i[1]}\n')
