from objects2 import *
from queue import SimpleQueue

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


    def simulate(self, schedules: Schedules, do_print=False) -> int:
        """
        in this approach, we iterate over cars, not over intersections
        
        Each car, in time t can be in one of 3 states:
            - driving the street s
            - waiting in a queue at the end of the street
            - crossing the intersection i
            
        Some cars are driving down the streets for long
            -> we shouldn't update their state each second
            We can calculate in what moment of simulation, the car is going to
            change its state -> perform the action

        To store the moments in which cars change their states, we create the list:
            - in each index idx, there is a queue of cars that are to change their
            state in time = idx


        The issue: How to predict in what time the car will be in the front of
        street's queue and be able to cross the intersection?
        - what is more efficient? Calculatint the light shifts and number of cars
        in front of the queue, or checking the possibility to change the state each
        second???

        Firstly, we use the second option.
        """
        score = 0
        cars_actions = [SimpleQueue() for _ in range(self.duration)]
        # cars_actions[t]: the queue of cars that are to update their state in time t

        # in the beginning, all cars are waiting to cross some intersection,
        # so for each car, we check how many cars are before them in the queue (may not
        # be efficient!)

        # so, we know, that the car will wait in the queue at least as many seconds,
        # as many cars in front of it in the street's queue
        for car in self.cars:
            cars_actions[car.cars_in_front_in_queue_when_entered].put(car)
            # we still keep the order of cars, no need to worry about that

        # then in each second, we consider only cars that are expected to change
        # state in given second
        # if no car is to change the state in a given second -> the queue is empty
        # -> then do nothing

        for t in range(self.duration):
            while not cars_actions[t].empty():
                # there are some cars that are to change their state in time t
                curr_car = cars_actions[t].get()
                next_time = curr_car.changeState(t)
                if t == 0:
                    score += self.bonus + (self.duration - t)
                elif next_time < self.duration:
                    cars_actions[next_time].put(curr_car)
                else:  # if car's next move would be performed after the simulation ends
                    continue

        print(f'score: {score}')
        return score

    def uniform_schedules(self):
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

    def greedy(self) -> set:
        """
        Generates schedules_dict for the intersections of the instance specified by Instance's parameters using greedy
        algorithm

        :return: set of schedules_dict for the intersections
        """
        schedules = set()
        # todo

        return schedules

    def xxx(self) -> set:  # todo - choose algorithm
        """
        Generates schedules_dict for the intersections of the instance specified by Instance's parameters using todo

        :return: set of schedules_dict for the intersections
        """
        schedules = set()
        # todo

        return schedules
