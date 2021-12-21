from objects import *


# contains all objects needed for the simulation
class Instance:
    """
    Contains all the information describing the simulation
    """
    def __init__(self):
        self.duration = 0           # (1 <= D <= 10^4)
        self.no_intersections = 0   # (2 <= I <= 10^5)
        self.no_streets = 0         # (2 <= S <= 10^5)
        self.no_cars = 0            # (1 <= V <= 10^3)
        self.bonus = 0              # (1 <= F <= 10^3)
        self.streets = dict()
        # self.cars = set()
        self.intersections = None   # list
        self.schedules = None  # todo - is even needed? we generate schedules using greedy and xxx
        self.time = 0

    def simulate(self, schedules) -> int:
        """
        Simulates the instance specified by Instance's parameters, using the given schedule

        :return: obtained score
        """
        cur_time = 0
        score = 0
        while cur_time < self.time:
            # do next step
            # todo

            cur_time += 1

        return score

    def uniform_schedules(self) :
        """
        this function returns the simplest schedule, that is, each street on each intersection
        has the green light for 1 second
        """
        schedules = Schedules()
        for i in self.intersections:
            data = []
            for street in i.streets_in:
                data.append((street.name, 1))
            schedules.add_schedule(i.id, data)

        return schedules



    def greedy(self) -> set:
        """
        Generates schedules for the intersections of the instance specified by Instance's parameters using greedy
        algorithm

        :return: set of schedules for the intersections
        """
        schedules = set()
        # todo

        return schedules

    def xxx(self) -> set:  # todo - choose algorithm
        """
        Generates schedules for the intersections of the instance specified by Instance's parameters using todo

        :return: set of schedules for the intersections
        """
        schedules = set()
        # todo

        return schedules
