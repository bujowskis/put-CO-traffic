import math
from objects3 import *


# contains all objects needed for the simulation
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
        self.streets = dict()
        self.cars = list()
        self.intersections = None   # list todo - set?

    def simulate(self, schedules: Schedules, do_print=False) -> int:
        """
        Simulates the instance using the given schedule

        works by iterating over all cars for each second of the simulation, skipping cars whenever possible, to save on
        execution time
            todo - not each, but shortest time until change? is it worth it?

        :return: obtained score
        """
        score = 0
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
                    car.driving = False
                    car.path[car.current_position].queue.append(car)
                    if len(car.path[car.current_position].queue) == 1:
                        # the car is the first one to go next; it can go through the next procedure
                        pass
                    else:
                        # the car has to wait for cars ahead
                        car.deep_in_queue = True
                        continue
                # the car is the first at end of its street, waiting for green
                till_green = schedules.timeTillGreen(car.path[car.current_position], time)
                if not till_green:
                    # car proceeds to next street
                    car.path[car.current_position].queue.pop(0)
                    # if there's any, update the car behind it
                    if len(car.path[car.current_position].queue):
                        car.path[car.current_position].queue[0].deep_in_queue = False
                        car.path[car.current_position].queue[0].next_time = time + 1

                    car.current_position += 1
                    if car.current_position == car.last_position:
                        time_at_end = time + car.path[car.current_position].drive_time
                        if time_at_end <= self.duration:
                            # the car will get to destination before end of simulation
                            score += self.bonus + self.duration - time_at_end
                        # no matter if the car made it on time, it's no longer needed to consider it
                        car.finished = True
                    else:
                        car.driving = True
                        car.next_time = time + car.path[car.current_position].drive_time
                else:
                    # wait with next action until the next green
                    car.next_time = time + till_green
                    continue

            time += 1

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

        schedules.add_functional_schedule()
        return schedules

    def xxx(self) -> Schedules:  # todo - choose algorithm
        """
        Generates schedules_dict for the intersections of the instance specified by Instance's parameters using todo

        :return: dict of schedules_dict for the intersections
        """
        schedules = Schedules()
        # todo

        return schedules
