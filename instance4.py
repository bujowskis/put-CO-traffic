import math
from objects3 import *
import random
import time
import matplotlib.pyplot as plt
from collections import defaultdict
from copy import deepcopy

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
        Simulates the instance using the given schedule. Qorks by iterating over all cars for each second of the
        simulation, skipping cars whenever possible, to save on execution time

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
                if car.next_time not in action_times:
                    action_times.add(car.next_time)

        score = [0]
        time = 0
        action_times = {self.duration}
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
                if till_green == -1:
                    # street is red forever - not possible for a car to cross the intersection
                    # wait forever? # FIXME
                    car.next_time = self.duration + 1

                if not till_green:
                    carGo(car)
                else:
                    # wait with next action until the next green
                    car.next_time = time + till_green
                    if car.next_time not in action_times:
                        action_times.add(car.next_time)
                    car.certain_go = True
                    continue

            next_action = min(action_times)
            action_times.discard(next_action)
            time = next_action

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

        return score[0]



    def intelligent_uniform_schedules(self) -> Schedules:
        """
        creates "intelligent" uniform schedules - every street that does have some cars passing through it gets exactly
        one second in its respective intersection's schedule
        """
        schedules = Schedules()
        for intersection in self.intersections:
            data = list()
            for street in intersection.streets_in:
                if street.cars_total:
                    data.append([street, 1])
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
                    data.append([street, normalized])
            if len(data):
                schedules.add_schedule(intersection.id, data)

        schedules.add_functional_schedule()
        return schedules

    def randomSchedules(self, variance):
        schedules = Schedules()
        for intersection in self.intersections:
            data = list()
            for street in intersection.streets_in:
                if street.cars_total:
                    value = random.expovariate(0.6) + 0.4  # TODO: to experiment a bit
                    data.append([street, value])
            if len(data):
                schedules.add_schedule(intersection.id, data)

        schedules.add_functional_schedule()
        return schedules


    def evoKiller(self, pop_size, max_no_improvement: int = 100, timeout: int = 300) -> (Schedules, int):
        """
        Generates a schedule using Evolutionary Algorithms methods
        @param pop_size: size of the population
        @param max_no_improvement: the maximum number of generations without improvement until termination, 100 by
        default
        @param timeout: time after the algorithm will terminate regardless of not reaching no improvement limit, 300s
        by default
        @return: the best Schedules found
        """
        all_scores = []
        best_individual = None
        best_score = 0
        simulation_times = []


        def blindMutation(old_schedules: Schedules):
            """
            Creates NEW schedules based on the old ones.
            Does not copy the old schedules, neither modify them
            """
            new_schedules = Schedules()

            for intersection, tuples in old_schedules.schedules_dict.items():
                shifts = random.choices([-2, -1, 0, 1, 2],
                                        weights=[1, 2, 5, 2, 1], k=len(tuples))
                # mutate tuples
                new_tuples = []
                for j, tuple_ in enumerate(tuples):
                    street_name, duration = tuple_
                    new_duration = max(duration + shifts[j], 1)
                    new_tuples.append((street_name, new_duration))
                # we give some small chance of shuffling the order of lights
                if random.random() < 0.07:
                    random.shuffle(new_tuples)
                new_schedules.add_schedule(intersection, new_tuples)
            new_schedules.add_functional_schedule()

            return new_schedules





        def crossover(schedules1: Schedules, schedules2: Schedules):
            child1, child2 = Schedules(), Schedules()
            for intersection_id, tuples1 in schedules1.schedules_dict.items():
                tuples2 = schedules2.schedules_dict[intersection_id]
                if random.random() < 0.5:
                    child1.add_schedule(intersection_id, tuples1)
                    child2.add_schedule(intersection_id, tuples2)
                else:
                    child1.add_schedule(intersection_id, tuples2)
                    child2.add_schedule(intersection_id, tuples1)
            child1.add_functional_schedule()
            child2.add_functional_schedule()
            return [0, child1], [0, child2]

        def mutate(schedules: Schedules, temp):
            """
            Mutates the schedules objects
            :param temp: temperature - determines the probability of gene changes
            """

            for data in schedules.schedules_dict.values():
                for street_in in data:
                    if random.random() < temp:  #TODO:  maybe another model (simulated annealing)
                        street_in[1] = max(round(random.gauss(0, 1)) + street_in[1], 0) # maybe some other dist




        def getInitPopulation():
            """
            individual in a population is a pair (schedules, requests)
            """

            first_population = []
            scores = []
            base_schedules_uniform = self.intelligent_uniform_schedules()

            nonlocal best_individual
            a = pop_size//4
            # ad some uniform schedules (mutated a bit
            for i in range(pop_size):
                if i <= a:
                    new_individual = [0, base_schedules_uniform.copySchedules()]
                    mutate(new_individual[1], 0.7)
                else:
                    new_individual = [0, self.randomSchedules(None)]

                new_individual[1].add_functional_schedule()
                new_individual[0] = self.simulate(new_individual[1])
                scores.append(new_individual[0])
                if new_individual[0] > best_individual[0]:
                    best_individual = new_individual
                first_population.append(new_individual)


            all_scores.append(scores)
            return first_population

        def getNextPopulation(old_population: list[[int, Schedules]], temp):
            """
            Individual in a population is a pair[score, schedules]  <--- stick to this
            No requests evaluated, since crossover destroys old schedule
            """
            new_population = []
            scores = []
            # then we perform a tournament, crossover the winning pair, mutate it with some probability
            # and add to the new population
            for t in range(pop_size//2):
                participants = random.choices(old_population, k=4)
                # we choose the best 2 out of k participants
                p1, p2 = sorted(participants, reverse=True, key=lambda x: x[0])[:2]  # sorts with respect to score
                child1, child2 = crossover(p1[1], p2[1])   # we pass schedules only

                nonlocal best_individual
                nonlocal no_improvement

                # now, mutate the kids
                if random.random() < 0.3:
                    mutate(child1[1], temp)
                if random.random() < 0.3:
                    mutate(child2[1], temp)

                # add functional schedules
                child1[1].add_functional_schedule()
                child2[1].add_functional_schedule()

                # calculate the score, update the best individual
                child1[0] = self.simulate(child1[1])
                if child1[0] > best_individual[0]:
                    best_individual = child1
                    no_improvement = 0
                child2[0] = self.simulate(child2[1])
                if child2[0] > best_individual[0]:
                    best_individual = child2
                    no_improvement = 0
                scores.append(child1[0])
                scores.append(child2[0])
                new_population.append(child1)
                new_population.append(child2)

            all_scores.append(scores)
            return new_population

        ############################
        start_time = time.time()
        best_individual = [0, None]
        no_improvement = 0
        # create the initial population (uniform schedules with some mutations)
        # evaluation is performed within the below function
        # population is a pair (score, schedules_object)
        population = getInitPopulation()  #TODO
        generation_counter = 1
        temp = 0.3
        while time.time() - start_time < timeout and no_improvement < max_no_improvement:
            population = getNextPopulation(population, temp)
            # track of the best solution is implemented in the inner function
            no_improvement += 1
            generation_counter += 1

        print(f'total time: {time.time() - start_time}\n')
        # plot the improvement
        # flatten the scores
        flat_scores = [item for sublist in all_scores for item in sublist]
        times = [x//pop_size for x in range(len(flat_scores))]

        plt.hist2d(x=times, y=flat_scores, cmap='YlOrRd', cmin=0.9, bins=[generation_counter-1, 100])
        plt.show()
        return best_individual[1], best_individual[0]
