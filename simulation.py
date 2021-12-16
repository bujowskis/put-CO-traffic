import objects as obj


# contains all objects needed for the simulation
class Simulation:
    """
    Contains all the information describing the simulation
    """
    def __init__(self):
        self.duration = 0           # (1 <= D <= 10^4)
        self.no_intersections = 0   # (2 <= I <= 10^5)
        self.no_streets = 0         # (2 <= S <= 10^5)
        self.no_cars = 0            # (1 <= V <= 10^3)
        self.bonus = 0              # (1 <= F <= 10^3)
        self.streets = set()
        self.cars = set()
        self.intersections = set()
        self.schedules = set()  # todo - is even needed? we generate schedules using greedy and xxx
        self.time = 0

    def simulate(self, schedules) -> int:
        """
        Simulates the instance specified by Simulation's parameters, using the given schedule

        :return: obtained score
        """
        cur_time = 0
        score = 0
        while cur_time < self.time:
            # do next step
            pass  # todo

        return score

    def greedy(self) -> set:
        """
        Generates schedules for the intersections of the instance specified by Simulation's parameters using greedy
        algorithm

        :return: set of schedules for the intersections
        """
        schedules = set()
        # todo

        return schedules

    def xxx(self) -> set:  # todo - choose algorithm
        """
        Generates schedules for the intersections of the instance specified by Simulation's parameters using todo

        :return: set of schedules for the intersections
        """
        schedules = set()
        # todo

        return schedules
