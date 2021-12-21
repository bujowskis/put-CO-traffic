from queue import SimpleQueue


class Street:
    def __init__(self, name, drive_time):
        self.name = name
        self.drive_time = drive_time
        self.queue = SimpleQueue()  # stores cars that are waiting
        self.light_is_green = False



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
    Schedule is a sequence of turning the lights on and off
    """

    def __init__(self):
        pass  # todo

    def export(self):
        pass  # todo
