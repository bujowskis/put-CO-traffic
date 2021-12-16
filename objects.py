from queue import SimpleQueue


class Street:
    def __init__(self, name, drive_time, ):
        self.name = name
        self.drive_time = drive_time
        self.queue = SimpleQueue()  # stores cars that are waiting
        self.light_is_green = False


class Car:
    def __init__(self):
        self.path = None
        self.current_position = None  # todo is it needed to keep track of? (probably yes)
        self.driving = 0  # time to reach next intersection


class Intersection:
    def __init__(self):
        self.idx = -1
        # todo - sets?
        self.streets_in = set()
        # self.streets_out = set() todo - probably not needed
        self.schedule = None


class Schedule:
    """
    Schedule is a sequence of turning the lights on and off
    """
    def __init__(self):
        pass  # todo

    def export(self):
        pass  # todo
