import math
from objects3 import *


class Instance:
    """
    Contains all the information describing the given instance
    """
    def __init__(self):
        self.duration = 0           # (1 <= D <= 10^4)
        self.no_intersections = 0   # (2 <= I <= 10^5)
        self.no_streets = 0         # (2 <= S <= 10^5)
        self.no_cars = 0            # (1 <= V <= 10^3)
        self.bonus = 0              # (1 <= F <= 10^3)
        self.streets = dict()       # dictionary of streets, mapping their names to their respective object
        self.cars = list()          # list of all cars
        self.intersections = None   # list of intersections, in order with respect to their id's

    def simulate(self, schedules: Schedules) -> int:
        """
        Simulates the instance using the given schedule

        works by iterating over all cars for each second of the simulation, skipping cars whenever possible, to save on
        execution time
            todo - not each, but shortest time until change? is it worth it?

        :return: obtained score
        """
        def carGo(car: Car):
            # car proceeds to next street
            car.path[car.current_position].popCar(time)
            car.current_position += 1
            if car.current_position == car.last_position:
                time_at_end = time + car.path[car.current_position].drive_time
                if time_at_end <= self.duration:
                    # the car will get to destination before end of simulation
                    score[0] += self.bonus + self.duration - time_at_end
                # no matter if the car made it on time, it's no longer needed to consider it
                car.finished = True
            else:
                car.driving = True
                car.next_time = time + car.path[car.current_position].drive_time

        # # todo - remove after done testing
        # print("before simulate:")
        # for street in self.streets.values():
        #     if street.queue[0]:
        #         print("{} - {}".format(street.name, street.queue))
        # print("\n")

        score = [0]
        time = 0
        while time < self.duration:
            for car in self.cars:
                if car.finished:
                    # the car already reached its destination
                    continue
                if car.deep_in_queue:
                    # the car is waiting in queue and is not the first one
                    continue
                if car.next_time != time:
                    # it's not time for the car's action
                    continue
                if car.driving:
                    # the car just arrived at end of the street
                    car.path[car.current_position].putCar(car)
                    if car.deep_in_queue:
                        continue
                if car.certain_go:
                    # it's certain the car can go now
                    car.certain_go = False
                    carGo(car)
                    continue
                # the car is the first at end of its street, waiting for green
                till_green = schedules.timeTillGreen(car.path[car.current_position], time)
                if not till_green:
                    carGo(car)
                else:
                    # wait with next action until the next green
                    car.next_time = time + till_green
                    car.certain_go = True
                    continue

            time += 1

        # cleanup states of cars and streets
        for car in self.cars:
            car: Car
            car.deep_in_queue = car.ini_deep_in_queue
            car.driving = False
            car.finished = False
            car.certain_go = False
            car.next_time = 0
            car.current_position = 0
        for street in self.streets.values():
            street.queue_first = 0
            street.queue_next = street.init_queue_next
            for i in range(street.init_queue_next, street.cars_total):
                street.queue[i] = None

        # # todo - remove after done testing
        # print("after simulate:")
        # for street in self.streets.values():
        #     if street.queue[0]:
        #         print("{} - {}".format(street.name, street.queue))
        # print("\n")

        # todo - consider passing cars and streets in non-destructive way instead of cleanup
        return score[0]

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

        schedules.add_functional_schedule()
        return schedules

    def intelligent_uniform_schedules(self) -> Schedules:
        """
        creates "intelligent" uniform schedules - every street that does have some cars passing through it gets exactly
        one second in its respective intersection's schedule

        :@todo - make sure it works before using
        """
        schedules = Schedules()
        for intersection in self.intersections:
            data = list()
            for street in intersection.streets_in:
                if street.cars_total:
                    data.append((street, 1))
            if len(data):
                schedules.add_schedule(intersection.id, data)

        schedules.add_functional_schedule()
        return schedules

    def greedy(self) -> Schedules:
        """
        Generates schedules_dict for the intersections of the instance specified by Instance's parameters using
        greedy-like heuristic algorithm

        It takes into account how many cars pass through the incoming streets of every intersection, and assigns time
        of green for each street according to the normalized proportions of total cars passing through the intersection

        Normalized proportions are calculated by dividing the count of cars by the minimal count of cars among the
        incoming streets, and then performing some operation to assign the time.

        :return: Schedules for the intersections
        """
        schedules = Schedules()

        for intersection in self.intersections:
            total_cars_count = 0
            min_cars = math.inf
            data = list()
            for street in intersection.streets_in:
                total_cars_count += street.cars_total
                if 0 < street.cars_total < min_cars:
                    min_cars = street.cars_total

            # normalize by dividing minimum positive time
            for street in intersection.streets_in:
                # normalized = math.ceil(street.cars_total / min_cars)  # by ceiling
                normalized = round(street.cars_total / min_cars)  # by rounding
                if normalized != 0:
                    data.append((street, normalized))
            if len(data):
                schedules.add_schedule(intersection.id, data)

        schedules.add_functional_schedule()
        return schedules

    def xxx(self) -> Schedules:  # todo - choose algorithm
        """
        Generates schedules_dict for the intersections of the instance using todo

        :return: dict of schedules_dict for the intersections
        """
        schedules = Schedules()
        # todo

        return schedules
