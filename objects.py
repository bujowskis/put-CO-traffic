from queue import SimpleQueue


class Street:
    def __init__(self, name, drive_time):
        self.name = name
        self.drive_time = drive_time
        self.queue = SimpleQueue()  # stores cars that are waiting
        self.light_is_green = False
        self.heading_car = None
        self.last_car = None
        self.cars_total = 0


class Car:
    def __init__(self, path):
        self.path = path
        self.last_idx = len(path) - 1  # index of the last street
        self.current_position = 0  # index relative to the position in path
        self.on_tail = None  # becomes tuple of form (Car_behind, offset in seconds)
        self.driving = 0  # used for leading cars, indicated how many seconds until end of street


class Intersection:
    def __init__(self, id: int):
        self.id = id
        self.streets_in = set()
        self.schedule = None
        # todo - maybe lights state


class Schedules:
    """
    Schedule is a SET of sequences of turning the lights on and off
    for each intersection
    """

    def __init__(self):

        self.schedules = {}     # key: intersection_id
                                # value: list of tuples: (street_name, duration)

    def add_schedule(self, intersection_id, data):
        self.schedules[str(intersection_id)] = data

    def updateIntersections(self):
        """
        invoking this function will update schedules for all intersections,
        that have their schedule specified
        """
        for schedule in self.schedules:
            pass

    def areValid(self):
        """
        checks if the set of schedules is valid
        """
        pass

    def export(self, filename):
        with open(filename, 'w') as out_file:
            out_file.write(f'{len(self.schedules.keys())}\n')  # todo - calculate how many
            for intersection_id in self.schedules.keys():
                out_file.write(f'{intersection_id}\n{len(self.schedules[intersection_id])}\n')
                for i in self.schedules[intersection_id]:
                    out_file.write(f'{i[0]} {i[1]}\n')


