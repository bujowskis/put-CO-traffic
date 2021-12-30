import math

from objects3 import *


# contains all objects needed for the simulation
class Instance:
    """
    Contains all the information describing the simulation
    """

    def __init__(self):
        self.duration = 0  # (1 <= D <= 10^4)
        self.no_intersections = 0  # (2 <= I <= 10^5)
        self.no_streets = 0  # (2 <= S <= 10^5)
        self.no_cars = 0  # (1 <= V <= 10^3)
        self.bonus = 0  # (1 <= F <= 10^3)
        self.streets = dict()
        self.cars = set()
        self.intersections = None  # list
        self.schedules = None  # todo - is even needed? we generate schedules_dict using greedy and xxx
        self.time = 0

    def simulate(self, schedules: Schedules, do_print=False) -> int:
        """
        Simulates the instance specified by Instance's parameters, using the given schedule

        works by iterating over all cars for each second of the simulation, skipping cars whenever possible, to save on
        execution time
            todo - not each, but shortest time until change? is it worth it?

        :return: obtained score
        """
        score = 0
        time = 0
        while time < self.duration:
            for car in self.cars:
                if car.next_time != time:
                    continue
                if car.in_queue:
                    # todo - at least leading's car waiting time / waiting time of car in front
                    #   may not be worth it, since this already skips the car if still in queue
                    car.next_time += 1
                    continue
                # if green, close  # todo - add mechanism of remembering "I can go for sure"?
                till_green = schedules.timeTillGreen()  # fixme - either make function work without intersection, or make Car know the intersection
                if not till_green:
                    #
        # todo - once car on final street, check if time left > time needed: add points

        print(f'score: {score}')
        return score

    def uniform_schedules(self) -> Schedules:
        """
        this function returns the simplest schedule, that is, each street on each intersection
        has the green light for 1 second
        """
        schedules = Schedules()
        for i in self.intersections:
            data = []
            for street in i.streets_in:
                data.append((street, 1))  # schedule will store the reference to street objects, not
                # only their names
            schedules.add_schedule(i.id, data)

        return schedules

    def greedy(self) -> Schedules:
        """
        Generates schedules_dict for the intersections of the instance specified by Instance's parameters using
        greedy-like heuristic algorithm

        :return: Schedules for the intersections
        """
        schedules = Schedules()
        # todo - don't consider the last street !!!
        for car in self.cars:
            # print("car: {}".format(car.car_id))
            car: Car
            # for strt_idx in range(len(car.path) - 1):  # -1 not to consider the last street
            #     # print("\tadding to street {}".format(street.name))
            #     car.path[strt_idx].cars_total += 1
            for street in car.path:
                # print("\tadding to street {}".format(street.name))
                street.cars_total += 1
        # print("\n")

        for intersection in self.intersections:
            total_cars_count = 0
            min_cars = math.inf
            data = list()
            # print(len(intersection.streets_in))
            for street in intersection.streets_in:
                # print("\t{}, {}".format(street.name, street.cars_total))
                total_cars_count += street.cars_total
                if 0 < street.cars_total < min_cars:
                    min_cars = street.cars_total
            # print(min_cars)

            # normalize by dividing minimum positive time, assign as many seconds as ceil(normalized)
            # todo - make something better - maybe combine with "add 1 second for every street it's better than"?
            for street in intersection.streets_in:
                normalized = math.ceil(street.cars_total / min_cars)
                # normalized = round(street.cars_total / min_cars)
                if normalized != 0:
                    data.append((street, math.ceil(street.cars_total / min_cars)))
            if len(data):
                schedules.add_schedule(intersection.id, data)

        return schedules

    def xxx(self) -> Schedules:  # todo - choose algorithm
        """
        Generates schedules_dict for the intersections of the instance specified by Instance's parameters using todo

        :return: dict of schedules_dict for the intersections
        """
        schedules = Schedules()
        # todo

        return schedules
