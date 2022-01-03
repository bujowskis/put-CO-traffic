import math
from objects3 import *
import random
from copy import deepcopy
import time
import matplotlib.pyplot as plt
from collections import defaultdict


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
        todo - consider if skipping to minimum time action is worth it

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

        # todo - consider passing cars and streets in non-destructive way instead of cleanup
        return score[0]

    def simulateWithRequests(self, schedules: Schedules) -> (int, dict):
        """
        Simulates the instance using the given schedule. Qorks by iterating over all cars for each second of the
        simulation, skipping cars whenever possible, to save on execution time
        todo - consider if skipping to minimum time action is worth it

        In this approach we additionally keep track of how much time in total did cars spent waiting
        in each street's queue.


        :return: obtained score
        """
        requests = defaultdict(lambda: 0)    # key: street_name; value: total waiting time (in seconds)

        def carGo(car: Car):
            # car proceeds to next street
            car.path[car.current_position].popCar(time)
            requests[car.path[car.current_position].name] += 1
            car.entered_queue = time - car.entered_queue
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

        # todo - consider passing cars and streets in non-destructive way instead of cleanup
        return score[0], requests

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



    def evoKiller(self, pop_size, max_generations) -> (Schedules, int):
        """
        Returns the best schedule found by doing some mutations


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

        def requestBasedMutation(old_schedules: Schedules, requests: defaultdict):
            """
            Creates NEW schedules based on the old ones.
            Does not copy the old schedules, neither modify them
            Looks for all the request on streets ending at a given intersection,

            """

            new_schedules = Schedules()

            for intersection, tuples in old_schedules.schedules_dict.items():
                if len(tuples) == 1:
                    # if just one street, make it always green
                    new_schedules.add_schedule(intersection, [(tuples[0][0], self.duration)])
                    continue
                new_tuples = []
                waiting_times = []
                for tuple_ in tuples:
                    street, duration = tuple_
                    waiting_times.append(requests[street.name])
                    new_tuples.append((street, duration))

                # if sum(waiting_times) == 0:
                #     # no change if there are no cars waiting on this intersection
                #     new_schedules.add_schedule(intersection, [(tuples[0][0], self.duration)])
                #     continue


                # now, with some probability, increase the duration on street that had the most requests
                # TODO: find out, what function will yield the best results

                try:
                    prob = max(waiting_times) / (sum(waiting_times) + max(waiting_times))
                except ZeroDivisionError:
                    prob = 0
                if random.random() < prob:
                    new_tuples[waiting_times.index(max(waiting_times))] = \
                        (new_tuples[waiting_times.index(max(waiting_times))][0],
                            new_tuples[waiting_times.index(max(waiting_times))][1] + 1)


                # and decrease the duration on street that had the least requests
                if random.random() < prob:  # FIXME: take the probability regarding the lesst request
                    new_tuples[waiting_times.index(min(waiting_times))] = \
                        (new_tuples[waiting_times.index(min(waiting_times))][0],
                            max(new_tuples[waiting_times.index(min(waiting_times))][1]-1, 1))

                # we give some small chance of shuffling the order of lights
                if random.random() < 0.07:
                    random.shuffle(new_tuples)

                new_schedules.add_schedule(intersection, new_tuples)
            new_schedules.add_functional_schedule()
            return new_schedules


        def getInitPopulation():
            """
            Individual in a population is a pair (schedules, requests)
            """
            begin_time = time.time()
            population = []
            scores = []
            base_schedules = self.greedy()
            for i in range(pop_size):
                new_schedules = blindMutation(base_schedules)
                score, requests = self.simulateWithRequests(new_schedules)
                nonlocal best_score
                if score > best_score:
                    best_score = score
                    nonlocal best_individual
                    best_individual = (new_schedules, requests)
                population.append((new_schedules, requests))
                scores.append(score)
            simulation_times.append(time.time() - begin_time)
            all_scores.append(scores)
            return population, scores

        def getNextPopulation(old_population: list, old_scores: list):
            """
            Returns the next population and scores (based on requests from previous simulation)
            Individual in a population is a pair (schedules, requests)
            """
            # TODO: for now the next population is created by blind mutation
            new_population = []
            max_score = max(old_scores)
            min_score = min(old_scores)
            try:
                weights = [((i-min_score)/(max_score-min_score))**4 for i in old_scores]  # kind of normalization
            except ZeroDivisionError:
                weights = [1 for _ in range(pop_size)]
            new_population = []
            new_scores = []
            # randomly choose items from old population to be selected and mutated
            # to form a new population
            nonlocal best_individual
            nonlocal best_score
            new_candidates = random.choices(old_population, weights=weights, k=pop_size-1)
            begin_time = time.time()
            for candidate in new_candidates:

                # copy the candidate, mutate the copy, evaluate and add to the new_population
                new_schedules = requestBasedMutation(candidate[0], candidate[1])
                score, new_requests = self.simulateWithRequests(new_schedules)
                new_population.append((new_schedules, new_requests))


                if score > best_score:
                    best_score = score
                    best_individual = (new_schedules, new_requests)
                new_scores.append(score)


            # always add current best to the population
            new_scores.append(best_score)
            new_population.append(best_individual)

            all_scores.append(scores)
            simulation_times.append(time.time() - begin_time)

            return new_population, new_scores


        start_time = time.time()


        # create the initial population (uniform schedules with some mutations)
        # evaluation is performed within the below function
        # population is a pair (score, schedules_object)

        population, scores = getInitPopulation()  # DONE

        generation_counter = 1
        while generation_counter < max_generations and time.time() - start_time < 5*60:

            population, scores = getNextPopulation(population, scores)
            # track of the best solution is implemented in the inner function

            generation_counter += 1


        print(f'total time: {time.time() - start_time}\n'
              f'time spent on simulations: {sum(simulation_times)}\n'
              f'time spent on other stuff: {time.time() - start_time- sum(simulation_times)}')

        # plot the improvement
        # flatten the scores
        flat_scores = [item for sublist in all_scores for item in sublist]
        times = [x//pop_size for x in range(len(flat_scores))]

        plt.hist2d(x=times, y=flat_scores, cmap='YlOrRd', cmin=0.9, bins=[generation_counter, 100])
        plt.show()
        return best_individual[0], best_score
